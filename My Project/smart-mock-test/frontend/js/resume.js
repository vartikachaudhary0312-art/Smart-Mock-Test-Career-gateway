/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Resume Upload & AI Analysis Module
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("resumeUploadView")) {
    ResumePage.init();
  }
});

const ResumePage = {
  init() {
    this.bindDropzone();
    this.bindFileInput();
  },

  bindDropzone() {
    const dropzone = document.getElementById("resumeDropzone");
    if (!dropzone) return;

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add("drag-over");
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove("drag-over");
      });
    });

    dropzone.addEventListener("drop", (e) => {
      const files = e.dataTransfer.files;
      if (files.length > 0) {
        this.handleFileUpload(files[0]);
      }
    });

    dropzone.addEventListener("click", () => {
      document.getElementById("resumeFileInput").click();
    });
  },

  bindFileInput() {
    const input = document.getElementById("resumeFileInput");
    if (!input) return;

    input.addEventListener("change", (e) => {
      if (e.target.files.length > 0) {
        this.handleFileUpload(e.target.files[0]);
      }
    });
  },

  async handleFileUpload(file) {
    const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
      App.showToast("Please upload a PDF or DOCX file.", "error");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      App.showToast("File size exceeds 5MB limit.", "error");
      return;
    }

    const progressBox = document.getElementById("resumeProgressBox");
    const resultBox = document.getElementById("resumeAnalysisResultBox");
    const bar = document.getElementById("resumeProgressBar");
    const fileNameText = document.getElementById("resumeFileNameText");

    progressBox.style.display = "block";
    resultBox.style.display = "none";
    fileNameText.textContent = `${file.name} (${(file.size / 1024).toFixed(0)} KB)`;

    let pct = 0;
    const interval = setInterval(() => {
      pct += 20;
      bar.style.width = `${pct}%`;
      if (pct >= 100) {
        clearInterval(interval);
        setTimeout(async () => {
          progressBox.style.display = "none";
          App.showToast("Resume parsed and analyzed successfully!", "success");
          const analysis = await API.analyzeResume(file.name, file.size);
          this.renderAnalysis(analysis);
        }, 300);
      }
    }, 200);
  },

  renderAnalysis(analysis) {
    const resultBox = document.getElementById("resumeAnalysisResultBox");
    if (!resultBox) return;

    resultBox.style.display = "block";

    document.getElementById("atsMatchScore").textContent = `${analysis.matchScore}%`;
    document.getElementById("atsParsedEducation").textContent = analysis.education;
    document.getElementById("atsParsedExperience").textContent = analysis.experienceLevel;

    // Skills
    const skillsContainer = document.getElementById("atsParsedSkillsContainer");
    skillsContainer.innerHTML = analysis.parsedSkills.map(s => `<span class="badge badge-purple me-1 mb-1">${s}</span>`).join("");

    // Recommendations
    const recContainer = document.getElementById("atsRecommendationsList");
    recContainer.innerHTML = analysis.recommendations.map(r => `<li class="mb-2"><i class="bi bi-lightbulb-fill text-warning me-2"></i>${r}</li>`).join("");

    // Suggested Roles
    const rolesContainer = document.getElementById("atsSuggestedRolesList");
    rolesContainer.innerHTML = analysis.suggestedRoles.map(r => `<li class="mb-2"><i class="bi bi-briefcase-fill text-primary me-2"></i>${r}</li>`).join("");
  }
};
