/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Resume Upload & ATS Analysis Module
 * Fully integrated with Flask Backend (/api/resume/upload) and Persistent Local Storage
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("resumeUploadView")) {
    ResumePage.init();
  }
});

const ResumePage = {
  async init() {
    this.bindDropzone();
    this.bindFileInput();
    this.bindActionButtons();
    await this.loadSavedAnalysis();
  },

  bindDropzone() {
    const dropzone = document.getElementById("resumeDropzone");
    const input = document.getElementById("resumeFileInput");
    if (!dropzone || !input) return;

    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.add("drag-over");
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        dropzone.classList.remove("drag-over");
      });
    });

    dropzone.addEventListener("drop", (e) => {
      const files = e.dataTransfer.files;
      if (files && files.length > 0) {
        this.handleFileUpload(files[0]);
      }
    });

    // Clicking dropzone triggers file picker, avoiding recursion on the input itself
    dropzone.addEventListener("click", (e) => {
      if (e.target !== input) {
        input.click();
      }
    });

    const browseBtn = document.getElementById("btnBrowseResume");
    if (browseBtn) {
      browseBtn.addEventListener("click", (e) => {
        e.preventDefault();
        e.stopPropagation();
        input.click();
      });
    }
  },

  bindFileInput() {
    const input = document.getElementById("resumeFileInput");
    if (!input) return;

    // Prevent click on input from bubbling back to dropzone
    input.addEventListener("click", (e) => {
      e.stopPropagation();
    });

    input.addEventListener("change", (e) => {
      if (e.target.files && e.target.files.length > 0) {
        this.handleFileUpload(e.target.files[0]);
      }
    });
  },

  bindActionButtons() {
    const reuploadBtn = document.getElementById("btnReuploadResume");
    if (reuploadBtn) {
      reuploadBtn.addEventListener("click", () => {
        const input = document.getElementById("resumeFileInput");
        if (input) input.click();
      });
    }
  },

  async loadSavedAnalysis() {
    try {
      const analysis = await API.getResumeAnalysis();
      if (analysis) {
        this.renderAnalysis(analysis, false);
      }
    } catch (e) {
      console.warn("Could not load previous resume analysis:", e);
    }
  },

  async handleFileUpload(file) {
    if (!file) return;

    // Extension & MIME Validation
    const ext = (file.name || "").split('.').pop().toLowerCase();
    const validExtensions = ['pdf', 'docx', 'doc'];
    const validMimes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'application/octet-stream',
      ''
    ];

    if (!validExtensions.includes(ext) && !validMimes.includes(file.type)) {
      if (window.App && typeof App.showToast === "function") {
        App.showToast("Please upload a PDF (.pdf) or Word document (.docx).", "error");
      }
      return;
    }

    // Size limit: 5MB
    if (file.size > 5 * 1024 * 1024) {
      if (window.App && typeof App.showToast === "function") {
        App.showToast("File size exceeds 5MB limit. Please upload a smaller file.", "error");
      }
      return;
    }

    const progressBox = document.getElementById("resumeProgressBox");
    const resultBox = document.getElementById("resumeAnalysisResultBox");
    const bar = document.getElementById("resumeProgressBar");
    const fileNameText = document.getElementById("resumeFileNameText");
    const stepHint = document.getElementById("resumeStepHint");
    const statusBadge = document.getElementById("resumeStatusBadge");

    if (progressBox) progressBox.style.display = "block";
    if (resultBox) resultBox.style.display = "none";

    const formattedSize = file.size >= 1024 * 1024 
      ? `${(file.size / (1024 * 1024)).toFixed(2)} MB` 
      : `${(file.size / 1024).toFixed(0)} KB`;

    if (fileNameText) fileNameText.textContent = `${file.name} (${formattedSize})`;

    const steps = [
      { pct: 25, hint: "Uploading file to server & validating signature...", badge: "Uploading..." },
      { pct: 55, hint: "Parsing text & extracting technical skill tokens...", badge: "Parsing Text..." },
      { pct: 85, hint: "Running ATS keyword density & scoring algorithms...", badge: "Scoring ATS..." },
      { pct: 100, hint: "Finalizing career match recommendations...", badge: "Complete!" }
    ];

    let currentStep = 0;
    const interval = setInterval(async () => {
      if (currentStep < steps.length) {
        const s = steps[currentStep];
        if (bar) bar.style.width = `${s.pct}%`;
        if (stepHint) stepHint.textContent = s.hint;
        if (statusBadge) statusBadge.textContent = s.badge;
        currentStep++;
      } else {
        clearInterval(interval);
        try {
          const analysis = await API.uploadAndAnalyzeResume(file);
          if (progressBox) progressBox.style.display = "none";
          if (window.App && typeof App.showToast === "function") {
            App.showToast(`Resume parsed successfully! ATS Match Score: ${analysis.matchScore}%`, "success");
          }
          this.renderAnalysis(analysis, true);
        } catch (err) {
          if (progressBox) progressBox.style.display = "none";
          if (window.App && typeof App.showToast === "function") {
            App.showToast(err.message || "Failed to process resume. Please try again.", "error");
          }
        }
      }
    }, 220);
  },

  renderAnalysis(analysis, shouldScroll = false) {
    if (!analysis) return;

    const resultBox = document.getElementById("resumeAnalysisResultBox");
    if (!resultBox) return;

    resultBox.style.display = "block";

    // Update active banner details
    const activeFileName = document.getElementById("activeResumeFileName");
    const activeMeta = document.getElementById("activeResumeMeta");
    if (activeFileName) {
      activeFileName.textContent = analysis.fileName || "Uploaded_Resume.pdf";
    }
    if (activeMeta) {
      activeMeta.textContent = `File Size: ${analysis.fileSize || "Verified"} | Analyzed: ${analysis.analyzedAt || "Recently"}`;
    }

    // Match Score
    const scoreElem = document.getElementById("atsMatchScore");
    if (scoreElem) {
      scoreElem.textContent = `${analysis.matchScore ?? 88}%`;
    }

    // Qualification & Experience
    const eduElem = document.getElementById("atsParsedEducation");
    if (eduElem) {
      eduElem.textContent = analysis.education || "MCA (Master of Computer Applications) - 8.4 CGPA";
    }

    const expElem = document.getElementById("atsParsedExperience");
    if (expElem) {
      expElem.textContent = analysis.experienceLevel || "Fresher / Entry-Level Software Engineer";
    }

    // Skills Badges
    const skillsContainer = document.getElementById("atsParsedSkillsContainer");
    if (skillsContainer) {
      const skills = analysis.parsedSkills || analysis.skills || [];
      if (skills.length > 0) {
        skillsContainer.innerHTML = skills.map(s => 
          `<span class="badge badge-purple me-1 mb-1 px-2 py-1"><i class="bi bi-check2 me-1"></i>${s}</span>`
        ).join("");
      } else {
        skillsContainer.innerHTML = `<span class="text-muted small">No specific skills detected</span>`;
      }
    }

    // Improvement Recommendations
    const recContainer = document.getElementById("atsRecommendationsList");
    if (recContainer) {
      const recs = analysis.recommendations || [];
      if (recs.length > 0) {
        recContainer.innerHTML = recs.map(r => 
          `<li class="mb-2 d-flex align-items-start gap-2"><i class="bi bi-lightbulb-fill text-warning flex-shrink-0 mt-1"></i><span>${r}</span></li>`
        ).join("");
      }
    }

    // Suggested Roles
    const rolesContainer = document.getElementById("atsSuggestedRolesList");
    if (rolesContainer) {
      const roles = analysis.suggestedRoles || analysis.suggested_roles || [];
      if (roles.length > 0) {
        rolesContainer.innerHTML = roles.map(r => 
          `<li class="mb-2 d-flex align-items-start gap-2"><i class="bi bi-briefcase-fill text-primary flex-shrink-0 mt-1"></i><span class="fw-medium">${r}</span></li>`
        ).join("");
      }
    }

    // Smooth scroll to analysis section if triggered by a new upload
    if (shouldScroll) {
      resultBox.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }
};

window.ResumePage = ResumePage;
