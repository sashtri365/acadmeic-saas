"""create student identity and academic structure tables

Revision ID: 0003_identity_and_academics
Revises: 0002_identity_and_rbac
Create Date: 2026-09-25
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0003_identity_and_academics"
down_revision: str | None = "0002_identity_and_rbac"
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
    op.create_table(
        "global_student_identities",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("legal_name", sa.String(length=200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )
    tenant_table(
        "student_enrollments",
        [
            sa.Column("global_student_id", sa.Uuid(), nullable=False),
            sa.Column("institution_specific_id", sa.String(length=80), nullable=False),
            sa.Column("status", sa.String(length=32), nullable=False),
            sa.ForeignKeyConstraint(["global_student_id"], ["global_student_identities.id"]),
        ],
    )
    op.create_table(
        "transfer_consents",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("student_enrollment_id", sa.Uuid(), nullable=False),
        sa.Column("source_tenant_id", sa.Uuid(), nullable=False),
        sa.Column("receiving_tenant_id", sa.Uuid(), nullable=False),
        sa.Column("consented_by", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.ForeignKeyConstraint(
            ["student_enrollment_id"], ["student_enrollments.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    tenant_table(
        "academic_years",
        [
            sa.Column("label", sa.String(80), nullable=False),
            sa.Column("starts_on", sa.DateTime(timezone=True), nullable=False),
            sa.Column("ends_on", sa.DateTime(timezone=True), nullable=False),
        ],
    )
    tenant_table(
        "academic_programs",
        [
            sa.Column("name", sa.String(160), nullable=False),
            sa.Column("institution_type", sa.String(40), nullable=False),
        ],
    )
    tenant_table(
        "academic_levels",
        [
            sa.Column("program_id", sa.Uuid(), nullable=False),
            sa.Column("label", sa.String(80), nullable=False),
            sa.Column("sequence", sa.Integer(), nullable=False),
            sa.ForeignKeyConstraint(["program_id"], ["academic_programs.id"], ondelete="CASCADE"),
        ],
    )
    tenant_table(
        "academic_sections",
        [
            sa.Column("level_id", sa.Uuid(), nullable=False),
            sa.Column("label", sa.String(80), nullable=False),
            sa.ForeignKeyConstraint(["level_id"], ["academic_levels.id"], ondelete="CASCADE"),
        ],
    )
    tenant_table(
        "academic_subjects",
        [
            sa.Column("code", sa.String(40), nullable=False),
            sa.Column("name", sa.String(160), nullable=False),
            sa.Column("credits", sa.Float(), nullable=True),
        ],
    )


def downgrade() -> None:
    for name in [
        "academic_subjects",
        "academic_sections",
        "academic_levels",
        "academic_programs",
        "academic_years",
    ]:
        op.drop_index(f"ix_{name}_tenant_id", table_name=name)
        op.drop_table(name)
    op.drop_table("transfer_consents")
    op.drop_index("ix_student_enrollments_tenant_id", table_name="student_enrollments")
    op.drop_table("student_enrollments")
    op.drop_table("global_student_identities")
