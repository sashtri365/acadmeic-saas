"""create fees and payment infrastructure tables

Revision ID: 0006_fees_payments
Revises: 0005_messaging_parent_links
Create Date: 2026-09-25
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0006_fees_payments"
down_revision: str | None = "0005_messaging_parent_links"
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
        "fee_structures",
        [
            sa.Column("name", sa.String(160), nullable=False),
            sa.Column("amount", sa.Numeric(12, 2), nullable=False),
            sa.Column("currency", sa.String(3), nullable=False),
        ],
    )
    tenant_table(
        "student_invoices",
        [
            sa.Column("student_enrollment_id", sa.Uuid(), nullable=False),
            sa.Column("total_amount", sa.Numeric(12, 2), nullable=False),
            sa.Column("currency", sa.String(3), nullable=False),
            sa.Column("status", sa.String(24), nullable=False),
        ],
    )
    tenant_table(
        "payments",
        [
            sa.Column("invoice_id", sa.Uuid(), nullable=False),
            sa.Column("provider", sa.String(40), nullable=False),
            sa.Column("provider_payment_id", sa.String(160), nullable=False),
            sa.Column("provider_token", sa.String(255), nullable=False),
            sa.Column("idempotency_key", sa.String(160), nullable=False),
            sa.Column("amount", sa.Numeric(12, 2), nullable=False),
            sa.Column("status", sa.String(24), nullable=False),
            sa.UniqueConstraint("idempotency_key"),
        ],
    )
    tenant_table(
        "transactions",
        [
            sa.Column("payment_id", sa.Uuid(), nullable=False),
            sa.Column("event_type", sa.String(40), nullable=False),
            sa.Column("provider_event_id", sa.String(160), nullable=False),
            sa.UniqueConstraint("provider_event_id"),
        ],
    )
    tenant_table(
        "receipts",
        [
            sa.Column("payment_id", sa.Uuid(), nullable=False),
            sa.Column("receipt_number", sa.String(80), nullable=False),
            sa.UniqueConstraint("receipt_number"),
        ],
    )
    tenant_table(
        "refunds",
        [
            sa.Column("payment_id", sa.Uuid(), nullable=False),
            sa.Column("amount", sa.Numeric(12, 2), nullable=False),
            sa.Column("provider_refund_id", sa.String(160), nullable=False),
        ],
    )
    tenant_table(
        "reconciliation_logs",
        [
            sa.Column("provider", sa.String(40), nullable=False),
            sa.Column("provider_event_id", sa.String(160), nullable=False),
            sa.Column("status", sa.String(24), nullable=False),
        ],
    )


def downgrade() -> None:
    for name in [
        "reconciliation_logs",
        "refunds",
        "receipts",
        "transactions",
        "payments",
        "student_invoices",
        "fee_structures",
    ]:
        op.drop_index(f"ix_{name}_tenant_id", table_name=name)
        op.drop_table(name)
