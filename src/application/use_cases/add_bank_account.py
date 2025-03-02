from typing import Optional

from src.application.exceptions import InactiveCompanyError, CompanyNotFoundError, InvalidPaymentMethodError
from src.core.logger import LoggerService
from src.domain.interfaces.company_service_adapter_interface import ICompanyServiceAdapter
from src.domain.interfaces.payment_gateway_interface import IPaymentGateway
from src.domain.interfaces.repositories_interfaces.bank_account_repository_interface import IBankAccountRepository
from src.domain.models.company_responses import CompanyResponseDTO
from src.domain.models.payment_methods import BankAccountPaymentMethod
from src.domain.schemas import AddBankAccountDTO


class AddBankAccountUseCase:
    """
    USE CASE: Create a new payment method (bank account).
    """
    def __init__(
            self,
            payment_gateway: IPaymentGateway,
            bank_account_repository: IBankAccountRepository,
            company_adapter: ICompanyServiceAdapter,
            logger: LoggerService,
    ) -> None:
        self._payment_gateway = payment_gateway
        self._bank_account_repository = bank_account_repository
        self._company_adapter = company_adapter
        self._logger = logger

    async def execute(self, bank_account: AddBankAccountDTO) -> BankAccountPaymentMethod:
        try:
            # Check if this company is existing in the system
            company = await self._company_adapter.get_company_by_id(bank_account.company_id)

            # Check if this company is inactive
            if not company.is_active:
                raise InactiveCompanyError(
                    status_code=403,
                    message="Company is not active."
                )

            bank_account = BankAccountPaymentMethod(**bank_account.to_dict())

            return await self._bank_account_repository.create(bank_account)
        except (
                InvalidPaymentMethodError,
                CompanyNotFoundError,
                InactiveCompanyError
        ) as e:
            self._logger.error(f"Error creating bank account: {e}.")
            raise
        except Exception as e:
            self._logger.critical(f"Unexpected error creating bank account: {str(e)}.")
            raise




