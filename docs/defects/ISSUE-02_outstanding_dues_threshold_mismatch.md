# GitHub Issue #2: [BUG] Outstanding dues between Rs. 1 and Rs. 1000 fail to block registration

- **Defect ID:** DEF-02
- **Requirement ID:** FR-04
- **Severity:** Critical
- **Component:** `registration.py` -> `registration_decision()`
- **Status:** Open - Confirmed Defect
- **Labels:** `bug`, `blackbox-failure`, `critical`

---

### Description
According to SRS requirement **FR-04**:
> "Registration is blocked with `DUES_BLOCK` if a student owes **any amount greater than Rs. 0**."
Furthermore, SRS Section 6 (Scenario 4) states:
> "Outstanding dues of Rs. 1 prevent registration."

In the current implementation, any student owing an amount between Rs. 1 and Rs. 1000 is allowed to register with status `REGISTERED` rather than receiving `DUES_BLOCK`.

### Failing Test IDs
- `TC_ECP_08` (`tests/test_blackbox.py::TestEquivalenceClassPartitioning::test_tc_ecp_08_valid_dues_positive_blocks_registration`)
- `TC_BVA_18` (`tests/test_blackbox.py::TestBoundaryValueAnalysis::test_tc_bva_18_dues_just_above_zero`)
- `TC_DT_01` (`tests/test_blackbox.py::TestDecisionTable::test_tc_dt_01_rule_01_dues_block`)
- `TC_DT_07` (`tests/test_blackbox.py::TestDecisionTable::test_tc_dt_07_rule_07_priority_dues_over_already_registered`)
- `TC_DT_08` (`tests/test_blackbox.py::TestDecisionTable::test_tc_dt_08_rule_08_priority_dues_over_prerequisites`)
- `TC_DT_09` (`tests/test_blackbox.py::TestDecisionTable::test_tc_dt_09_rule_09_priority_dues_over_credit_limit`)
- `TC_DT_10` (`tests/test_blackbox.py::TestDecisionTable::test_tc_dt_10_rule_10_priority_dues_over_seat_full`)
- `TC_STATE_04` (`tests/test_blackbox.py::TestStateTransitionsAndInvariants::test_tc_state_04_register_course_blocked_does_not_mutate`)

### Steps to Reproduce
1. Execute Python:
   ```python
   from registration import Student, Course, registration_decision
   student = Student("S001", current_credits=12, outstanding_dues=500)
   course = Course("CS201", credit_hours=3, capacity=30, enrolled=10)
   print(registration_decision(student, course))
   ```
2. Observe return value: `"REGISTERED"`.

### Expected Output
`"DUES_BLOCK"`.

### Actual Output
`"REGISTERED"`.

### Root Cause Analysis
In `registration.py`, line 50:
```python
if student.outstanding_dues > 1000:
    return "DUES_BLOCK"
```
The threshold was hardcoded to `> 1000` rather than `> 0`.
