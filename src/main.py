import asyncio

import uvicorn
from fastapi import FastAPI

from src.application.use_cases.add_bank_account import AddBankAccountUseCase
from src.application.use_cases.add_bank_card import AddBankCardUseCase
from src.core.logger import LoggerService
from src.infrastructure.adapters.bank_payment_gateway import BankPaymentGateway
from src.infrastructure.adapters.rabbitmq_api_gateway_listener import RabbitMQApiGatewayListener
from src.infrastructure.database.database import get_async_session
from src.infrastructure.repositories.bank_card_repository import BankCardRepository


async def setup_dependencies():
    """Initialize all dependencies."""
    payment_method_gateway = BankPaymentGateway()
    logger = LoggerService(__name__, "api_gateway_log.log")

    async_session = await get_async_session().__anext__()
    payment_method_repository = BankCardRepository(async_session)
    add_bank_card_use_case = AddBankCardUseCase(payment_method_gateway, payment_method_repository)
    add_bank_account_use_case = AddBankAccountUseCase(payment_method_gateway, payment_method_repository)

    rabbit_listener = RabbitMQApiGatewayListener(
        add_bank_card_use_case=add_bank_card_use_case,
        add_bank_account_use_case=add_bank_account_use_case,
        logger=logger
    )

    return rabbit_listener


async def start_rabbitmq_listener(listener: RabbitMQApiGatewayListener):
    """Start the RabbitMQ listener."""
    await listener.start_listening()


async def lifespan(app: FastAPI):
    """FastAPI lifespan event handler for startup and shutdown."""
    # Create dependencies
    listener = await setup_dependencies()

    # Start RabbitMQ listener
    listener_task = asyncio.create_task(
        start_rabbitmq_listener(listener)
    )

    yield  # Application runs here

    # Cleanup on shutdown
    listener_task.cancel()
    try:
        await listener_task
    except asyncio.CancelledError:
        pass


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(lifespan=lifespan)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='localhost',
        port=8003,
        reload=True  # Enable auto-reload during development
    )
