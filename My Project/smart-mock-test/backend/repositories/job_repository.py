import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "jobs.json"

class JobRepository:
    @staticmethod
    def _load_jobs() -> list[dict]:
        if not DATA_FILE.exists():
            return []
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _save_jobs(jobs: list[dict]):
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(jobs, f, indent=2)

    def find_all(self) -> list[dict]:
        return self._load_jobs()

    def find_by_id(self, job_id: int) -> dict | None:
        jobs = self._load_jobs()
        return next((j for j in jobs if j["id"] == job_id), None)

    def filter(self, company: str = None, location: str = None, skills: str = None, job_type: str = None) -> list[dict]:
        jobs = self._load_jobs()
        filtered = []
        for j in jobs:
            if company and company.lower() not in j.get("company", "").lower():
                continue
            if location and location.lower() not in j.get("location", "").lower():
                continue
            if job_type and job_type.lower() != j.get("job_type", "").lower():
                continue
            if skills:
                search_skill = skills.lower()
                job_skills = [s.lower() for s in j.get("skills", [])]
                if not any(search_skill in s for s in job_skills) and search_skill not in j.get("title", "").lower():
                    continue
            filtered.append(j)
        return filtered

    def create(self, job_data: dict) -> dict:
        jobs = self._load_jobs()
        new_id = max([j["id"] for j in jobs], default=0) + 1
        job_data["id"] = new_id
        jobs.insert(0, job_data)
        self._save_jobs(jobs)
        return job_data

    def update(self, job_id: int, update_fields: dict) -> dict | None:
        jobs = self._load_jobs()
        for j in jobs:
            if j["id"] == job_id:
                j.update(update_fields)
                self._save_jobs(jobs)
                return j
        return None

    def delete(self, job_id: int) -> bool:
        jobs = self._load_jobs()
        initial_len = len(jobs)
        jobs = [j for j in jobs if j["id"] != job_id]
        if len(jobs) < initial_len:
            self._save_jobs(jobs)
            return True
        return False
