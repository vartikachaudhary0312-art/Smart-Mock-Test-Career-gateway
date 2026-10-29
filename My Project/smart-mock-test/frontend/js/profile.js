/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Profile Management Page Logic
 * Dynamically populated from real authenticated user session and backend profile
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("profilePageView")) {
    ProfilePage.init();
  }
});

const ProfilePage = {
  async init() {
    const user = API.getCurrentUser();
    if (!user) {
      window.location.replace(API.getLoginUrl());
      return;
    }

    this.renderUserProfile(user);
    await this.fetchBackendProfile();
    this.bindSaveProfile();
  },

  renderUserProfile(user) {
    if (!user) return;

    const initials = (user.name || "Student").split(" ").map(n => n[0]).filter(Boolean).join("").substring(0, 2).toUpperCase() || "ST";

    // Bind Avatar & Card Headers
    const bigAvatar = document.getElementById("profileBigAvatar");
    const cardName = document.getElementById("profileCardName");
    const cardRole = document.getElementById("profileCardRole");
    const cardLoc = document.getElementById("profileCardLocation");

    if (bigAvatar) bigAvatar.textContent = initials;
    if (cardName) cardName.textContent = user.name || "Student";
    if (cardRole) cardRole.textContent = (user.role === "admin" ? "Administrator" : "Student Candidate");
    if (cardLoc) cardLoc.innerHTML = `<i class="bi bi-geo-alt me-1"></i>${user.location || "India"}`;

    // Bind Form Inputs
    const nameInput = document.getElementById("profileNameInput");
    const emailInput = document.getElementById("profileEmailInput");
    const phoneInput = document.getElementById("profilePhoneInput");
    const locInput = document.getElementById("profileLocationInput");
    const eduInput = document.getElementById("profileEducationInput");

    if (nameInput) nameInput.value = user.name || "";
    if (emailInput) emailInput.value = user.email || "";
    if (phoneInput) phoneInput.value = user.mobile || user.phone || "";
    if (locInput) locInput.value = user.location || "";
    if (eduInput) eduInput.value = user.education || "";
  },

  async fetchBackendProfile() {
    try {
      const token = localStorage.getItem("smt_auth_token");
      if (!token) return;

      const resp = await fetch(`${API.backendBaseUrl}/api/student/profile`, {
        headers: { "Authorization": `Bearer ${token}` }
      });
      if (resp.ok) {
        const json = await resp.json();
        if (json.data && json.data.profile) {
          const p = json.data.profile;
          const curr = API.getCurrentUser() || {};
          const merged = { ...curr, ...p };
          localStorage.setItem("smt_current_user", JSON.stringify(merged));
          this.renderUserProfile(merged);
        }
      }
    } catch (e) {
      // Offline fallback
    }
  },

  bindSaveProfile() {
    const form = document.getElementById("profileForm");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      
      const user = API.getCurrentUser();
      if (!user) {
        window.location.replace(API.getLoginUrl());
        return;
      }

      const updatedName = document.getElementById("profileNameInput").value.trim();
      const updatedPhone = document.getElementById("profilePhoneInput").value.trim();
      const updatedLoc = document.getElementById("profileLocationInput").value.trim();
      const updatedEdu = document.getElementById("profileEducationInput").value.trim();

      user.name = updatedName || user.name;
      user.mobile = updatedPhone;
      user.phone = updatedPhone;
      user.location = updatedLoc;
      user.education = updatedEdu;

      // Save locally
      localStorage.setItem("smt_current_user", JSON.stringify(user));
      const users = JSON.parse(localStorage.getItem("smt_users") || "[]");
      const idx = users.findIndex(u => String(u.id) === String(user.id) || u.email.toLowerCase() === user.email.toLowerCase());
      if (idx !== -1) {
        users[idx] = { ...users[idx], ...user };
        localStorage.setItem("smt_users", JSON.stringify(users));
      }

      // Sync with backend API
      try {
        const token = localStorage.getItem("smt_auth_token");
        if (token) {
          await fetch(`${API.backendBaseUrl}/api/student/profile`, {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
              name: user.name,
              mobile: user.mobile,
              location: user.location,
              education: user.education
            })
          });
        }
      } catch (err) {
        // Backend offline
      }

      this.renderUserProfile(user);
      App.initHeaderUser();
      App.showToast("Profile details updated successfully!", "success");
    });
  }
};
