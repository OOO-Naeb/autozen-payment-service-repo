import uuid

from src.application.interfaces.payment_gateway_interface import IPaymentGateway
from src.domain.exceptions import PaymentGatewayException
from src.domain.schemas import CardInfo


class BankPaymentGateway(IPaymentGateway):
    async def get_payment_token(self, card_info: CardInfo) -> str:
        print(type(card_info))
        print(card_info)
        # DEV ONLY ----------------------------------------------
        return f"TEST-PAYMENT-TOKEN FOR: {card_info.card_number}, UNIQUE_ID: {uuid.uuid4()}"
        # -------------------------------------------------------
