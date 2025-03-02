from src.application.exceptions import UserNotActiveError
from src.domain.interfaces.user_service_adapter_interface import IUserServiceAdapter
from src.domain.interfaces.payment_gateway_interface import IPaymentGateway
from src.domain.interfaces.repositories_interfaces.bank_card_repository_interface import IBankCardRepository
from src.domain.models.payment_methods import CardPaymentMethod
from src.domain.schemas import AddBankCardDTO

class AddBankCardUseCase:
    """
    USE CASE: Create a new payment method (bank card) and get a token from the payment gateway (bank API).
    """

    def __init__(
            self,
            payment_gateway: IPaymentGateway,
            bank_card_repository: IBankCardRepository,
            user_service_adapter: IUserServiceAdapter
    ) -> None:
        self._payment_gateway = payment_gateway
        self._bank_card_repository = bank_card_repository
        self._user_service_adapter = user_service_adapter

    async def execute(self, card_info: AddBankCardDTO) -> CardPaymentMethod:
        token = await self._payment_gateway.get_payment_token(card_info)
        balance = await self._payment_gateway.get_balance(token)

        # Check if this user is existing in the system
        user = await self._user_service_adapter.get_user_by_id(card_info.user_id)

        # Check if this user is inactive
        if not user.is_active:
            raise UserNotActiveError(
                status_code=403,
                message="User is not active."
            )

        card = CardPaymentMethod(
            card_holder_first_name=card_info.card_holder_first_name,
            card_holder_last_name=card_info.card_holder_last_name,
            card_last_four=card_info.card_number[-4:],  # Last 4 digits of the card number
            expiration_date=card_info.expiration_date,
            balance=balance,
            payment_token=token,
            user_id=card_info.user_id
        )

        return await self._bank_card_repository.create(card)