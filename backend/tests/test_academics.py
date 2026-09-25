from sqlalchemy import inspect

from app.models import (
    AcademicLevel,
    AcademicProgram,
    AcademicSection,
    AcademicSubject,
    AcademicYear,
    StudentEnrollment,
    TransferConsent,
)


def test_academic_hierarchy_is_institution_type_agnostic() -> None:
    assert AcademicProgram.__table__.c.institution_type.nullable is False
    assert AcademicLevel.__table__.c.label.nullable is False
    assert AcademicSection.__table__.c.label.nullable is False
    assert AcademicSubject.__table__.c.credits.nullable is True


def test_student_transfer_requires_immutable_consent_fields() -> None:
    columns = {column.name for column in inspect(TransferConsent).columns}

    assert {"source_tenant_id", "receiving_tenant_id", "consented_by"} <= columns
    assert StudentEnrollment.__table__.c.tenant_id.nullable is False
    assert AcademicYear.__table__.c.tenant_id.nullable is False
