from pathlib import Path


def test_performance_migration_adds_tenant_first_indexes() -> None:
    migration = Path(__file__).parents[1] / "alembic" / "versions" / "0009_performance_indexes.py"
    source = migration.read_text(encoding="utf-8")

    assert "ix_users_tenant_email" in source
    assert "ix_marks_tenant_exam_student_subject" in source
    assert "ix_messages_tenant_conversation_created" in source
    assert "uq_academic_subjects_tenant_code" in source
