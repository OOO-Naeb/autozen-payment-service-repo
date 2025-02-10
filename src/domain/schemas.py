import re
from dataclasses import dataclass
from datetime import date
from typing import Tuple, Optional, Union


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
class CardInfo:
    """Value object for card information before tokenization."""
    card_holder_first_name: str
    card_holder_last_name: str
    card_number: str
    expiration_date: str  # Format: MM/YY
    cvv_code: str

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


# Primarily for businesses
@dataclass(frozen=True)
class BankAccountInfo:
    account_holder_name: str
    account_number: str
    bank_name: str
    bank_bic: str

    def __post_init__(self):
        self._validate()

    def _validate(self) -> None:
        # Validating account number format goes here
        if not re.match(r"^\d{10,20}$", self.account_number):
            raise ValueError("Invalid account number format.")
