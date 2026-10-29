# Database Schema Documentation

## Smart Mock Test & Career Gateway Platform

This document describes the data architecture and storage schemas used in the **Smart Mock Test & Career Gateway Platform**.

---

## 1. Data Storage Architecture

The application uses a lightweight, transactional JSON document store located in the `backend/data/` directory. Each domain entity is persisted as a JSON collection with dedicated repository classes providing atomic read and write operations.

```
backend/data/
├── users.json              # Student & Admin account credentials and profiles
├── categories.json         # High-level technical and aptitude subject categories
├── subjects.json           # Detailed subject modules and test catalogs
├── questions.json          # Multi-choice question (MCQ) bank
├── test_attempts.json      # Live and historical test attempt sessions
├── security_events.json    # Anti-cheating proctoring event logs
├── results.json            # Final scored test results and performance summaries
├── jobs.json               # Career Gateway job openings
├── applications.json       # Student job applications
└── tests.json              # Preset test module configurations
```

---

## 2. Entity Schemas

### A. Users (`backend/data/users.json`)
Stores student and administrator accounts, hashed credentials, and student academic profiles.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Unique identifier for the user account |
| `name` | String | Full name of the candidate or administrator |
| `email` | String | Unique email address used for authentication |
| `password_hash` | String | Cryptographically salted and hashed password (`scrypt` / `pbkdf2:sha256`) |
| `role` | String | User authorization level (`student` or `admin`) |
| `mobile` | String | Contact phone number |
| `location` | String | Residential city / region |
| `education` | String | College name, degree program, and academic standing |
| `skills` | Array[String] | Technical competencies and programming languages |
| `status` | String | Account state (`Active`, `Inactive`, `Pending`) |
| `created_at` | String | Timestamp of registration (`YYYY-MM-DD HH:MM:SS`) |
| `resume_analysis` | Object | Cached ATS resume evaluation scores and recommendations |

---

### B. Categories (`backend/data/categories.json`)
Classifies technical subjects and interview tracks into functional categories.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | String | Unique category slug (e.g. `cat_programming`, `cat_core_cs`, `cat_quant`) |
| `name` | String | Human-readable category title |
| `description` | String | Overview of the topics and domains covered |
| `icon` | String | Bootstrap icon class name (e.g. `bi-code-square`, `bi-cpu`) |
| `subject_count` | Integer | Total number of subjects mapped to this category |

---

### C. Subjects (`backend/data/subjects.json`)
Defines the technical syllabus modules and test tracks available for mock assessments.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | String | Unique subject identifier (e.g. `sub_dsa`, `sub_python`, `sub_dbms`) |
| `category_id` | String | Foreign key mapping to `categories.json` |
| `category` | String | Denormalized category title |
| `name` | String | Subject title (e.g. `Data Structures & Algorithms`) |
| `code` | String | Short alphanumeric subject code (e.g. `CS-DSA`, `INT-PY`) |
| `icon` | String | Bootstrap icon identifier |
| `description` | String | Detailed topic summary |
| `topics` | Array[String] | Key subtopics evaluated in this module |
| `defaultDuration` | Integer | Standard baseline duration in minutes |
| `difficulty` | String | Difficulty rating (`Easy`, `Medium`, `Hard`, `Mixed`) |
| `question_count` | Integer | Total questions available in the question bank for this subject |

---

### D. Questions (`backend/data/questions.json`)
The complete question bank comprising multiple-choice questions across all CSE and aptitude subjects.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | String | Unique question identifier (e.g. `q_dsa_001`, `q_py_015`) |
| `subject_id` | String | Foreign key mapping to `subjects.json` |
| `subject` | String | Denormalized subject title |
| `category_id` | String | Denormalized category identifier |
| `difficulty` | String | Question complexity level (`easy`, `medium`, `hard`) |
| `question_text` | String | The full question stem |
| `options` | Array[String] | Array of 4 answer option strings `[Option A, Option B, Option C, Option D]` |
| `correct_option` | String | Letter of the correct choice (`A`, `B`, `C`, or `D`) |
| `correctIndex` | Integer | Zero-based index of the correct answer (`0` for A, `1` for B, etc.) |
| `explanation` | String | Comprehensive technical rationale and solution breakdown |

---

### E. Test Attempts (`backend/data/test_attempts.json`)
Tracks live, in-progress, and concluded proctored test sessions.

| Field | Type | Description |
| :--- | :--- | :--- |
| `attempt_id` | String | Unique session identifier (e.g. `att_1793298893_sub_dsa_1`) |
| `test_id` | String | Subject or test ID attempted |
| `user_id` | Integer | Foreign key mapping to candidate in `users.json` |
| `started_at` | String | Session start timestamp |
| `status` | String | Session status (`in_progress`, `completed`, `auto_submitted`) |
| `question_ids` | Array[String] | Selected rotated question IDs for this session |
| `violations_count` | Integer | Total proctoring violations recorded during the session |

---

### F. Security Events (`backend/data/security_events.json`)
Logs telemetry and anti-cheating alerts captured by the client-side proctoring engine.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Auto-incrementing log ID |
| `attempt_id` | String | Foreign key mapping to `test_attempts.json` |
| `user_id` | Integer | Foreign key mapping to `users.json` |
| `test_id` | String / Integer | Subject or test ID |
| `event_type` | String | Violation type (`fullscreen_exit`, `tab_switch`, `face_missing`, `multiple_faces`, `clipboard_attempt`, `camera_disconnect`) |
| `severity` | String | Severity rating (`warning`, `critical`, `termination`) |
| `timestamp` | String | ISO 8601 timestamp of occurrence |
| `details` | Object | Event description and violation count details |

---

### G. Results (`backend/data/results.json`)
Records post-examination evaluations, scores, and performance summaries.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Unique result ID |
| `user_id` | Integer | Foreign key mapping to `users.json` |
| `test_id` | String / Integer | Subject ID |
| `attempt_id` | String | Reference to `test_attempts.json` |
| `submission_reason` | String | Submission trigger (`manual`, `time_expired`, `security_auto_submit`) |
| `violations_count` | Integer | Total violations accumulated |
| `subject` | String | Subject title |
| `difficulty` | String | Assessment difficulty attempted |
| `total_questions` | Integer | Total number of questions presented |
| `correct_answers` | Integer | Number of correctly answered questions |
| `wrong_answers` | Integer | Number of incorrectly answered questions |
| `skipped_answers` | Integer | Number of unattempted questions |
| `score` | Integer | Earned marks |
| `percentage` | Float | Calculated percentage score |
| `accuracy` | Float | Ratio of correct answers to total attempted questions |
| `time_taken` | Integer | Total seconds spent |
| `created_at` | String | Completion timestamp |

---

### H. Jobs (`backend/data/jobs.json`)
Stores Career Gateway job listings, hiring company info, and requirements.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Unique job listing ID |
| `company` | String | Hiring company name (e.g. `TechCorp Solutions`, `CloudScale`) |
| `title` | String | Job position title |
| `location` | String | Work location (city or Remote) |
| `job_type` | String | Employment nature (`Full-Time`, `Internship`, `Contract`) |
| `experience` | String | Required experience level |
| `salary` | String | Offered CTC range |
| `skills` | Array[String] | Required technical skill keywords |
| `description` | String | Overview of responsibilities |
| `status` | String | Listing state (`Active`, `Closed`) |
| `created_at` | String | Date posted |

---

### I. Applications (`backend/data/applications.json`)
Tracks student applications submitted to Career Gateway job openings.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | Integer | Unique application record ID |
| `user_id` | Integer | Candidate user ID |
| `job_id` | Integer | Foreign key mapping to `jobs.json` |
| `status` | String | Workflow status (`Applied`, `Under Review`, `Shortlisted`, `Rejected`) |
| `applied_at` | String | Timestamp of submission |
| `resume_file` | String | Name of the attached resume file |
| `cover_letter` | String | Optional candidate statement |

