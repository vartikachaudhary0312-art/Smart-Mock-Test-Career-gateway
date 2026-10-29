import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'index.html')
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith('+++++++++++++++++++++++++++++<html'):
        lines[i] = '<html lang="en" data-bs-theme="light">\n'

with open(file_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Fixed index.html!")
