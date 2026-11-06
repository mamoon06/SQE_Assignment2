# GitHub Issue #1: [BUG] `check_credit_limit` rejects valid registration at exactly 18 credits

- **Defect ID:** DEF-01
- **Requirement ID:** FR-01
- **Severity:** High
- **Component:** `registration.py` -> `check_credit_limit()`
- **Status:** Open - Confirmed Defect
- **Labels:** `bug`, `blackbox-failure`, `high-priority`

---

### Description
According to SRS requirement **FR-01**:
> "`check_credit_limit(current_credits, new_credits)` returns `True` when `current_credits + new_credits <= 18`, and `False` otherwise, for valid arguments. A total of **exactly 18** is allowed."

However, calling `check_credit_limit()` when the sum equals 18 (e.g., current credits = 15, new credits = 3, or current credits = 17, new credits = 1) returns `False` instead of `True`.

### Failing Test IDs
- `TC_BVA_04` (`tests/test_blackbox.py::TestBoundaryValueAnalysis::test_tc_bva_04_current_credits_just_below_maximum`)
- `TC_BVA_14` (`tests/test_blackbox.py::TestBoundaryValueAnalysis::test_tc_bva_14_combined_credits_exact_boundary_18`)

### Steps to Reproduce
1. Execute python interactive shell or test script:
   ```python
   from registration import check_credit_limit
   result = check_credit_limit(15, 3)
   print(result)
   ```
2. Observe return value: `False`.

### Expected Output
`True` (15 + 3 = 18 <= 18 is permitted).

### Actual Output
`False`.

### Root Cause Analysis
In `registration.py`, line 34:
```python
return current_credits + new_credits < 18
```
A strict inequality (`<`) was implemented instead of less-than-or-equal (`<=`).
