# REST API Documentation

## Smart Mock Test & Career Gateway Platform

This document describes the REST API endpoints implemented in the backend application.

---

## 1. Overview & Conventions

- **Base URL:** `http://127.0.0.1:5000` (or `http://localhost:5000`)
- **Format:** All requests and responses use JSON (`Content-Type: application/json`), except multipart file uploads (`multipart/form-data`).
- **Authentication:** Protected endpoints require a Bearer token in the request header:
  ```http
  Authorization: Bearer <jwt_or_session_token>
  ```
- **Response Structure:**
  - Success responses return `{ "success": true, "data": ..., "message": "..." }`
  - Error responses return `{ "success": false, "error": "...", "message": "..." }`

---

## 2. System & Health

### `GET /api/health`
Verifies backend server health and reports service metadata.
- **Access:** Public
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "data": {
      "service": "backend",
      "status": "healthy",
      "version": "1.0.0",
      "admin_email": "vartikachaudhary0312@gmail.com"
    },
    "message": "Smart Mock Test API is running"
  }
  ```

---

## 3. Authentication (`/api/auth`)

### `POST /api/auth/register`
Creates a new student account.
- **Access:** Public
- **Request Body:**
  ```json
  {
    "name": "Jane Doe",
    "email": "jane@example.com",
    "password": "Password123!",
    "mobile": "+91 9876543210",
    "education": "B.Tech Computer Science"
  }
  ```
- **Response (201 Created):**
  ```json
  {
    "success": true,
    "data": {
      "user": { "id": 2, "name": "Jane Doe", "email": "jane@example.com", "role": "student" },
      "token": "token_string_here"
    },
    "message": "Registration successful"
  }
  ```

### `POST /api/auth/login`
Authenticates a student or administrator. Enforces that only the designated admin email (`vartikachaudhary0312@gmail.com`) can authenticate into the admin portal.
- **Access:** Public
- **Request Body:**
  ```json
  {
    "email": "student@example.com",
    "password": "Password123!"
  }
  ```
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "data": {
      "user": { "id": 1, "name": "Rahul Sharma", "email": "student@example.com", "role": "student" },
      "token": "token_string_here"
    },
    "message": "Login successful"
  }
  ```

### `POST /api/auth/send-otp`
Generates a 6-digit email OTP for two-factor verification or password recovery.
- **Request Body:** `{ "email": "student@example.com" }`

### `POST /api/auth/verify-otp`
Validates the submitted 6-digit OTP code.
- **Request Body:** `{ "email": "student@example.com", "otp": "123456" }`

### `GET /api/auth/me`
Retrieves the currently authenticated user's profile and active session state.
- **Headers:** `Authorization: Bearer <token>`

### `POST /api/auth/logout`
Terminates the user session and invalidates the authentication token.
- **Headers:** `Authorization: Bearer <token>`

---

## 4. Subjects & Categories (`/api/subjects`)

### `GET /api/subjects`
Retrieves all technical subjects, topic breakdowns, and available question counts.
- **Access:** Public
- **Query Parameters:** `?category=cat_core_cs` (optional filter)
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "data": [
      {
        "id": "sub_dsa",
        "name": "Data Structures & Algorithms",
        "category": "Core Computer Science",
        "code": "CS-DSA",
        "icon": "bi-diagram-3",
        "question_count": 50
      }
    ]
  }
  ```

### `GET /api/subjects/categories`
Retrieves all subject categories and their mapped subject counts.

### `GET /api/subjects/<id>`
Retrieves a single subject module by ID or slug.

---

## 5. Mock Tests & Proctoring (`/api/tests`)

### `GET /api/tests/<id>/questions`
Retrieves the question set for a given subject.
- **Query Parameters:** `?difficulty=Medium&length=10`

### `POST /api/tests/<id>/start`
Initializes a proctored examination attempt session.
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:** `{ "difficulty": "Medium", "length": 10 }`
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "data": {
      "attempt_id": "att_1793298893_sub_dsa_1",
      "test_id": "sub_dsa",
      "questions": [...],
      "duration_minutes": 15
    }
  }
  ```

### `POST /api/tests/<id>/security-event`
Logs an anti-cheating security violation (tab switch, fullscreen exit, missing face, etc.) during an active proctored attempt.
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "attempt_id": "att_1793298893_sub_dsa_1",
    "event_type": "tab_switch",
    "timestamp": "2026-10-30T00:04:00Z",
    "details": { "reason": "Page visibility changed to hidden", "violation_count": 1 }
  }
  ```

### `POST /api/tests/<id>/submit`
Submits student answers, calculates final scores, logs time spent, and stores performance analytics.
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "attempt_id": "att_1793298893_sub_dsa_1",
    "submission_reason": "Candidate Manual Submission",
    "violations_count": 0,
    "answers": [
      { "question_id": "q_dsa_001", "selected_option": "C" }
    ],
    "time_taken": 420
  }
  ```

---

## 6. Results & Analytics (`/api/results`)

### `GET /api/results/user/<userId>`
Retrieves past test attempts, scores, and accuracy metrics for a specific student.
- **Headers:** `Authorization: Bearer <token>`

### `GET /api/results/<id>`
Retrieves comprehensive details for a specific completed test result, including question-by-question explanations.

---

## 7. Resume Analysis (`/api/resume`)

### `POST /api/resume/upload`
Uploads a candidate's resume (PDF or DOCX) for server-side evaluation.
- **Content-Type:** `multipart/form-data`
- **Form Data:** `resume` (file)
- **Response (200 OK):**
  ```json
  {
    "success": true,
    "data": {
      "file_name": "resume.pdf",
      "skills_detected": ["Python", "Flask", "SQL", "Java"],
      "match_score": 85,
      "feedback": ["Add specific quantifiable achievements to projects"]
    }
  }
  ```

### `POST /api/resume/analyze`
Submits resume text or pre-extracted parameters for instant ATS matching against target job profiles.

---

## 8. Career Gateway & Applications (`/api/jobs`, `/api/applications`)

### `GET /api/jobs`
Retrieves available job vacancies with skill requirements and location filters.

### `GET /api/jobs/<id>`
Retrieves full position description and requirements for a specific job listing.

### `POST /api/applications`
Submits a student application for a specific job vacancy.
- **Headers:** `Authorization: Bearer <token>`
- **Request Body:**
  ```json
  {
    "job_id": 1,
    "cover_letter": "I am interested in this position...",
    "resume_file": "my_resume.pdf"
  }
  ```

### `GET /api/applications/user/<userId>`
Retrieves all applications submitted by the given candidate.

---

## 9. Admin Management (`/api/admin`)

*Note: All endpoints under `/api/admin/*` require administrator privileges.*

- **`GET /api/admin/overview`**: Summary counts of students, test attempts, questions, and applications.
- **`GET /api/admin/students`**: List of registered student accounts.
- **`GET /api/admin/questions`**: Full question bank management.
- **`POST /api/admin/questions`**: Create a new question.
- **`PUT /api/admin/questions/<id>`**: Update an existing question.
- **`DELETE /api/admin/questions/<id>`**: Remove a question.
- **`GET /api/admin/security-events`**: Audit log of all security violations across all test attempts.

