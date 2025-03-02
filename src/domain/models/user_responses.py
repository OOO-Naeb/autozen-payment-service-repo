from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.presentation.schemas import RolesEnum


@dataclass(frozen=True)
class UserResponseDTO:
    """
    Domain schema for user response DTO.
    """
    id: UUID
    first_name: str
    last_name: str
    roles: list[RolesEnum]
    is_active: bool

    email: str
    phone_number: str

    created_at: datetime
    updated_at: datetime

    def to_dict(self) -> dict:
        return dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            roles=[role.value for role in self.roles],
            is_active=self.is_active,
            email=self.email,
            phone_number=self.phone_number,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
