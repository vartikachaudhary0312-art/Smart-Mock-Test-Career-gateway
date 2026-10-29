import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'css', 'dashboard.css')

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

# 1. Update .header-logo-badge: add flex-shrink: 0
old_hlb = """.header-logo-badge {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #7C3AED, #A855F7);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
}"""

new_hlb = """.header-logo-badge {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #7C3AED, #A855F7);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.35rem;
  box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
  transition: transform var(--transition-fast), box-shadow var(--transition-fast);
  flex-shrink: 0;
}"""

content_norm = content_norm.replace(old_hlb, new_hlb)

# 2. Update .stats-grid and .quick-actions-grid and .action-card
old_dash_grids = """.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.25rem;
  margin-bottom: 1.5rem;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.action-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  text-decoration: none;
  color: var(--text);
}

.action-card:hover {
  transform: translateY(-3px);
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
  color: var(--primary);
}

.action-card-primary {
  background: linear-gradient(135deg, var(--primary-light), var(--surface));
  border-color: var(--primary);
}

.action-card-icon {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
  background-color: var(--surface-subtle);
  color: var(--primary);
}

.action-card-primary .action-card-icon {
  background-color: var(--primary);
  color: #ffffff;
}

.action-card-title {
  font-weight: 700;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
}

.action-card-desc {
  font-size: 0.78rem;
  color: var(--muted);
}"""

new_dash_grids = """.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 220px), 1fr));
  gap: 1.25rem;
  margin-bottom: 1.5rem;
  width: 100%;
}

.quick-actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 180px), 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
  width: 100%;
}

.action-card {
  background-color: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  text-decoration: none;
  color: var(--text);
  min-width: 0;
  width: 100%;
  box-sizing: border-box;
}

.action-card:hover {
  transform: translateY(-3px);
  border-color: var(--primary);
  box-shadow: var(--shadow-md);
  color: var(--primary);
}

.action-card-primary {
  background: linear-gradient(135deg, var(--primary-light), var(--surface));
  border-color: var(--primary);
}

.action-card-icon {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  margin-bottom: 0.75rem;
  background-color: var(--surface-subtle);
  color: var(--primary);
  flex-shrink: 0;
}

.action-card-primary .action-card-icon {
  background-color: var(--primary);
  color: #ffffff;
}

.action-card-title {
  font-weight: 700;
  font-size: 0.95rem;
  margin-bottom: 0.25rem;
  word-break: normal;
  overflow-wrap: break-word;
  max-width: 100%;
}

.action-card-desc {
  font-size: 0.78rem;
  color: var(--muted);
  word-break: normal;
  overflow-wrap: break-word;
  line-height: 1.35;
  max-width: 100%;
}"""

content_norm = content_norm.replace(old_dash_grids, new_dash_grids)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("SUCCESS: dashboard.css patched successfully!")

