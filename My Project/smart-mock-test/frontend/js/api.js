/**
 * SMART MOCK TEST & CAREER GATEWAY
 * API Abstraction Layer (Stage 1 Mock Data Provider)
 * 
 * FUTURE FLASK BACKEND INTEGRATION NOTE:
 * To integrate with Flask REST APIs in Stage 2, replace the localStorage operations inside
 * these async functions with standard `fetch('http://localhost:5000/api/...', { ... })` calls.
 * Keep all function signatures identical to ensure 100% frontend compatibility!
 */

const API = {
  backendBaseUrl: "http://127.0.0.1:5000",

  // --- AUTHENTICATION SERVICES ---
  async login(email, password, role = "student") {
    // Simulated REST API call delay
    await new Promise(res => setTimeout(res, 300));
    
    const users = JSON.parse(localStorage.getItem("smt_users") || "[]");
    const user = users.find(u => u.email.toLowerCase() === email.toLowerCase() && u.password === password);

    if (!user) {
      throw new Error("Invalid email or password.");
    }
    if (role && user.role !== role) {
      throw new Error(`Access denied. Registered account is a ${user.role}, not an ${role}.`);
    }

    // Save session
    const sessionUser = { id: user.id, name: user.name, email: user.email, role: user.role };
    localStorage.setItem("smt_current_user", JSON.stringify(sessionUser));
    return { success: true, user: sessionUser };
  },

  async register(userData) {
    await new Promise(res => setTimeout(res, 400));
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

    // Auto login
    const sessionUser = { id: newUser.id, name: newUser.name, email: newUser.email, role: newUser.role };
    localStorage.setItem("smt_current_user", JSON.stringify(sessionUser));
    return { success: true, user: sessionUser };
  },

  getCurrentUser() {
    const data = localStorage.getItem("smt_current_user");
    return data ? JSON.parse(data) : null;
  },

  logout() {
    localStorage.removeItem("smt_current_user");
    window.location.href = "../login.html";
  },

  // --- SUBJECTS SERVICES ---
  async getSubjects() {
    await new Promise(res => setTimeout(res, 150));
    return JSON.parse(localStorage.getItem("smt_subjects") || "[]");
  },

  async addSubject(subjectData) {
    await new Promise(res => setTimeout(res, 200));
    const subjects = JSON.parse(localStorage.getItem("smt_subjects") || "[]");
    const newSubject = { id: "sub_" + Date.now(), ...subjectData, questionCount: 0 };
    subjects.push(newSubject);
    localStorage.setItem("smt_subjects", JSON.stringify(subjects));
    return newSubject;
  },

  // --- QUESTIONS & MOCK TEST SERVICES ---
  async getQuestions(subjectId, difficulty) {
    await new Promise(res => setTimeout(res, 200));
    const allQuestions = JSON.parse(localStorage.getItem("smt_questions") || "[]");
    return allQuestions.filter(q => {
      const matchSubject = !subjectId || q.subjectId === subjectId;
      const matchDiff = !difficulty || q.difficulty.toLowerCase() === difficulty.toLowerCase();
      return matchSubject && matchDiff;
    });
  },

  async addQuestion(qData) {
    await new Promise(res => setTimeout(res, 250));
    const questions = JSON.parse(localStorage.getItem("smt_questions") || "[]");
    const newQuestion = { id: "q_" + Date.now(), ...qData };
    questions.push(newQuestion);
    localStorage.setItem("smt_questions", JSON.stringify(questions));

    // Update subject question count
    const subjects = JSON.parse(localStorage.getItem("smt_subjects") || "[]");
    const sub = subjects.find(s => s.id === qData.subjectId);
    if (sub) {
      sub.questionCount = (sub.questionCount || 0) + 1;
      localStorage.setItem("smt_subjects", JSON.stringify(subjects));
    }

    return newQuestion;
  },

  async submitTestResult(resultPayload) {
    await new Promise(res => setTimeout(res, 400));
    const results = JSON.parse(localStorage.getItem("smt_results") || "[]");
    const newResult = {
      id: "res_" + Date.now(),
      ...resultPayload,
      completedAt: new Date().toLocaleString()
    };
    results.unshift(newResult);
    localStorage.setItem("smt_results", JSON.stringify(results));
    localStorage.setItem("smt_latest_result", JSON.stringify(newResult));
    return newResult;
  },

  async getLatestResult() {
    const data = localStorage.getItem("smt_latest_result");
    return data ? JSON.parse(data) : null;
  },

  async getUserResults(userId) {
    await new Promise(res => setTimeout(res, 200));
    const results = JSON.parse(localStorage.getItem("smt_results") || "[]");
    return results.filter(r => r.userId === userId);
  },

  async getAllResults() {
    await new Promise(res => setTimeout(res, 200));
    return JSON.parse(localStorage.getItem("smt_results") || "[]");
  },

  // --- CAREER GATEWAY & JOBS SERVICES ---
  async getJobs(filters = {}) {
    await new Promise(res => setTimeout(res, 200));
    let jobs = JSON.parse(localStorage.getItem("smt_jobs") || "[]");
    if (filters.search) {
      const q = filters.search.toLowerCase();
      jobs = jobs.filter(j => 
        j.title.toLowerCase().includes(q) || 
        j.company.toLowerCase().includes(q) ||
        j.skillsRequired.some(s => s.toLowerCase().includes(q))
      );
    }
    if (filters.location) {
      jobs = jobs.filter(j => j.location.toLowerCase().includes(filters.location.toLowerCase()));
    }
    if (filters.type) {
      jobs = jobs.filter(j => j.type === filters.type);
    }
    return jobs;
  },

  async addJob(jobData) {
    await new Promise(res => setTimeout(res, 300));
    const jobs = JSON.parse(localStorage.getItem("smt_jobs") || "[]");
    const newJob = { id: "job_" + Date.now(), ...jobData, postedDate: new Date().toISOString().split("T")[0], status: "Active" };
    jobs.unshift(newJob);
    localStorage.setItem("smt_jobs", JSON.stringify(jobs));
    return newJob;
  },

  async applyJob(userId, jobId) {
    await new Promise(res => setTimeout(res, 300));
    const jobs = JSON.parse(localStorage.getItem("smt_jobs") || "[]");
    const job = jobs.find(j => j.id === jobId);
    if (!job) throw new Error("Job posting not found.");

    const apps = JSON.parse(localStorage.getItem("smt_applications") || "[]");
    const existing = apps.find(a => a.userId === userId && a.jobId === jobId);
    if (existing) {
      throw new Error("You have already submitted an application for this position.");
    }

    const newApp = {
      id: "app_" + Date.now(),
      userId,
      jobId,
      company: job.company,
      jobTitle: job.title,
      appliedDate: new Date().toISOString().split("T")[0],
      status: "Applied"
    };

    apps.unshift(newApp);
    localStorage.setItem("smt_applications", JSON.stringify(apps));
    return newApp;
  },

  async getUserApplications(userId) {
    await new Promise(res => setTimeout(res, 150));
    const apps = JSON.parse(localStorage.getItem("smt_applications") || "[]");
    return apps.filter(a => a.userId === userId);
  },

  async getAllApplications() {
    await new Promise(res => setTimeout(res, 200));
    return JSON.parse(localStorage.getItem("smt_applications") || "[]");
  },

  async updateApplicationStatus(appId, newStatus) {
    await new Promise(res => setTimeout(res, 250));
    const apps = JSON.parse(localStorage.getItem("smt_applications") || "[]");
    const app = apps.find(a => a.id === appId);
    if (app) {
      app.status = newStatus;
      localStorage.setItem("smt_applications", JSON.stringify(apps));
    }
    return app;
  },

  // --- RESUME MOCK PARSER ---
  async analyzeResume(fileName, fileSize) {
    await new Promise(res => setTimeout(res, 1200)); // Simulated AI parsing time
    return {
      fileName,
      fileSize: (fileSize / (1024 * 1024)).toFixed(2) + " MB",
      matchScore: 84,
      parsedSkills: ["Java", "Python", "SQL", "HTML5", "CSS3", "Git", "REST APIs"],
      education: "Master of Computer Applications (MCA) - 8.4 CGPA",
      experienceLevel: "Fresher / Entry Level",
      recommendations: [
        "Add practical deployment links (e.g. GitHub/Vercel) to your MCA project section.",
        "Highlight relational database design concepts & SQL join queries.",
        "Include unit testing frameworks (e.g. JUnit or PyTest)."
      ],
      suggestedRoles: [
        "Graduate Software Engineer Trainee",
        "Junior Python Backend Developer",
        "Frontend Web Specialist"
      ]
    };
  }
};
