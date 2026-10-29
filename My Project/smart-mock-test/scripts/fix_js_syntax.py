import os

p = os.path.join("My Project", "smart-mock-test", "frontend", "js", "mock-test.js")
with open(p, "r", encoding="utf-8") as f:
    c = f.read()

target = """  goToNextQuestion() {
    if (this.currentIndex < this.questions.length - 1) {
      this.currentIndex++;
      this.renderCurrentQuestion();
      this.renderQuestionPalette();

      // Reset scroll position of question scroll body so student starts next question at top
      const scrollBody = document.getElementById("testQuestionScrollBody");
      if (scrollBody) {
        scrollBody.scrollTop = 0;
      }
    } else {
      this.showSubmitConfirmationModal();
    }
  }
  },

  goToPrevQuestion() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.renderCurrentQuestion();
      this.renderQuestionPalette();

      const testCard = document.querySelector(".test-question-card");
      if (testCard) {
        testCard.scrollIntoView({ behavior: "smooth", block: "start" });
      } else {
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    }
  },"""

replacement = """  goToNextQuestion() {
    if (this.currentIndex < this.questions.length - 1) {
      this.currentIndex++;
      this.renderCurrentQuestion();
      this.renderQuestionPalette();

      // Reset scroll position of question scroll body so student starts next question at top
      const scrollBody = document.getElementById("testQuestionScrollBody");
      if (scrollBody) {
        scrollBody.scrollTop = 0;
      }
    } else {
      this.showSubmitConfirmationModal();
    }
  },

  goToPrevQuestion() {
    if (this.currentIndex > 0) {
      this.currentIndex--;
      this.renderCurrentQuestion();
      this.renderQuestionPalette();

      const scrollBody = document.getElementById("testQuestionScrollBody");
      if (scrollBody) {
        scrollBody.scrollTop = 0;
      }
    }
  },"""

if target in c:
    c = c.replace(target, replacement, 1)
    with open(p, "w", encoding="utf-8") as f:
        f.write(c)
    print("SUCCESS")
else:
    print("TARGET NOT FOUND")

