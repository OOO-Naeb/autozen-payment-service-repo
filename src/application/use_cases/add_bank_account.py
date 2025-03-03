from src.application.exceptions import InactiveCompanyError, CompanyNotFoundError, InvalidPaymentMethodError, \
    ExistingBankAccountError
from src.core.logger import LoggerService
from src.domain.interfaces.company_service_adapter_interface import ICompanyServiceAdapter
from src.domain.interfaces.payment_gateway_interface import IPaymentGateway
from src.domain.interfaces.repositories_interfaces.bank_account_repository_interface import IBankAccountRepository
from src.domain.models.payment_methods import BankAccountPaymentMethod
from src.domain.schemas import AddBankAccountDTO
from src.infrastructure.exceptions import CompanyServiceError


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

            # Check if this company already has a bank account in the 'bank_accounts' table
            bank_account_exists = await self._bank_account_repository.get_by_company_id(bank_account.company_id)
            if bank_account_exists:
                self._logger.warning(f"This company - {company.id} already has a bank account.")
                raise ExistingBankAccountError()

            # Check if this company is inactive
            if not company.is_active:
                self._logger.warning(f"Company - {company.id} is not active.")
                raise InactiveCompanyError(
                    status_code=403,
                    message="Company is not active."
                )

            bank_account = BankAccountPaymentMethod(**bank_account.to_dict())

            return await self._bank_account_repository.create(bank_account)
        except (
                CompanyServiceError,
                InactiveCompanyError,
                ExistingBankAccountError
        ):
            raise
        except Exception as e:
            self._logger.critical(f"Unexpected error creating bank account: {str(e)}.")
            raise
