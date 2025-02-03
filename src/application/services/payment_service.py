from src.domain.schemas import CardInfo, PaymentToken


class PaymentService:
    def __init__(self) -> None:
        pass

    async def get_payment_token(self, card_info: CardInfo) -> tuple[int, str]:
        """
        SERVICE METHOD: Send a request to the bank API to get a payment token for the given card information.

        Args:
            card_info (CardInfo): The card information to generate a payment token for.

        Returns:
            tuple[int, str]: Status code and payment token.
        """
        # DEV ONLY ----------------------------------------------
        return 200, f"TEST-PAYMENT-TOKEN FOR: {card_info['card_number']}"
        # -------------------------------------------------------
