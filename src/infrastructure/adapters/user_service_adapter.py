from datetime import datetime
import random
from uuid import UUID

from src.domain.interfaces.user_service_adapter_interface import IUserServiceAdapter
from src.domain.models.user_responses import UserResponseDTO
from src.infrastructure.exceptions import UserServiceError
from src.presentation.schemas import RolesEnum


class UserServiceAdapter(IUserServiceAdapter):
    async def get_user_by_id(self, user_id: UUID) -> UserResponseDTO | None:
        # DEV ONLY ----------------------------------------------
        if random.randint(0, 1) == 0:
            print("Russian test roulette!")
            raise UserServiceError(
                status_code=404,
                detail=f"User with ID: {user_id} not found.",
            )
        return UserResponseDTO(
            id=user_id,
            first_name="John",
            last_name="Doe",
            roles=[RolesEnum.USER],
            is_active=False,
            email="example@gmail.com",
            phone_number="+1234567890",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        # -------------------------------------------------------

