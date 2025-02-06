import datetime
import uuid

from sqlalchemy import String, TIMESTAMP, Boolean
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.database import Base

metadata = Base.metadata

class BankCardModel(Base):
    """SQLAlchemy model for bank cards."""
    __tablename__ = 'bank_cards'
    metadata = metadata

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    card_holder_first_name: Mapped[str] = mapped_column(String(255), nullable=True)
    card_holder_last_name: Mapped[str] = mapped_column(String(255), nullable=True)
    card_last_four: Mapped[str] = mapped_column(String(4), nullable=True)
    expiration_date: Mapped[str] = mapped_column(String(5), nullable=True)
    payment_token: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc)
    )


class BankAccountModel(Base):
    """SQLAlchemy model for bank accounts."""
    __tablename__ = 'bank_accounts'
    metadata = metadata

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_holder_name: Mapped[str] = mapped_column(String(255), nullable=True)
    account_number: Mapped[str] = mapped_column(String(50), nullable=True)
    bank_name: Mapped[str] = mapped_column(String(255), nullable=True)
    bank_bic: Mapped[str] = mapped_column(String(20), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc)
    )
