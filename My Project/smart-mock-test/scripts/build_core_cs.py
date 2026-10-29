"""
Generator for Core Computer Science Question Bank (700 Questions):
- Data Structures & Algorithms (sub_dsa): 100
- Database Management Systems (sub_dbms): 100
- Operating Systems (sub_os): 100
- Computer Networks (sub_cn): 100
- Object-Oriented Programming (sub_oop): 100
- Software Engineering (sub_se): 100
- SQL & Queries (sub_sql): 100
"""

import os
import sys

def build_data_core_cs():
    out_path = os.path.join(os.path.dirname(__file__), "data_core_cs.py")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write('''# Auto-generated Core Computer Science Question Bank
# Covers DSA (100), DBMS (100), OS (100), CN (100), OOP (100), SE (100), SQL (100)

def make_q(qid, subject_id, subject, category_id, difficulty, question, options, correct_idx, explanation):
    letters = ["A", "B", "C", "D"]
    return {
        "id": qid,
        "subject_id": subject_id,
        "subject": subject,
        "category_id": category_id,
        "difficulty": difficulty,
        "question_text": question,
        "question": question,
        "option_a": options[0],
        "option_b": options[1],
        "option_c": options[2],
        "option_d": options[3],
        "options": options,
        "correct_option": letters[correct_idx],
        "correctIndex": correct_idx,
        "explanation": explanation
    }

''')

if __name__ == "__main__":
    build_data_core_cs()
    print("Base data_core_cs initialized.")
