"""base_migration

Revision ID: d119887510de
Revises: 53ac6c8dec68
Create Date: 2026-03-31 17:56:27.196398

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '000000000001'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создание таблицы client
    op.create_table('client',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('contacts', sa.JSON(), default={}, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Создание таблицы order
    op.create_table('order',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('instruments', sa.JSON(), nullable=False),
        sa.Column('contract_price', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('created_date', sa.Date(), nullable=False),
        sa.Column('deadline_date', sa.Date(), nullable=True),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Создание индексов
    op.create_index(op.f('ix_order_id'), 'order', ['id'], unique=False)
    op.create_index(op.f('ix_order_title'), 'order', ['title'], unique=False)
    
    # Создание внешнего ключа
    op.create_foreign_key(
        'fk_order_client_id',
        'order', 'client',
        ['client_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
