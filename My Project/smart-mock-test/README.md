# SMART MOCK TEST AND CAREER GATEWAY
### MCA Final Year College Project — Stage 1 (Frontend) & Stage 2 (Backend)

## 📌 Project Overview
**Smart Mock Test & Career Gateway** is a modern, full-featured web platform built for MCA college project demonstration, viva presentation, and real student assessment.

- **Stage 1 (Frontend):** 100% complete responsive frontend built using HTML5, CSS3, Vanilla JavaScript, Bootstrap 5, Bootstrap Icons, and Chart.js.
- **Stage 2 (Backend):** Professional Python Flask REST API backend with modular repository pattern, clean JSON storage, password hashing, role-based authorization, and PyTest test suite.

---

## 🛠️ Technology Stack (Stage 2 Backend)
- **Language:** Python 3.x
- **Framework:** Flask 3.x
- **CORS Management:** Flask-CORS
- **Security & Password Hashing:** Werkzeug `generate_password_hash` / `check_password_hash` & `itsdangerous` URLSafeTimedSerializer
- **Environment Management:** `python-dotenv` & `config.py`
- **Testing:** PyTest (20/20 passing tests)
- **Data Layer (Stage 2):** Repository pattern (`backend/repositories/`) backed by JSON storage files (`backend/data/*.json`) — ready for zero-breaking-change MySQL migration in Stage 3.

---

## 🔑 Demo Login Credentials

### 👨‍🎓 Student Portal:
- **Email:** `student@example.com`
- **Password:** `Student@123`
- **Role:** `student`

### 🛡️ Admin Portal:
- **Email:** `admin@example.com`
- **Password:** `Admin@123`
- **Role:** `admin`
- **Admin Security Key:** `ADMIN2026`

---

## 📁 Complete Project Structure
```
smart-mock-test/
│
├── frontend/                          # Stage 1 Responsive UI (Intact & Untouched)
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── student-dashboard.html
│   ├── mock-test.html
│   ├── result.html
│   ├── resume.html
│   ├── career.html
│   ├── applications.html
│   ├── profile.html
│   ├── settings.html
│   ├── admin/
│   ├── css/
│   └── js/
│
├── backend/                           # Stage 2 Flask REST API Backend
│   ├── app.py                         # Application Factory & Blueprint registrations
│   ├── config.py                      # Development, Testing & Production configurations
│   ├── extensions.py                  # Flask-CORS extension instance
│   ├── requirements.txt               # Backend dependencies
│   ├── .env.example                   # Environment variable template
│   │
│   ├── routes/                        # REST API Endpoint Controllers
│   │   ├── auth_routes.py             # POST /api/auth/register, /login, /logout, GET /me
│   │   ├── student_routes.py          # GET, PUT /api/student/profile
│   │   ├── subject_routes.py          # GET /api/subjects
│   │   ├── test_routes.py             # GET, POST /api/tests, /start, /submit
│   │   ├── result_routes.py           # GET /api/results, /<id>, /analysis
│   │   ├── resume_routes.py           # POST /api/resume/upload
│   │   ├── job_routes.py              # GET /api/jobs, /<id>, POST /apply
│   │   ├── application_routes.py      # GET /api/applications
│   │   ├── notification_routes.py     # GET /api/notifications
│   │   └── admin_routes.py            # Dashboard, Students, Questions, Jobs & Apps Admin CRUD
│   │
│   ├── services/                      # Business Logic Layer
│   │   ├── auth_service.py
│   │   ├── student_service.py
│   │   ├── test_service.py
│   │   ├── result_service.py
│   │   ├── resume_service.py
│   │   ├── job_service.py
│   │   ├── application_service.py
│   │   └── admin_service.py
│   │
│   ├── repositories/                  # Data Abstraction Layer (JSON / MySQL ready)
│   │   ├── user_repository.py
│   │   ├── question_repository.py
│   │   ├── test_repository.py
│   │   ├── result_repository.py
│   │   ├── job_repository.py
│   │   └── application_repository.py
│   │
│   ├── data/                          # Development JSON Storage
│   │   ├── users.json
│   │   ├── subjects.json
│   │   ├── questions.json
│   │   ├── tests.json
│   │   ├── results.json
│   │   ├── jobs.json
│   │   └── applications.json
│   │
│   ├── utils/                         # Helper Utilities
│   │   ├── validators.py              # Email, phone, password, question & payload validators
│   │   ├── security.py                # Werkzeug password hashing & token signer
│   │   ├── responses.py               # Standardized success & error JSON formats
│   │   └── decorators.py              # @token_required & @role_required RBAC decorators
│   │
│   └── uploads/                       # Temporary resume upload directory
│
├── tests/                             # PyTest Automated Test Suite
│   ├── test_auth.py
│   ├── test_students.py
│   ├── test_subjects.py
│   ├── test_tests.py
│   ├── test_results.py
│   ├── test_jobs.py
│   └── test_applications.py
│
├── README.md                          # Documentation
└── .gitignore
```

---

## ⚡ Running the Backend Server

### 1. Virtual Environment Setup
```bash
# Run from the parent My Project directory in Windows PowerShell
Set-Location "C:\Users\HP\Desktop\Capstone\My Project"
.\.venv\Scripts\Activate.ps1
```

### 2. Install Dependencies
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Start Flask Development Server
```bash
python app.py
```
*Server will start at `http://127.0.0.1:5000`.* The API uses the JSON files in `smart-mock-test/backend/data`; no database initialization or migrations are needed. Upload storage is created under `backend/uploads` when needed. Copy `smart-mock-test\backend\.env.example` to `smart-mock-test\backend\.env` and configure the SMTP values to enable email OTP delivery. For Gmail, use a Google App Password, not your account password. The backend loads that file automatically. Use a unique `SECRET_KEY` outside development.

### 4. Health Check Endpoint
```bash
curl http://127.0.0.1:5000/api/health
```
**Response:**
```json
{
  "success": true,
  "message": "Smart Mock Test API is running",
  "data": {
    "service": "backend",
    "status": "healthy"
  }
}
```

---

## 🧪 Running PyTest Test Suite
```bash
$env:PYTHONPATH = (Join-Path (Get-Location) "smart-mock-test")
python -m pytest .\smart-mock-test\tests -q
```
Run from `My Project` with its `.venv` activated. The current suite contains 26 tests.

## Running the Frontend

In a second PowerShell terminal, from `My Project`, serve the existing static UI:
```powershell
Set-Location "C:\Users\HP\Desktop\Capstone\My Project"
python -m http.server 5501 --directory .\smart-mock-test\frontend
```
Open `http://127.0.0.1:5501`. The frontend uses browser `localStorage` for registration and test data; the test email OTP uses the Flask email API at `http://127.0.0.1:5000`.

---

## 📡 API Endpoint Summary

| Category | Method | Endpoint | Auth | Description |
| :--- | :--- | :--- | :--- | :--- |
| **System** | `GET` | `/api/health` | None | System health check |
| **Auth** | `POST` | `/api/auth/register` | None | Register new student or admin |
| | `POST` | `/api/auth/login` | None | Authenticate user & return Bearer token |
| | `POST` | `/api/auth/test-otp/send` | None | Send a short-lived test verification code to the supplied registration email |
| | `POST` | `/api/auth/test-otp/verify` | None | Verify a one-time code before launching a test |
| | `POST` | `/api/auth/logout` | Token | Logout session |
| | `GET` | `/api/auth/me` | Token | Fetch current authenticated user profile |
| **Student** | `GET` | `/api/student/profile` | Token | Get student profile details |
| | `PUT` | `/api/student/profile` | Token | Update student profile details |
| **Subjects** | `GET` | `/api/subjects` | None | Get subject list & question counts |
| **Tests** | `GET` | `/api/tests` | None | Get available test configurations |
| | `GET` | `/api/tests/<id>` | None | Get test metadata |
| | `POST` | `/api/tests/<id>/start` | Token | Start test (Returns questions **without** correct answers) |
| | `POST` | `/api/tests/<id>/submit` | Token | Submit test (Calculates score & accuracy server-side) |
| **Results** | `GET` | `/api/results` | Token | Get user test result history |
| | `GET` | `/api/results/<id>` | Token | Get single result detail |
| | `GET` | `/api/results/<id>/analysis` | Token | Generate strong/weak areas & recommendations |
| **Resume** | `POST` | `/api/resume/upload` | Token | Upload PDF/DOCX resume & get ATS analysis |
| **Jobs** | `GET` | `/api/jobs` | None | List jobs with search & filters |
| | `GET` | `/api/jobs/<id>` | None | Get job detail |
| | `POST` | `/api/jobs/<id>/apply` | Student | Submit application (Returns 409 if duplicate) |
| **Applications**| `GET` | `/api/applications` | Token | List candidate applications |
| **Admin** | `GET` | `/api/admin/dashboard` | Admin | Aggregate dashboard metrics & Chart.js datasets |
| | `GET` | `/api/admin/students` | Admin | Get student directory |
| | `PUT` | `/api/admin/students/<id>/status` | Admin | Block or activate student account |
| | `GET` | `/api/admin/questions` | Admin | Get master question bank |
| | `POST` | `/api/admin/questions` | Admin | Create question (4 options + explanation) |
| | `PUT` | `/api/admin/questions/<id>` | Admin | Update question |
| | `DELETE`| `/api/admin/questions/<id>` | Admin | Delete question |
| | `GET` | `/api/admin/jobs` | Admin | Manage job postings |
| | `POST` | `/api/admin/jobs` |  | Create new job post |
| | `PUT` | `/api/admin/applications/<id>/status` | Admin | Update candidate application status |

---

## 🔮 Stage 3 & Stage 4 Roadmap

### **STAGE 3 — DATABASE (MySQL)**
In Stage 3, MySQL tables & connection pooling will be introduced. The Repository classes inside `backend/repositories/` will be updated to execute MySQL queries instead of loading JSON files. **No route or service signatures will change.**

### **STAGE 4 — FULL INTEGRATION**
In Stage 4, the frontend `frontend/js/api.js` will replace local storage operations with standard `fetch('http://127.0.0.1:5000/api/...')` REST calls to seamlessly connect the frontend, backend, and MySQL database.
