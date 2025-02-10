import datetime
import uuid

from src.infrastructure.exceptions import InvalidPaymentMethodException
from src.domain.interfaces.payment_gateway_interface import IPaymentGateway
from src.domain.interfaces.repositories_interfaces.bank_card_repository_interface import IBankCardRepository
from src.domain.models.payment_methods import CardPaymentMethod
from src.domain.schemas import CardInfo


class AddBankCardUseCase:
    """
    USE CASE: Create a new payment method (bank card) and get a token from the payment gateway (bank API).
    """

    def __init__(self, payment_gateway: IPaymentGateway,
                 bank_card_repository: IBankCardRepository) -> None:
        self._payment_gateway = payment_gateway
        self._bank_card_repository = bank_card_repository

    async def execute(self, raw_data: dict) -> CardPaymentMethod:
        card_info = CardInfo(**raw_data)
        token = await self._payment_gateway.get_payment_token(card_info)
        payment_method = self._add_bank_card(card_info, token)

        return await self._bank_card_repository.create(payment_method)

    @staticmethod
    def _add_bank_card(card_info: CardInfo, payment_token: str) -> CardPaymentMethod:
        current_time = datetime.datetime.now(datetime.UTC)

        return CardPaymentMethod(
            id=uuid.uuid4(),
            card_holder_first_name=card_info.card_holder_first_name,
            card_holder_last_name=card_info.card_holder_last_name,
            card_last_four=card_info.card_number[-4:],
            expiration_month=card_info.expiration_month,
            expiration_year=card_info.expiration_year,
            payment_token=payment_token,
            created_at=current_time,
            updated_at=current_time
        )

    @staticmethod
    def _validate_card(card: CardPaymentMethod) -> None:
        """Validate the bank card before creation."""
        if not card.can_be_used_for_payment():
            raise InvalidPaymentMethodException("This bank card cannot be used for payment.")
