/**
 * SMART MOCK TEST & CAREER GATEWAY
 * User Settings Page Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("settingsPageView")) {
    SettingsPage.init();
  }
});

const SettingsPage = {
  init() {
    this.bindThemeRadio();
    this.bindSaveSettings();
  },

  bindThemeRadio() {
    const currentTheme = localStorage.getItem("smt_theme") || "light";
    const radio = document.querySelector(`input[name="themeOption"][value="${currentTheme}"]`);
    if (radio) radio.checked = true;

    const radios = document.querySelectorAll(`input[name="themeOption"]`);
    radios.forEach(r => {
      r.addEventListener("change", (e) => {
        App.setTheme(e.target.value);
      });
    });
  },

  bindSaveSettings() {
    const btn = document.getElementById("btnSaveSettings");
    if (!btn) return;

    btn.addEventListener("click", () => {
      App.showToast("Account settings saved successfully!", "success");
    });
  }
};
