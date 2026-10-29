/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Centralized Anti-Cheating & Examination Security Policy Configuration
 *
 * All thresholds, grace periods, and proctoring rules are configured here.
 */

const SecurityConfig = {
  // Grace periods (in seconds) to prevent false positives from brief lighting or movement
  faceMissingGraceSeconds: 5,        // Grace period before registering face-missing violation
  cameraDisconnectGraceSeconds: 5,   // Grace period before registering camera disconnect violation
  focusLossGraceSeconds: 1,          // Debounce/tolerance for brief window focus transitions
  multipleFacesGraceSeconds: 3,      // Grace period for multiple faces detected

  // Maximum allowed violations before automatic test submission
  maxFaceMissingViolations: 3,       // Max allowed face missing / out of frame violations
  maxMultipleFacesViolations: 2,     // Max allowed multiple faces violations
  maxTabSwitchViolations: 3,         // Max allowed tab switches / window blur
  maxFullscreenExitViolations: 2,    // Max allowed fullscreen exits
  maxClipboardViolations: 3,         // Max allowed copy/cut/paste attempts
  maxCameraDisconnectViolations: 2,  // Max allowed camera disconnections

  // Cumulative total violations threshold across all categories
  maxTotalViolations: 6,

  // Lighting luminance boundaries (0 to 255 grayscale average)
  minLuminance: 30,                  // Values below this indicate room is too dark
  maxLuminance: 245,                 // Values above this indicate camera is overexposed

  // Detection sampling frequency
  faceDetectionIntervalMs: 600,      // Face check interval in milliseconds

  // Feature Toggles
  enforceFullscreen: true,
  blockClipboard: true,
  blockContextMenu: true,
  monitorCamera: true,
  monitorTabSwitch: true,

  // Human-readable violation descriptions
  messages: {
    face_missing: "Face not detected. Please sit directly in front of the camera.",
    multiple_faces: "Multiple faces detected. Only the registered student is permitted.",
    poor_lighting: "Face not sufficiently visible due to poor lighting or camera angle.",
    camera_disconnect: "Camera stream stopped or disconnected. Reconnect camera to proceed.",
    tab_switch: "Tab switch or window minimized. You must stay inside the examination window.",
    fullscreen_exit: "Fullscreen mode was exited. Fullscreen is mandatory for this examination.",
    clipboard_attempt: "Copying, cutting, pasting, and text selection are restricted during the test."
  }
};

// Freeze configuration to prevent accidental modification
if (typeof Object.freeze === "function") {
  Object.freeze(SecurityConfig);
  Object.freeze(SecurityConfig.messages);
}

// Export for module/global environments
if (typeof module !== "undefined" && module.exports) {
  module.exports = SecurityConfig;
}

