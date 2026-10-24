from backend.repositories.result_repository import ResultRepository

class ResultService:
    def __init__(self):
        self.result_repo = ResultRepository()

    def get_user_results(self, user_id: int) -> list[dict]:
        return self.result_repo.find_by_user_id(user_id)

    def get_result_by_id(self, result_id: int) -> dict | None:
        return self.result_repo.find_by_id(result_id)

    def get_performance_analysis(self, result_id: int) -> tuple[bool, str, dict | None]:
        result = self.result_repo.find_by_id(result_id)
        if not result:
            return False, f"Result record #{result_id} not found.", None

        pct = result.get("percentage", 0.0)
        subject = result.get("subject", "General CS")

        if pct >= 75.0:
            strong_areas = [f"{subject} Fundamentals", "Conceptual MCQs", "Syntax & Structure"]
            weak_areas = ["Edge Cases", "Complex Scenario Optimization"]
            recommendations = [
                f"Attempt Hard difficulty tests in {subject}.",
                "Explore advanced career opportunities in Career Gateway matching your skill profile.",
                "Maintain test consistency with weekly practice mocks."
            ]
        elif pct >= 50.0:
            strong_areas = [f"Basic {subject} Definitions", "Core Syntax"]
            weak_areas = ["Problem Solving Under Time Limits", "Advanced Algorithmic Logic"]
            recommendations = [
                f"Revise intermediate topics in {subject}.",
                "Practice problem solving code traces.",
                "Re-attempt mock assessment on Medium difficulty."
            ]
        else:
            strong_areas = ["Primary Terminology"]
            weak_areas = [f"{subject} Core Concepts", "Logic Execution", "Time Management"]
            recommendations = [
                f"Re-study fundamental textbook modules for {subject}.",
                "Practice basic MCQs step-by-step.",
                "Take Easy level diagnostic test to build confidence."
            ]

        analysis = {
            "result_id": result_id,
            "subject": subject,
            "percentage": pct,
            "strong_areas": strong_areas,
            "weak_areas": weak_areas,
            "recommendations": recommendations
        }

        return True, "Performance analysis generated", analysis
