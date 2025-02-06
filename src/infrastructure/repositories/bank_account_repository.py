import datetime
import uuid
from typing import Optional

from src.application.interfaces.bank_account_repository_interface import IBankAccountRepository
from src.domain.models.payment_methods import BankAccountPaymentMethod
from src.infrastructure.dao.bank_account_dao import BankAccountDAO
from src.infrastructure.database.models import BankAccountModel


class BankAccountRepository(IBankAccountRepository):
    """Implementation of bank account repository supporting polymorphism."""

    def __init__(self, async_session):
        self._dao = BankAccountDAO(async_session)

    @staticmethod
    def _to_domain(model: BankAccountModel) -> BankAccountPaymentMethod:
        """Convert database model to domain model."""
        return BankAccountPaymentMethod(
            id=model.id,
            account_holder_name=model.account_holder_name,
            account_number=model.account_number,
            bank_name=model.bank_name,
            bank_bic=model.bank_bic,
            is_active=model.is_active,

            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def _to_model(domain: BankAccountPaymentMethod) -> BankAccountModel:
        """Convert domain model to database model."""
        model_id = domain.id if domain.id is not None else uuid.uuid4()

        return BankAccountModel(
            id=model_id,
            account_holder_name=domain.account_holder_name,
            account_number=domain.account_number,
            bank_name=domain.bank_name,
            bank_bic=domain.bank_bic,
            is_active=domain.is_active,

            created_at=domain.created_at if domain.created_at is not None else datetime.datetime.now(
                datetime.timezone.utc),
            updated_at=domain.updated_at if domain.updated_at is not None else datetime.datetime.now(
                datetime.timezone.utc)
        )

    async def create(self, bank_account: BankAccountPaymentMethod) -> BankAccountPaymentMethod:
        model = self._to_model(bank_account)
        created_model = await self._dao.create(model)

        return self._to_domain(created_model)

    async def get_by_id(self, bank_account_id: uuid.UUID) -> Optional[BankAccountPaymentMethod]:
        model = await self._dao.get_by_id(bank_account_id)

        return self._to_domain(model) if model else None

    # Temporarily commented out due to the lack of 'user_id' field in the database model

    # async def get_by_user_id(self, user_id: UUID) -> List[BankAccountPaymentMethod]:
    #     models = await self._dao.get_by_user_id(user_id)
    #     return [self._to_domain(model) for model in models]

    async def update(self, bank_account: BankAccountPaymentMethod) -> BankAccountPaymentMethod:
        model = self._to_model(bank_account)
        updated_model = await self._dao.update(model)

        return self._to_domain(updated_model)

    async def delete(self, bank_account_id: uuid.UUID) -> None:
        await self._dao.delete(bank_account_id)
        