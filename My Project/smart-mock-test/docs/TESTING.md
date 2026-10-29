# Testing Documentation & Quality Assurance Guide

## Smart Mock Test & Career Gateway Platform

This document details the automated testing framework, test suites, and verification procedures for the **Smart Mock Test & Career Gateway Platform**.

---

## 1. Automated Backend Test Suite (PyTest)

The backend is verified using `pytest`. The automated suite currently comprises **57 tests** with a **100% pass rate**.

### Running the Test Suite
To execute the full automated test suite from the repository root:

```bash
python -m pytest "My Project/smart-mock-test/tests"
```

To run with verbose per-test output:

```bash
python -m pytest "My Project/smart-mock-test/tests" -v
```

To run a specific test suite:

```bash
python -m pytest "My Project/smart-mock-test/tests/test_auth.py"
```

---

## 2. Test Suite Breakdown

| Test File | Tests | Focus Area |
| :--- | :---: | :--- |
| `test_auth.py` | 15 | Student registration, password hashing (`scrypt`), login authentication, token verification, single-admin email enforcement (`vartikachaudhary0312@gmail.com`), and role-based access control. |
| `test_career_gateway_subjects.py` | 9 | Subject categorization, catalog filtering, topic breakdowns, and Career Gateway test module mapping. |
| `test_proctoring_security.py` | 6 | Attempt session creation, proctoring security telemetry, violation threshold checks, and auto-submission triggers. |
| `test_resume.py` | 5 | Resume document parsing, skill extraction, ATS score evaluation, and feedback generation. |
| `test_email_otp.py` | 4 | 6-digit OTP code generation, expiration tolerance, and email verification workflow. |
| `test_upgrade_enhancements.py` | 4 | Security event logging, attempt persistence, and question rotation mechanisms. |
| `test_applications.py` | 3 | Job application submission, candidate status tracking, and candidate retrieval. |
| `test_students.py` | 3 | Student profile queries, profile updates, and statistics calculation. |
| `test_tests.py` | 3 | Test session initialization, question bank rotation, and answer submission. |
| `test_jobs.py` | 2 | Career Gateway job retrieval and search filters. |
| `test_results.py` | 2 | Post-examination score calculation, accuracy percentages, and result persistence. |
| `test_subjects.py` | 1 | Subject catalog query by ID and category. |
| **Total** | **57** | **100% Passing** |

---

## 3. Frontend JavaScript Syntax Verification

All client-side scripts are verified for syntax correctness using the Node.js compiler:

```bash
python -c "
import glob, subprocess
files = glob.glob('My Project/smart-mock-test/frontend/js/*.js')
for f in files:
    res = subprocess.run(['node', '-c', f], capture_output=True, text=True)
    assert res.returncode == 0, f'Error in {f}: {res.stderr}'
print('All 21 JavaScript files syntax-verified.')
"
```

### Verified Client Files (21 Modules)
- `admin.js`
- `api.js`
- `app.js`
- `applications.js`
- `auth.js`
- `career.js`
- `charts.js`
- `dashboard.js`
- `exam-security.js`
- `face-detector.js`
- `facefinder-data.js`
- `mock-data.js`
- `mock-test.js`
- `navigation.js`
- `pico.js`
- `profile.js`
- `result.js`
- `resume.js`
- `security-config.js`
- `settings.js`
- `validation.js`

---

## 4. Headless Browser Layout & Viewport Verification

The project includes headless Chrome browser automation scripts (`scripts/`) to verify UI layout, responsive fitting, and interactive navigation without requiring manual clicks:

- **`scripts/verify_full_mock_test_flow.py`**:
  Verifies the complete student examination journey in a real browser:
  1. *Stage 1:* Subject cards listing page isolation (ensures active assessment workspace is hidden).
  2. *Stage 2:* Card selection and navigation to Test Details (Step 2).
  3. *Stage 3:* "Back to Mock Tests" navigation returning cleanly to Step 1.
  4. *Stage 4:* Active test launching (Step 4), confirming question is at top, options are directly below, and Continue button is accessible in the viewport without page scrolling.
  5. *Stage 5:* Option selection updates, purple highlighting, and Continue state readiness.
  6. *Stage 6:* Advancing to Question 2 and confirming Previous button is enabled.
  7. *Stage 7:* Returning to Question 1 and verifying selected answer is preserved.
  8. *Stage 8:* Submit confirmation modal appearance.
  9. *Stage 9:* Mobile viewport (375x667) responsiveness and button accessibility.

### Running Layout Verification
With the backend server running on `http://127.0.0.1:5000`:

```bash
python "My Project/smart-mock-test/scripts/verify_full_mock_test_flow.py"
```

