"""
Master Assembler for Smart Mock Test & Career Gateway Question Bank
1. Integrates Core CS, Programming, Aptitude, Placement, and Specialized questions.
2. Validates schema and deduplicates.
3. Updates backend/data/questions.json.
4. Synchronizes actual question counts in subjects.json and categories.json.
5. Updates frontend/js/mock-data.js.
"""

import os
import sys
import json
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.build_core_cs_bank import generate_core_cs
from scripts.build_prog_bank import generate_programming_bank
from scripts.build_aptitude_bank import generate_aptitude_bank
from scripts.build_placement_bank import generate_placement_bank
from scripts.build_specialized_bank import generate_specialized_bank

def assemble():
    print("--- 1. Generating Question Sets ---")
    core_cs = generate_core_cs()
    prog = generate_programming_bank()
    apt = generate_aptitude_bank()
    plc = generate_placement_bank()

    covered_ids = set(q["subject_id"] for q in (core_cs + prog + apt + plc))
    print(f"Subjects covered by primary banks: {len(covered_ids)}")

    spec = generate_specialized_bank(covered_ids)

    all_questions = core_cs + prog + apt + plc + spec
    print(f"Total raw questions generated: {len(all_questions)}")

    # Schema verification & deduplication
    seen_ids = set()
    cleaned_questions = []
    for q in all_questions:
        if q["id"] in seen_ids:
            # disambiguate id
            q["id"] = f"{q['id']}_{len(cleaned_questions)}"
        seen_ids.add(q["id"])

        # Validate fields
        assert "question" in q and len(q["question"]) > 0
        assert "options" in q and len(q["options"]) == 4
        assert "correctIndex" in q and 0 <= q["correctIndex"] <= 3
        assert "explanation" in q and len(q["explanation"]) > 0
        assert "subject_id" in q and len(q["subject_id"]) > 0

        # Ensure compatibility fields
        q["question_text"] = q["question"]
        q["option_a"] = q["options"][0]
        q["option_b"] = q["options"][1]
        q["option_c"] = q["options"][2]
        q["option_d"] = q["options"][3]
        q["correct_option"] = ["A", "B", "C", "D"][q["correctIndex"]]

        cleaned_questions.append(q)

    print(f"Verified & clean questions count: {len(cleaned_questions)}")

    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    questions_path = os.path.join(base_dir, "backend", "data", "questions.json")
    subjects_path = os.path.join(base_dir, "backend", "data", "subjects.json")
    categories_path = os.path.join(base_dir, "backend", "data", "categories.json")
    mock_data_js_path = os.path.join(base_dir, "frontend", "js", "mock-data.js")

    # 1. Write backend/data/questions.json
    with open(questions_path, "w", encoding="utf-8") as f:
        json.dump(cleaned_questions, f, indent=2, ensure_ascii=False)
    print(f"Saved {questions_path} ({len(cleaned_questions)} questions)")

    # 2. Count questions per subject
    subject_counts = Counter(q["subject_id"] for q in cleaned_questions)
    print("Subject counts sample:", subject_counts.most_common(10))

    # 3. Update backend/data/subjects.json
    with open(subjects_path, "r", encoding="utf-8") as f:
        subjects = json.load(f)

    for sub in subjects:
        count = subject_counts.get(sub["id"], 0)
        sub["question_count"] = count
        sub["questionCount"] = count

    with open(subjects_path, "w", encoding="utf-8") as f:
        json.dump(subjects, f, indent=2, ensure_ascii=False)
    print(f"Updated {subjects_path} with accurate question counts across {len(subjects)} subjects")

    # 4. Count questions per category & update backend/data/categories.json
    with open(categories_path, "r", encoding="utf-8") as f:
        categories = json.load(f)

    cat_question_counts = Counter(q.get("category_id") for q in cleaned_questions)
    # Also sum by matching subject category mapping
    sub_to_cat = {s["id"]: s.get("category_id") for s in subjects}
    for q in cleaned_questions:
        c_id = q.get("category_id") or sub_to_cat.get(q["subject_id"])
        if c_id:
            cat_question_counts[c_id] += 1

    for cat in categories:
        # Sum questions from all topics belonging to this category
        cat_topics = cat.get("topic_ids", [])
        total_for_cat = sum(subject_counts.get(tid, 0) for tid in cat_topics)
        cat["total_questions"] = total_for_cat
        cat["topic_count"] = len(cat_topics)

    with open(categories_path, "w", encoding="utf-8") as f:
        json.dump(categories, f, indent=2, ensure_ascii=False)
    print(f"Updated {categories_path} with accurate total questions")

    # 5. Update frontend/js/mock-data.js
    with open(mock_data_js_path, "r", encoding="utf-8") as f:
        js_content = f.read()

    # Prepare JSON serializations
    q_json_str = json.dumps(cleaned_questions, ensure_ascii=False)
    sub_json_str = json.dumps(subjects, ensure_ascii=False)
    cat_json_str = json.dumps(categories, ensure_ascii=False)

    # In mock-data.js, replace the initial questions array, subjects array, and categories array
    # Let's write a python updater for mock-data.js that replaces INITIAL_QUESTIONS, INITIAL_SUBJECTS, INITIAL_CATEGORIES
    update_mock_data_file(mock_data_js_path, cleaned_questions, subjects, categories)
    print("Synchronized frontend/js/mock-data.js")

def update_mock_data_file(mock_data_path, questions, subjects, categories):
    with open(mock_data_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Search for INITIAL_SUBJECTS, INITIAL_CATEGORIES, INITIAL_QUESTIONS
    # We will write a clean mock-data.js that keeps all mock tests, jobs, results, applications, but embeds the fresh categories, subjects, and questions!
    new_lines = []
    in_skip = False
    skip_marker = None

    for line in lines:
        if "const INITIAL_CATEGORIES =" in line:
            new_lines.append(f"const INITIAL_CATEGORIES = {json.dumps(categories, indent=2)};\n")
            in_skip = True
            skip_marker = "const INITIAL_SUBJECTS ="
        elif "const INITIAL_SUBJECTS =" in line:
            new_lines.append(f"const INITIAL_SUBJECTS = {json.dumps(subjects, indent=2)};\n")
            in_skip = True
            skip_marker = "const INITIAL_QUESTIONS ="
        elif "const INITIAL_QUESTIONS =" in line:
            new_lines.append(f"const INITIAL_QUESTIONS = {json.dumps(questions, indent=2)};\n")
            in_skip = True
            skip_marker = "const INITIAL_TESTS ="
        elif in_skip and skip_marker and skip_marker in line:
            in_skip = False
            new_lines.append(line)
        elif not in_skip:
            new_lines.append(line)

    with open(mock_data_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    assemble()
