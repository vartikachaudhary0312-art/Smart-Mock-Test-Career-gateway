# Project Directory Structure

## Smart Mock Test & Career Gateway Platform

This document describes the directory organization and architectural layout of the **Smart Mock Test & Career Gateway Platform**.

---

## 1. Top-Level Repository Overview

```
Smart-Mock-Test-Career-gateway/
├── .gitignore                      # Git root ignore definitions
├── package-lock.json               # Root lockfile
├── README.md                       # Root repository description
└── My Project/
    └── smart-mock-test/            # Main project root
        ├── run.py                  # Primary application entry point (Flask & Web Server)
        ├── README.md               # Comprehensive project documentation
        ├── PROJECT_STRUCTURE.md    # This file - architectural layout
        ├── docs/                   # Technical documentation directory
        ├── backend/                # Python / Flask backend application
        ├── frontend/               # Vanilla JS, HTML5, CSS3 responsive frontend
        ├── tests/                  # Automated PyTest test suite (57 test cases)
        └── scripts/                # Verification, layout audit, and data utilities
```

---

## 2. Main Application Directory (`My Project/smart-mock-test/`)

### A. Root Files
- **`run.py`**: Launches the Flask development server on port 5000 (`http://127.0.0.1:5000`), automatically serving both backend REST API endpoints (`/api/*`) and frontend static HTML pages (`/`).
- **`README.md`**: Project overview, feature breakdown, installation instructions, environment setup, and test execution guide.
- **`PROJECT_STRUCTURE.md`**: Complete architectural layout and component reference.
- **`.gitignore`**: Excludes `__pycache__`, virtual environments, `.env`, uploads, and temporary diagnostic files from version control.

---

### B. Backend Architecture (`backend/`)

The backend is built with Python 3 and Flask, utilizing a modular Application Factory pattern and repository-based data access.

```
backend/
├── app.py                          # Flask application factory (create_app) & blueprint registry
├── config.py                       # Configuration classes (Development, Testing, Production)
├── extensions.py                   # Flask-CORS and third-party extension instances
├── requirements.txt                # Python package dependencies
├── .env.example                    # Template environment variables (no secrets)
│
├── data/                           # JSON-based persistent data stores
│   ├── users.json                  # Student & Admin credentials and profile records
│   ├── categories.json             # Subject category classifications
│   ├── subjects.json               # Complete CSE and aptitude subject catalog
│   ├── questions.json              # Full multi-subject MCQ question bank
│   ├── results.json                # Evaluated test session results and answer breakdowns
│   ├── test_attempts.json          # Proctored test attempt sessions
│   ├── security_events.json        # Logged anti-cheating violations and proctoring telemetry
│   ├── jobs.json                   # Career Gateway job openings and listings
│   ├── applications.json           # Student job applications and status tracking
│   └── tests.json                  # Preset test definitions
│
├── repositories/                   # Data Access Layer (JSON file reading & writing)
│   ├── user_repository.py          # User retrieval, password hashing, and provisioning
│   ├── question_repository.py      # Question filtering by subject, difficulty, and ID
│   ├── test_repository.py          # Subject catalog queries and test definitions
│   ├── attempt_repository.py       # Session lifecycle tracking and attempt validation
│   ├── result_repository.py        # Score calculation and result persistence
│   ├── security_event_repository.py# Anti-cheating violation logging
│   ├── job_repository.py           # Career job search, retrieval, and filtering
│   └── application_repository.py   # Job application management
│
├── routes/                         # API Controllers (Flask Blueprints)
│   ├── auth_routes.py              # Login, registration, OTP email verification, /api/auth/me
│   ├── student_routes.py           # Student profile queries and profile updates
│   ├── subject_routes.py           # Subject and category catalog retrieval
│   ├── test_routes.py              # Test initialization, question delivery, and final submission
│   ├── result_routes.py            # Result analytics and past attempt retrieval
│   ├── resume_routes.py            # Resume upload, parsing, and ATS score analysis
│   ├── job_routes.py               # Career Gateway job listings and search
│   ├── application_routes.py       # Job application submission and status tracking
│   ├── notification_routes.py      # User notifications and system alerts
│   └── admin_routes.py             # Administrative statistics, user management, and catalog controls
│
├── services/                       # Business Logic Layer
│   ├── auth_service.py             # Authentication logic, password verification, token issuance
│   ├── email_otp_service.py        # 6-digit OTP generation and email delivery emulation
│   ├── student_service.py          # Student statistics and performance aggregations
│   ├── test_service.py             # Question rotation, score evaluation, and attempt handling
│   ├── result_service.py           # Result calculation, grade scoring, and analytics
│   ├── resume_service.py           # Resume skill matching and ATS evaluation engine
│   ├── job_service.py              # Job query filtering and application logic
│   ├── application_service.py      # Application workflow management
│   └── admin_service.py            # Admin dashboard analytics aggregations
│
├── utils/                          # Common Utilities & Helpers
│   ├── decorators.py               # Authentication and role-based access decorators (@token_required, @admin_required)
│   ├── responses.py                # Standardized JSON response formatters (success_response, error_response)
│   ├── security.py                 # Password hashing (werkzeug.security) and token verification
│   └── validators.py               # Input validation helpers for registration and test inputs
│
└── uploads/                        # Server storage for uploaded student resume files
```

---

### C. Frontend Architecture (`frontend/`)

The frontend is implemented using HTML5, CSS3, JavaScript (ES6+), and Bootstrap 5.3, supporting both light and dark themes.

```
frontend/
├── index.html                      # Landing page with platform overview and quick links
├── login.html                      # Authentication portal (Student & Admin login)
├── register.html                   # Student self-registration portal
├── student-dashboard.html          # Student dashboard (statistics, test history, recent tests)
├── mock-test.html                  # 4-step interactive mock test engine & assessment workspace
├── result.html                     # Post-test performance analytics, score cards, and detailed review
├── resume.html                     # AI-driven ATS resume analysis and skill recommendations
├── career.html                     # Career Gateway job listings, filtering, and application modals
├── applications.html               # Student job application tracker and status updates
├── profile.html                    # Student profile view and personal information editor
├── settings.html                   # Account preferences, theme switching, and password controls
│
├── css/                            # Styling & Layout Sheets
│   ├── variables.css               # Design tokens, CSS custom properties, purple theme variables
│   ├── global.css                  # Typography, base reset, theme toggle overrides, card utilities
│   ├── components.css              # Navigation sidebar, top header, buttons, badges, modals
│   ├── test.css                    # Mock test step views, option cards, timer, action toolbar
│   ├── dashboard.css               # Stat cards, performance widgets, recent activity tables
│   ├── career.css                  # Job cards, category pills, search bar, application cards
│   ├── auth.css                    # Login & registration container, input floating labels
│   ├── result.css                  # Score meters, summary badges, question-by-question review cards
│   └── responsive.css              # Breakpoint adjustments across mobile, tablet, and desktop
│
├── js/                             # Client-Side Modules & Engines
│   ├── api.js                      # Centralized API client with dual-host failover and token injection
│   ├── app.js                      # Core app initialization, theme manager, session validation
│   ├── navigation.js               # Responsive collapsible sidebar drawer navigation controller
│   ├── mock-test.js                # Mock test flow manager (Step 1 -> Step 2 -> Step 3 -> Step 4)
│   ├── exam-security.js            # Anti-cheating proctoring engine (fullscreen, clipboard, tabs)
│   ├── face-detector.js            # Client-side face detection engine using Pico.js
│   ├── pico.js                     # Lightweight local face detection cascade runtime
│   ├── facefinder-data.js          # Base64-encoded cascade binary for local face detection
│   ├── facefinder.bin              # Binary cascade fallback data
│   ├── security-config.js          # Centralized proctoring thresholds and violation limits
│   ├── dashboard.js                # Dashboard telemetry, chart rendering, and statistics
│   ├── career.js                   # Career Gateway job filtering and application logic
│   ├── resume.js                   # Resume file upload, ATS score gauge, and feedback rendering
│   ├── result.js                   # Result page analytics and question review rendering
│   ├── profile.js                  # User profile data loading and profile updating
│   ├── auth.js                     # Login and registration form validation and submission
│   ├── validation.js               # Client-side form input validation helpers
│   ├── charts.js                   # Chart.js helper wrappers for score analytics
│   ├── settings.js                 # Theme toggling and account preferences handlers
│   ├── admin.js                    # Admin portal dashboard and management scripts
│   └── mock-data.js                # Client-side offline fallback data fixtures
│
└── admin/                          # Dedicated Admin Portal Views
    ├── dashboard.html              # Admin statistics overview, user metrics, test metrics
    ├── students.html               # Student user account directory
    ├── subjects.html               # Subject module catalog manager
    ├── questions.html              # Question bank editor and importer
    ├── tests.html                  # Preset test definitions manager
    ├── results.html                # Platform-wide test attempt records
    ├── jobs.html                   # Job listing management portal
    ├── applications.html           # Job applications review portal
    └── reports.html                # Academic performance reports
```

---

### D. Automated Test Suite (`tests/`)

The test suite covers backend routes, security policies, and authentication mechanisms using `pytest`.

```
tests/
├── __init__.py
├── test_auth.py                    # 15 tests: Registration, login, admin security, token validation
├── test_career_gateway_subjects.py # 9 tests: Subject catalog queries and category classifications
├── test_proctoring_security.py     # 6 tests: Proctoring event logging, attempts, security violations
├── test_resume.py                  # 5 tests: Resume file uploads, ATS scoring, skill extraction
├── test_email_otp.py               # 4 tests: 6-digit OTP generation, delivery, and verification
├── test_upgrade_enhancements.py    # 4 tests: Security event logging, attempt tracking, validation
├── test_applications.py            # 3 tests: Job application workflow and status updates
├── test_students.py                # 3 tests: Student profile retrieval and updates
├── test_tests.py                   # 3 tests: Test session initialization, start, and question delivery
├── test_jobs.py                    # 2 tests: Career job listing retrieval and filtering
├── test_results.py                 # 2 tests: Test result calculation and score records
└── test_subjects.py                # 1 test: Subject module retrieval
```

---

### E. Verification & Utility Scripts (`scripts/`)

Verification scripts used during development for headless browser layout testing and verification:
- `verify_full_mock_test_flow.py`: Full headless Chrome end-to-end verification of mock test navigation, card selection, and layout.
- `test_live_mock_test_layout.py`: Viewport and action bar positioning validation across laptop viewports.
- `test_mobile_mock_test_layout.py`: Mobile (375x667, 414x896) viewport responsiveness verification.
- `verify_admin_auth.py`: Admin single-email authentication verification script.
- `dark_mode_audit.py`: Dark mode contrast and theme consistency audit script.

