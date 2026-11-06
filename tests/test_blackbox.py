"""Black-Box Test Suite for Student Course Registration System.

Course: SE3002 Software Quality Engineering - Assignment 2
Techniques:
    - Equivalence Class Partitioning (ECP)
    - Boundary Value Analysis (BVA)
    - Decision Table Testing
    - State Transition & Invariant Verification

Author: Student (Black-Box Testing Specialist)
Expected results derived strictly from REQUIREMENTS.md specification.
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
    """Equivalence Class Partitioning tests covering valid and invalid classes."""

    def test_tc_ecp_01_valid_credit_hours_within_limit(self):
        """TC_ECP_01: Valid current credits and course credits with sum <= 18.
        Requirement: FR-01. Representative: 12 + 3 = 15 <= 18 -> True.
        """
        assert check_credit_limit(12, 3) is True

    def test_tc_ecp_02_invalid_credit_hours_exceeding_limit(self):
        """TC_ECP_02: Valid current credits and course credits with sum > 18.
        Requirement: FR-01. Representative: 16 + 4 = 20 > 18 -> False.
        """
        assert check_credit_limit(16, 4) is False

    def test_tc_ecp_03_invalid_current_credits_negative(self):
        """TC_ECP_03: Invalid current credits (< 0).
        Requirement: FR-02. Representative: current = -2.
        """
        with pytest.raises(ValueError, match="Invalid current credits"):
            check_credit_limit(-2, 3)

    def test_tc_ecp_04_invalid_current_credits_above_maximum(self):
        """TC_ECP_04: Invalid current credits (> 18).
        Requirement: FR-02. Representative: current = 20.
        """
        with pytest.raises(ValueError, match="Invalid current credits"):
            check_credit_limit(20, 3)

    def test_tc_ecp_05_invalid_course_credits_below_minimum(self):
        """TC_ECP_05: Invalid course credits (< 1).
        Requirement: FR-02. Representative: new_credits = 0.
        """
        with pytest.raises(ValueError, match="Invalid course credits"):
            check_credit_limit(10, 0)

    def test_tc_ecp_06_invalid_course_credits_above_maximum(self):
        """TC_ECP_06: Invalid course credits (> 4).
        Requirement: FR-02. Representative: new_credits = 5.
        """
        with pytest.raises(ValueError, match="Invalid course credits"):
            check_credit_limit(10, 5)

    def test_tc_ecp_07_valid_dues_zero_allows_registration(self):
        """TC_ECP_07: Outstanding dues == 0 allows registration.
        Requirement: FR-04. Representative: dues = 0.
        """
        student = Student("S001", current_credits=12, outstanding_dues=0)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_ecp_08_valid_dues_positive_blocks_registration(self):
        """TC_ECP_08: Outstanding dues > 0 blocks registration with DUES_BLOCK.
        Requirement: FR-04. Representative: dues = 500 (Rs. 500 > 0).
        """
        student = Student("S001", current_credits=12, outstanding_dues=500)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_ecp_09_invalid_dues_negative(self):
        """TC_ECP_09: Outstanding dues < 0 raises ValueError('Invalid dues').
        Requirement: FR-15. Representative: dues = -100.
        """
        student = Student("S001", outstanding_dues=-100)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        with pytest.raises(ValueError, match="Invalid dues"):
            registration_decision(student, course)

    def test_tc_ecp_10_prerequisites_empty_requirement(self):
        """TC_ECP_10: Course with no prerequisites required returns True.
        Requirement: FR-03. Representative: required = set(), completed = set().
        """
        assert prerequisites_satisfied(set(), set()) is True

    def test_tc_ecp_11_prerequisites_all_satisfied(self):
        """TC_ECP_11: Student has completed all required prerequisites.
        Requirement: FR-03. Representative: required={'CS101', 'CS102'},
        completed={'CS101', 'CS102', 'MATH101'}.
        """
        required = {"CS101", "CS102"}
        completed = {"CS101", "CS102", "MATH101"}
        assert prerequisites_satisfied(completed, required) is True

    def test_tc_ecp_12_prerequisites_partially_satisfied_fails(self):
        """TC_ECP_12: Student completed only a subset of prerequisites.
        Requirement: FR-03, FR-06. Representative: required={'CS101', 'MATH101'},
        completed={'CS101'}. Must return False / PREREQUISITES_MISSING.
        """
        required = {"CS101", "MATH101"}
        completed = {"CS101"}
        assert prerequisites_satisfied(completed, required) is False

        student = Student("S001", completed_courses=completed, current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, prerequisites=required)
        assert registration_decision(student, course) == "PREREQUISITES_MISSING"

    def test_tc_ecp_13_prerequisites_none_satisfied_fails(self):
        """TC_ECP_13: Student completed none of the required prerequisites.
        Requirement: FR-03, FR-06. Representative: required={'CS101'}, completed=set().
        """
        assert prerequisites_satisfied(set(), {"CS101"}) is False

    def test_tc_ecp_14_already_registered_status(self):
        """TC_ECP_14: Student already enrolled in target course returns ALREADY_REGISTERED.
        Requirement: FR-05. Representative: course in student.registered_courses.
        """
        student = Student("S001", registered_courses={"CS201"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "ALREADY_REGISTERED"

    def test_tc_ecp_15_seat_available_registered(self):
        """TC_ECP_15: Course has available seats (enrolled < capacity).
        Requirement: FR-08. Representative: enrolled=15, capacity=30.
        """
        student = Student("S001", current_credits=9)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=15)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_ecp_16_seat_full_waitlisted(self):
        """TC_ECP_16: Course is at full capacity (enrolled == capacity).
        Requirement: FR-08. Representative: enrolled=30, capacity=30.
        """
        student = Student("S001", current_credits=9)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30)
        assert registration_decision(student, course) == "WAITLISTED"

    def test_tc_ecp_17_invalid_capacity_zero_or_negative(self):
        """TC_ECP_17: Course capacity < 1 raises ValueError('Invalid capacity or enrollment').
        Requirement: FR-15. Representative: capacity = 0.
        """
        student = Student("S001")
        course = Course("CS201", credit_hours=3, capacity=0, enrolled=0)
        with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
            registration_decision(student, course)

    def test_tc_ecp_18_invalid_enrollment_exceeds_capacity(self):
        """TC_ECP_18: Course enrollment > capacity raises ValueError.
        Requirement: FR-15. Representative: capacity = 30, enrolled = 35.
        """
        student = Student("S001")
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=35)
        with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
            registration_decision(student, course)


# =====================================================================
# SECTION 2: BOUNDARY VALUE ANALYSIS (BVA)
# Requirements Covered: FR-01, FR-02, FR-04, FR-08, FR-15
# =====================================================================

class TestBoundaryValueAnalysis:
    """Boundary Value Analysis focusing on boundary extremes, just-inside, and just-outside."""

    # --- Current Credits Boundaries (0 to 18) ---

    def test_tc_bva_01_current_credits_just_below_minimum(self):
        """TC_BVA_01: Current credits just below min (-1).
        Requirement: FR-02. Boundary: -1 (< 0).
        """
        with pytest.raises(ValueError, match="Invalid current credits"):
            check_credit_limit(-1, 3)

    def test_tc_bva_02_current_credits_exact_minimum(self):
        """TC_BVA_02: Current credits at min boundary (0).
        Requirement: FR-01, FR-02. Boundary: 0 (0 + 3 = 3 <= 18 -> True).
        """
        assert check_credit_limit(0, 3) is True

    def test_tc_bva_03_current_credits_just_above_minimum(self):
        """TC_BVA_03: Current credits just above min (1).
        Requirement: FR-01, FR-02. Boundary: 1 (1 + 3 = 4 <= 18 -> True).
        """
        assert check_credit_limit(1, 3) is True

    def test_tc_bva_04_current_credits_just_below_maximum(self):
        """TC_BVA_04: Current credits just below max (17).
        Requirement: FR-01, FR-02. Boundary: 17 (17 + 1 = 18 <= 18 -> True).
        """
        assert check_credit_limit(17, 1) is True

    def test_tc_bva_05_current_credits_exact_maximum(self):
        """TC_BVA_05: Current credits at max boundary (18).
        Requirement: FR-01, FR-02. Boundary: 18 (18 + 1 = 19 > 18 -> False).
        """
        assert check_credit_limit(18, 1) is False

    def test_tc_bva_06_current_credits_just_above_maximum(self):
        """TC_BVA_06: Current credits just above max (19).
        Requirement: FR-02. Boundary: 19 (> 18).
        """
        with pytest.raises(ValueError, match="Invalid current credits"):
            check_credit_limit(19, 1)

    # --- Course Credits Boundaries (1 to 4) ---

    def test_tc_bva_07_course_credits_just_below_minimum(self):
        """TC_BVA_07: Course credits just below min (0).
        Requirement: FR-02. Boundary: 0 (< 1).
        """
        with pytest.raises(ValueError, match="Invalid course credits"):
            check_credit_limit(10, 0)

    def test_tc_bva_08_course_credits_exact_minimum(self):
        """TC_BVA_08: Course credits at min boundary (1).
        Requirement: FR-01, FR-02. Boundary: 1 (10 + 1 = 11 <= 18 -> True).
        """
        assert check_credit_limit(10, 1) is True

    def test_tc_bva_09_course_credits_just_above_minimum(self):
        """TC_BVA_09: Course credits just above min (2).
        Requirement: FR-01, FR-02. Boundary: 2 (10 + 2 = 12 <= 18 -> True).
        """
        assert check_credit_limit(10, 2) is True

    def test_tc_bva_10_course_credits_just_below_maximum(self):
        """TC_BVA_10: Course credits just below max (3).
        Requirement: FR-01, FR-02. Boundary: 3 (10 + 3 = 13 <= 18 -> True).
        """
        assert check_credit_limit(10, 3) is True

    def test_tc_bva_11_course_credits_exact_maximum(self):
        """TC_BVA_11: Course credits at max boundary (4).
        Requirement: FR-01, FR-02. Boundary: 4 (10 + 4 = 14 <= 18 -> True).
        """
        assert check_credit_limit(10, 4) is True

    def test_tc_bva_12_course_credits_just_above_maximum(self):
        """TC_BVA_12: Course credits just above max (5).
        Requirement: FR-02. Boundary: 5 (> 4).
        """
        with pytest.raises(ValueError, match="Invalid course credits"):
            check_credit_limit(10, 5)

    # --- Combined 18-Credit Maximum Boundaries ---

    def test_tc_bva_13_combined_credits_just_below_boundary(self):
        """TC_BVA_13: Combined credits just below 18 (17).
        Requirement: FR-01. Boundary: 14 + 3 = 17 <= 18 -> True.
        """
        assert check_credit_limit(14, 3) is True

    def test_tc_bva_14_combined_credits_exact_boundary_18(self):
        """TC_BVA_14: Combined credits exactly at limit (18).
        Requirement: FR-01. Specification explicit: 'A total of exactly 18 is allowed.'
        Boundary: 15 + 3 = 18 <= 18 -> True.
        """
        assert check_credit_limit(15, 3) is True

    def test_tc_bva_15_combined_credits_just_above_boundary(self):
        """TC_BVA_15: Combined credits just above 18 (19).
        Requirement: FR-01. Boundary: 16 + 3 = 19 > 18 -> False.
        """
        assert check_credit_limit(16, 3) is False

    # --- Dues Near Zero Boundaries ---

    def test_tc_bva_16_dues_just_below_zero(self):
        """TC_BVA_16: Dues just below 0 (-1).
        Requirement: FR-15. Boundary: -1 (< 0).
        """
        student = Student("S001", outstanding_dues=-1)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        with pytest.raises(ValueError, match="Invalid dues"):
            registration_decision(student, course)

    def test_tc_bva_17_dues_exact_zero(self):
        """TC_BVA_17: Dues exactly at 0.
        Requirement: FR-04. Boundary: 0 (Allowed -> REGISTERED).
        """
        student = Student("S001", current_credits=12, outstanding_dues=0)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_bva_18_dues_just_above_zero(self):
        """TC_BVA_18: Dues just above 0 (1 rupee).
        Requirement: FR-04. Specification explicit: 'any positive balance blocks new registrations.'
        Boundary: 1 (> 0 -> DUES_BLOCK).
        """
        student = Student("S001", current_credits=12, outstanding_dues=1)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "DUES_BLOCK"

    # --- Course Capacity and Enrollment Boundaries ---

    def test_tc_bva_19_capacity_just_below_min(self):
        """TC_BVA_19: Capacity just below min (0).
        Requirement: FR-15. Boundary: capacity = 0 (< 1).
        """
        student = Student("S001")
        course = Course("CS201", credit_hours=3, capacity=0, enrolled=0)
        with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
            registration_decision(student, course)

    def test_tc_bva_20_capacity_min_positive(self):
        """TC_BVA_20: Capacity at min positive boundary (1).
        Requirement: FR-08, FR-15. Boundary: capacity = 1, enrolled = 0 -> REGISTERED.
        """
        student = Student("S001", current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=1, enrolled=0)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_bva_21_enrollment_exact_minimum(self):
        """TC_BVA_21: Enrollment at min (0).
        Requirement: FR-08. Boundary: enrolled = 0 < capacity (30) -> REGISTERED.
        """
        student = Student("S001", current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=0)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_bva_22_enrollment_just_below_capacity(self):
        """TC_BVA_22: Enrollment just below capacity (capacity - 1).
        Requirement: FR-08. Boundary: enrolled = 29, capacity = 30 -> REGISTERED.
        """
        student = Student("S001", current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=29)
        assert registration_decision(student, course) == "REGISTERED"

    def test_tc_bva_23_enrollment_exact_capacity(self):
        """TC_BVA_23: Enrollment exactly at capacity (capacity).
        Requirement: FR-08. Specification: 'When enrolled == capacity, outcome is WAITLISTED.'
        Boundary: enrolled = 30, capacity = 30 -> WAITLISTED.
        """
        student = Student("S001", current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30)
        assert registration_decision(student, course) == "WAITLISTED"

    def test_tc_bva_24_enrollment_just_above_capacity(self):
        """TC_BVA_24: Enrollment just above capacity (capacity + 1).
        Requirement: FR-15. Boundary: enrolled = 31, capacity = 30 -> ValueError.
        """
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

    # --- Distinct Outcomes (Rules 1 to 6) ---

    def test_tc_dt_01_rule_01_dues_block(self):
        """TC_DT_01 [Rule 1]: C1=True (dues > 0).
        All other conditions don't care. Outcome: DUES_BLOCK.
        """
        student = Student("S001", outstanding_dues=100, current_credits=10)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_dt_02_rule_02_already_registered(self):
        """TC_DT_02 [Rule 2]: C1=False, C2=True (already registered).
        C3, C4, C5 don't care. Outcome: ALREADY_REGISTERED.
        """
        student = Student("S001", outstanding_dues=0, registered_courses={"CS201"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "ALREADY_REGISTERED"

    def test_tc_dt_03_rule_03_prerequisites_missing(self):
        """TC_DT_03 [Rule 3]: C1=False, C2=False, C3=False (prereqs not satisfied).
        C4, C5 don't care. Outcome: PREREQUISITES_MISSING.
        """
        student = Student("S001", outstanding_dues=0, completed_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, prerequisites={"CS101"})
        assert registration_decision(student, course) == "PREREQUISITES_MISSING"

    def test_tc_dt_04_rule_04_credit_limit(self):
        """TC_DT_04 [Rule 4]: C1=False, C2=False, C3=True, C4=False (credits exceeded).
        C5 don't care. Outcome: CREDIT_LIMIT.
        """
        student = Student("S001", outstanding_dues=0, current_credits=16)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "CREDIT_LIMIT"

    def test_tc_dt_05_rule_05_waitlisted(self):
        """TC_DT_05 [Rule 5]: C1=False, C2=False, C3=True, C4=True, C5=False (full).
        Outcome: WAITLISTED.
        """
        student = Student("S001", outstanding_dues=0, current_credits=12)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30)
        assert registration_decision(student, course) == "WAITLISTED"

    def test_tc_dt_06_rule_06_registered(self):
        """TC_DT_06 [Rule 6]: C1=False, C2=False, C3=True, C4=True, C5=True (available).
        Outcome: REGISTERED.
        """
        student = Student("S001", outstanding_dues=0, current_credits=12)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=15)
        assert registration_decision(student, course) == "REGISTERED"

    # --- Priority Interactions (Rules 7 to 15) ---

    def test_tc_dt_07_rule_07_priority_dues_over_already_registered(self):
        """TC_DT_07 [Rule 7]: C1=True, C2=True.
        Dues has higher priority than already registered. Outcome: DUES_BLOCK.
        """
        student = Student("S001", outstanding_dues=100, registered_courses={"CS201"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_dt_08_rule_08_priority_dues_over_prerequisites(self):
        """TC_DT_08 [Rule 8]: C1=True, C3=False.
        Dues has higher priority than missing prerequisites. Outcome: DUES_BLOCK.
        """
        student = Student("S001", outstanding_dues=200, completed_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, prerequisites={"CS101"})
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_dt_09_rule_09_priority_dues_over_credit_limit(self):
        """TC_DT_09 [Rule 9]: C1=True, C4=False (16 + 3 = 19).
        Dues has higher priority than credit limit. Outcome: DUES_BLOCK.
        """
        student = Student("S001", outstanding_dues=50, current_credits=16)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_dt_10_rule_10_priority_dues_over_seat_full(self):
        """TC_DT_10 [Rule 10]: C1=True, C5=False (enrolled == capacity).
        Dues has higher priority than waitlist. Outcome: DUES_BLOCK.
        """
        student = Student("S001", outstanding_dues=50, current_credits=12)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30)
        assert registration_decision(student, course) == "DUES_BLOCK"

    def test_tc_dt_11_rule_11_priority_already_reg_over_prerequisites(self):
        """TC_DT_11 [Rule 11]: C1=False, C2=True, C3=False.
        Already registered has higher priority than prerequisites. Outcome: ALREADY_REGISTERED.
        """
        student = Student("S001", outstanding_dues=0, registered_courses={"CS201"}, completed_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, prerequisites={"CS101"})
        assert registration_decision(student, course) == "ALREADY_REGISTERED"

    def test_tc_dt_12_rule_12_priority_already_reg_over_credit_limit(self):
        """TC_DT_12 [Rule 12]: C1=False, C2=True, C4=False.
        Already registered has higher priority than credit limit. Outcome: ALREADY_REGISTERED.
        """
        student = Student("S001", outstanding_dues=0, registered_courses={"CS201"}, current_credits=17)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        assert registration_decision(student, course) == "ALREADY_REGISTERED"

    def test_tc_dt_13_rule_13_priority_prerequisites_over_credit_limit(self):
        """TC_DT_13 [Rule 13]: C1=False, C2=False, C3=False, C4=False.
        Prerequisites has higher priority than credit limit. Outcome: PREREQUISITES_MISSING.
        """
        student = Student("S001", outstanding_dues=0, current_credits=17, completed_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, prerequisites={"CS101"})
        assert registration_decision(student, course) == "PREREQUISITES_MISSING"

    def test_tc_dt_14_rule_14_priority_prerequisites_over_availability(self):
        """TC_DT_14 [Rule 14]: C1=False, C2=False, C3=False, C5=False (seat full).
        Prerequisites has higher priority than waitlisting. Outcome: PREREQUISITES_MISSING.
        """
        student = Student("S001", outstanding_dues=0, current_credits=12, completed_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30, prerequisites={"CS101"})
        assert registration_decision(student, course) == "PREREQUISITES_MISSING"

    def test_tc_dt_15_rule_15_priority_credit_limit_over_availability(self):
        """TC_DT_15 [Rule 15]: C1=False, C2=False, C3=True, C4=False, C5=False (seat full).
        Credit limit has higher priority than waitlisting. Outcome: CREDIT_LIMIT.
        """
        student = Student("S001", outstanding_dues=0, current_credits=16)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30)
        assert registration_decision(student, course) == "CREDIT_LIMIT"

    # --- Input Validation Priority (Rules 16 to 19) ---

    def test_tc_dt_16_rule_16_validation_dues_negative(self):
        """TC_DT_16 [Rule 16]: Dues < 0 raises ValueError('Invalid dues')."""
        student = Student("S001", outstanding_dues=-5)
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
        with pytest.raises(ValueError, match="Invalid dues"):
            registration_decision(student, course)

    def test_tc_dt_17_rule_17_validation_capacity_invalid(self):
        """TC_DT_17 [Rule 17]: Capacity < 1 raises ValueError('Invalid capacity or enrollment')."""
        student = Student("S001", outstanding_dues=0)
        course = Course("CS201", credit_hours=3, capacity=0, enrolled=0)
        with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
            registration_decision(student, course)

    def test_tc_dt_18_rule_18_validation_enrollment_invalid(self):
        """TC_DT_18 [Rule 18]: Enrolled > capacity raises ValueError('Invalid capacity or enrollment')."""
        student = Student("S001", outstanding_dues=0)
        course = Course("CS201", credit_hours=3, capacity=20, enrolled=25)
        with pytest.raises(ValueError, match="Invalid capacity or enrollment"):
            registration_decision(student, course)

    def test_tc_dt_19_rule_19_validation_priority_dues_first(self):
        """TC_DT_19 [Rule 19]: Negative dues AND invalid capacity.
        Requirement FR-15: 'Validate dues first.'
        Must raise ValueError('Invalid dues').
        """
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
        """TC_STATE_01: registration_decision must not mutate student or course state.
        Requirement: FR-10.
        """
        student = Student("S001", current_credits=12, outstanding_dues=0, registered_courses={"CS101"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, waitlist=[])

        decision = registration_decision(student, course)
        assert decision == "REGISTERED"

        # Verify no mutations
        assert student.current_credits == 12
        assert student.registered_courses == {"CS101"}
        assert course.enrolled == 10
        assert course.waitlist == []

    def test_tc_state_02_register_course_success_state_update(self):
        """TC_STATE_02: Successful registration updates registered_courses, credits, and course.enrolled.
        Requirement: FR-11.
        """
        student = Student("S001", current_credits=12, outstanding_dues=0, registered_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)

        decision = register_course(student, course)
        assert decision == "REGISTERED"
        assert "CS201" in student.registered_courses
        assert student.current_credits == 15
        assert course.enrolled == 11

    def test_tc_state_03_register_course_waitlisted_state_update(self):
        """TC_STATE_03: Waitlisted student added to waitlist once; no credit/enrolled changes.
        Requirement: FR-12.
        """
        student = Student("S001", current_credits=12, outstanding_dues=0, registered_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=30, waitlist=[])

        decision = register_course(student, course)
        assert decision == "WAITLISTED"
        assert course.waitlist == ["S001"]
        assert student.current_credits == 12
        assert "CS201" not in student.registered_courses
        assert course.enrolled == 30

        # Attempting again should not duplicate in waitlist
        decision_repeat = register_course(student, course)
        assert decision_repeat == "WAITLISTED"
        assert course.waitlist == ["S001"]

    def test_tc_state_04_register_course_blocked_does_not_mutate(self):
        """TC_STATE_04: Unsuccessful registration (e.g. dues block) does not alter state.
        Requirement: FR-12.
        """
        student = Student("S001", current_credits=12, outstanding_dues=500, registered_courses=set())
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=10, waitlist=[])

        decision = register_course(student, course)
        assert decision == "DUES_BLOCK"
        assert student.current_credits == 12
        assert student.registered_courses == set()
        assert course.enrolled == 10
        assert course.waitlist == []

    def test_tc_state_05_withdraw_course_success_state_update(self):
        """TC_STATE_05: Successful withdrawal removes course, decrements credits, and decrements course.enrolled.
        Requirement: FR-13.
        """
        student = Student("S001", current_credits=15, registered_courses={"CS201"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=15)

        result = withdraw_course(student, course)
        assert result is True
        assert "CS201" not in student.registered_courses
        assert student.current_credits == 12
        assert course.enrolled == 14

    def test_tc_state_06_withdraw_course_not_enrolled_does_not_mutate(self):
        """TC_STATE_06: Withdrawal when not enrolled returns False and mutates nothing.
        Requirement: FR-14.
        """
        student = Student("S001", current_credits=12, registered_courses={"CS101"})
        course = Course("CS201", credit_hours=3, capacity=30, enrolled=15)

        result = withdraw_course(student, course)
        assert result is False
        assert student.registered_courses == {"CS101"}
        assert student.current_credits == 12
        assert course.enrolled == 15
