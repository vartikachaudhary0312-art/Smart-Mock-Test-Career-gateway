import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'css', 'career.css')

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

# 1. Update .job-card
old_jc = """.job-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  transition: all var(--transition-normal);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  box-shadow: var(--shadow-sm);
  position: relative;
  overflow: hidden;
}"""

new_jc = """.job-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
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
}

.job-card h5 {
  word-break: normal;
  overflow-wrap: break-word;
  line-height: 1.35;
}"""

content_norm = content_norm.replace(old_jc, new_jc)

# 2. Update .job-company-logo: add flex-shrink: 0
old_jcl = """.job-company-logo {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--primary-light), var(--surface-subtle));
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.3rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow-sm);
}"""

new_jcl = """.job-company-logo {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--primary-light), var(--surface-subtle));
  color: var(--primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.3rem;
  margin-bottom: 1rem;
  box-shadow: var(--shadow-sm);
  flex-shrink: 0;
}"""

content_norm = content_norm.replace(old_jcl, new_jcl)

# 3. Update .timeline-circle: add flex-shrink: 0
old_tc = """.timeline-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background-color: var(--surface);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--muted);
  margin-bottom: 0.4rem;
}"""

new_tc = """.timeline-circle {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: 2px solid var(--border);
  background-color: var(--surface);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--muted);
  margin-bottom: 0.4rem;
  flex-shrink: 0;
}"""

content_norm = content_norm.replace(old_tc, new_tc)

# 4. Update .subject-card-enhanced
old_sce = """.subject-card-enhanced {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  transition: all var(--transition-normal);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
  box-shadow: var(--shadow-sm);
  position: relative;
}"""

new_sce = """.subject-card-enhanced {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
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

content_norm = content_norm.replace(old_sce, new_sce)

# 5. Update .category-portal-card
old_cpc = """.category-portal-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all var(--transition-normal);
  cursor: pointer;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}"""

new_cpc = """.category-portal-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: all var(--transition-normal);
  cursor: pointer;
  position: relative;
  box-shadow: var(--shadow-sm);
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
}

.category-portal-card h5 {
  word-break: normal;
  overflow-wrap: break-word;
  line-height: 1.35;
}"""

content_norm = content_norm.replace(old_cpc, new_cpc)

# 6. Update .config-option-card
old_coc = """.config-option-card {
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  padding: 0.75rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: center;
}"""

new_coc = """.config-option-card {
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
}

.config-option-card .fw-bold {
  word-break: normal;
  overflow-wrap: break-word;
}

.config-option-card .small {
  word-break: normal;
  overflow-wrap: break-word;
  line-height: 1.35;
}"""

content_norm = content_norm.replace(old_coc, new_coc)

# 7. Update .practice-runner-container and .practice-option-item
old_prc = """.practice-runner-container {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-md);
  max-width: 900px;
  margin: 0 auto;
}"""

new_prc = """.practice-runner-container {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 2rem;
  box-shadow: var(--shadow-md);
  max-width: 900px;
  width: 100%;
  margin: 0 auto;
  min-width: 0;
  box-sizing: border-box;
}"""

content_norm = content_norm.replace(old_prc, new_prc)

old_poi = """.practice-option-item {
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
  margin-bottom: 0.85rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  gap: 1rem;
  background-color: var(--surface);
  font-size: 0.95rem;
}"""

new_poi = """.practice-option-item {
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1rem 1.25rem;
  margin-bottom: 0.85rem;
  cursor: pointer;
  transition: all var(--transition-fast);
  display: flex;
  align-items: center;
  gap: 1rem;
  background-color: var(--surface);
  font-size: 0.95rem;
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
  word-break: normal;
  overflow-wrap: break-word;
}

.practice-option-item > div:last-child {
  flex: 1 1 0%;
  min-width: 0;
  word-break: normal;
  overflow-wrap: break-word;
}"""

content_norm = content_norm.replace(old_poi, new_poi)

# 8. Update .topic-card-badge: fix word-break
old_tcb = """.topic-card-badge {
  white-space: normal;
  word-break: break-word;
}"""

new_tcb = """.topic-card-badge {
  white-space: normal;
  word-break: normal;
  overflow-wrap: break-word;
}"""

content_norm = content_norm.replace(old_tcb, new_tcb)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("SUCCESS: career.css patched successfully!")

