from abc import abstractmethod, ABC
from typing import Optional
from uuid import UUID

from src.domain.models.payment_methods import BankAccountPaymentMethod


class IBankAccountRepository(ABC):
    """Repository interface for bank cards."""

    @abstractmethod
    async def create(self, bank_account: BankAccountPaymentMethod) -> BankAccountPaymentMethod:
        """Create a new bank account."""
        pass

    @abstractmethod
    async def get_by_id(self, bank_account: UUID) -> Optional[BankAccountPaymentMethod]:
        """Get a bank account by ID."""
        pass

    @abstractmethod
    async def get_by_company_id(self, company_id: UUID) -> BankAccountPaymentMethod:
        """Get bank account for a certain company."""
        pass

    @abstractmethod
    async def update(self, bank_account: BankAccountPaymentMethod) -> BankAccountPaymentMethod:
        """Update a bank account."""
        pass

    @abstractmethod
    async def delete(self, bank_account: UUID) -> None:
        """Delete a bank card."""
        pass
