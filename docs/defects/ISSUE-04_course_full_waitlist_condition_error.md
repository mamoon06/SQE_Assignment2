# GitHub Issue #4: [BUG] `registration_decision` returns `REGISTERED` instead of `WAITLISTED` when capacity is full

- **Defect ID:** DEF-04
- **Requirement ID:** FR-08
- **Severity:** High
- **Component:** `registration.py` -> `registration_decision()`
- **Status:** Open - Confirmed Defect
- **Labels:** `bug`, `blackbox-failure`, `high-priority`

---

### Description
According to SRS requirement **FR-08**:
> "When `enrolled == capacity`, an otherwise eligible student receives `WAITLISTED`; when `enrolled < capacity`, the outcome is `REGISTERED`."
And SRS Section 6 (Scenario 5):
> "If a course has capacity 30 and enrolled 30, an otherwise eligible student joins the waiting list."

In the current code, when `enrolled == capacity` (e.g., 30/30), `registration_decision` returns `"REGISTERED"` rather than `"WAITLISTED"`.

### Failing Test IDs
- `TC_ECP_16` (`tests/test_blackbox.py::TestEquivalenceClassPartitioning::test_tc_ecp_16_seat_full_waitlisted`)
- `TC_BVA_23` (`tests/test_blackbox.py::TestBoundaryValueAnalysis::test_tc_bva_23_enrollment_exact_capacity`)
- `TC_DT_05` (`tests/test_blackbox.py::TestDecisionTable::test_tc_dt_05_rule_05_waitlisted`)
- `TC_STATE_03` (`tests/test_blackbox.py::TestStateTransitionsAndInvariants::test_tc_state_03_register_course_waitlisted_state_update`)

### Steps to Reproduce
1. Execute Python:
   ```python
   from registration import Student, Course, registration_decision
   student = Student("S001", current_credits=10)
   course = Course("CS201", credit_hours=3, capacity=30, enrolled=30)
   print(registration_decision(student, course))
   ```
2. Observe return value: `"REGISTERED"`.

### Expected Output
`"WAITLISTED"`.

### Actual Output
`"REGISTERED"`.

### Root Cause Analysis
In `registration.py`, line 58:
```python
if course.enrolled > course.capacity:
    return "WAITLISTED"
```
The comparison uses strict inequality (`>`). However, earlier input validation (line 48) raises a `ValueError` if `course.enrolled > course.capacity`. Therefore, line 58 is never reached when `enrolled > capacity`, and returns `"REGISTERED"` when `enrolled == capacity`. The correct logic should check `if course.enrolled >= course.capacity: return "WAITLISTED"`.
