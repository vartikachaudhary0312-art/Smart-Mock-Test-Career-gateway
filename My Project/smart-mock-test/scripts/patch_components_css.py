import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'css', 'components.css')

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

old_block = """/* Cards System */
.card-custom {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal), border-color var(--transition-normal), background-color var(--transition-normal), color var(--transition-normal);
  overflow: hidden;
}

.card-custom:hover {
  box-shadow: var(--shadow-md);
}

.card-custom-interactive:hover {
  transform: translateY(-4px);
  border-color: var(--primary);
  box-shadow: var(--shadow-lg);
}

.card-header-custom {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: transparent;
}

.card-body-custom {
  padding: 1.5rem;
}

.card-title-custom {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
  margin: 0;
}

/* Stat Cards */
.stat-card {
  padding: 1.25rem;
  display: flex;
  align-items: flex-start;
  gap: 1rem;

}

.stat-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}"""

new_block = """/* Cards System */
.card-custom {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  transition: transform var(--transition-normal), box-shadow var(--transition-normal), border-color var(--transition-normal), background-color var(--transition-normal), color var(--transition-normal);
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
}

.card-custom:hover {
  box-shadow: var(--shadow-md);
}

.card-custom-interactive:hover {
  transform: translateY(-4px);
  border-color: var(--primary);
  box-shadow: var(--shadow-lg);
}

.card-header-custom {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 0.5rem;
  background-color: transparent;
  min-width: 0;
}

.card-body-custom {
  padding: 1.5rem;
  min-width: 0;
  box-sizing: border-box;
}

.card-title-custom {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
  margin: 0;
  word-break: normal;
  overflow-wrap: break-word;
  min-width: 0;
}

/* Stat Cards */
.stat-card {
  padding: 1.25rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
}

.stat-card > div:last-child {
  flex: 1 1 0%;
  min-width: 0;
}

.stat-icon-wrapper {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}"""

content_norm = content_norm.replace(old_block, new_block)

# Also update stat-value and stat-label
old_stat_text = """.stat-value {
  font-size: 1.65rem;
  font-weight: 800;
  color: var(--text);
  line-height: 1.1;
  margin-bottom: 0.2rem;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--muted);
  font-weight: 500;
}"""

new_stat_text = """.stat-value {
  font-size: 1.65rem;
  font-weight: 800;
  color: var(--text);
  line-height: 1.1;
  margin-bottom: 0.2rem;
  word-break: normal;
  overflow-wrap: break-word;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--muted);
  font-weight: 500;
  word-break: normal;
  overflow-wrap: break-word;
}"""

content_norm = content_norm.replace(old_stat_text, new_stat_text)

# Also ensure modals and dropdowns have clean boundaries
old_modal = """.modal-content {
  background-color: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
}"""

new_modal = """.modal-content {
  background-color: var(--surface);
  border: 1px solid var(--border);
  color: var(--text);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-xl);
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
}"""

content_norm = content_norm.replace(old_modal, new_modal)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("SUCCESS: components.css patched successfully!")

