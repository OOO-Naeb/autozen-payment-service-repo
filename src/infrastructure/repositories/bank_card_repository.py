import uuid
import datetime
from typing import Optional
from uuid import UUID


from src.application.interfaces.bank_card_repository_interface import IBankCardRepository
from src.domain.models.payment_methods import CardPaymentMethod
from src.infrastructure.dao.bank_card_dao import BankCardDAO
from src.infrastructure.database.models import BankCardModel


class BankCardRepository(IBankCardRepository):
    """Implementation of bank card repository supporting polymorphism."""
    def __init__(self, async_session):
        self._dao = BankCardDAO(async_session)

    @staticmethod
    def _to_domain(model: BankCardModel) -> CardPaymentMethod:
        """Convert database model to domain model."""
        try:
            month_str, year_str = model.expiration_date.split('/')
            expiration_month = int(month_str)
            expiration_year = int("20" + year_str) if len(year_str) == 2 else int(year_str)
        except Exception as e:
            raise ValueError(f"Invalid expiration_date format in DB model: {model.expiration_date}") from e

        return CardPaymentMethod(
            id=model.id,
            card_holder_first_name=model.card_holder_first_name,
            card_holder_last_name=model.card_holder_last_name,
            card_last_four=model.card_last_four,
            expiration_month=expiration_month,
            expiration_year=expiration_year,
            payment_token=model.payment_token,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def _to_model(domain: CardPaymentMethod) -> BankCardModel:
        """Convert domain model to database model."""
        model_id = domain.id if domain.id is not None else uuid.uuid4()
        expiration_date = f"{domain.expiration_month:02d}/{str(domain.expiration_year)[-2:]}"

        return BankCardModel(
            id=model_id,
            card_holder_first_name=domain.card_holder_first_name,
            card_holder_last_name=domain.card_holder_last_name,
            card_last_four=domain.card_last_four,
            expiration_date=expiration_date,
            payment_token=domain.payment_token,
            is_active=True,

            created_at=domain.created_at if domain.created_at is not None else datetime.datetime.now(datetime.timezone.utc),
            updated_at=domain.updated_at if domain.updated_at is not None else datetime.datetime.now(datetime.timezone.utc)
        )

    async def create(self, card: CardPaymentMethod) -> CardPaymentMethod:
        model = self._to_model(card)
        created_model = await self._dao.create(model)

        return self._to_domain(created_model)

    async def get_by_id(self, card_id: UUID) -> Optional[CardPaymentMethod]:
        model = await self._dao.get_by_id(card_id)

        return self._to_domain(model) if model else None

    # Temporarily commented out due to the lack of 'user_id' field in the database model

    # async def get_by_user_id(self, user_id: UUID) -> List[CardPaymentMethod]:
    #     models = await self._dao.get_by_user_id(user_id)
    #     return [self._to_domain(model) for model in models]

    async def update(self, card: CardPaymentMethod) -> CardPaymentMethod:
        model = self._to_model(card)
        updated_model = await self._dao.update(model)

        return self._to_domain(updated_model)

    async def delete(self, card_id: UUID) -> None:
        await self._dao.delete(card_id)
