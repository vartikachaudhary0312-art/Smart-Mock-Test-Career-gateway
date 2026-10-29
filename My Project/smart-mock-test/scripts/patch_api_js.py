with open('My Project/smart-mock-test/frontend/js/api.js', 'r', encoding='utf-8') as f:
    content = f.read()

content_norm = content.replace('\r\n', '\n')

old_login_block = """  // --- AUTHENTICATION SERVICES ---
  async login(email, password, role = "student") {
    try {
      const resp = await fetch(`${this.backendBaseUrl}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, role })
      });
      if (resp.ok) {
        const json = await resp.json();
        if (json.data && json.data.token) {
          localStorage.setItem("smt_auth_token", json.data.token);
        }
        if (json.data && json.data.user) {
          localStorage.setItem("smt_current_user", JSON.stringify(json.data.user));
          return { success: true, user: json.data.user };
        }
      }
    } catch (e) {
      // Backend unavailable; seamless fallback to local mock store
    }

    await new Promise(res => setTimeout(res, 200));
    const users = JSON.parse(localStorage.getItem("smt_users") || "[]");
    const user = users.find(u => u.email.toLowerCase() === email.toLowerCase() && u.password === password);

    if (!user) {
      throw new Error("Invalid email or password.");
    }
    if (role && user.role !== role) {
      throw new Error(`Access denied. Registered account is a ${user.role}, not an ${role}.`);
    }

    const sessionUser = { id: user.id, name: user.name, email: user.email, role: user.role };
    localStorage.setItem("smt_current_user", JSON.stringify(sessionUser));
    return { success: true, user: sessionUser };
  },"""

new_login_block = """  // --- AUTHENTICATION SERVICES ---
  async login(email, password, role = "student") {
    let resp;
    try {
      resp = await fetch(`${this.backendBaseUrl}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password, role })
      });
    } catch (networkErr) {
      if (role === "admin") {
        throw new Error("Admin authentication requires an active connection to the backend server. Please verify Flask is running on port 5000.");
      }
      throw new Error("Unable to reach the backend authentication service. Please ensure the backend server is running.");
    }

    if (resp.ok) {
      const json = await resp.json();
      if (json.data && json.data.token) {
        localStorage.setItem("smt_auth_token", json.data.token);
      }
      if (json.data && json.data.user) {
        localStorage.setItem("smt_current_user", JSON.stringify(json.data.user));
        return { success: true, user: json.data.user };
      }
      return { success: true };
    } else {
      const errJson = await resp.json().catch(() => ({}));
      throw new Error(errJson.message || "Invalid email or password.");
    }
  },"""

old_register_block = """  async register(userData) {
    try {
      const resp = await fetch(`${this.backendBaseUrl}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData)
      });
      if (resp.ok) {
        const json = await resp.json();
        if (json.data && json.data.token) {
          localStorage.setItem("smt_auth_token", json.data.token);
        }
        if (json.data && json.data.user) {
          localStorage.setItem("smt_current_user", JSON.stringify(json.data.user));

          // Also sync to local smt_users for offline resilience
          const users = JSON.parse(localStorage.getItem("smt_users") || "[]");
          const idx = users.findIndex(u => u.email.toLowerCase() === json.data.user.email.toLowerCase());
          const fullUser = { ...userData, ...json.data.user };
          if (idx !== -1) users[idx] = fullUser;
          else users.push(fullUser);
          localStorage.setItem("smt_users", JSON.stringify(users));

          return { success: true, user: json.data.user };
        }
      } else {
        const errJson = await resp.json().catch(() => ({}));
        if (errJson.message) {
          throw new Error(errJson.message);
        }
      }
    } catch (e) {
      if (e.message && !e.message.includes("Failed to fetch") && !e.message.includes("NetworkError")) {
        throw e;
      }
      // Backend unavailable; seamless fallback to local mock store
    }

    await new Promise(res => setTimeout(res, 300));
    const users = JSON.parse(localStorage.getItem("smt_users") || "[]");

    if (users.some(u => u.email.toLowerCase() === userData.email.toLowerCase())) {
      throw new Error("An account with this email address already exists.");
    }

    const newUser = {
      id: "usr_" + Date.now(),
      ...userData,
      registeredAt: new Date().toISOString().split("T")[0]
    };

    users.push(newUser);
    localStorage.setItem("smt_users", JSON.stringify(users));

    const sessionUser = { id: newUser.id, name: newUser.name, email: newUser.email, role: newUser.role || "student" };
    localStorage.setItem("smt_current_user", JSON.stringify(sessionUser));
    return { success: true, user: sessionUser };
  },"""

new_register_block = """  async register(userData) {
    let resp;
    try {
      resp = await fetch(`${this.backendBaseUrl}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData)
      });
    } catch (networkErr) {
      throw new Error("Unable to connect to the backend registration service. Please verify the backend is running on port 5000.");
    }

    if (resp.ok) {
      const json = await resp.json();
      if (json.data && json.data.token) {
        localStorage.setItem("smt_auth_token", json.data.token);
      }
      if (json.data && json.data.user) {
        localStorage.setItem("smt_current_user", JSON.stringify(json.data.user));
        return { success: true, user: json.data.user };
      }
      return { success: true };
    } else {
      const errJson = await resp.json().catch(() => ({}));
      throw new Error(errJson.message || "Registration failed.");
    }
  },"""

assert old_login_block in content_norm, "old_login_block not found"
content_norm = content_norm.replace(old_login_block, new_login_block)

assert old_register_block in content_norm, "old_register_block not found"
content_norm = content_norm.replace(old_register_block, new_register_block)

with open('My Project/smart-mock-test/frontend/js/api.js', 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("api.js successfully patched")

