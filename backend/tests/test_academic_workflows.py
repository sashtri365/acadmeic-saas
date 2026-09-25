from uuid import uuid4

import pytest

from app.models import calculate_grade, validate_score
from app.rbac import AuthenticatedUser, can_edit_assignment


def test_marks_are_range_validated_and_graded() -> None:
    assert calculate_grade(95, 100) == "A"
    assert calculate_grade(75, 100) == "C"
    with pytest.raises(ValueError):
        validate_score(101, 100)


def test_teacher_cannot_edit_another_teachers_assignment() -> None:
    teacher_a = AuthenticatedUser(uuid4(), uuid4(), frozenset({"teacher"}))
    teacher_b_id = uuid4()

    assert not can_edit_assignment(teacher_a, teacher_b_id, "section-8a:math", "section-8a:math")
    assert not can_edit_assignment(
        teacher_a, teacher_a.user_id, "section-8a:math", "section-9a:math"
    )
    assert can_edit_assignment(teacher_a, teacher_a.user_id, "section-8a:math", "section-8a:math")
