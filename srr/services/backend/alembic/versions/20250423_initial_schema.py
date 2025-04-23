"""initial schema

Revision ID: 20250423_initial
Revises: 
Create Date: 2025-04-23 10:22:50.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20250423_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Users
    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('username', sa.String(100), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('full_name', sa.String(255), nullable=False),
        sa.Column('roles', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('department', sa.String(255), nullable=True),
        sa.Column('organization', sa.String(255), nullable=True),
        sa.Column('position', sa.String(255), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, default=True),
        sa.Column('hashed_password', sa.String(255), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username'),
        sa.UniqueConstraint('email'),
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

    # Resource Types
    op.create_table(
        'resource_types',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('schema', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('required_properties', postgresql.ARRAY(sa.String()), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_resource_types_name'), 'resource_types', ['name'], unique=True)

    # Resources
    op.create_table(
        'resources',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('resource_type_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('properties', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('requires_approval', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['resource_type_id'], ['resource_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_resources_name'), 'resources', ['name'])

    # Resource Managers
    op.create_table(
        'resource_managers',
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.ForeignKeyConstraint(['resource_id'], ['resources.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('resource_id', 'user_id')
    )

    # Bookings
    op.create_table(
        'bookings',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('purpose', sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(['resource_id'], ['resources.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('end_time > start_time', name='check_booking_end_after_start')
    )
    op.create_index(op.f('ix_bookings_start_time'), 'bookings', ['start_time'])
    op.create_index(op.f('ix_bookings_end_time'), 'bookings', ['end_time'])
    op.create_index(op.f('ix_bookings_status'), 'bookings', ['status'])
    op.create_index('ix_bookings_resource_dates', 'bookings', ['resource_id', 'start_time', 'end_time'])
    op.create_index('ix_bookings_user', 'bookings', ['user_id'])

    # Booking Approvals
    op.create_table(
        'booking_approvals',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('booking_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('approver_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('decision_time', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['booking_id'], ['bookings.id'], ),
        sa.ForeignKeyConstraint(['approver_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_booking_approvals_booking', 'booking_approvals', ['booking_id'])


def downgrade():
    op.drop_table('booking_approvals')
    op.drop_table('bookings')
    op.drop_table('resource_managers')
    op.drop_table('resources')
    op.drop_table('resource_types')
    op.drop_table('users')
