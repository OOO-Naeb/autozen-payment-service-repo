from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from src.domain.models.payment_methods import CardPaymentMethod


class IBankCardRepository(ABC):
    """Repository interface for bank cards."""

    @abstractmethod
    async def create(self, bank_card: CardPaymentMethod) -> CardPaymentMethod:
        """Create a new bank card."""
        pass

    @abstractmethod
    async def get_by_id(self, bank_card_id: UUID) -> Optional[CardPaymentMethod]:
        """Get a bank card by ID."""
        pass

    # Temporarily commented out due to the lack of implementation in the repository

    # @abstractmethod
    # async def get_by_user_id(self, user_id: UUID) -> List[CardPaymentMethod]:
    #     """Get all bank cards for a user."""
    #     pass

    @abstractmethod
    async def update(self, bank_card: CardPaymentMethod) -> CardPaymentMethod:
        """Update a bank card."""
        pass

    @abstractmethod
    async def delete(self, bank_card_id: UUID) -> None:
        """Delete a bank card."""
        pass
