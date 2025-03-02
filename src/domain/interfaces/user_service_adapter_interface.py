from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.models.user_responses import UserResponseDTO


class IUserServiceAdapter(ABC):
    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> UserResponseDTO:
        pass
