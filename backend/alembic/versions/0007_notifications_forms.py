"""create notifications and configurable forms

Revision ID: 0007_notifications_forms
Revises: 0006_fees_payments
Create Date: 2026-09-25
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0007_notifications_forms"
down_revision: str | None = "0006_fees_payments"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def tenant_table(name: str, columns: list[sa.Column]) -> None:
    op.create_table(
        name,
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        *columns,
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(f"ix_{name}_tenant_id", name, ["tenant_id"])


def upgrade() -> None:
    tenant_table(
        "notification_templates",
        [
            sa.Column("channel", sa.String(20), nullable=False),
            sa.Column("title", sa.String(160), nullable=False),
            sa.Column("body_template", sa.String(1000), nullable=False),
        ],
    )
    tenant_table(
        "notifications",
        [
            sa.Column("recipient_user_id", sa.Uuid(), nullable=False),
            sa.Column("title", sa.String(160), nullable=False),
            sa.Column("body", sa.String(1000), nullable=False),
            sa.Column("sensitive", sa.Boolean(), nullable=False, server_default=sa.false()),
        ],
    )
    tenant_table(
        "form_definitions",
        [
            sa.Column("form_key", sa.String(80), nullable=False),
            sa.Column("version", sa.Integer(), nullable=False),
            sa.Column("schema", sa.JSON(), nullable=False),
        ],
    )
    tenant_table(
        "form_submissions",
        [
            sa.Column("form_definition_id", sa.Uuid(), nullable=False),
            sa.Column("submitted_by", sa.Uuid(), nullable=False),
            sa.Column("values", sa.JSON(), nullable=False),
        ],
    )


def downgrade() -> None:
    for name in ["form_submissions", "form_definitions", "notifications", "notification_templates"]:
        op.drop_index(f"ix_{name}_tenant_id", table_name=name)
        op.drop_table(name)
