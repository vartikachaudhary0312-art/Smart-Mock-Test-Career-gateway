with open('My Project/smart-mock-test/frontend/js/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

old_check = """    const path = window.location.pathname.replace(/\\\\/g, "/").toLowerCase();
    if (path.includes("/admin/") && user.role !== "admin") {
      window.location.replace(API.getLoginUrl());
      return false;
    }"""

new_check = """    const path = window.location.pathname.replace(/\\\\/g, "/").toLowerCase();
    if (path.includes("/admin/")) {
      const token = localStorage.getItem("smt_auth_token");
      const adminEmail = "vartikachaudhary0312@gmail.com";
      if (!token || user.role !== "admin" || (user.email || "").toLowerCase() !== adminEmail) {
        window.location.replace(API.getLoginUrl());
        return false;
      }
    }"""

assert old_check in content_norm, "old_check not found"
content_norm = content_norm.replace(old_check, new_check)

with open('My Project/smart-mock-test/frontend/js/app.js', 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("app.js checkAuth patched")

