import datetime
import uuid

from src.infrastructure.exceptions import InvalidPaymentMethodException
from src.domain.interfaces.payment_gateway_interface import IPaymentGateway
from src.domain.interfaces.repositories_interfaces.bank_account_repository_interface import IBankAccountRepository
from src.domain.models.payment_methods import BankAccountPaymentMethod
from src.domain.schemas import BankAccountInfo


class AddBankAccountUseCase:
    """
    USE CASE: Create a new payment method (bank account) and get a token from the payment gateway (bank API).
    """
    def __init__(self, payment_gateway: IPaymentGateway,
                 bank_account_repository: IBankAccountRepository) -> None:
        self._payment_gateway = payment_gateway
        self._bank_account_repository = bank_account_repository

    async def execute(self, bank_account_info: BankAccountInfo) -> BankAccountPaymentMethod:
        bank_account_info = self._add_bank_account(bank_account_info)

        return await self._bank_account_repository.create(bank_account_info)

    @staticmethod
    def _add_bank_account(bank_account_info: BankAccountInfo) -> BankAccountPaymentMethod:
        current_time = datetime.datetime.now(datetime.UTC)

        return BankAccountPaymentMethod(
            id=uuid.uuid4(),
            account_holder_name=bank_account_info.account_holder_name,
            account_number=bank_account_info.account_number,
            bank_name=bank_account_info.bank_name,
            bank_bic=bank_account_info.bank_bic,
            created_at=current_time,
            updated_at=current_time
        )

    @staticmethod
    def _validate_bank_account(bank_account: BankAccountPaymentMethod) -> None:
        """Validate the bank account before creation."""
        if not bank_account.can_be_used_for_payment():
            raise InvalidPaymentMethodException("This bank account cannot be used for payment.")
