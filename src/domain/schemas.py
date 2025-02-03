import re
from datetime import date
from typing import Annotated

from pydantic import BaseModel, StringConstraints, field_validator


class PaymentToken(BaseModel):
    payment_token: str


class CardInfo(BaseModel):
    card_holder_first_name: str
    card_holder_last_name: str
    card_number: Annotated[str, StringConstraints(min_length=11, max_length=11)]
    expiration_date: Annotated[str, StringConstraints(pattern=r"^(0[1-9]|1[0-2])\/\d{2}$")]
    cvv_code: Annotated[str, StringConstraints(min_length=3, max_length=3)]

    @field_validator("expiration_date")
    @classmethod
    def validate_expiration(cls, v):
        match = re.match(r"^(0[1-9]|1[0-2])/(\d{2})$", v)
        if not match:
            raise ValueError("Invalid expiration date format. Use MM/YY instead.")

        month, year = int(match[1]), int(match[2])

        full_year = 2000 + year

        exp_date = date(full_year, month, 1)
        if exp_date < date.today():
            raise ValueError("Expiration date must be in the future")

        return v
