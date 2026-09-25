"""create attendance homework exams and marks

Revision ID: 0004_attendance_exams_results
Revises: 0003_identity_and_academics
Create Date: 2026-09-25
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0004_attendance_exams_results"
down_revision: str | None = "0003_identity_and_academics"
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
        "attendance_records",
        [
            sa.Column("student_enrollment_id", sa.Uuid(), nullable=False),
            sa.Column("section_id", sa.Uuid(), nullable=False),
            sa.Column("recorded_by", sa.Uuid(), nullable=False),
            sa.Column("attendance_date", sa.DateTime(timezone=True), nullable=False),
            sa.Column("status", sa.String(16), nullable=False),
        ],
    )
    tenant_table(
        "homework",
        [
            sa.Column("section_id", sa.Uuid(), nullable=False),
            sa.Column("subject_id", sa.Uuid(), nullable=False),
            sa.Column("teacher_user_id", sa.Uuid(), nullable=False),
            sa.Column("title", sa.String(200), nullable=False),
            sa.Column("instructions", sa.String(4000), nullable=False),
            sa.Column("due_at", sa.DateTime(timezone=True), nullable=False),
        ],
    )
    tenant_table(
        "exams",
        [
            sa.Column("section_id", sa.Uuid(), nullable=False),
            sa.Column("title", sa.String(160), nullable=False),
            sa.Column("published", sa.Boolean(), nullable=False, server_default=sa.false()),
        ],
    )
    tenant_table(
        "marks",
        [
            sa.Column("exam_id", sa.Uuid(), nullable=False),
            sa.Column("subject_id", sa.Uuid(), nullable=False),
            sa.Column("student_enrollment_id", sa.Uuid(), nullable=False),
            sa.Column("teacher_assignment_id", sa.Uuid(), nullable=False),
            sa.Column("score", sa.Float(), nullable=False),
            sa.Column("maximum_score", sa.Float(), nullable=False),
        ],
    )


def downgrade() -> None:
    for name in ["marks", "exams", "homework", "attendance_records"]:
        op.drop_index(f"ix_{name}_tenant_id", table_name=name)
        op.drop_table(name)
