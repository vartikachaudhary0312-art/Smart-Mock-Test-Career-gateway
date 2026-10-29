import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'css', 'global.css')

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

# 1. Update box sizing and html, body
old_reset = """* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  font-family: var(--font-family);
  background-color: var(--background);
  color: var(--text);
  line-height: 1.5;
  min-height: 100vh;
  transition: background-color var(--transition-normal), color var(--transition-normal);
  overflow-x: hidden;
}"""

new_reset = """*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  font-family: var(--font-family);
  background-color: var(--background);
  color: var(--text);
  line-height: 1.5;
  min-height: 100vh;
  width: 100%;
  max-width: 100%;
  transition: background-color var(--transition-normal), color var(--transition-normal);
  overflow-x: hidden;
  position: relative;
}

h1, h2, h3, h4, h5, h6,
.h1, .h2, .h3, .h4, .h5, .h6 {
  word-break: normal;
  overflow-wrap: break-word;
}

p, span, label, td, th {
  overflow-wrap: break-word;
}

.badge {
  word-break: normal;
  overflow-wrap: break-word;
}"""

content_norm = content_norm.replace(old_reset, new_reset)

# 2. Update .brand-logo with flex-shrink: 0
old_bl = """.brand-logo {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 700;
  box-shadow: var(--shadow-purple);
}"""

new_bl = """.brand-logo {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, var(--primary), var(--primary-dark));
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 700;
  box-shadow: var(--shadow-purple);
  flex-shrink: 0;
}"""

content_norm = content_norm.replace(old_bl, new_bl)

# 3. Update .app-container, .app-main, and .page-body
old_shell = """.app-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
}"""

new_shell = """.app-container {
  display: flex;
  min-height: 100vh;
  width: 100%;
  max-width: 100%;
  overflow-x: hidden;
}"""

content_norm = content_norm.replace(old_shell, new_shell)

old_am = """.app-main {
  flex: 1;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  min-width: 0; /* Prevents flex overflow */
  transition: margin-left var(--transition-slow);
}"""

new_am = """.app-main {
  flex: 1;
  margin-left: var(--sidebar-width);
  display: flex;
  flex-direction: column;
  min-width: 0; /* Prevents flex overflow */
  max-width: 100%;
  overflow-x: hidden;
  transition: margin-left var(--transition-slow);
}"""

content_norm = content_norm.replace(old_am, new_am)

old_pb = """.page-body {
  padding: 1.5rem;
  flex: 1;
}"""

new_pb = """.page-body {
  padding: 1.5rem;
  flex: 1;
  min-width: 0;
  max-width: 100%;
  box-sizing: border-box;
}"""

content_norm = content_norm.replace(old_pb, new_pb)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("SUCCESS: global.css patched successfully!")

