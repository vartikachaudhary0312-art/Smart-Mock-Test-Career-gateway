/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Profile Management Page Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("profilePageView")) {
    ProfilePage.init();
  }
});

const ProfilePage = {
  init() {
    this.loadUserData();
    this.bindSaveProfile();
  },

  loadUserData() {
    const user = API.getCurrentUser();
    if (!user) return;

    document.getElementById("profileNameInput").value = user.name || "";
    document.getElementById("profileEmailInput").value = user.email || "";
    document.getElementById("profilePhoneInput").value = user.phone || "";
    document.getElementById("profileLocationInput").value = user.location || "";
    document.getElementById("profileEducationInput").value = user.education || "";

    const initials = (user.name || "S").split(" ").map(n => n[0]).join("").substring(0, 2).toUpperCase();
    document.getElementById("profileBigAvatar").textContent = initials;
  },

  bindSaveProfile() {
    const form = document.getElementById("profileForm");
    if (!form) return;

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      
      const user = API.getCurrentUser() || {};
      user.name = document.getElementById("profileNameInput").value.trim();
      user.phone = document.getElementById("profilePhoneInput").value.trim();
      user.location = document.getElementById("profileLocationInput").value.trim();
      user.education = document.getElementById("profileEducationInput").value.trim();

      localStorage.setItem("smt_current_user", JSON.stringify(user));
      App.showToast("Profile details updated successfully!", "success");
      App.initHeaderUser();
    });
  }
};
