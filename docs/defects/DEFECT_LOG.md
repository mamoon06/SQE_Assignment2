# Defect Log — Student Course Registration System

**Project:** SE3002 Software Quality Engineering — Assignment 2  
**Testing Phase:** Part A (Black-Box Testing)  
**Status Date:** Current Testing Baseline  

---

## 1. Summary of Discovered Defects

| Defect ID | GitHub Issue Title | Req ID | Severity | Failed Test IDs | Status |
|---|---|---|---|---|---|
| **DEF-01** | [BUG] `check_credit_limit` rejects valid registration at exactly 18 credits | FR-01 | High | `TC_BVA_04`, `TC_BVA_14` | Open - Confirmed Defect |
| **DEF-02** | [BUG] Outstanding dues between Rs. 1 and Rs. 1000 fail to block registration | FR-04 | Critical | `TC_ECP_08`, `TC_BVA_18`, `TC_DT_01`, `TC_DT_07`, `TC_DT_08`, `TC_DT_09`, `TC_DT_10`, `TC_STATE_04` | Open - Confirmed Defect |
| **DEF-03** | [BUG] `prerequisites_satisfied` accepts partial completion instead of requiring all prerequisites | FR-03, FR-06 | High | `TC_ECP_12` | Open - Confirmed Defect |
| **DEF-04** | [BUG] `registration_decision` returns `REGISTERED` instead of `WAITLISTED` when capacity is full | FR-08 | High | `TC_ECP_16`, `TC_BVA_23`, `TC_DT_05`, `TC_STATE_03` | Open - Confirmed Defect |
| **DEF-05** | [BUG] `withdraw_course` fails to decrement course enrollment count | FR-13 | High | `TC_STATE_05` | Open - Confirmed Defect |

---

## 2. GitHub Issue Mapping and References

All defects have corresponding issue markdown reports stored in `docs/defects/` and ready for immediate logging to the GitHub repository:

- **Issue #1**: `docs/defects/ISSUE-01_check_credit_limit_strict_inequality.md`
- **Issue #2**: `docs/defects/ISSUE-02_outstanding_dues_threshold_mismatch.md`
- **Issue #3**: `docs/defects/ISSUE-03_prerequisites_intersection_instead_of_subset.md`
- **Issue #4**: `docs/defects/ISSUE-04_course_full_waitlist_condition_error.md`
- **Issue #5**: `docs/defects/ISSUE-05_withdraw_course_missing_enrollment_decrement.md`

---

## 3. Recommended Fix Plan for Defect Fix Branch (`defect-fixes`)

| Defect ID | File | Current Code (Line) | Corrected Code |
|---|---|---|---|
| **DEF-01** | `registration.py` | `return current_credits + new_credits < 18` (L34) | `return current_credits + new_credits <= 18` |
| **DEF-02** | `registration.py` | `if student.outstanding_dues > 1000:` (L50) | `if student.outstanding_dues > 0:` |
| **DEF-03** | `registration.py` | `return bool(completed.intersection(required))` (L41) | `return required.issubset(completed)` |
| **DEF-04** | `registration.py` | `if course.enrolled > course.capacity:` (L58) | `if course.enrolled >= course.capacity:` |
| **DEF-05** | `registration.py` | `withdraw_course()` missing decrement (L80) | Add: `course.enrolled -= 1` |
