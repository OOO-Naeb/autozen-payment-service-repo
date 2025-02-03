import asyncio

import uvicorn
from fastapi import FastAPI
from starlette.middleware.base import BaseHTTPMiddleware

from src.application.services.payment_service import PaymentService
from src.core.middleware.exceptions_middleware import PaymentExceptionMiddleware
from src.infrastructure.adapters.rabbitmq_api_gateway_listener import RabbitMQAPIGatewayListener

payment_service = PaymentService()


async def start_rabbitmq_listener(service: PaymentService):
    queues_listener = RabbitMQAPIGatewayListener(payment_service=service)

    await queues_listener.start_listening()


async def lifespan(app: FastAPI):
    task = asyncio.create_task(start_rabbitmq_listener(service=payment_service))

    yield

    task.cancel()


app = FastAPI(lifespan=lifespan)

app.add_middleware(BaseHTTPMiddleware, dispatch=PaymentExceptionMiddleware(app=app).dispatch)

if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8003)
