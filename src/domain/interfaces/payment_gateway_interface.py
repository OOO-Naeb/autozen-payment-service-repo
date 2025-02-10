from abc import abstractmethod, ABC

from src.domain.schemas import CardInfo, BankAccountInfo


class IPaymentGateway(ABC):
    @abstractmethod
    async def get_payment_token(self, payment_method_info: CardInfo | BankAccountInfo) -> str:
        pass
