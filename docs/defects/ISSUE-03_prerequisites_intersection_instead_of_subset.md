# GitHub Issue #3: [BUG] `prerequisites_satisfied` accepts partial completion instead of requiring all prerequisites

- **Defect ID:** DEF-03
- **Requirement ID:** FR-03, FR-06
- **Severity:** High
- **Component:** `registration.py` -> `prerequisites_satisfied()`
- **Status:** Open - Confirmed Defect
- **Labels:** `bug`, `blackbox-failure`, `high-priority`

---

### Description
According to SRS requirement **FR-03**:
> "`prerequisites_satisfied(completed, required)` returns `True` only if **every** course in `required` appears in `completed`. If `required` is empty, it returns `True`."
And SRS Section 6 (Scenario 3):
> "A course requiring both `CS101` and `MATH101` must reject a student who completed only `CS101`."

In the current code, completing any single course from the prerequisite set causes `prerequisites_satisfied` to return `True`, allowing the student to register despite missing other prerequisites.

### Failing Test IDs
- `TC_ECP_12` (`tests/test_blackbox.py::TestEquivalenceClassPartitioning::test_tc_ecp_12_prerequisites_partially_satisfied_fails`)

### Steps to Reproduce
1. Execute Python:
   ```python
   from registration import prerequisites_satisfied
   completed = {"CS101"}
   required = {"CS101", "MATH101"}
   print(prerequisites_satisfied(completed, required))
   ```
2. Observe return value: `True`.

### Expected Output
`False` (and in registration decision: `"PREREQUISITES_MISSING"`).

### Actual Output
`True`.

### Root Cause Analysis
In `registration.py`, line 41:
```python
return bool(completed.intersection(required))
```
Using set intersection checks whether the intersection is non-empty (at least one course matches), rather than verifying that the required set is completely contained in the completed set (`required.issubset(completed)`).
