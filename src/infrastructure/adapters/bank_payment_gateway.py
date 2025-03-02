import uuid
from decimal import Decimal

from src.domain.interfaces.payment_gateway_interface import IPaymentGateway
from src.domain.schemas import AddBankCardDTO


class BankPaymentGateway(IPaymentGateway):
    async def get_payment_token(self, card_info: AddBankCardDTO) -> str:
        print(type(card_info))
        print(card_info)
        # DEV ONLY ----------------------------------------------
        return f"TEST-PAYMENT-TOKEN FOR: {card_info.card_number}, UNIQUE_ID: {uuid.uuid4()}"
        # -------------------------------------------------------

    async def get_balance(self, token: str) -> Decimal:
        # DEV ONLY ----------------------------------------------
        return Decimal(10000.00)
        # -------------------------------------------------------
