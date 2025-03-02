from abc import abstractmethod, ABC
from decimal import Decimal

from src.domain.schemas import AddBankCardDTO, AddBankAccountDTO


class IPaymentGateway(ABC):
    @abstractmethod
    async def get_payment_token(self, payment_method_info: AddBankCardDTO | AddBankAccountDTO) -> str:
        pass

    @abstractmethod
    async def get_balance(self, token: str) -> Decimal:
        pass
