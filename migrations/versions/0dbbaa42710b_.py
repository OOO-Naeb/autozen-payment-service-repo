"""empty message

Revision ID: 0dbbaa42710b
Revises: 
Create Date: 2025-03-01 19:09:08.053823

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0dbbaa42710b'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('bank_accounts',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('account_holder_name', sa.String(length=255), nullable=True),
    sa.Column('account_number', sa.String(length=50), nullable=True),
    sa.Column('bank_name', sa.String(length=255), nullable=True),
    sa.Column('bank_bic', sa.String(length=20), nullable=True),
    sa.Column('balance', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('company_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bank_cards',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('card_holder_first_name', sa.String(length=255), nullable=True),
    sa.Column('card_holder_last_name', sa.String(length=255), nullable=True),
    sa.Column('card_last_four', sa.String(length=4), nullable=True),
    sa.Column('expiration_date', sa.String(length=5), nullable=True),
    sa.Column('payment_token', sa.String(length=255), nullable=False),
    sa.Column('balance', sa.Numeric(precision=12, scale=2), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('payment_token')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('bank_cards')
    op.drop_table('bank_accounts')
    # ### end Alembic commands ###
