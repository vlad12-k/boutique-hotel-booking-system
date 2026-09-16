"""Add persistent staff authentication and security audit events.

Revision ID: 20260916_0002
Revises: 20260916_0001
Create Date: 2026-09-16
"""

from alembic import op
import sqlalchemy as sa


revision = "20260916_0002"
down_revision = "20260916_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "staff_account",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("display_name", sa.String(length=120), nullable=False),
        sa.Column("password_hash", sa.String(length=512), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            "password_changed_at",
            sa.DateTime(timezone=True),
            nullable=False,
        ),
        sa.Column("last_login_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint(
            "email = lower(email)",
            name="ck_staff_account_email_normalised",
        ),
        sa.CheckConstraint(
            "role IN ('owner', 'staff')",
            name="ck_staff_account_role",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "security_audit_event",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("staff_account_id", sa.Integer(), nullable=True),
        sa.Column("event_type", sa.String(length=50), nullable=False),
        sa.Column("outcome", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["staff_account_id"],
            ["staff_account.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_security_audit_event_type_created",
        "security_audit_event",
        ["event_type", "created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_security_audit_event_type_created",
        table_name="security_audit_event",
    )
    op.drop_table("security_audit_event")
    op.drop_table("staff_account")
