"""White-box tests for registration.py (SE3002 Assignment 2).

Expected results are taken from REQUIREMENTS.md, NOT from the code's behaviour.
Tests that fail against the supplied source are intentional defect findings
and must not be edited to force a pass.

Techniques: statement/branch coverage, basis path testing for
registration_decision, and MC/DC for its validation condition
(C1: enrolled < 0, C2: enrolled > capacity, C3: capacity < 1).
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import registration  # noqa: E402
from registration import (  # noqa: E402
    Course,
    Student,
    check_credit_limit,
    prerequisites_satisfied,
    register_course,
    registration_decision,
    withdraw_course,
)


def make_student(**kw):
    defaults = dict(student_id="S1")
    defaults.update(kw)
    return Student(**defaults)


def make_course(**kw):
    defaults = dict(code="CS201", credit_hours=3, capacity=30, enrolled=0)
    defaults.update(kw)
    return Course(**defaults)


# ---------------------------------------------------------------------------
# check_credit_limit  (FR-01, FR-02)
# ---------------------------------------------------------------------------
def test_credit_limit_total_below_18_true():
    assert check_credit_limit(14, 3) is True


def test_credit_limit_total_exactly_18_true():  # FR-01 (defect: uses < 18)
    assert check_credit_limit(15, 3) is True


def test_credit_limit_total_above_18_false():
    assert check_credit_limit(16, 3) is False


def test_credit_limit_current_below_range():
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(-1, 3)


def test_credit_limit_current_above_range():
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(19, 3)


def test_credit_limit_new_below_range():
    with pytest.raises(ValueError, match="Invalid course credits"):
        check_credit_limit(10, 0)


def test_credit_limit_new_above_range():
    with pytest.raises(ValueError, match="Invalid course credits"):
        check_credit_limit(10, 5)


def test_credit_limit_validation_order_current_first():  # FR-02
    with pytest.raises(ValueError, match="Invalid current credits"):
        check_credit_limit(-1, 99)


# ---------------------------------------------------------------------------
# prerequisites_satisfied  (FR-03)
# ---------------------------------------------------------------------------
def test_prereq_empty_required_true():
    assert prerequisites_satisfied(set(), set()) is True


def test_prereq_all_completed_true():
    assert prerequisites_satisfied({"CS101", "MATH101"}, {"CS101", "MATH101"}) is True


def test_prereq_none_completed_false():
    assert prerequisites_satisfied({"PHY101"}, {"CS101", "MATH101"}) is False


def test_prereq_partially_completed_false():  # FR-03 (defect: any match passes)
    assert prerequisites_satisfied({"CS101"}, {"CS101", "MATH101"}) is False


# ---------------------------------------------------------------------------
# registration_decision: basis paths P1-P8 and MC/DC  (FR-04..FR-10, FR-15)
# ---------------------------------------------------------------------------
def test_path_P1_negative_dues_raises():
    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(make_student(outstanding_dues=-1), make_course())


def test_dues_validated_before_capacity():  # FR-15 ordering
    with pytest.raises(ValueError, match="Invalid dues"):
        registration_decision(
            make_student(outstanding_dues=-1), make_course(capacity=0, enrolled=0)
        )


# MC/DC pairs for: C1 or C2 or C3
def test_mcdc_T0_valid_capacity_no_error():
    assert registration_decision(make_student(), make_course(enrolled=0, capacity=5)) == "REGISTERED"


def test_mcdc_T1_C1_enrolled_negative():
    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(make_student(), make_course(enrolled=-1, capacity=5))


def test_mcdc_T2_C2_enrolled_above_capacity():
    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(make_student(), make_course(enrolled=6, capacity=5))


def test_mcdc_T3_C3_capacity_below_one():
    with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
        registration_decision(make_student(), make_course(enrolled=0, capacity=0))


def test_path_P3_dues_block_large_balance():
    assert registration_decision(make_student(outstanding_dues=1001), make_course()) == "DUES_BLOCK"


def test_dues_zero_not_blocked():
    assert registration_decision(make_student(outstanding_dues=0), make_course()) == "REGISTERED"


def test_dues_one_rupee_blocks():  # FR-04 (defect: threshold is 1000)
    assert registration_decision(make_student(outstanding_dues=1), make_course()) == "DUES_BLOCK"


def test_dues_1000_blocks():  # FR-04 boundary (defect: threshold is 1000)
    assert registration_decision(make_student(outstanding_dues=1000), make_course()) == "DUES_BLOCK"


def test_path_P4_already_registered():
    s = make_student(registered_courses={"CS201"})
    assert registration_decision(s, make_course()) == "ALREADY_REGISTERED"


def test_path_P5_prerequisites_missing():
    s = make_student(completed_courses={"CS101"})
    c = make_course(prerequisites={"CS101", "MATH101"})
    assert registration_decision(s, c) == "PREREQUISITES_MISSING"  # defect 2 affects this


def test_prereq_none_completed_decision():
    c = make_course(prerequisites={"CS101"})
    assert registration_decision(make_student(), c) == "PREREQUISITES_MISSING"


def test_path_P6_credit_limit_exceeded():
    assert registration_decision(make_student(current_credits=16), make_course()) == "CREDIT_LIMIT"


def test_credit_total_exactly_18_registers():  # FR-01/FR-07 (defect 1)
    assert registration_decision(make_student(current_credits=15), make_course()) == "REGISTERED"


def test_path_P7_course_full_waitlisted():  # FR-08 (defect 4: unreachable branch)
    c = make_course(capacity=30, enrolled=30)
    assert registration_decision(make_student(), c) == "WAITLISTED"


def test_path_P8_registered_seat_available():
    c = make_course(capacity=30, enrolled=29)
    assert registration_decision(make_student(), c) == "REGISTERED"


def test_invalid_current_credits_propagates():
    with pytest.raises(ValueError, match="Invalid current credits"):
        registration_decision(make_student(current_credits=19), make_course())


def test_invalid_course_credits_propagates():
    with pytest.raises(ValueError, match="Invalid course credits"):
        registration_decision(make_student(), make_course(credit_hours=5))


# Priority order (FR-09)
def test_priority_dues_over_already_registered():
    s = make_student(outstanding_dues=5000, registered_courses={"CS201"})
    assert registration_decision(s, make_course()) == "DUES_BLOCK"


def test_priority_already_registered_over_prereq():
    s = make_student(registered_courses={"CS201"})
    c = make_course(prerequisites={"CS101"})
    assert registration_decision(s, c) == "ALREADY_REGISTERED"


def test_priority_prereq_over_credit_limit():
    s = make_student(current_credits=18)
    c = make_course(prerequisites={"CS101"})
    assert registration_decision(s, c) == "PREREQUISITES_MISSING"


def test_priority_credit_limit_over_waitlist():  # FR-09
    s = make_student(current_credits=17)
    c = make_course(capacity=30, enrolled=30)
    assert registration_decision(s, c) == "CREDIT_LIMIT"


def test_decision_does_not_mutate_state():  # FR-10
    s = make_student(current_credits=3)
    c = make_course(enrolled=5)
    registration_decision(s, c)
    assert s.current_credits == 3 and s.registered_courses == set()
    assert c.enrolled == 5 and c.waitlist == []


# ---------------------------------------------------------------------------
# register_course  (FR-11, FR-12)
# ---------------------------------------------------------------------------
def test_register_success_updates_state():
    s, c = make_student(current_credits=3), make_course(enrolled=5)
    assert register_course(s, c) == "REGISTERED"
    assert "CS201" in s.registered_courses
    assert s.current_credits == 6
    assert c.enrolled == 6


def test_register_blocked_makes_no_changes():  # FR-12
    s, c = make_student(outstanding_dues=5000), make_course(enrolled=5)
    assert register_course(s, c) == "DUES_BLOCK"
    assert s.registered_courses == set() and s.current_credits == 0
    assert c.enrolled == 5 and c.waitlist == []


def test_register_full_course_joins_waitlist_real_flow():  # FR-12 (defect 4)
    s, c = make_student(current_credits=3), make_course(capacity=30, enrolled=30)
    assert register_course(s, c) == "WAITLISTED"
    assert c.waitlist == ["S1"]
    assert s.current_credits == 3 and s.registered_courses == set()
    assert c.enrolled == 30


# The WAITLISTED branch is unreachable through the real decision function,
# so we force it with monkeypatch to cover the compound condition in
# register_course: decision == "WAITLISTED" and id not in waitlist.
def test_register_waitlist_branch_student_absent(monkeypatch):
    monkeypatch.setattr(registration, "registration_decision", lambda s, c: "WAITLISTED")
    s, c = make_student(), make_course()
    assert register_course(s, c) == "WAITLISTED"
    assert c.waitlist == ["S1"]


def test_register_waitlist_branch_student_already_present(monkeypatch):
    monkeypatch.setattr(registration, "registration_decision", lambda s, c: "WAITLISTED")
    s, c = make_student(), make_course(waitlist=["S1"])
    assert register_course(s, c) == "WAITLISTED"
    assert c.waitlist == ["S1"]  # no duplicate


# ---------------------------------------------------------------------------
# withdraw_course  (FR-13, FR-14)
# ---------------------------------------------------------------------------
def test_withdraw_not_registered_returns_false_no_change():  # FR-14
    s, c = make_student(current_credits=6), make_course(enrolled=10)
    assert withdraw_course(s, c) is False
    assert s.current_credits == 6 and c.enrolled == 10


def test_withdraw_registered_updates_student():
    s = make_student(current_credits=6, registered_courses={"CS201"})
    c = make_course(enrolled=10)
    assert withdraw_course(s, c) is True
    assert "CS201" not in s.registered_courses
    assert s.current_credits == 3


def test_withdraw_decrements_enrollment():  # FR-13 (defect 5)
    s = make_student(current_credits=6, registered_courses={"CS201"})
    c = make_course(enrolled=10)
    withdraw_course(s, c)
    assert c.enrolled == 9
