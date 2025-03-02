from abc import abstractmethod, ABC
from uuid import UUID

from src.domain.models.company_responses import CompanyResponseDTO


class ICompanyServiceAdapter(ABC):
    @abstractmethod
    async def get_company_by_id(self, user_id: UUID) -> CompanyResponseDTO:
        pass
