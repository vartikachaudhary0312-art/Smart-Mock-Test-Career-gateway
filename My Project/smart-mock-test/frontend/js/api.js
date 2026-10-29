/**
 * SMART MOCK TEST & CAREER GATEWAY
 * API Abstraction Layer
 * Fully Integrated with Flask REST Backend, Intelligent Fallback & Local Storage Backup
 */

const API = {
  backendBaseUrl: "http://127.0.0.1:5000",

  /**
   * Determine prioritized list of backend base URLs based on runtime origin and network environment.
   */
  getBackendCandidates() {
    if (typeof window !== "undefined" && window.location) {
      const loc = window.location;
      // If served directly from Flask on port 5000
      if (loc.port === "5000") {
        return [loc.origin];
      }
      if (loc.hostname === "localhost") {
        return ["http://localhost:5000", "http://127.0.0.1:5000"];
      }
      if (loc.hostname === "127.0.0.1") {
        return ["http://127.0.0.1:5000", "http://localhost:5000"];
      }
    }
    const candidates = [this.backendBaseUrl, "http://127.0.0.1:5000", "http://localhost:5000"];
    return candidates.filter((v, i, a) => a.indexOf(v) === i);
  },

  /**
   * Resilient HTTP request runner with dual-host retry (127.0.0.1 <-> localhost)
   * and automatic Bearer token injection.
   */
  async request(endpoint, options = {}) {
    const candidates = this.getBackendCandidates();
    const token = typeof localStorage !== "undefined" ? localStorage.getItem("smt_auth_token") : null;
    const defaultHeaders = {
      "Content-Type": "application/json"
    };
    if (token) {
      defaultHeaders["Authorization"] = `Bearer ${token}`;
    }

    const mergedOptions = {
      ...options,
      headers: {
        ...defaultHeaders,
        ...(options.headers || {})
      }
    };

    let lastError = null;
    const path = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;

    for (let i = 0; i < candidates.length; i++) {
      const base = candidates[i];
      const url = `${base}${path}`;
      try {
        const resp = await fetch(url, mergedOptions);
        // Successful network connection established
        this.backendBaseUrl = base;
        return resp;
      } catch (err) {
        lastError = err;
        // On connection failure (e.g. refused or IPv6 mismatch), try candidate
      }
    }

    throw lastError || new Error("Failed to connect to backend server.");
  },

  /**
   * Convenience wrapper that executes request and parses JSON or throws on HTTP error.
   */
  async requestJson(endpoint, options = {}) {
    const resp = await this.request(endpoint, options);
    const json = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      const msg = json.message || json.error || `HTTP ${resp.status} Request Failed`;
      const err = new Error(msg);
      err.status = resp.status;
      err.data = json;
      throw err;
    }
    return json;
  },

  // --- AUTHENTICATION SERVICES ---
  async login(email, password, role = "student") {
    let resp;
    try {
      resp = await this.request("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password, role })
      });
    } catch (networkErr) {
      if (role === "admin") {
        throw new Error("Admin authentication requires an active connection to the backend server. Please verify Flask is running on port 5000.");
      }
      throw new Error("Unable to reach the backend authentication service. Please ensure the backend server is running on port 5000.");
    }

    const json = await resp.json().catch(() => ({}));
    if (resp.ok) {
      if (json.data && json.data.token) {
        localStorage.setItem("smt_auth_token", json.data.token);
      }
      if (json.data && json.data.user) {
        localStorage.setItem("smt_current_user", JSON.stringify(json.data.user));
        return { success: true, user: json.data.user };
      }
      return { success: true };
    } else {
      throw new Error(json.message || "Invalid email or password.");
    }
  },

  getLoginUrl() {
    const pathname = window.location.pathname.replace(/\\/g, "/");
    if (pathname.includes("/admin/")) {
      return "../login.html";
    }
    const idx = pathname.lastIndexOf("/frontend/");
    if (idx !== -1) {
      return pathname.substring(0, idx + "/frontend/".length) + "login.html";
    }
    return "login.html";
  },

  async register(userData) {
    let resp;
    try {
      resp = await this.request("/api/auth/register", {
        method: "POST",
        body: JSON.stringify(userData)
      });
    } catch (networkErr) {
      throw new Error("Unable to connect to the backend registration service. Please verify the backend is running on port 5000.");
    }

    const json = await resp.json().catch(() => ({}));
    if (resp.ok) {
      if (json.data && json.data.token) {
        localStorage.setItem("smt_auth_token", json.data.token);
      }
      if (json.data && json.data.user) {
        localStorage.setItem("smt_current_user", JSON.stringify(json.data.user));
        return { success: true, user: json.data.user };
      }
      return { success: true };
    } else {
      throw new Error(json.message || "Registration failed.");
    }
  },

  getCurrentUser() {
    const data = localStorage.getItem("smt_current_user");
    return data ? JSON.parse(data) : null;
  },

  async logout() {
    try {
      const token = localStorage.getItem("smt_auth_token");
      if (token) {
        await this.request("/api/auth/logout", {
          method: "POST"
        }).catch(() => {});
      }
    } catch (e) {
      // Ignore backend network errors during logout
    } finally {
      localStorage.removeItem("smt_current_user");
      localStorage.removeItem("smt_auth_token");
      sessionStorage.clear();
      window.location.replace(this.getLoginUrl());
    }
  },

  // --- CATEGORIES & TOPICS SERVICES ---
  async getCategories() {
    try {
      const resp = await this.request("/api/subjects/categories");
      if (resp.ok) {
        const json = await resp.json();
        if (json.data && Array.isArray(json.data) && json.data.length > 0) {
          localStorage.setItem("smt_categories", JSON.stringify(json.data));
          return json.data;
        }
      }
    } catch (e) {
      // Backend unavailable; fallback
    }
    await new Promise(res => setTimeout(res, 30));
    const cached = localStorage.getItem("smt_categories");
    if (cached) {
      try {
        const parsed = JSON.parse(cached);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      } catch (err) {}
    }
    if (typeof DEFAULT_MOCK_DATA !== "undefined" && DEFAULT_MOCK_DATA.categories) {
      return DEFAULT_MOCK_DATA.categories;
    }
    return [];
  },

  async getCategoryById(catId) {
    try {
      const resp = await this.request(`/api/subjects/categories/${catId}`);
      if (resp.ok) {
        const json = await resp.json();
        if (json.data) return json.data;
      }
    } catch (e) {}

    const categories = await this.getCategories();
    const cId = String(catId || "").toLowerCase();
    const cat = categories.find(c => 
      String(c.id || "").toLowerCase() === cId || 
      String(c.slug || "").toLowerCase() === cId ||
      String(c.name || "").toLowerCase() === cId
    );
    if (!cat) return null;

    const subjects = await this.getSubjects();
    const catTopics = subjects.filter(s => s.category_id === cat.id || s.category === cat.name);
    return { ...cat, topics: catTopics };
  },

  async getSubjects(categoryId = null) {
    try {
      const url = categoryId 
        ? `/api/subjects?category_id=${encodeURIComponent(categoryId)}`
        : "/api/subjects";
      const resp = await this.request(url);
      if (resp.ok) {
        const json = await resp.json();
        if (json.data && Array.isArray(json.data) && json.data.length > 0) {
          if (!categoryId) {
            localStorage.setItem("smt_subjects", JSON.stringify(json.data));
          }
          return json.data;
        }
      }
    } catch (e) {
      // Backend unavailable; fallback
    }
    await new Promise(res => setTimeout(res, 30));
    const cached = localStorage.getItem("smt_subjects");
    let subjects = [];
    if (cached) {
      try {
        subjects = JSON.parse(cached);
      } catch (err) {}
    }
    if ((!subjects || subjects.length === 0) && typeof DEFAULT_MOCK_DATA !== "undefined") {
      subjects = DEFAULT_MOCK_DATA.subjects || [];
    }

    if (categoryId) {
      const cLower = String(categoryId).toLowerCase();
      return subjects.filter(s => 
        String(s.category_id || "").toLowerCase() === cLower || 
        String(s.category || "").toLowerCase() === cLower
      );
    }
    return subjects;
  },

  async getSubjectById(subjectId) {
    const subjects = await this.getSubjects();
    const sId = String(subjectId || "").toLowerCase();
    return subjects.find(s => 
      String(s.id || "").toLowerCase() === sId || 
      String(s.code || "").toLowerCase() === sId ||
      String(s.name || "").toLowerCase() === sId
    ) || null;
  },

  async addSubject(subjectData) {
    await new Promise(res => setTimeout(res, 200));
    const subjects = JSON.parse(localStorage.getItem("smt_subjects") || "[]");
    const newSubject = { id: "sub_" + Date.now(), ...subjectData, question_count: 0 };
    subjects.push(newSubject);
    localStorage.setItem("smt_subjects", JSON.stringify(subjects));
    return newSubject;
  },

  _getQuestionsStore() {
    let allQuestions = [];
    const cached = localStorage.getItem("smt_questions");
    if (cached) {
      try {
        allQuestions = JSON.parse(cached);
      } catch (e) {}
    }
    if (!Array.isArray(allQuestions) || allQuestions.length < 50) {
      if (typeof DEFAULT_MOCK_DATA !== "undefined" && Array.isArray(DEFAULT_MOCK_DATA.questions)) {
        allQuestions = DEFAULT_MOCK_DATA.questions;
        try {
          localStorage.setItem("smt_questions", JSON.stringify(allQuestions));
        } catch (e) {}
      }
    }
    return allQuestions || [];
  },

  // --- PRACTICE & TEST QUESTIONS SERVICES ---
  async getPracticeQuestions(subjectId, difficulty = null, length = null) {
    // Try backend practice route first
    try {
      const resp = await this.request(`/api/tests/${subjectId}/practice`, {
        method: "POST",
        body: JSON.stringify({ difficulty, length })
      });
      if (resp.ok) {
        const json = await resp.json();
        if (json.data && Array.isArray(json.data) && json.data.length > 0) {
          return json.data;
        }
      }
    } catch (e) {
      // Backend unavailable; fallback
    }

    await new Promise(res => setTimeout(res, 40));
    const allQuestions = this._getQuestionsStore();
    const sTarget = String(subjectId).trim().toLowerCase();

    let matched = allQuestions.filter(q => {
      const qSubId = String(q.subject_id || q.subjectId || "").trim().toLowerCase();
      const qSubName = String(q.subject || "").trim().toLowerCase();
      
      let matchSubject = (qSubId === sTarget || qSubName === sTarget);
      if (!matchSubject) {
        if ((sTarget === "sub_java" || sTarget === "java") && qSubName.includes("java") && !qSubName.includes("script")) matchSubject = true;
        else if ((sTarget === "sub_python" || sTarget === "python") && qSubName.includes("python")) matchSubject = true;
        else if ((sTarget === "sub_dsa" || sTarget === "dsa") && (qSubName.includes("data structure") || qSubName.includes("dsa"))) matchSubject = true;
        else if ((sTarget === "sub_dbms" || sTarget === "dbms") && (qSubName.includes("database") || qSubName.includes("dbms"))) matchSubject = true;
        else if ((sTarget === "sub_percentages" || sTarget === "percentages") && (qSubName.includes("percentage") || qSubName.includes("ratio"))) matchSubject = true;
      }

      let matchDiff = true;
      if (difficulty && difficulty.toLowerCase() !== "mixed" && difficulty.toLowerCase() !== "all") {
        matchDiff = String(q.difficulty || "").toLowerCase() === difficulty.toLowerCase();
      }
      return matchSubject && matchDiff;
    });

    if (matched.length === 0 && difficulty && difficulty.toLowerCase() !== "mixed") {
      // Fallback to all difficulty levels for this same topic
      matched = allQuestions.filter(q => {
        const qSubId = String(q.subject_id || q.subjectId || "").trim().toLowerCase();
        const qSubName = String(q.subject || "").trim().toLowerCase();
        return (qSubId === sTarget || qSubName === sTarget);
      });
    }

    if (length && typeof length === "number" && length > 0) {
      matched = matched.slice(0, length);
    }
    return matched;
  },

  async getQuestions(subjectId, difficulty) {
    // Try backend questions first
    try {
      const resp = await this.request("/api/admin/questions");
      if (resp.ok) {
        const json = await resp.json();
        if (json.data && Array.isArray(json.data) && json.data.length > 0) {
          return json.data;
        }
      }
    } catch (e) {}

    await new Promise(res => setTimeout(res, 40));
    const allQuestions = this._getQuestionsStore();
    const sTarget = String(subjectId).trim().toLowerCase();

    return allQuestions.filter(q => {
      let matchSubject = true;
      if (subjectId) {
        const qSubId = String(q.subject_id || q.subjectId || "").trim().toLowerCase();
        const qSubName = String(q.subject || "").trim().toLowerCase();
        
        matchSubject = (qSubId === sTarget || qSubName === sTarget);
        if (!matchSubject) {
          if ((sTarget === "sub_java" || sTarget === "java") && qSubName.includes("java") && !qSubName.includes("script")) matchSubject = true;
          else if ((sTarget === "sub_python" || sTarget === "python") && qSubName.includes("python")) matchSubject = true;
          else if ((sTarget === "sub_dsa" || sTarget === "dsa") && (qSubName.includes("data structure") || qSubName.includes("dsa"))) matchSubject = true;
          else if ((sTarget === "sub_dbms" || sTarget === "dbms") && (qSubName.includes("database") || qSubName.includes("dbms"))) matchSubject = true;
          else if ((sTarget === "sub_sql" || sTarget === "sql") && qSubName.includes("sql")) matchSubject = true;
          else if ((sTarget === "sub_percentages" || sTarget === "percentages") && (qSubName.includes("percentage") || qSubName.includes("ratio"))) matchSubject = true;
        }
      }

      let matchDiff = true;
      if (difficulty && difficulty.toLowerCase() !== "mixed" && difficulty.toLowerCase() !== "all") {
        matchDiff = String(q.difficulty || "").toLowerCase() === difficulty.toLowerCase();
      }

      return matchSubject && matchDiff;
    });
  },

  async savePracticeResult(practicePayload) {
    await new Promise(res => setTimeout(res, 100));
    const results = JSON.parse(localStorage.getItem("smt_practice_results") || "[]");
    const newRecord = {
      id: "prac_" + Date.now(),
      ...practicePayload,
      completedAt: new Date().toLocaleString()
    };
    results.unshift(newRecord);
    localStorage.setItem("smt_practice_results", JSON.stringify(results));
    return newRecord;
  },

  async getUserPracticeResults(userId) {
    await new Promise(res => setTimeout(res, 50));
    const results = JSON.parse(localStorage.getItem("smt_practice_results") || "[]");
    if (!userId) return results;
    return results.filter(r => r.userId === userId);
  },

  _normalizeResult(r) {
    if (!r) return null;
    const scorePct = r.scorePct !== undefined && !isNaN(Number(r.scorePct))
      ? Math.round(Number(r.scorePct))
      : (r.percentage !== undefined && !isNaN(Number(r.percentage))
          ? Math.round(Number(r.percentage))
          : (r.score !== undefined && !isNaN(Number(r.score)) ? Math.round(Number(r.score)) : 0));

    const subjectName = r.subjectName || r.subject || "General Computer Science";
    const completedAt = r.completedAt || r.created_at || new Date().toLocaleString();
    const correct = Number(r.correct ?? r.correct_answers ?? 0);
    const incorrect = Number(r.incorrect ?? r.wrong_answers ?? 0);
    const skipped = Number(r.skipped ?? r.skipped_answers ?? 0);
    const totalQuestions = Number(r.totalQuestions ?? r.total_questions ?? (correct + incorrect + skipped || 10));
    const timeSpentMinutes = r.timeSpentMinutes !== undefined 
      ? Number(r.timeSpentMinutes) 
      : (r.time_taken ? Math.max(1, Math.round(Number(r.time_taken) / 60)) : 15);

    return {
      ...r,
      id: r.id || ("res_" + Date.now()),
      userId: r.userId || r.user_id,
      user_id: r.user_id || r.userId,
      subjectName,
      subject: subjectName,
      difficulty: (r.difficulty || "medium").toLowerCase(),
      scorePct: isNaN(scorePct) ? 0 : scorePct,
      percentage: isNaN(scorePct) ? 0 : scorePct,
      correct: isNaN(correct) ? 0 : correct,
      correct_answers: isNaN(correct) ? 0 : correct,
      incorrect: isNaN(incorrect) ? 0 : incorrect,
      wrong_answers: isNaN(incorrect) ? 0 : incorrect,
      skipped: isNaN(skipped) ? 0 : skipped,
      skipped_answers: isNaN(skipped) ? 0 : skipped,
      totalQuestions: isNaN(totalQuestions) ? 10 : totalQuestions,
      total_questions: isNaN(totalQuestions) ? 10 : totalQuestions,
      timeSpentMinutes: isNaN(timeSpentMinutes) ? 15 : timeSpentMinutes,
      time_taken: r.time_taken || (timeSpentMinutes * 60),
      completedAt,
      created_at: completedAt,
      submission_reason: r.submission_reason || "manual",
      violations_count: Number(r.violations_count || 0)
    };
  },

  async submitTestResult(resultPayload) {
    await new Promise(res => setTimeout(res, 200));
    const results = JSON.parse(localStorage.getItem("smt_results") || "[]");
    const normalized = this._normalizeResult({
      id: "res_" + Date.now(),
      ...resultPayload,
      completedAt: new Date().toLocaleString()
    });
    results.unshift(normalized);
    localStorage.setItem("smt_results", JSON.stringify(results));
    localStorage.setItem("smt_latest_result", JSON.stringify(normalized));
    return normalized;
  },

  async getLatestResult() {
    const data = localStorage.getItem("smt_latest_result");
    if (data) {
      try {
        return this._normalizeResult(JSON.parse(data));
      } catch (e) {}
    }
    try {
      const results = await this.getUserResults();
      if (results && results.length > 0) {
        return results[0];
      }
    } catch (e) {}
    return null;
  },

  async getUserResults(userId) {
    try {
      const res = await this.requestJson("/api/results", { method: "GET" });
      if (res && res.data && Array.isArray(res.data)) {
        return res.data.map(r => this._normalizeResult(r));
      }
    } catch (e) {}

    await new Promise(res => setTimeout(res, 50));
    const results = JSON.parse(localStorage.getItem("smt_results") || "[]");
    const filtered = userId ? results.filter(r => String(r.userId || r.user_id) === String(userId)) : results;
    return filtered.map(r => this._normalizeResult(r));
  },

  async getAllResults() {
    try {
      const res = await this.requestJson("/api/admin/results", { method: "GET" });
      if (res && res.data && Array.isArray(res.data)) {
        return res.data.map(r => this._normalizeResult(r));
      }
    } catch (e) {}

    await new Promise(res => setTimeout(res, 50));
    const results = JSON.parse(localStorage.getItem("smt_results") || "[]");
    return results.map(r => this._normalizeResult(r));
  },

  // --- CAREER GATEWAY & JOBS SERVICES ---
  async getJobs(filters = {}) {
    let jobs = [];
    try {
      const params = new URLSearchParams();
      if (filters.search) params.append("skills", filters.search);
      if (filters.location) params.append("location", filters.location);
      if (filters.type) params.append("type", filters.type);
      const qs = params.toString() ? `?${params.toString()}` : "";
      const res = await this.requestJson(`/api/jobs${qs}`, { method: "GET" });
      if (res && res.data && Array.isArray(res.data) && res.data.length > 0) {
        jobs = res.data;
      }
    } catch (e) {}

    if (!jobs || jobs.length === 0) {
      await new Promise(res => setTimeout(res, 50));
      jobs = JSON.parse(localStorage.getItem("smt_jobs") || "[]");
    }

    jobs = jobs.map(j => {
      const skills = Array.isArray(j.skillsRequired)
        ? j.skillsRequired
        : (Array.isArray(j.skills) ? j.skills : (typeof j.skills === "string" ? j.skills.split(",").map(s => s.trim()) : ["Software Engineering"]));
      return {
        ...j,
        skillsRequired: skills,
        skills: skills,
        location: j.location || "Remote, India",
        salary: j.salary || "Competitive",
        status: j.status || "Active",
        type: j.type || j.job_type || "Full-Time",
        job_type: j.job_type || j.type || "Full-Time"
      };
    });

    if (filters.search) {
      const q = filters.search.toLowerCase();
      jobs = jobs.filter(j => 
        (j.title || "").toLowerCase().includes(q) || 
        (j.company || "").toLowerCase().includes(q) ||
        (j.skillsRequired && j.skillsRequired.some(s => s.toLowerCase().includes(q)))
      );
    }
    if (filters.location) {
      jobs = jobs.filter(j => j.location && j.location.toLowerCase().includes(filters.location.toLowerCase()));
    }
    if (filters.type) {
      jobs = jobs.filter(j => j.type === filters.type || j.job_type === filters.type);
    }
    return jobs;
  },

  async getJobById(jobId) {
    try {
      const res = await this.requestJson(`/api/jobs/${jobId}`, { method: "GET" });
      if (res && res.data) return res.data;
    } catch (e) {}

    const jobs = await this.getJobs();
    return jobs.find(j => String(j.id) === String(jobId)) || null;
  },

  async applyJob(userId, jobId) {
    try {
      const res = await this.requestJson(`/api/jobs/${jobId}/apply`, {
        method: "POST"
      });
      if (res && res.data) return res.data;
    } catch (e) {
      if (e.status === 400 || e.status === 409) throw e;
    }

    await new Promise(res => setTimeout(res, 250));
    const applications = JSON.parse(localStorage.getItem("smt_applications") || "[]");
    
    const existing = applications.find(a => a.userId === userId && a.jobId === jobId);
    if (existing) {
      throw new Error("You have already submitted an application for this position.");
    }

    const job = await this.getJobById(jobId);
    if (!job) throw new Error("Job opportunity not found.");

    const newApp = {
      id: "app_" + Date.now(),
      userId,
      jobId,
      jobTitle: job.title,
      company: job.company,
      location: job.location,
      status: "Submitted",
      statusClass: "badge-purple",
      appliedAt: new Date().toISOString().split("T")[0],
      timeline: [
        { label: "Applied", date: new Date().toISOString().split("T")[0], completed: true },
        { label: "Resume Screening", date: "Pending", completed: false },
        { label: "Technical Interview", date: "Pending", completed: false },
        { label: "HR Offer", date: "Pending", completed: false }
      ]
    };

    applications.unshift(newApp);
    localStorage.setItem("smt_applications", JSON.stringify(applications));
    return newApp;
  },

  async getUserApplications(userId) {
    try {
      const res = await this.requestJson("/api/applications", { method: "GET" });
      if (res && res.data) return res.data;
    } catch (e) {}

    await new Promise(res => setTimeout(res, 100));
    const apps = JSON.parse(localStorage.getItem("smt_applications") || "[]");
    return apps.filter(a => a.userId === userId);
  },

  // --- RESUME & PROFILE SERVICES ---
  async getStudentProfile(userId) {
    try {
      const res = await this.requestJson("/api/student/profile", { method: "GET" });
      if (res && res.data && res.data.profile) return res.data.profile;
    } catch (e) {}

    const users = JSON.parse(localStorage.getItem("smt_users") || "[]");
    return users.find(u => u.id === userId) || null;
  },

  async updateStudentProfile(userId, profileData) {
    try {
      const res = await this.requestJson("/api/student/profile", {
        method: "PUT",
        body: JSON.stringify(profileData)
      });
      if (res && res.data && res.data.profile) {
        const updated = res.data.profile;
        const current = this.getCurrentUser();
        if (current) {
          localStorage.setItem("smt_current_user", JSON.stringify({ ...current, ...updated }));
        }
        return updated;
      }
    } catch (e) {}

    const users = JSON.parse(localStorage.getItem("smt_users") || "[]");
    const idx = users.findIndex(u => u.id === userId);
    if (idx !== -1) {
      users[idx] = { ...users[idx], ...profileData };
      localStorage.setItem("smt_users", JSON.stringify(users));
      
      const current = this.getCurrentUser();
      if (current && current.id === userId) {
        localStorage.setItem("smt_current_user", JSON.stringify({ ...current, ...profileData }));
      }
      return users[idx];
    }
    throw new Error("User profile not found.");
  },

  // --- RESUME ANALYSIS SERVICES ---
  _normalizeResumeAnalysis(data, fallbackName = "Resume.pdf", fallbackSize = "150 KB") {
    if (!data) return null;
    const skills = data.parsedSkills || data.skills || [
      "Python", "Java", "Data Structures & Algorithms", "SQL", "Flask",
      "HTML5", "CSS3", "JavaScript", "REST APIs", "Git", "Problem Solving"
    ];

    let educationStr = "MCA (Master of Computer Applications) - 8.4 CGPA";
    if (typeof data.education === "string" && data.education.trim()) {
      educationStr = data.education;
    } else if (Array.isArray(data.education_details) && data.education_details.length > 0) {
      const e0 = data.education_details[0];
      educationStr = `${e0.degree || "MCA"} (${e0.performance || "8.4 CGPA"})`;
    } else if (Array.isArray(data.education) && data.education.length > 0) {
      const e0 = data.education[0];
      educationStr = typeof e0 === "string" ? e0 : `${e0.degree || "MCA"} (${e0.performance || "8.4 CGPA"})`;
    }

    let experienceStr = "Fresher / Entry-Level Software Engineer";
    if (typeof data.experienceLevel === "string" && data.experienceLevel.trim()) {
      experienceStr = data.experienceLevel;
    } else if (Array.isArray(data.experience) && data.experience.length > 0) {
      const x0 = data.experience[0];
      experienceStr = typeof x0 === "string" ? x0 : (x0.role || "Software Project Intern");
    }

    const normalized = {
      fileName: data.fileName || data.file_name || fallbackName,
      file_name: data.fileName || data.file_name || fallbackName,
      fileSize: data.fileSize || data.file_size || fallbackSize,
      file_size: data.fileSize || data.file_size || fallbackSize,
      matchScore: data.matchScore ?? data.match_score ?? 88,
      match_score: data.matchScore ?? data.match_score ?? 88,
      education: educationStr,
      experienceLevel: experienceStr,
      parsedSkills: skills,
      skills: skills,
      recommendations: data.recommendations || [
        "Highlight database normalization and complex SQL join query performance.",
        "Include live deployed URL links or GitHub repository URLs for MCA capstone projects.",
        "Mention unit testing frameworks like PyTest or JUnit to boost ATS compatibility score above 90%."
      ],
      suggestedRoles: data.suggestedRoles || data.suggested_roles || [
        "Graduate Software Engineer Trainee (TCS, Infosys, Wipro)",
        "Junior Full-Stack Python / Web Developer",
        "Associate Backend Engineer (FastAPI / Flask)"
      ],
      suggested_roles: data.suggestedRoles || data.suggested_roles || [
        "Graduate Software Engineer Trainee (TCS, Infosys, Wipro)",
        "Junior Full-Stack Python / Web Developer",
        "Associate Backend Engineer (FastAPI / Flask)"
      ],
      analyzedAt: data.analyzedAt || data.analyzed_at || new Date().toLocaleString()
    };

    try {
      localStorage.setItem("smt_resume_analysis", JSON.stringify(normalized));
      localStorage.setItem("smt_uploaded_resume", normalized.fileName);
    } catch (e) {}

    return normalized;
  },

  async uploadAndAnalyzeResume(file) {
    if (file && typeof file === "object" && file.name) {
      try {
        const candidates = this.getBackendCandidates();
        const token = localStorage.getItem("smt_auth_token");
        const formData = new FormData();
        formData.append("file", file);

        for (let i = 0; i < candidates.length; i++) {
          const base = candidates[i];
          try {
            const resp = await fetch(`${base}/api/resume/upload`, {
              method: "POST",
              headers: token ? { "Authorization": `Bearer ${token}` } : {},
              body: formData
            });
            if (resp.ok) {
              const json = await resp.json();
              if (json.data) {
                this.backendBaseUrl = base;
                return this._normalizeResumeAnalysis(json.data, file.name, `${(file.size / 1024).toFixed(0)} KB`);
              }
            }
          } catch (netErr) {
            // try next candidate
          }
        }
      } catch (err) {
        console.warn("Backend resume upload failed, falling back to simulated ATS parser:", err);
      }
    }

    const fileName = file ? (file.name || String(file)) : "Resume.pdf";
    const fileSize = file && file.size ? file.size : 102400;
    return this.analyzeResume(fileName, fileSize);
  },

  async analyzeResume(fileName = "Resume.pdf", fileSize = 102400) {
    await new Promise(res => setTimeout(res, 200));

    const currentUser = this.getCurrentUser() || {};
    const userEdu = currentUser.education || "Master of Computer Applications (MCA)";
    const formattedSize = typeof fileSize === "number" ? `${(fileSize / 1024).toFixed(0)} KB` : String(fileSize);

    const fallbackData = {
      fileName: fileName,
      file_name: fileName,
      fileSize: formattedSize,
      file_size: formattedSize,
      matchScore: 88,
      match_score: 88,
      education: userEdu.includes("MCA") || userEdu.includes("Master")
        ? "MCA (Master of Computer Applications) - 8.4 CGPA"
        : `${userEdu} - Final Year`,
      experienceLevel: "Fresher / Entry-Level Software Engineer",
      parsedSkills: [
        "Python", "Java", "Data Structures & Algorithms", "SQL", "Flask",
        "HTML5", "CSS3", "JavaScript", "REST APIs", "Git", "Problem Solving"
      ],
      skills: [
        "Python", "Java", "Data Structures & Algorithms", "SQL", "Flask",
        "HTML5", "CSS3", "JavaScript", "REST APIs", "Git", "Problem Solving"
      ],
      recommendations: [
        "Highlight database normalization and complex SQL join query performance.",
        "Include live deployed URL links or GitHub repository URLs for MCA capstone projects.",
        "Mention unit testing frameworks like PyTest or JUnit to boost ATS compatibility score above 90%."
      ],
      suggestedRoles: [
        "Graduate Software Engineer Trainee (TCS, Infosys, Wipro)",
        "Junior Full-Stack Python / Web Developer",
        "Associate Backend Engineer (FastAPI / Flask)"
      ],
      suggested_roles: [
        "Graduate Software Engineer Trainee (TCS, Infosys, Wipro)",
        "Junior Full-Stack Python / Web Developer",
        "Associate Backend Engineer (FastAPI / Flask)"
      ],
      analyzedAt: new Date().toLocaleString()
    };

    return this._normalizeResumeAnalysis(fallbackData, fileName, formattedSize);
  },

  async getResumeAnalysis() {
    try {
      const res = await this.requestJson("/api/resume/latest", { method: "GET" });
      if (res && res.data) {
        return this._normalizeResumeAnalysis(res.data);
      }
    } catch (e) {}

    const saved = localStorage.getItem("smt_resume_analysis");
    if (saved) {
      try {
        return JSON.parse(saved);
      } catch (e) {}
    }
    return null;
  },

  async deleteResume() {
    try {
      await this.requestJson("/api/resume", { method: "DELETE" });
    } catch (e) {}
    localStorage.removeItem("smt_resume_analysis");
    localStorage.removeItem("smt_uploaded_resume");
    return true;
  },

  // --- ADMIN PORTAL SERVICES (CONNECTED TO FLASK /api/admin/*) ---
  async getAdminDashboard() {
    const res = await this.requestJson("/api/admin/dashboard", { method: "GET" });
    return res.data;
  },

  async getAdminStudents() {
    const res = await this.requestJson("/api/admin/students", { method: "GET" });
    return res.data;
  },

  async getAdminStudentDetail(studentId) {
    const res = await this.requestJson(`/api/admin/students/${studentId}`, { method: "GET" });
    return res.data;
  },

  async updateStudentStatus(studentId, status) {
    const res = await this.requestJson(`/api/admin/students/${studentId}/status`, {
      method: "PUT",
      body: JSON.stringify({ status })
    });
    return res.data;
  },

  async getAdminQuestions() {
    const res = await this.requestJson("/api/admin/questions", { method: "GET" });
    return res.data;
  },

  async createAdminQuestion(questionData) {
    const res = await this.requestJson("/api/admin/questions", {
      method: "POST",
      body: JSON.stringify(questionData)
    });
    return res.data;
  },

  async updateAdminQuestion(questionId, questionData) {
    const res = await this.requestJson(`/api/admin/questions/${questionId}`, {
      method: "PUT",
      body: JSON.stringify(questionData)
    });
    return res.data;
  },

  async deleteAdminQuestion(questionId) {
    const res = await this.requestJson(`/api/admin/questions/${questionId}`, {
      method: "DELETE"
    });
    return res;
  },

  async getAdminResults() {
    const res = await this.requestJson("/api/admin/results", { method: "GET" });
    return res.data;
  },

  async getAdminJobs() {
    const res = await this.requestJson("/api/admin/jobs", { method: "GET" });
    return res.data;
  },

  async createAdminJob(jobData) {
    const res = await this.requestJson("/api/admin/jobs", {
      method: "POST",
      body: JSON.stringify(jobData)
    });
    return res.data;
  },

  async updateAdminJob(jobId, jobData) {
    const res = await this.requestJson(`/api/admin/jobs/${jobId}`, {
      method: "PUT",
      body: JSON.stringify(jobData)
    });
    return res.data;
  },

  async deleteAdminJob(jobId) {
    const res = await this.requestJson(`/api/admin/jobs/${jobId}`, {
      method: "DELETE"
    });
    return res;
  },

  async getAllApplications() {
    try {
      const res = await this.requestJson("/api/admin/applications", { method: "GET" });
      if (res && res.data) return res.data;
    } catch (e) {}
    return JSON.parse(localStorage.getItem("smt_applications") || "[]");
  },

  async updateApplicationStatus(appId, status) {
    try {
      const res = await this.requestJson(`/api/admin/applications/${appId}/status`, {
        method: "PUT",
        body: JSON.stringify({ status })
      });
      return res.data;
    } catch (e) {
      const apps = JSON.parse(localStorage.getItem("smt_applications") || "[]");
      const idx = apps.findIndex(a => String(a.id) === String(appId));
      if (idx !== -1) {
        apps[idx].status = status;
        localStorage.setItem("smt_applications", JSON.stringify(apps));
        return apps[idx];
      }
      throw e;
    }
  },

  async addJob(jobData) {
    try {
      return await this.createAdminJob(jobData);
    } catch (e) {
      const jobs = JSON.parse(localStorage.getItem("smt_jobs") || "[]");
      const newJob = { id: "job_" + Date.now(), ...jobData, status: "Active" };
      jobs.push(newJob);
      localStorage.setItem("smt_jobs", JSON.stringify(jobs));
      return newJob;
    }
  },

  async addQuestion(questionData) {
    try {
      return await this.createAdminQuestion(questionData);
    } catch (e) {
      const questions = this._getQuestionsStore();
      const newQ = { id: Date.now(), ...questionData };
      questions.push(newQ);
      localStorage.setItem("smt_questions", JSON.stringify(questions));
      return newQ;
    }
  }
};
