/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Chart.js Integration & Analytics Visualization Manager
 */

const ChartManager = {
  instances: {},

  getThemeColors() {
    const isDark = document.documentElement.getAttribute("data-bs-theme") === "dark";
    return {
      textColor: isDark ? "#94A3B8" : "#64748B",
      gridColor: isDark ? "#334155" : "#E2E8F0",
      primary: "#6D4AFF",
      primaryLight: "rgba(109, 74, 255, 0.15)",
      success: "#16A34A",
      warning: "#F59E0B",
      danger: "#DC2626",
      info: "#0EA5E9"
    };
  },

  destroy(canvasId) {
    if (this.instances[canvasId]) {
      this.instances[canvasId].destroy();
      delete this.instances[canvasId];
    }
  },

  renderScoreTrendChart(canvasId, labels, dataPoints) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    this.destroy(canvasId);

    const colors = this.getThemeColors();
    const ctx = canvas.getContext("2d");

    this.instances[canvasId] = new Chart(ctx, {
      type: "line",
      data: {
        labels: labels,
        datasets: [{
          label: "Score Percentage (%)",
          data: dataPoints,
          borderColor: colors.primary,
          backgroundColor: colors.primaryLight,
          borderWidth: 3,
          fill: true,
          tension: 0.4,
          pointRadius: 5,
          pointBackgroundColor: colors.primary
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            padding: 12,
            backgroundColor: "#0F172A",
            titleFont: { size: 14, weight: 'bold' },
            bodyFont: { size: 13 }
          }
        },
        scales: {
          x: {
            grid: { color: colors.gridColor },
            ticks: { color: colors.textColor }
          },
          y: {
            min: 0,
            max: 100,
            grid: { color: colors.gridColor },
            ticks: { color: colors.textColor, callback: v => v + "%" }
          }
        }
      }
    });
  },

  renderSubjectPerformanceChart(canvasId, subjects, scores) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    this.destroy(canvasId);

    const colors = this.getThemeColors();
    const ctx = canvas.getContext("2d");

    this.instances[canvasId] = new Chart(ctx, {
      type: "bar",
      data: {
        labels: subjects,
        datasets: [{
          label: "Average Score (%)",
          data: scores,
          backgroundColor: colors.primary,
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { grid: { display: false }, ticks: { color: colors.textColor } },
          y: { min: 0, max: 100, grid: { color: colors.gridColor }, ticks: { color: colors.textColor } }
        }
      }
    });
  },

  renderResultBreakdownDoughnut(canvasId, correct, incorrect, skipped) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    this.destroy(canvasId);

    const colors = this.getThemeColors();
    const ctx = canvas.getContext("2d");

    this.instances[canvasId] = new Chart(ctx, {
      type: "doughnut",
      data: {
        labels: ["Correct", "Incorrect", "Skipped"],
        datasets: [{
          data: [correct, incorrect, skipped],
          backgroundColor: [colors.success, colors.danger, colors.warning],
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: "bottom", labels: { color: colors.textColor, font: { weight: "600" } } }
        },
        cutout: "70%"
      }
    });
  },

  updateTheme() {
    Object.keys(this.instances).forEach(id => {
      // Re-trigger render if needed
    });
  }
};

window.ChartManager = ChartManager;
