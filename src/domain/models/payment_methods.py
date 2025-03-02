from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Dict, Any
import uuid

from sqlalchemy import Numeric


@dataclass
class PaymentMethod(ABC):
    id: Optional[uuid.UUID] = field(default_factory=uuid.uuid4)
    is_active: bool = field(default=True)
    balance: Decimal = field(default=Decimal(0.00))

    created_at: Optional[datetime] = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = field(default_factory=datetime.now)

    @abstractmethod
    def can_be_used_for_payment(self) -> bool:
        """Check if the payment method can be used for payment."""
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        """Convert the domain object to a dictionary."""
        pass

    def convert_datetime_fields_to_str(self, data: Any) -> Any:
        """
        Convert datetime/date fields to strings in the given data.
        """
        if isinstance(data, (datetime, date)):
            return data.isoformat()
        elif isinstance(data, dict):
            return {key: self.convert_datetime_fields_to_str(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.convert_datetime_fields_to_str(item) for item in data]
        else:
            return data

    def to_serializable_dict(self) -> Dict[str, Any]:
        """
        Convert the domain object to a dictionary with datetime/date fields converted to strings.
        """
        raw_dict = self.to_dict()
        return self.convert_datetime_fields_to_str(raw_dict)


# Primarily for users
@dataclass(kw_only=True)
class CardPaymentMethod(PaymentMethod):
    user_id: uuid.UUID
    card_holder_first_name: str = ""
    card_holder_last_name: str = ""
    card_last_four: str = ""
    expiration_date: str = ""
    payment_token: str = ""

    @property
    def card_holder_full_name(self) -> str:
        return f"{self.card_holder_first_name} {self.card_holder_last_name}"

    def is_expired(self) -> bool:
        if not self.expiration_date:
            return True
        try:
            month, year = map(int, self.expiration_date.split('/'))
            today = date.today()
            # Assuming expiration_date is always the first day of the month
            exp_date = date(year + 2000, month, 1) # Adding 2000 to handle 2-digit year
            return exp_date < today
        except ValueError:
            return True


    def can_be_used_for_payment(self) -> bool:
        return not self.is_expired() and self.is_active

    def to_dict(self) -> dict:
        return dict(
            id=self.id,
            card_holder_first_name=self.card_holder_first_name,
            card_holder_last_name=self.card_holder_last_name,
            card_last_four=self.card_last_four,
            expiration_date=self.expiration_date,
            payment_token=self.payment_token,
            balance=self.balance,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )


# Primarily for businesses
@dataclass(kw_only=True)
class BankAccountPaymentMethod(PaymentMethod):
    company_id: uuid.UUID
    account_holder_name: str = ""
    account_number: str = ""
    bank_name: str | None = ""
    bank_bic: str | None = ""
    is_active: bool = True

    company_id: uuid.UUID

    def can_be_used_for_payment(self) -> bool:
        return self.is_active

    def to_dict(self) -> dict:
        return dict(
            id=self.id,
            account_holder_name=self.account_holder_name,
            account_number=self.account_number,
            bank_name=self.bank_name,
            bank_bic=self.bank_bic,
            balance=self.balance,
            company_id=self.company_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )