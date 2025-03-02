from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

@dataclass
class CompanyResponseDTO:
    """
    Domain DTO for a company.
    """
    company_id: UUID
    id: UUID
    name: str = ""
    is_active: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    # TODO: Add new fields later

    def is_company_active(self) -> bool:
        """
        Returns True if the company is active, False otherwise.
        """
        return self.is_active
