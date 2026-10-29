import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'css', 'responsive.css')

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

additions = """
/* Mobile Exam Screen & Widget Optimization */
@media (max-width: 575.98px) {
  .proctor-pip-widget {
    width: 135px;
    bottom: 12px;
    right: 12px;
  }
  .proctor-pip-video-wrap {
    height: 85px;
  }
  .proctor-pip-header {
    font-size: 0.65rem;
    padding: 4px 8px;
  }
  .proctor-pip-footer {
    font-size: 0.65rem;
    padding: 3px 8px;
  }
  .test-header-bar {
    padding: 0.65rem 0.85rem;
  }
  .timer-badge {
    font-size: 0.95rem;
    padding: 0.3rem 0.65rem;
  }
  .difficulty-options {
    grid-template-columns: 1fr;
    gap: 0.75rem;
  }
  .length-options-grid, #cfgLengthOptions {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.5rem;
  }
  .length-options-grid > div:last-child,
  #cfgLengthOptions > div:last-child {
    grid-column: span 2;
  }
}

/* Tablet Optimizations */
@media (min-width: 576px) and (max-width: 991.98px) {
  .difficulty-options {
    grid-template-columns: repeat(2, 1fr);
    gap: 0.85rem;
  }
  .length-options-grid, #cfgLengthOptions {
    grid-template-columns: repeat(auto-fit, minmax(110px, 1fr));
    gap: 0.65rem;
  }
}
"""

if "Mobile Exam Screen & Widget Optimization" not in content_norm:
    content_norm += additions
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content_norm)
    print("SUCCESS: responsive.css updated with responsive audit additions!")
else:
    print("responsive.css already contains additions.")

