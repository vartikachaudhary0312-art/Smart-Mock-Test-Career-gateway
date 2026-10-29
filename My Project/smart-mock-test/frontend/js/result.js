/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Result & Performance Analytics Page Logic
 * Resilient rendering with full property normalization & NaN guards
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("resultPageView")) {
    ResultPage.init();
  }
});

const ResultPage = {
  async init() {
    const rawResult = await API.getLatestResult();
    if (!rawResult) {
      const container = document.getElementById("resultPageView");
      if (container) {
        container.innerHTML = `
          <div class="card-custom p-5 text-center">
            <i class="bi bi-journal-x fs-1 text-muted mb-3"></i>
            <h5>No Recent Test Result Found</h5>
            <p class="text-muted">Take a mock test to generate comprehensive performance analytics.</p>
            <a href="mock-test.html" class="btn btn-primary-custom">Start Mock Test</a>
          </div>
        `;
      }
      return;
    }

    const result = {
      ...rawResult,
      scorePct: Number(rawResult.scorePct ?? rawResult.percentage ?? rawResult.score ?? 0),
      subjectName: rawResult.subjectName || rawResult.subject || "General Computer Science",
      difficulty: (rawResult.difficulty || "medium").toLowerCase(),
      correct: Number(rawResult.correct ?? rawResult.correct_answers ?? 0),
      incorrect: Number(rawResult.incorrect ?? rawResult.wrong_answers ?? 0),
      skipped: Number(rawResult.skipped ?? rawResult.skipped_answers ?? 0),
      totalQuestions: Number(rawResult.totalQuestions ?? rawResult.total_questions ?? 10),
      timeSpentMinutes: rawResult.timeSpentMinutes !== undefined ? rawResult.timeSpentMinutes : (rawResult.time_taken ? Math.round(rawResult.time_taken / 60) : 15)
    };

    if (isNaN(result.scorePct)) result.scorePct = 0;

    this.renderHeaderSummary(result);
    this.renderCharts(result);
    this.renderPerformanceAnalysis(result);
    this.renderQuestionReview(result);
  },

  renderHeaderSummary(r) {
    const safeScore = isNaN(r.scorePct) ? 0 : r.scorePct;
    const scoreBadge = document.getElementById("resultScoreBadge");
    if (scoreBadge) {
      scoreBadge.style.setProperty("--score-pct", safeScore);
      const scoreNum = document.getElementById("resultScoreNumber");
      if (scoreNum) scoreNum.textContent = `${safeScore}%`;
    }

    const subEl = document.getElementById("resultSubjectName");
    const diffEl = document.getElementById("resultDifficultyBadge");
    const corrEl = document.getElementById("resultCorrectCount");
    const incorrEl = document.getElementById("resultIncorrectCount");
    const skipEl = document.getElementById("resultSkippedCount");
    const timeEl = document.getElementById("resultTimeSpent");

    if (subEl) subEl.textContent = r.subjectName;
    if (diffEl) diffEl.textContent = r.difficulty;
    if (corrEl) corrEl.textContent = r.correct;
    if (incorrEl) incorrEl.textContent = r.incorrect;
    if (skipEl) skipEl.textContent = r.skipped;
    if (timeEl) timeEl.textContent = `${r.timeSpentMinutes} mins`;

    // Render Proctoring & Integrity Summary
    const proctorContainer = document.getElementById("resultProctoringBadgeContainer");
    if (proctorContainer) {
      let badgeHtml = "";
      const reason = r.submission_reason || "manual";
      const violations = Number(r.violations_count || 0);

      if (reason.startsWith("security_auto_submit")) {
        badgeHtml += `<span class="badge bg-danger mb-1 me-1"><i class="bi bi-shield-x me-1"></i>Security Auto-Submitted</span>`;
      } else if (reason === "timer_expired") {
        badgeHtml += `<span class="badge bg-warning text-dark mb-1 me-1"><i class="bi bi-clock-history me-1"></i>Timer Expired</span>`;
      } else {
        badgeHtml += `<span class="badge bg-success mb-1 me-1"><i class="bi bi-check-circle me-1"></i>Verified Submission</span>`;
      }

      if (violations === 0) {
        badgeHtml += `<span class="badge bg-success-subtle text-success border border-success"><i class="bi bi-shield-check me-1"></i>Clean Record (0 Violations)</span>`;
      } else {
        badgeHtml += `<span class="badge bg-warning-subtle text-warning border border-warning"><i class="bi bi-exclamation-triangle me-1"></i>${violations} Security Events</span>`;
      }

      proctorContainer.innerHTML = badgeHtml;
    }
  },

  renderCharts(r) {
    if (!window.ChartManager) return;
    const safeScore = isNaN(r.scorePct) ? 0 : r.scorePct;
    ChartManager.renderResultBreakdownDoughnut("resultDoughnutChart", r.correct, r.incorrect, r.skipped);
    ChartManager.renderScoreTrendChart("resultHistoryTrendChart", ["Test 1", "Test 2", "Latest Test"], [65, 72, safeScore]);
  },

  renderPerformanceAnalysis(r) {
    const strongElem = document.getElementById("resultStrongAreasList");
    const weakElem = document.getElementById("resultWeakAreasList");
    const suggestionsElem = document.getElementById("resultSuggestionsList");

    if (!strongElem) return;

    const safeScore = isNaN(r.scorePct) ? 0 : r.scorePct;
    const totalQ = r.totalQuestions > 0 ? r.totalQuestions : 10;
    const accuracy = Math.round((r.correct / totalQ) * 100);

    if (safeScore >= 75) {
      strongElem.innerHTML = `
        <li class="mb-2"><i class="bi bi-check-circle-fill text-success me-2"></i>Strong conceptual mastery of ${r.subjectName}.</li>
        <li class="mb-2"><i class="bi bi-check-circle-fill text-success me-2"></i>Excellent accuracy rate (${accuracy}%).</li>
      `;
      if (weakElem) weakElem.innerHTML = `<li class="text-muted">Minor optimization needed in time allocation per question.</li>`;
      if (suggestionsElem) {
        suggestionsElem.innerHTML = `
          <li class="mb-2"><i class="bi bi-lightbulb-fill text-warning me-2"></i>Maintain your score by taking Hard difficulty tests.</li>
          <li class="mb-2"><i class="bi bi-lightbulb-fill text-warning me-2"></i>Apply for jobs matching ${r.subjectName} in Career Gateway!</li>
        `;
      }
    } else {
      strongElem.innerHTML = `<li class="mb-2"><i class="bi bi-check-circle-fill text-success me-2"></i>Good understanding of fundamental syntax and concepts.</li>`;
      if (weakElem) {
        weakElem.innerHTML = `
          <li class="mb-2"><i class="bi bi-x-circle-fill text-danger me-2"></i>Application-based problem solving under time pressure.</li>
          <li class="mb-2"><i class="bi bi-x-circle-fill text-danger me-2"></i>Advanced topics in ${r.subjectName}.</li>
        `;
      }
      if (suggestionsElem) {
        suggestionsElem.innerHTML = `
          <li class="mb-2"><i class="bi bi-lightbulb-fill text-warning me-2"></i>Revise core definitions and practice code trace exercises.</li>
          <li class="mb-2"><i class="bi bi-lightbulb-fill text-warning me-2"></i>Re-attempt ${r.subjectName} test on Medium difficulty.</li>
        `;
      }
    }
  },

  renderQuestionReview(r) {
    const container = document.getElementById("resultQuestionReviewContainer");
    if (!container || !r.detailedReview || !Array.isArray(r.detailedReview)) return;

    let html = "";
    const prefixes = ["A", "B", "C", "D"];

    r.detailedReview.forEach((item, idx) => {
      const isCorrect = item.status === "correct";
      const isSkipped = item.status === "skipped";

      let statusBadge = `<span class="badge badge-green"><i class="bi bi-check-lg me-1"></i>Correct</span>`;
      let itemClass = "is-correct";
      if (!isCorrect && !isSkipped) {
        statusBadge = `<span class="badge badge-danger"><i class="bi bi-x-lg me-1"></i>Incorrect</span>`;
        itemClass = "is-incorrect";
      } else if (isSkipped) {
        statusBadge = `<span class="badge badge-warning"><i class="bi bi-dash-lg me-1"></i>Skipped</span>`;
        itemClass = "is-skipped";
      }

      const qText = item.question_text || item.question || "Question text unavailable";
      const userText = item.userOpt !== null && item.userOpt !== undefined && item.options
        ? `${prefixes[item.userOpt]}: ${item.options[item.userOpt]}`
        : "Skipped";
      const correctText = item.correctIndex !== undefined && item.options
        ? `${prefixes[item.correctIndex]}: ${item.options[item.correctIndex]}`
        : "N/A";
      const explanation = item.explanation || "No explanation provided.";

      html += `
        <div class="question-review-item ${itemClass}">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <h6 class="fw-bold mb-0">Question ${idx + 1}</h6>
            ${statusBadge}
          </div>
          <p class="fw-semibold text-dark mb-3">${qText}</p>
          <div class="small mb-3">
            <div><strong>Your Answer:</strong> ${userText}</div>
            <div><strong>Correct Answer:</strong> ${correctText}</div>
          </div>
          <div class="bg-light p-2 rounded small border text-muted">
            <i class="bi bi-info-circle me-1"></i><strong>Explanation:</strong> ${explanation}
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }
};

window.ResultPage = ResultPage;
