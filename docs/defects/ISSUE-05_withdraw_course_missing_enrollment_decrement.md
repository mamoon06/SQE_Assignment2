# GitHub Issue #5: [BUG] `withdraw_course` fails to decrement course enrollment count

- **Defect ID:** DEF-05
- **Requirement ID:** FR-13
- **Severity:** High
- **Component:** `registration.py` -> `withdraw_course()`
- **Status:** Open - Confirmed Defect
- **Labels:** `bug`, `blackbox-failure`, `high-priority`

---

### Description
According to SRS requirement **FR-13**:
> "`withdraw_course` returns `True` when the student is enrolled in the course; it removes the course from `registered_courses`, subtracts its credit hours, and **decrements `enrolled` by one**."
And SRS Section 6 (Scenario 6):
> "Withdrawing an enrolled student reduces both student credits and course enrollment."

In the current code, withdrawing an enrolled student removes the course from `registered_courses` and reduces the student's credit hours, but leaves `course.enrolled` unchanged.

### Failing Test IDs
- `TC_STATE_05` (`tests/test_blackbox.py::TestStateTransitionsAndInvariants::test_tc_state_05_withdraw_course_success_state_update`)

### Steps to Reproduce
1. Execute Python:
   ```python
   from registration import Student, Course, withdraw_course
   student = Student("S001", current_credits=15, registered_courses={"CS201"})
   course = Course("CS201", credit_hours=3, capacity=30, enrolled=15)
   result = withdraw_course(student, course)
   print(f"Result: {result}, Course Enrolled: {course.enrolled}")
   ```
2. Observe output: `Result: True, Course Enrolled: 15`.

### Expected Output
`Result: True, Course Enrolled: 14`.

### Actual Output
`Result: True, Course Enrolled: 15` (enrolled count not decremented).

### Root Cause Analysis
In `registration.py`, lines 79–81:
```python
student.registered_courses.remove(course.code)
student.current_credits -= course.credit_hours
return True
```
The statement `course.enrolled -= 1` is completely absent before the return.
