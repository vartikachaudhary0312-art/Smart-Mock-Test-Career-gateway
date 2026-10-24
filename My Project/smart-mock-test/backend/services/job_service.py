from backend.repositories.job_repository import JobRepository

class JobService:
    def __init__(self):
        self.job_repo = JobRepository()

    def get_jobs(self, company: str = None, location: str = None, skills: str = None, job_type: str = None) -> list[dict]:
        return self.job_repo.filter(company=company, location=location, skills=skills, job_type=job_type)

    def get_job_by_id(self, job_id: int) -> dict | None:
        return self.job_repo.find_by_id(job_id)

    def create_job(self, job_data: dict) -> tuple[bool, str, dict | None, int]:
        required = ["title", "company", "location"]
        for f in required:
            if not job_data.get(f):
                return False, f"Missing required field: {f}", None, 400

        job_obj = {
            "title": job_data["title"].strip(),
            "company": job_data["company"].strip(),
            "location": job_data["location"].strip(),
            "job_type": job_data.get("job_type", "Full-Time"),
            "experience": job_data.get("experience", "0 - 1 Years"),
            "salary": job_data.get("salary", "Competitive"),
            "skills": job_data.get("skills", []),
            "description": job_data.get("description", ""),
            "status": "Active"
        }

        created = self.job_repo.create(job_obj)
        return True, "Job posting created successfully", created, 201

    def update_job(self, job_id: int, update_data: dict) -> tuple[bool, str, dict | None, int]:
        updated = self.job_repo.update(job_id, update_data)
        if not updated:
            return False, f"Job posting #{job_id} not found.", None, 404
        return True, "Job posting updated successfully", updated, 200

    def delete_job(self, job_id: int) -> tuple[bool, str, int]:
        deleted = self.job_repo.delete(job_id)
        if not deleted:
            return False, f"Job posting #{job_id} not found.", 404
        return True, "Job posting deleted successfully", 200
