import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.models import BankAccountModel


class BankAccountDAO:
    """Data Access Object for bank accounts."""

    def __init__(self, async_session: AsyncSession):
        self._async_session = async_session

    async def create(self, model: BankAccountModel) -> BankAccountModel:
        self._async_session.add(model)
        await self._async_session.commit()
        await self._async_session.refresh(model)
        return model

    async def get_by_id(self, bank_account_id: UUID) -> Optional[BankAccountModel]:
        result = await self._async_session.execute(
            select(BankAccountModel).where(BankAccountModel.id == bank_account_id)
        )
        return result.scalar_one_or_none()

    # Temporarily commented out due to the lack of a user_id field in the BankAccountModel

    # async def get_by_user_id(self, user_id: UUID) -> List[BankCardModel]:
    #     result = await self._async_session.execute(
    #         select(BankCardModel)
    #         .where(BankCardModel.user_id == user_id)
    #         .order_by(BankCardModel.created_at.desc())
    #     )
    #     return list(result.scalars().all())

    async def update(self, model: BankAccountModel) -> BankAccountModel:
        await self._async_session.merge(model)
        return model

    async def delete(self, payment_method_id: UUID) -> None:
        await self._async_session.execute(
            update(BankAccountModel)
            .where(BankAccountModel.id == payment_method_id)
            .values(deleted_at=datetime.datetime.now(datetime.UTC))
        )
