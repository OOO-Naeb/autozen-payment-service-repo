import uuid
from datetime import datetime
import random
from uuid import UUID

from src.domain.interfaces.company_service_adapter_interface import ICompanyServiceAdapter
from src.domain.models.company_responses import CompanyResponseDTO
from src.infrastructure.exceptions import CompanyServiceError


class CompanyServiceAdapter(ICompanyServiceAdapter):
    async def get_company_by_id(self, company_id: UUID) -> CompanyResponseDTO | None:
        # DEV ONLY ----------------------------------------------
        if random.randint(0, 1) == 0:
            print("Russian test roulette!")
            raise CompanyServiceError(
                status_code=404,
                detail=f"Company with ID: {company_id} not found.",
            )
        return CompanyResponseDTO(
            id=company_id,
            name="OOO \"Naeb\" Ltd.",
            is_active=True,
            company_id=uuid.uuid4(),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        # -------------------------------------------------------

