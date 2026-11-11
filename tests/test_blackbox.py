"""Black-Box Test Suite for Student Course Registration System.

Software Quality Engineering - Assignment 2
Techniques:
    - Equivalence Class Partitioning
    - Boundary Value Analysis
    - Decision Table Testing
    - State Transition & Invariant Verification
"""

import pytest
from registration import (
    Student,
    Course,
    check_credit_limit,
    prerequisites_satisfied,
    registration_decision,
    register_course,
    withdraw_course,
)


# =====================================================================
# SECTION 1: EQUIVALENCE CLASS PARTITIONING (ECP)
# Requirements Covered: FR-01, FR-02, FR-03, FR-04, FR-05, FR-06,
#                       FR-07, FR-08, FR-10, FR-11, FR-12, FR-13, FR-14, FR-15
# =====================================================================

class TestEquivalenceClassPartitioning:
    """Equivalance Class Partitioning tests covering valid and invalid classes."""

    def test_tc_ecp_01_valid_credit_hours_within_limit(self):
        assert check_credit_limit(12, 3) is True

    def test_tc_ecp_02_invalid_credit_hours_exceeding_limit(self):
        assert check_credit_limit(16, 4) is False

    def test_tc_ecp_03_invalid_current_credits_negative(self):
        with pytest.raises(ValueError, match="Invalid current credits"):
            check_credit_limit(-2, 3)

    def test_tc_ecp_04_invalid_current_credits_above_maximum(self):
        with pytest.raises(ValueError, match="Invalid current credits"):
            check_credit_limit(20, 3)

    def test_tc_ecp_05_invalid_course_credits_below_minimum(self):
        with pytest.raises(ValueError, match="Invalid course credits"):
            check_credit_limit(10, 0)

    def test_tc_ecp_06_invalid_course_credits_above_maximum(self):
        with pytest.raises(ValueError, match="Invalid course credits"):
            check_credit_limit(10, 5)

    def test_tc_ecp_07_valid_dues_zero_allows_registration(self):
        student = Student("S001", current_credits=12, outstanding_dues=0)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_ecp_08_valid_dues_positive_blocks_registration(self):
        student = Student("S001", current_credits=12, outstanding_dues=500)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_ecp_09_invalid_dues_negative(self):
        student = Student("S001", outstanding_dues=-100)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        with pytest.raises(ValueError, match="Invalid dues"):
            registration_decision(student, course)

    def test_tc_ecp_10_prerequisites_empty_requirement(self):
        assert prerequisites_satisfied(set(), set()) is True

    def test_tc_ecp_11_prerequisites_all_satisfied(self):
        required = {"CS101", "CS102"}
        completed = {"CS101", "CS102", "MATH101"}
        assert prerequisites_satisfied(completed, required) is True

    def test_tc_ecp_12_prerequisites_partially_satisfied_fails(self):
        required = {"CS101", "MATH101"}
        completed = {"CS101"}
        assert prerequisites_satisfied(completed, required) is False

        student = Student("S001", completed_courses=completed, current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, prerequisites=required)
        assert registration_decision(student, course) == "PREREQUISITES_MISSING"

    def test_tc_ecp_13_prerequisites_none_satisfied_fails(self):
        assert prerequisites_satisfied(set(), {"CS101"}) is False

    def test_tc_ecp_14_already_registered_status(self):
        student = Student("S001", registered_courses={"CS201"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "ALREADY_REGISTERED"

    def test_tc_ecp_15_seat_available_registered(self):
        student = Student("S001", current_credits=9)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=15)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_ecp_16_seat_full_waitlisted(self):
        student = Student("S001", current_credits=9)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30)
        assert registration_decision(student, course) == "WAITLISTED"

    def test_tc_ecp_17_invalid_capacity_zero_or_negative(self):
        student = Student("S001")
        course = Course("CS201", credit_hours=3, capacity=0, enrolled=0)
        with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
            registration_decision(student, course)

    def test_tc_ecp_18_invalid_enrollment_exceeds_capacity(self):
        student = Student("S001")
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=35)
        with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
            registration_decision(student, course)


# =====================================================================
# SECTION 2: BOUNDARY VALUE ANALYSIS (BVA)
# Requirements Covered: FR-01, FR-02, FR-04, FR-08, FR-15
# =====================================================================

class TestBoundaryValueAnalysis:
    """Boundary Value Analysis focusing on boundary extremes."""

    def test_tc_bva_01_current_credits_just_below_minimum(self):
        with pytest.raises(ValueError, match="Invalid current credits"):
            check_credit_limit(-1, 3)

    def test_tc_bva_02_current_credits_exact_minimum(self):
        assert check_credit_limit(0, 3) is True

    def test_tc_bva_03_current_credits_just_above_minimum(self):
        assert check_credit_limit(1, 3) is True

    def test_tc_bva_04_current_credits_just_below_maximum(self):
        assert check_credit_limit(17, 1) is True

    def test_tc_bva_05_current_credits_exact_maximum(self):
        assert check_credit_limit(18, 1) is False

    def test_tc_bva_06_current_credits_just_above_maximum(self):
        with pytest.raises(ValueError, match="Invalid current credits"):
            check_credit_limit(19, 1)

    def test_tc_bva_07_course_credits_just_below_minimum(self):
        with pytest.raises(ValueError, match="Invalid course credits"):
            check_credit_limit(10, 0)

    def test_tc_bva_08_course_credits_exact_minimum(self):
        assert check_credit_limit(10, 1) is True

    def test_tc_bva_09_course_credits_just_above_minimum(self):
        assert check_credit_limit(10, 2) is True

    def test_tc_bva_10_course_credits_just_below_maximum(self):
        assert check_credit_limit(10, 3) is True

    def test_tc_bva_11_course_credits_exact_maximum(self):
        assert check_credit_limit(10, 4) is True

    def test_tc_bva_12_course_credits_just_above_maximum(self):
        with pytest.raises(ValueError, match="Invalid course credits"):
            check_credit_limit(10, 5)

    def test_tc_bva_13_combined_credits_just_below_boundary(self):
        assert check_credit_limit(14, 3) is True

    def test_tc_bva_14_combined_credits_exact_boundary_18(self):
        assert check_credit_limit(15, 3) is True

    def test_tc_bva_15_combined_credits_just_above_boundary(self):
        assert check_credit_limit(16, 3) is False
        
    def test_tc_bva_16_dues_just_below_zero(self):
        student = Student("S001", outstanding_dues=-1)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        with pytest.raises(ValueError, match="Invalid dues"):
            registration_decision(student, course)

    def test_tc_bva_17_dues_exact_zero(self):
        student = Student("S001", current_credits=12, outstanding_dues=0)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_bva_18_dues_just_above_zero(self):
        student = Student("S001", current_credits=12, outstanding_dues=1)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_bva_19_capacity_just_below_min(self):
        student = Student("S001")
        course = Course("CS201", credit_hours=3, capacity=0, enrolled=0)
        with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
            registration_decision(student, course)

    def test_tc_bva_20_capacity_min_positive(self):
        student = Student("S001", current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=1, enrolled=0)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_bva_21_enrollment_exact_minimum(self):
        student = Student("S001", current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=0)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_bva_22_enrollment_just_below_capacity(self):
        student = Student("S001", current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=29)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_bva_23_enrollment_exact_capacity(self):
        student = Student("S001", current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30)
        assert registration_decision(student, course) == "WAITLISTED"

    def test_tc_bva_24_enrollment_just_above_capacity(self):
        student = Student("S001")
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=31)
        with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
            registration_decision(student, course)

# =====================================================================
# SECTION 3: DECISION TABLE TESTING
# Requirements Covered: FR-04, FR-05, FR-06, FR-07, FR-08, FR-09, FR-15
# Conditions:
#   C1: Dues > 0
#   C2: Already Registered
#   C3: Prerequisites Satisfied
#   C4: Credit Limit Satisfied (sum <= 18)
#   C5: Seat Available (enrolled < capacity)
# Priority Order: Dues -> Already Registered -> Prerequisites -> Credit Limit -> Availability
# =====================================================================

class TestDecisionTable:
    """Decision Table testing verifying all distinct outcomes and priority combinations."""

    def test_tc_dt_01_rule_01_dues_block(self):
        student = Student("S001", outstanding_dues=100, current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_dt_02_rule_02_already_registered(self):
        student = Student("S001", outstanding_dues=0, registered_courses={"CS201"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "ALREADY_REGISTERED"

    def test_tc_dt_03_rule_03_prerequisites_missing(self):
        student = Student("S001", outstanding_dues=0, completed_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, prerequisites={"CS101"})
        assert registration_decision(student, course) == "PREREQUISITES_MISSING"

    def test_tc_dt_04_rule_04_credit_limit(self):
        student = Student("S001", outstanding_dues=0, current_credits=16)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "CREDIT_LIMIT"

    def test_tc_dt_05_rule_05_waitlisted(self):
        student = Student("S001", outstanding_dues=0, current_credits=12)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30)
        assert registration_decision(student, course) == "WAITLISTED"

    def test_tc_dt_06_rule_06_registered(self):
        student = Student("S001", outstanding_dues=0, current_credits=12)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=15)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_dt_07_rule_07_priority_dues_over_already_registered(self):
        student = Student("S001", outstanding_dues=100, registered_courses={"CS201"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_dt_08_rule_08_priority_dues_over_prerequisites(self):
        student = Student("S001", outstanding_dues=200, completed_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, prerequisites={"CS101"})
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_dt_09_rule_09_priority_dues_over_credit_limit(self):
        student = Student("S001", outstanding_dues=50, current_credits=16)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_dt_10_rule_10_priority_dues_over_seat_full(self):
        student = Student("S001", outstanding_dues=50, current_credits=12)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30)
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_dt_11_rule_11_priority_already_reg_over_prerequisites(self):
        student = Student("S001", outstanding_dues=0, registered_courses={"CS201"}, completed_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, prerequisites={"CS101"})
        assert registration_decision(student, course) == "ALREADY_REGISTERED"

    def test_tc_dt_12_rule_12_priority_already_reg_over_credit_limit(self):
        student = Student("S001", outstanding_dues=0, registered_courses={"CS201"}, current_credits=17)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "ALREADY_REGISTERED"

    def test_tc_dt_13_rule_13_priority_prerequisites_over_credit_limit(self):
        student = Student("S001", outstanding_dues=0, current_credits=17, completed_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, prerequisites={"CS101"})
        assert registration_decision(student, course) == "PREREQUISITES_MISSING"

    def test_tc_dt_14_rule_14_priority_prerequisites_over_availability(self):
        student = Student("S001", outstanding_dues=0, current_credits=12, completed_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30, prerequisites={"CS101"})
        assert registration_decision(student, course) == "PREREQUISITES_MISSING"

    def test_tc_dt_15_rule_15_priority_credit_limit_over_availability(self):
        student = Student("S001", outstanding_dues=0, current_credits=16)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30)
        assert registration_decision(student, course) == "CREDIT_LIMIT"

    def test_tc_dt_16_rule_16_validation_dues_negative(self):
        student = Student("S001", outstanding_dues=-5)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        with pytest.raises(ValueError, match="Invalid dues"):
            registration_decision(student, course)

    def test_tc_dt_17_rule_17_validation_capacity_invalid(self):
        student = Student("S001", outstanding_dues=0)
        course = Course("CS201", credit_hours=3, capacity=0, enrolled=0)
        with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
            registration_decision(student, course)

    def test_tc_dt_18_rule_18_validation_enrollment_invalid(self):
        student = Student("S001", outstanding_dues=0)
        course = Course("CS201", credit_hours=3, capacity=20, enrolled=25)
        with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
            registration_decision(student, course)

    def test_tc_dt_19_rule_19_validation_priority_dues_first(self):
        student = Student("S001", outstanding_dues=-10)
        course = Course("CS201", credit_hours=3, capacity=0, enrolled=0)
        with pytest.raises(ValueError, match="Invalid dues"):
            registration_decision(student, course)

# =====================================================================
# SECTION 4: STATE TRANSITION & INVARIANT VERIFICATION
# Requirements Covered: FR-10, FR-11, FR-12, FR-13, FR-14
# =====================================================================

class TestStateTransitionsAndInvariants:
    """Verifies that successful operations update states correctly and unsuccessful ones do not mutate state."""

    def test_tc_state_01_registration_decision_does_not_mutate(self):
        student = Student("S001", current_credits=12, outstanding_dues=0, registered_courses={"CS101"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, waitlist=[])

        decision = registration_decision(student, course)
        assert decision == "REGISTERED"

        assert student.current_credits == 12
        assert student.registered_courses == {"CS101"}
        assert course.enrolled == 10
        assert course.waitlist == []

    def test_tc_state_02_register_course_success_state_update(self):
        student = Student("S001", current_credits=12, outstanding_dues=0, registered_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)

        decision = register_course(student, course)
        assert decision == "REGISTERED"
        assert "CS201" in student.registered_courses
        assert student.current_credits == 15
        assert course.enrolled == 11

    def test_tc_state_03_register_course_waitlisted_state_update(self):
        student = Student("S001", current_credits=12, outstanding_dues=0, registered_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30, waitlist=[])

        decision = register_course(student, course)
        assert decision == "WAITLISTED"
        assert course.waitlist == ["S001"]
        assert student.current_credits == 12
        assert "CS201" not in student.registered_courses
        assert course.enrolled == 30

        decision_repeat = register_course(student, course)
        assert decision_repeat == "WAITLISTED"
        assert course.waitlist == ["S001"]

    def test_tc_state_04_register_course_blocked_does_not_mutate(self):
        student = Student("S001", current_credits=12, outstanding_dues=500, registered_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, waitlist=[])

        decision = register_course(student, course)
        assert decision == "DUES_BLOCK"
        assert student.current_credits == 12
        assert student.registered_courses == set()
        assert course.enrolled == 10
        assert course.waitlist == []

    def test_tc_state_05_withdraw_course_success_state_update(self):
        student = Student("S001", current_credits=15, registered_courses={"CS201"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=15)

        result = withdraw_course(student, course)
        assert result is True
        assert "CS201" not in student.registered_courses
        assert student.current_credits == 12
        assert course.enrolled == 14

    def test_tc_state_06_withdraw_course_not_enrolled_does_not_mutate(self):
        student = Student("S001", current_credits=12, registered_courses={"CS101"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=15)

        result = withdraw_course(student, course)
        assert result is False
        assert student.registered_courses == {"CS101"}
        assert student.current_credits == 12
        assert course.enrolled == 15
