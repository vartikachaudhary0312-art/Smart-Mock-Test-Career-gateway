/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Result & Performance Analytics Page Logic
 */

document.addEventListener("DOMContentLoaded", () => {
  if (document.getElementById("resultPageView")) {
    ResultPage.init();
  }
});

const ResultPage = {
  async init() {
    const result = await API.getLatestResult();
    if (!result) {
      document.getElementById("resultPageView").innerHTML = `
        <div class="card-custom p-5 text-center">
          <i class="bi bi-journal-x fs-1 text-muted mb-3"></i>
          <h5>No Recent Test Result Found</h5>
          <p class="text-muted">Take a mock test to generate comprehensive performance analytics.</p>
          <a href="mock-test.html" class="btn btn-primary-custom">Start Mock Test</a>
        </div>
      `;
      return;
    }

    this.renderHeaderSummary(result);
    this.renderCharts(result);
    this.renderPerformanceAnalysis(result);
    this.renderQuestionReview(result);
  },

  renderHeaderSummary(r) {
    const scoreBadge = document.getElementById("resultScoreBadge");
    if (scoreBadge) {
      scoreBadge.style.setProperty("--score-pct", r.scorePct);
      document.getElementById("resultScoreNumber").textContent = `${r.scorePct}%`;
    }

    document.getElementById("resultSubjectName").textContent = r.subjectName;
    document.getElementById("resultDifficultyBadge").textContent = r.difficulty;
    document.getElementById("resultCorrectCount").textContent = r.correct;
    document.getElementById("resultIncorrectCount").textContent = r.incorrect;
    document.getElementById("resultSkippedCount").textContent = r.skipped;
    document.getElementById("resultTimeSpent").textContent = `${r.timeSpentMinutes} mins`;
  },

  renderCharts(r) {
    ChartManager.renderResultBreakdownDoughnut("resultDoughnutChart", r.correct, r.incorrect, r.skipped);
    ChartManager.renderScoreTrendChart("resultHistoryTrendChart", ["Test 1", "Test 2", "Latest Test"], [65, 72, r.scorePct]);
  },

  renderPerformanceAnalysis(r) {
    const strongElem = document.getElementById("resultStrongAreasList");
    const weakElem = document.getElementById("resultWeakAreasList");
    const suggestionsElem = document.getElementById("resultSuggestionsList");

    if (!strongElem) return;

    if (r.scorePct >= 75) {
      strongElem.innerHTML = `
        <li class="mb-2"><i class="bi bi-check-circle-fill text-success me-2"></i>Strong conceptual mastery of ${r.subjectName}.</li>
        <li class="mb-2"><i class="bi bi-check-circle-fill text-success me-2"></i>Excellent accuracy rate (${Math.round((r.correct / r.totalQuestions) * 100)}%).</li>
      `;
      weakElem.innerHTML = `<li class="text-muted">Minor optimization needed in time allocation per question.</li>`;
      suggestionsElem.innerHTML = `
        <li class="mb-2"><i class="bi bi-lightbulb-fill text-warning me-2"></i>Maintain your score by taking Hard difficulty tests.</li>
        <li class="mb-2"><i class="bi bi-lightbulb-fill text-warning me-2"></i>Apply for jobs matching ${r.subjectName} in Career Gateway!</li>
      `;
    } else {
      strongElem.innerHTML = `<li class="mb-2"><i class="bi bi-check-circle-fill text-success me-2"></i>Good understanding of fundamental syntax and concepts.</li>`;
      weakElem.innerHTML = `
        <li class="mb-2"><i class="bi bi-x-circle-fill text-danger me-2"></i>Application-based problem solving under time pressure.</li>
        <li class="mb-2"><i class="bi bi-x-circle-fill text-danger me-2"></i>Advanced topics in ${r.subjectName}.</li>
      `;
      suggestionsElem.innerHTML = `
        <li class="mb-2"><i class="bi bi-lightbulb-fill text-warning me-2"></i>Revise core definitions and practice code trace exercises.</li>
        <li class="mb-2"><i class="bi bi-lightbulb-fill text-warning me-2"></i>Re-attempt ${r.subjectName} test on Medium difficulty.</li>
      `;
    }
  },

  renderQuestionReview(r) {
    const container = document.getElementById("resultQuestionReviewContainer");
    if (!container || !r.detailedReview) return;

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

      html += `
        <div class="question-review-item ${itemClass}">
          <div class="d-flex justify-content-between align-items-center mb-2">
            <h6 class="fw-bold mb-0">Question ${idx + 1}</h6>
            ${statusBadge}
          </div>
          <p class="fw-semibold text-dark mb-3">${item.question}</p>
          <div class="small mb-3">
            <div><strong>Your Answer:</strong> ${item.userOpt !== null ? prefixes[item.userOpt] + ": " + item.options[item.userOpt] : "Skipped"}</div>
            <div><strong>Correct Answer:</strong> ${prefixes[item.correctIndex]}: ${item.options[item.correctIndex]}</div>
          </div>
          <div class="bg-light p-2 rounded small border text-muted">
            <i class="bi bi-info-circle me-1"></i><strong>Explanation:</strong> ${item.explanation}
          </div>
        </div>
      `;
    });

    container.innerHTML = html;
  }
};
