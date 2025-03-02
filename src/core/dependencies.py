from starlette.requests import Request

from src.application.use_cases.add_bank_account import AddBankAccountUseCase
from src.application.use_cases.add_bank_card import AddBankCardUseCase
from src.core.logger import LoggerService
from src.infrastructure.adapters.bank_payment_gateway import BankPaymentGateway
from src.infrastructure.adapters.company_service_adapter import CompanyServiceAdapter
from src.infrastructure.adapters.user_service_adapter import UserServiceAdapter
from src.infrastructure.database.database import get_async_session
from src.infrastructure.repositories.bank_account_repository import BankAccountRepository
from src.infrastructure.repositories.bank_card_repository import BankCardRepository


async def setup_dependencies():
    """Initialize all dependencies."""
    payment_method_gateway = BankPaymentGateway()
    user_service_adapter = UserServiceAdapter()
    logger = LoggerService(__name__, "payment_service_log.log")
    async_session = await get_async_session().__anext__()
    rabbitmq_company_adapter = CompanyServiceAdapter()

    bank_card_repository = BankCardRepository(async_session)
    bank_account_repository = BankAccountRepository(async_session)

    add_bank_card_use_case = AddBankCardUseCase(payment_method_gateway, bank_card_repository, user_service_adapter)
    add_bank_account_use_case = AddBankAccountUseCase(
        payment_method_gateway, bank_account_repository, rabbitmq_company_adapter, logger
    )

    dependencies = {
        "add_bank_card_use_case": add_bank_card_use_case,
        "add_bank_account_use_case": add_bank_account_use_case,
        "logger": logger
    }

    return dependencies


def get_add_bank_card_use_case(request: Request) -> AddBankCardUseCase:
    return request.app.state.dependencies["add_bank_card_use_case"]


def get_add_bank_account_use_case(request: Request) -> AddBankAccountUseCase:
    return request.app.state.dependencies["add_bank_account_use_case"]


def get_logger(request: Request) -> LoggerService:
    return request.app.state.dependencies["logger"]

