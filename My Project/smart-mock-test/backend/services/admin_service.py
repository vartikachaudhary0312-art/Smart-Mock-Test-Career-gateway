from backend.repositories.user_repository import UserRepository
from backend.repositories.result_repository import ResultRepository
from backend.repositories.job_repository import JobRepository
from backend.repositories.application_repository import ApplicationRepository
from backend.repositories.question_repository import QuestionRepository

class AdminService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.result_repo = ResultRepository()
        self.job_repo = JobRepository()
        self.app_repo = ApplicationRepository()
        self.question_repo = QuestionRepository()

    def get_dashboard_metrics(self) -> dict:
        students = self.user_repo.find_students()
        results = self.result_repo.find_all()
        jobs = self.job_repo.find_all()
        apps = self.app_repo.find_all()

        total_students = len(students)
        tests_attempted = len(results)
        valid_pcts = [float(r.get("percentage") or 0.0) for r in results if r.get("percentage") is not None]
        avg_score = round(sum(valid_pcts) / len(valid_pcts), 1) if valid_pcts else 0.0
        active_jobs = len([j for j in jobs if j.get("status") == "Active"])
        total_applications = len(apps)

        # Chart.js Ready Datasets
        students_growth = {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May"],
            "data": [12, 28, 45, 68, max(85, total_students)]
        }

        test_attempts = {
            "labels": ["Week 1", "Week 2", "Week 3", "Week 4"],
            "data": [10, 25, 40, tests_attempted]
        }

        average_scores = {
            "labels": ["Java", "Python", "DSA", "DBMS", "SQL", "Web"],
            "data": [80, 65, 70, 85, 90, 75]
        }

        status_counts = {"Applied": 0, "Under Review": 0, "Shortlisted": 0, "Interview": 0, "Selected": 0, "Rejected": 0}
        for a in apps:
            st = a.get("status", "Applied")
            if st in status_counts:
                status_counts[st] += 1

        application_status = {
            "labels": list(status_counts.keys()),
            "data": list(status_counts.values())
        }

        return {
            "total_students": total_students,
            "tests_attempted": tests_attempted,
            "average_score": avg_score,
            "active_jobs": active_jobs,
            "total_applications": total_applications,
            "students_growth": students_growth,
            "test_attempts": test_attempts,
            "average_scores": average_scores,
            "application_status": application_status
        }
