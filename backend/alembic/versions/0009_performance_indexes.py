"""add tenant-first lookup indexes and scoped uniqueness

Revision ID: 0009_performance_indexes
Revises: 0008_dashboards_audit
Create Date: 2026-09-25
"""

from collections.abc import Sequence

from alembic import op

revision: str = "0009_performance_indexes"
down_revision: str | None = "0008_dashboards_audit"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index("ix_users_tenant_email", "users", ["tenant_id", "email"], unique=True)
    op.create_index(
        "ix_attendance_tenant_student_date",
        "attendance_records",
        ["tenant_id", "student_enrollment_id", "attendance_date"],
    )
    op.create_index(
        "ix_marks_tenant_exam_student_subject",
        "marks",
        ["tenant_id", "exam_id", "student_enrollment_id", "subject_id"],
        unique=True,
    )
    op.create_index(
        "ix_messages_tenant_conversation_created",
        "messages",
        ["tenant_id", "conversation_id", "created_at"],
    )
    op.create_index(
        "ix_invoices_tenant_student_status",
        "student_invoices",
        ["tenant_id", "student_enrollment_id", "status"],
    )
    op.create_index(
        "ix_audit_logs_tenant_created",
        "audit_logs",
        ["tenant_id", "created_at"],
    )
    op.create_unique_constraint(
        "uq_academic_subjects_tenant_code",
        "academic_subjects",
        ["tenant_id", "code"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_academic_subjects_tenant_code", "academic_subjects", type_="unique")
    op.drop_index("ix_audit_logs_tenant_created", table_name="audit_logs")
    op.drop_index("ix_invoices_tenant_student_status", table_name="student_invoices")
    op.drop_index("ix_messages_tenant_conversation_created", table_name="messages")
    op.drop_index("ix_marks_tenant_exam_student_subject", table_name="marks")
    op.drop_index("ix_attendance_tenant_student_date", table_name="attendance_records")
    op.drop_index("ix_users_tenant_email", table_name="users")
