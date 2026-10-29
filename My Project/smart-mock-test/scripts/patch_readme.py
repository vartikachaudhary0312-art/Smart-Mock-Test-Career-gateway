with open('My Project/smart-mock-test/README.md', 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

old_cred_section = """## 🔑 Demo Login Credentials

### 👨‍🎓 Student Portal:
- **Email:** `student@example.com`
- **Password:** `Student@123`
- **Role:** `student`

### 🛡️ Admin Portal:
- **Email:** `admin@example.com`
- **Password:** `Admin@123`
- **Role:** `admin`
- **Admin Security Key:** `ADMIN2026`"""

new_cred_section = """## 🔑 Authentication & Admin Portal Configuration

### 👨‍🎓 Student Portal (Self-Service Registration):
- Students can register with their own credentials via `register.html` or log in via `login.html`.
- Standard student account for testing:
  - **Email:** `student@example.com`
  - **Password:** `Student@123`
  - **Role:** `student`

### 🛡️ Authorized Admin Account (Single Fixed Administrator):
- **Email:** `vartikachaudhary0312@gmail.com`
- **Role:** `admin`
- **Password:** Configured via `ADMIN_PASSWORD` environment variable in `backend/.env`.
- **Security:**
  - Only `vartikachaudhary0312@gmail.com` can authenticate as the Administrator.
  - Public Admin registration is completely disabled; all public registrations are assigned the `student` role.
  - Passwords are encrypted using Werkzeug PBKDF2/scrypt hashing and never stored in plaintext.
  - If `ADMIN_PASSWORD` is missing in the environment, Admin login is refused with a 503 error."""

assert old_cred_section in content_norm, "old_cred_section not found"
content_norm = content_norm.replace(old_cred_section, new_cred_section)

with open('My Project/smart-mock-test/README.md', 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("README.md credentials section updated")

