import re
from dataclasses import dataclass
from datetime import date
from typing import Tuple, Optional, Union
from uuid import UUID


@dataclass
class RabbitMQResponse:
    """Value object for RabbitMQ response with error handling."""
    status_code: int
    body: Union[str, dict]
    success: bool = True
    error_message: Optional[str] = None
    error_origin: Optional[str] = None

    @classmethod
    def success_response(cls, status_code: int, body: Union[str, dict]) -> "RabbitMQResponse":
        return cls(
            status_code=status_code,
            body=body,
            success=True
        )

    @classmethod
    def error_response(cls, status_code: int, message: str = '', error_origin: str = 'Payment Service') -> "RabbitMQResponse":
        return cls(
            status_code=status_code,
            body={},
            success=False,
            error_message=message,
            error_origin=error_origin
        )


# Primarily for users
@dataclass(frozen=True)
class AddBankCardDTO:
    """
    Domain DTO schema for adding a bank card to the user's account.
    """
    user_id: UUID
    card_holder_first_name: str
    card_holder_last_name: str
    card_number: str  # 11-16 digits
    expiration_date: str  # Format: MM/YY
    cvv_code: str  # 3 digits

    def __post_init__(self):
        self._validate()

    def _validate(self) -> None:
        """Validate card information."""
        if not (11 <= len(self.card_number) <= 16):
            raise ValueError("Card number must be between 11 and 16 digits")

        if not re.match(r"^(0[1-9]|1[0-2])/\d{2}$", self.expiration_date):
            raise ValueError("Invalid expiration date format. Use MM/YY")

        if len(self.cvv_code) != 3:
            raise ValueError("CVV must be 3 digits")

        month, year = self._parse_expiration()
        exp_date = date(2000 + year, month, 1)
        if exp_date < date.today():
            raise ValueError("Expiration date must be in the future")

    def _parse_expiration(self) -> Tuple[int, int]:
        """Parse expiration date into month and year."""
        month, year = map(int, self.expiration_date.split('/'))
        return month, year

    @property
    def expiration_month(self) -> int:
        """Get expiration month."""
        return self._parse_expiration()[0]

    @property
    def expiration_year(self) -> int:
        """Get expiration year as four-digit year."""
        return 2000 + self._parse_expiration()[1]

    @property
    def last_four_digits(self) -> str:
        """Get last four digits of card number."""
        return self.card_number[-4:]

    def to_dict(self) -> dict:
        """Convert the domain DTO object to a dictionary."""
        return dict(
            card_holder_first_name=self.card_holder_first_name,
            card_holder_last_name=self.card_holder_last_name,
            card_number=self.card_number,
            expiration_date=self.expiration_date,
            cvv_code=self.cvv_code
        )


# Primarily for businesses
@dataclass(frozen=True)
class AddBankAccountDTO:
    """
    Domain DTO schema for adding a bank account to the company's account.
    """
    account_holder_name: str
    account_number: str
    company_id: UUID

    def __post_init__(self) -> None:
        if not self.account_holder_name.strip():
            raise ValueError("account_holder_name cannot be empty or consist only of spaces.")
        if not self.account_number.strip():
            raise ValueError("account_number cannot be empty or consist only of spaces.")

    def to_dict(self) -> dict:
        """
        Convert the domain DTO object to a dictionary.
        """
        return dict(
            account_holder_name=self.account_holder_name,
            account_number=self.account_number,
            company_id= str(self.company_id)
        )
