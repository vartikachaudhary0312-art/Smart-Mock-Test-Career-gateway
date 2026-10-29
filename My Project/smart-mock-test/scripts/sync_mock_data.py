"""
Syncs frontend/js/mock-data.js cleanly with backend JSON files
"""
import json
import os

def sync():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    questions_path = os.path.join(base_dir, "backend", "data", "questions.json")
    subjects_path = os.path.join(base_dir, "backend", "data", "subjects.json")
    categories_path = os.path.join(base_dir, "backend", "data", "categories.json")
    mock_data_path = os.path.join(base_dir, "frontend", "js", "mock-data.js")

    with open(questions_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
    with open(subjects_path, "r", encoding="utf-8") as f:
        subjects = json.load(f)
    with open(categories_path, "r", encoding="utf-8") as f:
        categories = json.load(f)

    with open(mock_data_path, "r", encoding="utf-8") as f:
        c = f.read()

    cat_idx = c.find("categories: [")
    jobs_idx = c.find("jobs: [")

    head = c[:cat_idx]
    tail = c[jobs_idx:]

    cat_json = json.dumps(categories, indent=2)
    sub_json = json.dumps(subjects, indent=2)
    q_json = json.dumps(questions, indent=2)

    new_content = (
        head +
        f"categories: {cat_json},\n\n" +
        f"  subjects: {sub_json},\n\n" +
        f"  questions: {q_json},\n\n  " +
        tail
    )

    with open(mock_data_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Synced mock-data.js successfully! Length: {len(new_content)}")

if __name__ == "__main__":
    sync()
