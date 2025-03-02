import datetime
import uuid
from decimal import Decimal

from sqlalchemy import String, TIMESTAMP, Boolean, ForeignKey, Numeric
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
    balance: Mapped[Numeric] = mapped_column(Numeric(precision=12, scale=2), default=Decimal(0.00), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, default=uuid.uuid4)

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc)
    )

    def __repr__(self):
        return f"<BankCard(id={self.id}, user_id={self.user_id}, balance={self.balance})>"


class BankAccountModel(Base):
    """SQLAlchemy model for bank accounts."""
    __tablename__ = 'bank_accounts'
    metadata = metadata

    id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_holder_name: Mapped[str] = mapped_column(String(255), nullable=True)
    account_number: Mapped[str] = mapped_column(String(50), nullable=True)
    bank_name: Mapped[str] = mapped_column(String(255), nullable=True)
    bank_bic: Mapped[str] = mapped_column(String(20), nullable=True)
    balance: Mapped[Numeric] = mapped_column(Numeric(precision=12, scale=2), default=Decimal(0.00), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    company_id: Mapped[uuid.UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False, default=uuid.uuid4)

    created_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.datetime.now(datetime.timezone.utc),
        onupdate=datetime.datetime.now(datetime.timezone.utc)
    )

    def __repr__(self):
        return f"<BankAccount(id={self.id}, company_id={self.company_id}, balance={self.balance})>"
