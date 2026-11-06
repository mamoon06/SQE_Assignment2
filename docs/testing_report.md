# Software Quality Engineering (SE3002) — Assignment 2
## Comprehensive Testing Report: Student Course Registration System

**Date:** November 2026  
**Artifact:** Final Testing Report (Part A & Black-Box Delivery)  
**System Under Test:** Student Course Registration System (`registration.py`)  
**Specification:** Software Requirements Specification (`REQUIREMENTS.md`)  

---

### Group Members & Role Distribution

| Member Name | Role / Specialization | Primary Assigned Responsibilities |
|---|---|---|
| **Mamoon (Member 1)** | **Black-Box Testing Specialist** | Part A (ECP, BVA, Decision Table, Suite Optimization, Pytest Suite), Repository Setup, CI Pipeline, Defect Logging |
| **Partner (Member 2)** | **White-Box Testing Specialist** | Part B (CFG, Cyclomatic Complexity, MC/DC Analysis, White-Box Pytest Suite), Defect Resolution Branch |

---

## 1. Executive Summary

This report documents the rigorous quality engineering and verification process applied to the **Student Course Registration System**. Testing was conducted strictly against the authoritative requirements in `REQUIREMENTS.md` without tailoring assertions to flawed source-code logic.

A total of **67 black-box test cases** were designed and executed across four core testing dimensions:
1. **Equivalence Class Partitioning (ECP)** — 18 tests
2. **Boundary Value Analysis (BVA)** — 24 tests
3. **Decision Table Testing (DT)** — 19 tests
4. **State Transition & Invariant Verification (STATE)** — 6 tests

### Key Baseline Results:
- **Total Tests Executed:** 67
- **Tests Passed:** 51
- **Legitimate Failures (Pre-Fix Defects):** 16
- **Initial Statement & Branch Coverage:** **89%** (57 statements, 26 branches, 4 uncovered statements, 3 partial branches)
- **Distinct Defects Discovered:** **5 critical and high-severity logical defects**

---

## 2. Part A: Black-Box Test Design and Methodology

### 2.1 Equivalence Class Partitioning (ECP) — Task A1
Equivalence partitioning divides the input domain and system state into valid and invalid classes where the system is expected to behave consistently.

#### Input Domains and Partitioning:
1. **Credit Hours Limit (`check_credit_limit`)**:
   - Class 1 (Valid Sum): $0 \le \text{current} \le 18$, $1 \le \text{new} \le 4$, $\text{current} + \text{new} \le 18 \rightarrow \text{True}$.
   - Class 2 (Invalid Sum Exceeded): Valid arguments where $\text{current} + \text{new} > 18 \rightarrow \text{False}$.
   - Class 3 (Invalid Current Credits Below Min): $\text{current} < 0 \rightarrow \text{ValueError("Invalid current credits")}$.
   - Class 4 (Invalid Current Credits Above Max): $\text{current} > 18 \rightarrow \text{ValueError("Invalid current credits")}$.
   - Class 5 (Invalid Course Credits Below Min): $\text{new} < 1 \rightarrow \text{ValueError("Invalid course credits")}$.
   - Class 6 (Invalid Course Credits Above Max): $\text{new} > 4 \rightarrow \text{ValueError("Invalid course credits")}$.
2. **Outstanding Dues (`registration_decision`)**:
   - Class 7 (Valid Zero Dues): $\text{dues} = 0 \rightarrow$ Eligible (Proceeds to subsequent checks).
   - Class 8 (Valid Positive Dues): $\text{dues} > 0 \rightarrow \text{"DUES\_BLOCK"}$.
   - Class 9 (Invalid Negative Dues): $\text{dues} < 0 \rightarrow \text{ValueError("Invalid dues")}$.
3. **Prerequisites (`prerequisites_satisfied`)**:
   - Class 10 (Empty Required Set): $\text{required} = \emptyset \rightarrow \text{True}$.
   - Class 11 (All Prerequisites Completed): $\text{required} \subseteq \text{completed} \rightarrow \text{True}$.
   - Class 12 (Partial Prerequisites Completed): $\text{completed} \cap \text{required} \neq \emptyset$, but $\text{required} \not\subseteq \text{completed} \rightarrow \text{False}$.
   - Class 13 (No Prerequisites Completed): $\text{completed} \cap \text{required} = \emptyset \rightarrow \text{False}$.
4. **Duplicate Registration**:
   - Class 14 (Already Registered): $\text{course.code} \in \text{student.registered\_courses} \rightarrow \text{"ALREADY\_REGISTERED"}$.
5. **Course Capacity and Availability**:
   - Class 15 (Seats Available): $0 \le \text{enrolled} < \text{capacity} \rightarrow \text{"REGISTERED"}$.
   - Class 16 (Full Capacity): $\text{enrolled} = \text{capacity} \rightarrow \text{"WAITLISTED"}$.
   - Class 17 (Invalid Capacity): $\text{capacity} < 1 \rightarrow \text{ValueError("Invalid capacity or enrollment")}$.
   - Class 18 (Invalid Enrollment): $\text{enrolled} > \text{capacity} \rightarrow \text{ValueError("Invalid capacity or enrollment")}$.

#### Summary of ECP Test Results:
| Test ID | Req ID | Partition Description | Representative Input | Expected Output | Actual (Initial Code) | Defect Note |
|---|---|---|---|---|---|---|
| `TC_ECP_01` | FR-01 | Valid Credit Sum $\le 18$ | `current=12, course=3` | `True` | PASS | Sum 15 |
| `TC_ECP_02` | FR-01 | Invalid Credit Sum $> 18$ | `current=16, course=4` | `False` | PASS | Sum 20 |
| `TC_ECP_03` | FR-02 | Invalid Current Credits $< 0$ | `current=-2, course=3` | `ValueError` | PASS | Negative credits caught |
| `TC_ECP_04` | FR-02 | Invalid Current Credits $> 18$ | `current=20, course=3` | `ValueError` | PASS | Credits $> 18$ caught |
| `TC_ECP_05` | FR-02 | Invalid Course Credits $< 1$ | `current=10, course=0` | `ValueError` | PASS | Course credits $< 1$ caught |
| `TC_ECP_06` | FR-02 | Invalid Course Credits $> 4$ | `current=10, course=5` | `ValueError` | PASS | Course credits $> 4$ caught |
| `TC_ECP_07` | FR-04 | Valid Zero Dues | `dues=0` | `"REGISTERED"` | PASS | Zero dues allowed |
| `TC_ECP_08` | FR-04 | Valid Positive Dues | `dues=500` | `"DUES_BLOCK"` | **FAIL** | **DEF-02**: checks `dues > 1000` |
| `TC_ECP_09` | FR-15 | Invalid Negative Dues | `dues=-100` | `ValueError` | PASS | Negative dues caught |
| `TC_ECP_10` | FR-03 | Empty Prerequisite Set | `required=set()` | `True` | PASS | Empty set returns True |
| `TC_ECP_11` | FR-03 | All Prerequisites Passed | `req={'CS101','CS102'}` | `True` | PASS | Complete match |
| `TC_ECP_12` | FR-03 | Partial Prerequisites Met | `req={'CS101','MATH101'}` | `False` | **FAIL** | **DEF-03**: uses `intersection` |
| `TC_ECP_13` | FR-03 | No Prerequisites Met | `req={'CS101'}, comp={}` | `False` | PASS | Empty completed returns False |
| `TC_ECP_14` | FR-05 | Already Registered | `code in registered` | `"ALREADY_REGISTERED"` | PASS | Duplicate rejected |
| `TC_ECP_15` | FR-08 | Seat Available | `enrolled=15, cap=30` | `"REGISTERED"` | PASS | Seats available |
| `TC_ECP_16` | FR-08 | Seat Full | `enrolled=30, cap=30` | `"WAITLISTED"` | **FAIL** | **DEF-04**: checks `enrolled > cap` |
| `TC_ECP_17` | FR-15 | Capacity $< 1$ | `cap=0, enrolled=0` | `ValueError` | PASS | Capacity 0 caught |
| `TC_ECP_18` | FR-15 | Enrolled $>$ Capacity | `cap=30, enrolled=35` | `ValueError` | PASS | Over-enrollment caught |

---

### 2.2 Boundary Value Analysis (BVA) — Task A2
Boundary Value Analysis targets faults occurring at edges and transitional boundaries of input and state variables.

#### Boundaries Evaluated:
1. **Current Credits ($0 \le \text{credits} \le 18$)**:
   - Just below min: $-1$ (Invalid)
   - Min boundary: $0$ (Valid)
   - Just above min: $1$ (Valid)
   - Just below max: $17$ (Valid)
   - Max boundary: $18$ (Valid)
   - Just above max: $19$ (Invalid)
2. **New Course Credits ($1 \le \text{credits} \le 4$)**:
   - Just below min: $0$ (Invalid)
   - Min boundary: $1$ (Valid)
   - Just above min: $2$ (Valid)
   - Just below max: $3$ (Valid)
   - Max boundary: $4$ (Valid)
   - Just above max: $5$ (Invalid)
3. **Combined Credit Load Maximum ($18$)**:
   - Just below limit: $14 + 3 = 17 \le 18 \rightarrow \text{True}$
   - Exact limit boundary: $15 + 3 = 18 \le 18 \rightarrow \text{True}$ (Explicitly permitted by FR-01)
   - Just above limit: $16 + 3 = 19 > 18 \rightarrow \text{False}$
4. **Outstanding Dues Near Zero**:
   - Just below zero: $-1$ (Invalid $\rightarrow$ `ValueError("Invalid dues")`)
   - Exact zero: $0$ (Valid $\rightarrow$ Eligible)
   - Just above zero: $1$ (Valid positive $\rightarrow$ `"DUES_BLOCK"`)
5. **Capacity & Enrollment**:
   - Capacity just below min: $0$ (Invalid $\rightarrow$ `ValueError`)
   - Capacity min: $1$ (Valid)
   - Enrollment min: $0$ (Valid)
   - Enrollment just below capacity: $\text{capacity} - 1 = 29$ (Available $\rightarrow$ `"REGISTERED"`)
   - Enrollment at exact capacity: $\text{capacity} = 30$ (Full $\rightarrow$ `"WAITLISTED"`)
   - Enrollment just above capacity: $\text{capacity} + 1 = 31$ (Invalid $\rightarrow$ `ValueError`)

#### Summary of BVA Test Results:
| Test ID | Boundary Variable | Point Type | Input | Expected | Actual (Initial Code) | Defect Note |
|---|---|---|---|---|---|---|
| `TC_BVA_01` | Current credits | Just below min (-1) | `current=-1, new=3` | `ValueError` | PASS | Lower bound exception |
| `TC_BVA_02` | Current credits | Min (0) | `current=0, new=3` | `True` | PASS | 0 credits valid |
| `TC_BVA_03` | Current credits | Just above min (1) | `current=1, new=3` | `True` | PASS | 1 credit valid |
| `TC_BVA_04` | Current credits | Just below max (17) | `current=17, new=1` | `True` | **FAIL** | **DEF-01**: Sum 18 returns False |
| `TC_BVA_05` | Current credits | Max (18) | `current=18, new=1` | `False` | PASS | Sum 19 returns False |
| `TC_BVA_06` | Current credits | Just above max (19) | `current=19, new=1` | `ValueError` | PASS | Upper bound exception |
| `TC_BVA_07` | Course credits | Just below min (0) | `current=10, new=0` | `ValueError` | PASS | Lower course credit bound |
| `TC_BVA_08` | Course credits | Min (1) | `current=10, new=1` | `True` | PASS | Min course credit valid |
| `TC_BVA_09` | Course credits | Just above min (2) | `current=10, new=2` | `True` | PASS | 2 credits valid |
| `TC_BVA_10` | Course credits | Just below max (3) | `current=10, new=3` | `True` | PASS | 3 credits valid |
| `TC_BVA_11` | Course credits | Max (4) | `current=10, new=4` | `True` | PASS | Max course credit valid |
| `TC_BVA_12` | Course credits | Just above max (5) | `current=10, new=5` | `ValueError` | PASS | Upper course credit bound |
| `TC_BVA_13` | Combined load | Just below (17) | `current=14, new=3` | `True` | PASS | Sum 17 valid |
| `TC_BVA_14` | Combined load | Exact boundary (18) | `current=15, new=3` | `True` | **FAIL** | **DEF-01**: Sum 18 returns False |
| `TC_BVA_15` | Combined load | Just above (19) | `current=16, new=3` | `False` | PASS | Sum 19 rejected |
| `TC_BVA_16` | Dues near zero | Just below 0 (-1) | `dues=-1` | `ValueError` | PASS | Negative dues rejected |
| `TC_BVA_17` | Dues near zero | Exact zero (0) | `dues=0` | `"REGISTERED"` | PASS | 0 dues eligible |
| `TC_BVA_18` | Dues near zero | Just above 0 (1) | `dues=1` | `"DUES_BLOCK"` | **FAIL** | **DEF-02**: Rs. 1 not blocked |
| `TC_BVA_19` | Capacity | Just below min (0) | `cap=0, enr=0` | `ValueError` | PASS | Capacity 0 rejected |
| `TC_BVA_20` | Capacity | Min positive (1) | `cap=1, enr=0` | `"REGISTERED"` | PASS | Capacity 1 valid |
| `TC_BVA_21` | Enrollment | Min enrolled (0) | `cap=30, enr=0` | `"REGISTERED"` | PASS | Enrolled 0 valid |
| `TC_BVA_22` | Enrollment | Just below cap (29) | `cap=30, enr=29` | `"REGISTERED"` | PASS | 1 seat remaining |
| `TC_BVA_23` | Enrollment | Exact capacity (30) | `cap=30, enr=30` | `"WAITLISTED"` | **FAIL** | **DEF-04**: Full returns REGISTERED |
| `TC_BVA_24` | Enrollment | Just above cap (31) | `cap=30, enr=31` | `ValueError` | PASS | Over-capacity rejected |

---

### 2.3 Decision Table Testing — Task A3
The decision logic for `registration_decision()` involves multiple conditions with a strict hierarchical evaluation order established by **FR-09**:
$$\text{Dues} \succ \text{Already Registered} \succ \text{Prerequisites} \succ \text{Credit Limit} \succ \text{Availability}$$

#### Conditions:
- **C1:** Outstanding dues $> 0$ (T / F / Invalid $<0$)
- **C2:** Already registered in course (T / F)
- **C3:** Prerequisites satisfied (T / F)
- **C4:** Credit limit satisfied ($\text{current} + \text{course} \le 18$) (T / F)
- **C5:** Seat available ($\text{enrolled} < \text{capacity}$) (T [Available] / F [Full])

#### Decision Table Matrix:
| Rule | Test ID | C1 (Dues>0) | C2 (Already) | C3 (Prereq) | C4 (Credits) | C5 (Seats) | Expected Action / Decision | Actual (Initial Code) | Defect Note |
|---|---|---|---|---|---|---|---|---|---|
| **R01** | `TC_DT_01` | **T (100)** | — | — | — | — | `DUES_BLOCK` | **FAIL** | **DEF-02**: Dues 100 not blocked |
| **R02** | `TC_DT_02` | **F (0)** | **T** | — | — | — | `ALREADY_REGISTERED` | PASS | Already registered returned |
| **R03** | `TC_DT_03` | **F (0)** | **F** | **F** | — | — | `PREREQUISITES_MISSING` | PASS | Missing prereqs returned |
| **R04** | `TC_DT_04` | **F (0)** | **F** | **T** | **F (19)** | — | `CREDIT_LIMIT` | PASS | Exceeded credits returned |
| **R05** | `TC_DT_05` | **F (0)** | **F** | **T** | **T (15)** | **F (30/30)** | `WAITLISTED` | **FAIL** | **DEF-04**: Full returns REGISTERED |
| **R06** | `TC_DT_06` | **F (0)** | **F** | **T** | **T (15)** | **T (15/30)** | `REGISTERED` | PASS | Eligible registration |
| **R07** | `TC_DT_07` | **T (100)** | **T** | — | — | — | `DUES_BLOCK` | **FAIL** | **DEF-02**: Priority masking failed |
| **R08** | `TC_DT_08` | **T (200)** | **F** | **F** | — | — | `DUES_BLOCK` | **FAIL** | **DEF-02**: Priority masking failed |
| **R09** | `TC_DT_09` | **T (50)** | **F** | **T** | **F (19)** | — | `DUES_BLOCK` | **FAIL** | **DEF-02**: Priority masking failed |
| **R10** | `TC_DT_10` | **T (50)** | **F** | **T** | **T (15)** | **F (30/30)** | `DUES_BLOCK` | **FAIL** | **DEF-02**: Priority masking failed |
| **R11** | `TC_DT_11` | **F (0)** | **T** | **F** | — | — | `ALREADY_REGISTERED` | PASS | Reg prioritized over prereq |
| **R12** | `TC_DT_12` | **F (0)** | **T** | **T** | **F (20)** | — | `ALREADY_REGISTERED` | PASS | Reg prioritized over credits |
| **R13** | `TC_DT_13` | **F (0)** | **F** | **F** | **F (20)** | — | `PREREQUISITES_MISSING` | PASS | Prereq prioritized over credits |
| **R14** | `TC_DT_14` | **F (0)** | **F** | **F** | **T (15)** | **F (30/30)** | `PREREQUISITES_MISSING` | PASS | Prereq prioritized over availability |
| **R15** | `TC_DT_15` | **F (0)** | **F** | **T** | **F (19)** | **F (30/30)** | `CREDIT_LIMIT` | PASS | Credits prioritized over availability |
| **R16** | `TC_DT_16` | **Invalid (-5)** | — | — | — | — | `ValueError("Invalid dues")` | PASS | Dues validated first |
| **R17** | `TC_DT_17` | **F (0)** | — | — | — | **Invalid (Cap 0)** | `ValueError("Invalid capacity...")` | PASS | Capacity validated |
| **R18** | `TC_DT_18` | **F (0)** | — | — | — | **Invalid (25/20)** | `ValueError("Invalid capacity...")` | PASS | Over-enrollment validated |
| **R19** | `TC_DT_19` | **Invalid (-10)**| — | — | — | **Invalid (Cap 0)** | `ValueError("Invalid dues")` | PASS | Dues validated before capacity |

---

### 2.4 State Transition and Invariant Verification
Requirements FR-10 through FR-14 specify state transitions and side-effect guarantees:
1. `TC_STATE_01` (FR-10): `registration_decision` must be a pure evaluation without mutating student or course objects. (**Passed**)
2. `TC_STATE_02` (FR-11): Successful `register_course` adds course to `registered_courses`, increments student credits, and increments `course.enrolled`. (**Passed**)
3. `TC_STATE_03` (FR-12): Waitlisted student is appended to `course.waitlist` without mutating credits or enrolled count. (**Failed** due to DEF-04 returning `REGISTERED`).
4. `TC_STATE_04` (FR-12): Blocked registration (e.g., dues) leaves both objects completely unmutated. (**Failed** due to DEF-02).
5. `TC_STATE_05` (FR-13): Successful `withdraw_course` removes course, decrements credits, and decrements `course.enrolled`. (**Failed** due to DEF-05: `course.enrolled -= 1` missing).
6. `TC_STATE_06` (FR-14): Attempted withdrawal of non-enrolled course returns `False` without mutating either object. (**Passed**).

---

### 2.5 Test Suite Optimization & Traceability — Task A5

#### Duplication vs. Complementary Value:
A key principle of test suite optimization is distinguishing **redundant duplicates** from **complementary technique applications**:
- **ECP vs. BVA**: ECP tests partition interiors (e.g., `current=12, course=3` giving sum 15; `dues=500`), confirming general equivalence. BVA specifically tests boundary singularities ($17, 18, 19$; dues $0, 1$). These are **not duplicates** because boundary defects (such as `< 18` instead of `<= 18`) are completely invisible to ECP interior tests.
- **BVA vs. Decision Table**: Decision table rules test the interaction and priority masking of multiple simultaneous conditions. For example, Rule 10 tests dues $>0$ combined with a full course ($30/30$). While both conditions appear in BVA individually, their interaction verifies the precedence requirement (FR-09).
- **Consolidation**: Exact duplicate inputs (such as validating negative dues `dues = -1`) were consolidated into single shared assertions where appropriate, while preserving full traceability from requirements to test IDs.

The full traceability mapping is documented in sheet 4 of `docs/blackbox_test_design.xlsx`.

---

## 3. Part B: White-Box Testing (Prepared for Member 2)

> **Note for Member 2:**  
> This section is reserved for the white-box testing analysis to be conducted on feature branch `whitebox-testing`.  
> Starter test file: `tests/test_whitebox.py`.  
> CFG diagram asset: `docs/cfg.png`.

### 3.1 Control Flow Graph (CFG) & Cyclomatic Complexity
- Target Function: `registration_decision(student: Student, course: Course)`
- Graph Metrics:
  $$V(G) = E - N + 2 = P + 1$$
- Independent Basis Paths: (To be detailed by Member 2).

### 3.2 Coverage Gap Analysis (Initial Black-Box Baseline)
Black-box test suite achieved **89% statement and branch coverage**.
Uncovered locations in initial baseline:
- Line 51: `return "DUES_BLOCK"` (Uncovered because dues check was bugged at `> 1000`)
- Line 59: `return "WAITLISTED"` (Unreachable because `enrolled > capacity` contradicts line 48 validation)
- Lines 70–71: `course.waitlist.append(student.student_id)` (Unreached because `WAITLISTED` was never returned)

Member 2 will add tests in `tests/test_whitebox.py` to exercise all reachable code branches and achieve 100% post-fix coverage.

### 3.3 Condition Coverage and MC/DC Analysis
(To be completed by Member 2 for the compound decisions in `check_credit_limit` and `registration_decision`).

---

## 4. Part C: Defect Management & GitHub Collaboration

### 4.1 Git Branching & Commit Workflow
The repository follows a clean feature-branch Git workflow:
- `main`: Protected production-ready baseline.
- `blackbox-testing`: Feature branch for Part A test suite, Excel workbooks, and defect issues.
- `whitebox-testing`: Feature branch for Part B CFG, basis paths, and white-box test suite.
- `defect-fixes`: Dedicated bug-fix branch to resolve confirmed defects with regression testing.

### 4.2 Discovered Defects Summary

#### Defect 1: `check_credit_limit` Rejects 18 Credits (FR-01)
- **GitHub Issue:** #1 (`docs/defects/ISSUE-01_check_credit_limit_strict_inequality.md`)
- **Severity:** High
- **Root Cause:** `registration.py` line 34 used `< 18` instead of `<= 18`.
- **Failing Tests:** `TC_BVA_04`, `TC_BVA_14`.

#### Defect 2: Outstanding Dues Threshold Mismatch (FR-04)
- **GitHub Issue:** #2 (`docs/defects/ISSUE-02_outstanding_dues_threshold_mismatch.md`)
- **Severity:** Critical
- **Root Cause:** `registration.py` line 50 checked `student.outstanding_dues > 1000` instead of `> 0`.
- **Failing Tests:** `TC_ECP_08`, `TC_BVA_18`, `TC_DT_01`, `TC_DT_07`-`TC_DT_10`, `TC_STATE_04`.

#### Defect 3: Prerequisites Evaluated with Set Intersection (FR-03, FR-06)
- **GitHub Issue:** #3 (`docs/defects/ISSUE-03_prerequisites_intersection_instead_of_subset.md`)
- **Severity:** High
- **Root Cause:** `registration.py` line 41 returned `bool(completed.intersection(required))` which evaluates to `True` if any single prerequisite is satisfied.
- **Failing Tests:** `TC_ECP_12`.

#### Defect 4: Course Full Returns `REGISTERED` Instead of `WAITLISTED` (FR-08)
- **GitHub Issue:** #4 (`docs/defects/ISSUE-04_course_full_waitlist_condition_error.md`)
- **Severity:** High
- **Root Cause:** `registration.py` line 58 checked `course.enrolled > course.capacity`. Because line 48 prevents `enrolled > capacity`, full courses ($30/30$) fell through to `REGISTERED`.
- **Failing Tests:** `TC_ECP_16`, `TC_BVA_23`, `TC_DT_05`, `TC_STATE_03`.

#### Defect 5: `withdraw_course` Omits Enrollment Decrement (FR-13)
- **GitHub Issue:** #5 (`docs/defects/ISSUE-05_withdraw_course_missing_enrollment_decrement.md`)
- **Severity:** High
- **Root Cause:** `registration.py` line 80 decreased credits but never executed `course.enrolled -= 1`.
- **Failing Tests:** `TC_STATE_05`.

### 4.3 CI/CD GitHub Actions Pipeline
The automated workflow configured in `.github/workflows/tests.yml`:
1. Executes on every push and PR across feature branches.
2. Sets up Python 3.12 and installs dependencies.
3. Executes pytest with branch coverage reporting (`--cov-branch`).
4. Configured with `continue-on-error: true` on initial runs to preserve historical CI logs of legitimate pre-fix test failures.

---

## 5. Repository Structure Compliance

```text
SQE-Assignment-2/
├── registration.py
├── requirements.txt
├── README.md
├── REQUIREMENTS.md
├── .gitignore
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   └── defect_report.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── tests.yml
├── tests/
│   ├── __init__.py
│   ├── test_blackbox.py
│   └── test_whitebox.py
└── docs/
    ├── blackbox_test_design.xlsx
    ├── decision_table.xlsx
    ├── cfg.png
    ├── testing_report.md
    ├── PULL_REQUEST_BLACKBOX.md
    └── defects/
        ├── DEFECT_LOG.md
        ├── ISSUE-01_check_credit_limit_strict_inequality.md
        ├── ISSUE-02_outstanding_dues_threshold_mismatch.md
        ├── ISSUE-03_prerequisites_intersection_instead_of_subset.md
        ├── ISSUE-04_course_full_waitlist_condition_error.md
        └── ISSUE-05_withdraw_course_missing_enrollment_decrement.md
```

All required files and artifacts are fully in place according to Section 3 of the assignment specification.

---

## 6. Submission Checklist Verification

- [x] **Derive expected results strictly from SRS (`REQUIREMENTS.md`) without consulting code logic.**
- [x] **Design comprehensive ECP cases ($\ge 8$ required; 18 designed and executed).**
- [x] **Design comprehensive BVA cases ($\ge 10$ required; 24 designed and executed).**
- [x] **Design complete Decision Table with priority interaction rules (19 rules tested).**
- [x] **Implement executable pytest test suite in `tests/test_blackbox.py`.**
- [x] **Execute tests and preserve pass/fail evidence without altering assertions (51 passed, 16 failed).**
- [x] **Perform test suite optimization and traceability mapping (`docs/blackbox_test_design.xlsx`).**
- [x] **Create complete professional Excel design workbooks (`blackbox_test_design.xlsx`, `decision_table.xlsx`).**
- [x] **Set up Git repository, feature branching strategy, and descriptive commit history.**
- [x] **Log all 5 confirmed defects as GitHub Issues with reproduction steps and test IDs.**
- [x] **Configure automated GitHub Actions CI workflow with pytest and branch coverage.**
- [x] **Provide comprehensive Testing Report (`docs/testing_report.md`) with clear role separation.**
