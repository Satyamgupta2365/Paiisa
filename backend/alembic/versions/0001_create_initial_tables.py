"""create initial tables

Revision ID: 0001
Revises: 
Create Date: 2026-03-13 18:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('preferred_payment_method', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    op.create_table('transactions',
    sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
    sa.Column('user_id', sa.Uuid(as_uuid=True), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('category', sa.String(length=80), nullable=True),
    sa.Column('payment_method', sa.String(length=50), nullable=False),
    sa.Column('cashback_earned', sa.Float(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('pine_labs_txn_id', sa.String(length=100), nullable=True),
    sa.Column('ai_recommendation', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_transactions_user_id'), 'transactions', ['user_id'], unique=False)

    op.create_table('offers',
    sa.Column('id', sa.Uuid(as_uuid=True), nullable=False),
    sa.Column('payment_method', sa.String(length=50), nullable=False),
    sa.Column('cashback_percentage', sa.Float(), nullable=False),
    sa.Column('max_cashback', sa.Float(), nullable=True),
    sa.Column('min_amount', sa.Float(), nullable=False),
    sa.Column('category', sa.String(length=80), nullable=True),
    sa.Column('conditions', sa.Text(), nullable=True),
    sa.Column('valid_until', sa.DateTime(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('offers')
    op.drop_index(op.f('ix_transactions_user_id'), table_name='transactions')
    op.drop_table('transactions')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
