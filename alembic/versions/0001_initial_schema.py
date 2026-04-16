"""initial schema

Revision ID: 0001_initial_schema
Revises: 
Create Date: 2026-04-16 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'organizations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('slug', sa.String(length=80), nullable=False, unique=True),
        sa.Column('whatsapp_phone_number', sa.String(length=40), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('role', sa.String(length=30), nullable=False, server_default='seller'),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index(op.f('ix_users_organization_id'), 'users', ['organization_id'], unique=False)

    op.create_table(
        'vehicles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('brand', sa.String(length=80), nullable=False),
        sa.Column('model', sa.String(length=80), nullable=False),
        sa.Column('version', sa.String(length=120), nullable=True),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('mileage', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('fuel_type', sa.String(length=50), nullable=True),
        sa.Column('transmission', sa.String(length=50), nullable=True),
        sa.Column('price', sa.Numeric(14, 2), nullable=True),
        sa.Column('currency', sa.String(length=10), nullable=False, server_default='ARS'),
        sa.Column('status', sa.String(length=20), nullable=False, server_default='available'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('photos_json', sa.Text(), nullable=True),
    )
    op.create_index(op.f('ix_vehicles_organization_id'), 'vehicles', ['organization_id'], unique=False)

    op.create_table(
        'leads',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('full_name', sa.String(length=120), nullable=True),
        sa.Column('phone', sa.String(length=40), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=True),
        sa.Column('source', sa.String(length=40), nullable=False, server_default='whatsapp'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='new'),
        sa.Column('interest_notes', sa.Text(), nullable=True),
        sa.Column('assigned_user_id', sa.Integer(), nullable=True),
    )
    op.create_index(op.f('ix_leads_organization_id'), 'leads', ['organization_id'], unique=False)
    op.create_index(op.f('ix_leads_phone'), 'leads', ['phone'], unique=False)

    op.create_table(
        'conversations',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('lead_id', sa.Integer(), sa.ForeignKey('leads.id'), nullable=True),
        sa.Column('channel', sa.String(length=30), nullable=False, server_default='whatsapp'),
        sa.Column('customer_phone', sa.String(length=40), nullable=False),
        sa.Column('current_agent_type', sa.String(length=30), nullable=False, server_default='seller'),
        sa.Column('status', sa.String(length=30), nullable=False, server_default='open'),
    )
    op.create_index(op.f('ix_conversations_organization_id'), 'conversations', ['organization_id'], unique=False)
    op.create_index(op.f('ix_conversations_customer_phone'), 'conversations', ['customer_phone'], unique=False)

    op.create_table(
        'messages',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('conversation_id', sa.Integer(), sa.ForeignKey('conversations.id'), nullable=False),
        sa.Column('sender_type', sa.String(length=20), nullable=False),
        sa.Column('sender_name', sa.String(length=120), nullable=True),
        sa.Column('message_text', sa.Text(), nullable=False),
        sa.Column('raw_payload_json', sa.Text(), nullable=True),
    )
    op.create_index(op.f('ix_messages_conversation_id'), 'messages', ['conversation_id'], unique=False)

    op.create_table(
        'agents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('type', sa.String(length=30), nullable=False),
        sa.Column('active', sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column('prompt', sa.Text(), nullable=True),
    )
    op.create_index(op.f('ix_agents_organization_id'), 'agents', ['organization_id'], unique=False)

    op.create_table(
        'audit_logs',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('organization_id', sa.Integer(), sa.ForeignKey('organizations.id'), nullable=True),
        sa.Column('entity_type', sa.String(length=50), nullable=False),
        sa.Column('entity_id', sa.String(length=50), nullable=True),
        sa.Column('action', sa.String(length=80), nullable=False),
        sa.Column('actor_type', sa.String(length=30), nullable=True),
        sa.Column('payload_json', sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('audit_logs')
    op.drop_index(op.f('ix_agents_organization_id'), table_name='agents')
    op.drop_table('agents')
    op.drop_index(op.f('ix_messages_conversation_id'), table_name='messages')
    op.drop_table('messages')
    op.drop_index(op.f('ix_conversations_customer_phone'), table_name='conversations')
    op.drop_index(op.f('ix_conversations_organization_id'), table_name='conversations')
    op.drop_table('conversations')
    op.drop_index(op.f('ix_leads_phone'), table_name='leads')
    op.drop_index(op.f('ix_leads_organization_id'), table_name='leads')
    op.drop_table('leads')
    op.drop_index(op.f('ix_vehicles_organization_id'), table_name='vehicles')
    op.drop_table('vehicles')
    op.drop_index(op.f('ix_users_organization_id'), table_name='users')
    op.drop_table('users')
    op.drop_table('organizations')
