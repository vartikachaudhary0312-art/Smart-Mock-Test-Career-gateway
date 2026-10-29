with open('My Project/smart-mock-test/frontend/js/mock-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

old_users_block = """  users: [
    {
      id: "usr_student_01",
      name: "Rahul Sharma",
      email: "student@example.com",
      password: "Student@123",
      role: "student",
      phone: "+91 9876543210",
      location: "Bangalore, India",
      education: "MCA 4th Sem, ABC Institute of Technology",
      skills: ["Java", "Python", "SQL", "HTML/CSS", "Data Structures"],
      registeredAt: "2026-01-15"
    },
    {
      id: "usr_admin_01",
      name: "System Admin",
      email: "vartikachaudhary0312@gmail.com",
      password: "Vartika1234@",
      role: "admin",
      phone: "+91 9876543211",
      location: "New Delhi, India",
      registeredAt: "2025-11-01"
    }
  ],"""

new_users_block = """  users: [
    {
      id: "usr_student_01",
      name: "Rahul Sharma",
      email: "student@example.com",
      role: "student",
      phone: "+91 9876543210",
      location: "Bangalore, India",
      education: "MCA 4th Sem, ABC Institute of Technology",
      skills: ["Java", "Python", "SQL", "HTML/CSS", "Data Structures"],
      registeredAt: "2026-01-15"
    },
    {
      id: "usr_admin_01",
      name: "System Admin",
      email: "vartikachaudhary0312@gmail.com",
      role: "admin",
      phone: "+91 9876543211",
      location: "New Delhi, India",
      registeredAt: "2025-11-01"
    }
  ],"""

assert old_users_block in content_norm, "old_users_block not found"
content_norm = content_norm.replace(old_users_block, new_users_block)

old_local_init = """  if (!localStorage.getItem("smt_users")) {
    localStorage.setItem("smt_users", JSON.stringify(DEFAULT_MOCK_DATA.users));
  }"""

new_local_init = """  // User credentials are authenticated securely via backend only"""

assert old_local_init in content_norm, "old_local_init not found"
content_norm = content_norm.replace(old_local_init, new_local_init)

with open('My Project/smart-mock-test/frontend/js/mock-data.js', 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("mock-data.js patched successfully")

