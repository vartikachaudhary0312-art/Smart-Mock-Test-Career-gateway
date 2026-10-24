/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Form Validation Utility Engine
 */

const Validation = {
  isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  },

  isValidPhone(phone) {
    const re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/;
    return re.test(String(phone).trim());
  },

  validateForm(formElement) {
    let isValid = true;
    const inputs = formElement.querySelectorAll("[data-validate]");

    inputs.forEach(input => {
      this.clearFieldError(input);
      const rules = input.getAttribute("data-validate").split("|");
      const val = input.value.trim();

      for (let rule of rules) {
        if (rule === "required" && !val) {
          this.showFieldError(input, "This field is required.");
          isValid = false;
          break;
        }
        if (rule === "email" && val && !this.isValidEmail(val)) {
          this.showFieldError(input, "Please enter a valid email address.");
          isValid = false;
          break;
        }
        if (rule === "phone" && val && !this.isValidPhone(val)) {
          this.showFieldError(input, "Please enter a valid phone number.");
          isValid = false;
          break;
        }
        if (rule.startsWith("min:")) {
          const minLen = parseInt(rule.split(":")[1]);
          if (val && val.length < minLen) {
            this.showFieldError(input, `Must be at least ${minLen} characters.`);
            isValid = false;
            break;
          }
        }
        if (rule.startsWith("match:")) {
          const targetId = rule.split(":")[1];
          const targetInput = document.getElementById(targetId);
          if (targetInput && val !== targetInput.value.trim()) {
            this.showFieldError(input, "Passwords do not match.");
            isValid = false;
            break;
          }
        }
      }
    });

    return isValid;
  },

  showFieldError(inputElem, errorMsg) {
    inputElem.classList.add("is-invalid");
    let feedback = inputElem.parentElement.querySelector(".invalid-feedback");
    if (!feedback) {
      feedback = document.createElement("div");
      feedback.className = "invalid-feedback d-block text-danger small mt-1";
      inputElem.parentElement.appendChild(feedback);
    }
    feedback.textContent = errorMsg;
  },

  clearFieldError(inputElem) {
    inputElem.classList.remove("is-invalid");
    const feedback = inputElem.parentElement.querySelector(".invalid-feedback");
    if (feedback) feedback.remove();
  }
};
