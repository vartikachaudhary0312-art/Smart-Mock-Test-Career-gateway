import os
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
ALLOWED_MIMETYPES = {'application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'}

class ResumeService:
    def __init__(self, upload_folder: str):
        self.upload_folder = upload_folder

    def process_resume_upload(self, file_obj) -> tuple[bool, str, dict | None, int]:
        if not file_obj or file_obj.filename == '':
            return False, "No file provided in request.", None, 400

        filename = secure_filename(file_obj.filename)
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''

        if ext not in ALLOWED_EXTENSIONS:
            return False, "Invalid file format. Only PDF and DOCX files are allowed.", None, 400

        # Create upload folder if missing
        os.makedirs(self.upload_folder, exist_ok=True)
        save_path = os.path.join(self.upload_folder, filename)
        file_obj.save(save_path)

        file_size_mb = os.path.getsize(save_path) / (1024 * 1024)

        # Mock ATS resume analysis result
        mock_analysis = {
            "file_name": filename,
            "file_size": f"{file_size_mb:.2f} MB",
            "match_score": 84,
            "skills": ["Python", "Java", "SQL", "HTML5", "CSS3", "JavaScript", "REST APIs", "Git"],
            "education": [
                {
                    "degree": "Master of Computer Applications (MCA)",
                    "performance": "8.4 CGPA",
                    "status": "Final Year"
                }
            ],
            "experience": [
                {
                    "role": "Software Project Intern",
                    "highlights": ["Built Smart Mock Test & Career Gateway application", "Implemented Flask REST APIs"]
                }
            ],
            "projects": ["Smart Mock Test & Career Gateway Platform", "Student Placement Tracker"],
            "recommendations": [
                "Highlight database normalization and SQL join query experience.",
                "Include GitHub or deployment URL links for final year MCA projects.",
                "Mention unit testing frameworks like PyTest or JUnit."
            ],
            "suggested_roles": [
                "Graduate Software Engineer Trainee",
                "Junior Python Backend Developer",
                "Associate Web Specialist"
            ]
        }

        return True, "Resume uploaded and analyzed successfully", mock_analysis, 200
