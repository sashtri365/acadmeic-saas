"""create scoped messaging and parent links

Revision ID: 0005_messaging_parent_links
Revises: 0004_attendance_exams_results
Create Date: 2026-09-25
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0005_messaging_parent_links"
down_revision: str | None = "0004_attendance_exams_results"
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
        "conversations",
        [
            sa.Column("scope_key", sa.String(160), nullable=False),
            sa.Column("subject", sa.String(200), nullable=False),
        ],
    )
    op.create_table(
        "conversation_participants",
        sa.Column("conversation_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("conversation_id", "user_id"),
    )
    op.create_index(
        "ix_conversation_participants_tenant_id", "conversation_participants", ["tenant_id"]
    )
    tenant_table(
        "messages",
        [
            sa.Column("conversation_id", sa.Uuid(), nullable=False),
            sa.Column("sender_id", sa.Uuid(), nullable=False),
            sa.Column("body", sa.String(8000), nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
            sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["sender_id"], ["users.id"]),
        ],
    )
    op.create_table(
        "parent_student_links",
        sa.Column("parent_user_id", sa.Uuid(), nullable=False),
        sa.Column("student_enrollment_id", sa.Uuid(), nullable=False),
        sa.Column("tenant_id", sa.Uuid(), nullable=False),
        sa.Column("verified_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["parent_user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["student_enrollment_id"], ["student_enrollments.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["tenant_id"], ["tenants.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("parent_user_id", "student_enrollment_id"),
    )
    op.create_index("ix_parent_student_links_tenant_id", "parent_student_links", ["tenant_id"])


def downgrade() -> None:
    op.drop_index("ix_parent_student_links_tenant_id", table_name="parent_student_links")
    op.drop_table("parent_student_links")
    op.drop_index("ix_messages_tenant_id", table_name="messages")
    op.drop_table("messages")
    op.drop_index("ix_conversation_participants_tenant_id", table_name="conversation_participants")
    op.drop_table("conversation_participants")
    op.drop_index("ix_conversations_tenant_id", table_name="conversations")
    op.drop_table("conversations")
