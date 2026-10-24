from datetime import datetime
from backend.repositories.application_repository import ApplicationRepository
from backend.repositories.job_repository import JobRepository

class ApplicationService:
    def __init__(self):
        self.app_repo = ApplicationRepository()
        self.job_repo = JobRepository()

    def get_student_applications(self, student_id: int) -> list[dict]:
        return self.app_repo.find_by_student_id(student_id)

    def get_all_applications(self) -> list[dict]:
        return self.app_repo.find_all()

    def apply_for_job(self, student_id: int, job_id: int) -> tuple[bool, str, dict | None, int]:
        job = self.job_repo.find_by_id(job_id)
        if not job:
            return False, f"Job posting #{job_id} not found.", None, 404

        existing = self.app_repo.find_by_student_and_job(student_id, job_id)
        if existing:
            return False, "You have already submitted an application for this position.", None, 409

        app_obj = {
            "student_id": student_id,
            "job_id": job_id,
            "company": job["company"],
            "job_title": job["title"],
            "location": job.get("location", "India"),
            "status": "Applied",
            "applied_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        created = self.app_repo.create(app_obj)
        return True, "Application submitted successfully", created, 201

    def update_application_status(self, app_id: int, status: str) -> tuple[bool, str, dict | None, int]:
        valid_statuses = ["Applied", "Under Review", "Shortlisted", "Interview", "Selected", "Rejected"]
        if status not in valid_statuses:
            return False, f"Invalid status value. Must be one of: {valid_statuses}", None, 400

        updated = self.app_repo.update_status(app_id, status)
        if not updated:
            return False, f"Application #{app_id} not found.", None, 404

        return True, f"Application status updated to '{status}'", updated, 200
