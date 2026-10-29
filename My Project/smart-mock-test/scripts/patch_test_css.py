import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'css', 'test.css')

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

# 1. Update .subject-card: remove overflow: hidden;
old_sc = """.subject-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.35rem;
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100%;
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
}"""

new_sc = """.subject-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem 1.35rem;
  cursor: pointer;
  transition: all var(--transition-normal);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100%;
  box-shadow: var(--shadow-sm);
  position: relative;
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
}"""

content_norm = content_norm.replace(old_sc, new_sc)

# 2. Update .subject-card-info: remove overflow: hidden;
old_sci = """.subject-card-info {
  flex: 1 1 0%;
  min-width: 0;
  max-width: 100%;
  overflow: hidden;
}"""

new_sci = """.subject-card-info {
  flex: 1 1 0%;
  min-width: 0;
  max-width: 100%;
}"""

content_norm = content_norm.replace(old_sci, new_sci)

# 3. Update .subject-card-badges .badge (remove overflow-wrap: anywhere)
old_scb = """.subject-card-badges .badge {
  white-space: normal !important;
  text-align: left;
  line-height: 1.25;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  font-size: 0.72rem;
  border-radius: var(--radius-sm);
  word-break: break-word;
  overflow-wrap: anywhere;
  max-width: 100%;
}"""

new_scb = """.subject-card-badges .badge {
  white-space: normal !important;
  text-align: left;
  line-height: 1.25;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  font-size: 0.72rem;
  border-radius: var(--radius-sm);
  word-break: normal;
  overflow-wrap: break-word;
  max-width: 100%;
}"""

content_norm = content_norm.replace(old_scb, new_scb)

# 4. Update .subject-card-count
old_scc = """.subject-card-count {
  font-size: 0.82rem;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  min-width: 0;
  word-break: break-word;
  flex: 1 1 auto;
}"""

new_scc = """.subject-card-count {
  font-size: 0.82rem;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  min-width: 0;
  word-break: normal;
  overflow-wrap: break-word;
  flex: 1 1 auto;
}"""

content_norm = content_norm.replace(old_scc, new_scc)

# 5. Update .difficulty-options and .difficulty-card
old_diff = """.difficulty-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
}

.difficulty-card {
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.25rem;
  cursor: pointer;
  background-color: var(--surface);
  transition: all var(--transition-fast);
}

.difficulty-card:hover, .difficulty-card.selected {
  border-color: var(--primary);
}

.difficulty-card.selected {
  background-color: var(--primary-light);
}"""

new_diff = """.difficulty-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr));
  gap: 1rem;
  width: 100%;
}

.difficulty-options > [class*="col-"] {
  width: 100% !important;
  max-width: 100% !important;
  flex: 1 1 100% !important;
  padding: 0 !important;
}

.difficulty-card {
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.15rem 1.25rem;
  cursor: pointer;
  background-color: var(--surface);
  transition: all var(--transition-fast);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 100%;
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
}

.difficulty-card:hover, .difficulty-card.selected {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(109, 74, 255, 0.08);
}

.difficulty-card.selected {
  background-color: var(--primary-light);
}

.difficulty-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  flex-wrap: wrap;
  margin-bottom: 0.5rem;
  min-width: 0;
  width: 100%;
}

.difficulty-card-desc {
  font-size: 0.825rem;
  color: var(--muted);
  line-height: 1.4;
  word-break: normal;
  overflow-wrap: break-word;
  margin: 0;
}"""

content_norm = content_norm.replace(old_diff, new_diff)

# 6. Update .cfg-len-card
old_len = """/* Test Configuration Length Cards */
.cfg-len-card {
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem;
  cursor: pointer;
  background-color: var(--surface);
  transition: all var(--transition-fast);
}

.cfg-len-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(109, 74, 255, 0.08);
}

.cfg-len-card.selected {
  border-color: var(--primary);
  background-color: var(--primary-light);
  color: var(--primary);
  font-weight: 600;
}"""

new_len = """/* Test Configuration Length Cards */
.length-options-grid, #cfgLengthOptions {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 140px), 1fr));
  gap: 0.75rem;
  width: 100%;
}

.length-options-grid > [class*="col-"],
#cfgLengthOptions > [class*="col-"] {
  width: 100% !important;
  max-width: 100% !important;
  padding: 0 !important;
}

.cfg-len-card {
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem 0.75rem;
  cursor: pointer;
  background-color: var(--surface);
  transition: all var(--transition-fast);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  min-height: 100%;
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
}

.cfg-len-card:hover {
  border-color: var(--primary);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(109, 74, 255, 0.08);
}

.cfg-len-card.selected {
  border-color: var(--primary);
  background-color: var(--primary-light);
  color: var(--primary);
  font-weight: 600;
}

.cfg-len-value {
  font-size: clamp(1rem, 2vw, 1.25rem);
  font-weight: 700;
  white-space: nowrap;
  word-break: normal;
  margin-bottom: 0.2rem;
}

.cfg-len-time {
  font-size: 0.75rem;
  white-space: nowrap;
}"""

content_norm = content_norm.replace(old_len, new_len)

# 7. Replace 100vw in fullscreen exam mode
content_norm = content_norm.replace(
    "width: 100vw !important;\n  max-width: 100vw !important;",
    "width: 100% !important;\n  max-width: 100% !important;"
)
content_norm = content_norm.replace(
    "width: 100vw;\n  height: 100vh;\n  background: rgba(15, 23, 42, 0.88);",
    "position: fixed;\n  inset: 0;\n  width: 100%;\n  height: 100%;\n  background: rgba(15, 23, 42, 0.88);"
)
content_norm = content_norm.replace(
    "width: 100vw;\n  height: 100vh;\n  background: rgba(15, 23, 42, 0.95);",
    "position: fixed;\n  inset: 0;\n  width: 100%;\n  height: 100%;\n  background: rgba(15, 23, 42, 0.95);"
)

# 8. Update .question-option-item
old_qopt = """.question-option-item {
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
  margin-bottom: 0.85rem;
  cursor: pointer;
  background-color: var(--surface);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all var(--transition-fast);
}"""

new_qopt = """.question-option-item {
  border: 1.5px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
  margin-bottom: 0.85rem;
  cursor: pointer;
  background-color: var(--surface);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all var(--transition-fast);
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
  word-break: normal;
  overflow-wrap: break-word;
}

.question-option-item > span:last-child {
  flex: 1 1 0%;
  min-width: 0;
  word-break: normal;
  overflow-wrap: break-word;
}"""

content_norm = content_norm.replace(old_qopt, new_qopt)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("SUCCESS: test.css patched successfully!")

