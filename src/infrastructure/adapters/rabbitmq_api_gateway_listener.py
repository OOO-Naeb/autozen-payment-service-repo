import json
from typing import Annotated, Callable

import aio_pika
from fastapi import Depends

from src.application.services.payment_service import PaymentService
from src.core.config import settings
from src.core.logger import LoggerService
from src.domain.exceptions import SourceUnavailableException
from src.domain.schemas import CardInfo
from src.infrastructure.interfaces.queue_listener_interface import IQueueListener


class RabbitMQAPIGatewayListener(IQueueListener):
    def __init__(self, payment_service: Annotated[PaymentService, Depends(PaymentService)]) -> None:
        self.payment_service = payment_service
        self.logger = LoggerService(__name__, "api_gateway_log.log")
        self.connection = None
        self.channel = None
        self.exchange = None
        self.exchange_name = 'GATEWAY-PAYMENT-EXCHANGE.direct'
        self.operation_types_and_handlers = {
            'add_new_payment_method': self.payment_service.get_payment_token,
        }

    async def connect(self):
        if not self.connection or self.connection.is_closed:
            try:
                self.connection = await aio_pika.connect_robust(
                    settings.RABBITMQ_URL,
                    timeout=10,
                    client_properties={'client_name': 'Payment Service'}
                )
                self.channel = await self.connection.channel()
                self.exchange = await self.channel.declare_exchange(
                    self.exchange_name, aio_pika.ExchangeType.DIRECT, durable=True
                )
            except aio_pika.exceptions.AMQPConnectionError as e:
                self.logger.error(
                    f"RabbitMQ service is unavailable. Connection error: {e}. From: RabbitMQAPIGatewayListener, connect()"
                )
                raise SourceUnavailableException(detail="RabbitMQ service is unavailable.")

    async def _initialize_queue(self) -> None:
        await self.connect()

        payment_queue = await self.channel.declare_queue('PAYMENT.all', durable=True)

        await payment_queue.bind(self.exchange, routing_key='PAYMENT.all')
        await payment_queue.consume(self._create_callback())

        self.logger.info(f"[*] Listening to queue 'PAYMENT_QUEUE' with exchange '{self.exchange_name}'.")


    async def start_listening(self) -> None:
        await self.connect()
        await self._initialize_queue()

    def _create_callback(self) -> Callable:
        async def callback(message: aio_pika.IncomingMessage):
            async with message.process():
                self.logger.info(f"[X] Received message from {message.routing_key} - {message.body}")
                data = json.loads(message.body.decode())

                # Dev logs
                print("Correlation ID from sender ->", message.correlation_id)
                print("To send back to:", message.reply_to)

                operation_type = data.get("operation_type")

                # Delete unnecessary 'operation_type' key from the data and leave only the card info
                del data["operation_type"]
                card_info = CardInfo(**data)

                handler = self.operation_types_and_handlers.get(operation_type)

                try:
                    # PyCharm bug possibly???
                    # noinspection PyArgumentList
                    status_code, response = await handler(card_info)
                except Exception as e:
                    self.logger.error(f"Error while handling operation '{operation_type}': {e}")
                    status_code, response = 500, {"error": str(e)}

                response_message = json.dumps({
                    "status_code": status_code,
                    "body": response
                })

                await self.channel.default_exchange.publish(
                    aio_pika.Message(
                        body=response_message.encode(),
                        correlation_id=message.correlation_id
                    ),
                    routing_key=message.reply_to
                )
                self.logger.info(f"Sent response with correlation_id {message.correlation_id}")

        return callback
