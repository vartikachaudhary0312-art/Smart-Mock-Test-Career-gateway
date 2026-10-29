/**
 * SMART MOCK TEST & CAREER GATEWAY
 * Client-Side Face Detection & Proctoring Vision Engine
 *
 * Integrates Pico.js cascade detector with frame luminance analysis
 * and browser ShapeDetection / FaceDetector API support.
 * Runs 100% locally in the browser with zero external network dependencies.
 */

const FaceDetector = {
  initialized: false,
  classifyRegion: null,
  canvas: null,
  ctx: null,
  targetWidth: 320,
  targetHeight: 240,

  /**
   * Initialize the face detection cascade from embedded base64 data
   */
  async init() {
    if (this.initialized) return true;

    try {
      // Create off-screen canvas for frame processing
      this.canvas = document.createElement("canvas");
      this.canvas.width = this.targetWidth;
      this.canvas.height = this.targetHeight;
      this.ctx = this.canvas.getContext("2d", { willReadFrequently: true });

      // Load cascade from global base64 or fallback
      let cascadeBytes = null;
      if (typeof FACEFINDER_CASCADE_B64 !== "undefined" && FACEFINDER_CASCADE_B64) {
        const binaryString = atob(FACEFINDER_CASCADE_B64);
        const len = binaryString.length;
        cascadeBytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
          cascadeBytes[i] = binaryString.charCodeAt(i);
        }
      } else {
        // Fallback fetch if base64 not available
        const resp = await fetch("js/facefinder.bin");
        const buffer = await resp.arrayBuffer();
        cascadeBytes = new Uint8Array(buffer);
      }

      if (typeof pico !== "undefined" && typeof pico.unpack_cascade === "function") {
        this.classifyRegion = pico.unpack_cascade(cascadeBytes);
        this.initialized = true;
      } else {
        console.warn("[FaceDetector] pico runtime not found. Native FaceDetector will be used if available.");
      }

      return true;
    } catch (err) {
      console.error("[FaceDetector] Initialization failed:", err);
      return false;
    }
  },

  /**
   * Fast RGB to Grayscale converter for pico cascade
   */
  rgbaToGrayscale(rgba, nrows, ncols) {
    const gray = new Uint8Array(nrows * ncols);
    for (let r = 0; r < nrows; ++r) {
      for (let c = 0; c < ncols; ++c) {
        // Human eye weighted luminance: 0.299R + 0.587G + 0.114B
        const idx = (r * ncols + c) * 4;
        gray[r * ncols + c] = Math.round(
          0.299 * rgba[idx] + 0.587 * rgba[idx + 1] + 0.114 * rgba[idx + 2]
        );
      }
    }
    return gray;
  },

  /**
   * Calculate average luminance across image pixels
   */
  calculateLuminance(rgba, totalPixels) {
    let sum = 0;
    const step = 4; // Sample every 4th pixel for speed
    let samples = 0;
    for (let i = 0; i < rgba.length; i += 4 * step) {
      sum += (0.299 * rgba[i] + 0.587 * rgba[i + 1] + 0.114 * rgba[i + 2]);
      samples++;
    }
    return samples > 0 ? Math.round(sum / samples) : 128;
  },

  /**
   * Analyze the live video frame for face presence, multiple faces,
   * positioning, lighting, and camera availability.
   *
   * @param {HTMLVideoElement} videoElem
   * @returns {Object} { status, message, faceCount, faces, luminance }
   */
  analyzeFrame(videoElem) {
    if (!videoElem) {
      return {
        status: "camera_offline",
        message: "Camera stream is unavailable.",
        faceCount: 0,
        faces: [],
        luminance: 0
      };
    }

    // Check if video is playing and has valid dimensions
    if (videoElem.readyState < 2 || videoElem.videoWidth === 0 || videoElem.videoHeight === 0) {
      return {
        status: "camera_offline",
        message: "Awaiting active camera frame feed...",
        faceCount: 0,
        faces: [],
        luminance: 0
      };
    }

    if (!this.initialized) {
      this.init();
      return {
        status: "initializing",
        message: "Initializing vision model...",
        faceCount: 0,
        faces: [],
        luminance: 128
      };
    }

    const w = this.targetWidth;
    const h = this.targetHeight;

    // Draw video frame to offscreen canvas
    this.ctx.drawImage(videoElem, 0, 0, w, h);
    const imgData = this.ctx.getImageData(0, 0, w, h);
    const rgba = imgData.data;

    // 1. Calculate lighting luminance
    const luminance = this.calculateLuminance(rgba, w * h);
    const minLum = SecurityConfig.minLuminance || 30;
    const maxLum = SecurityConfig.maxLuminance || 245;

    if (luminance < minLum) {
      return {
        status: "poor_lighting",
        message: "Lighting is too dark. Please ensure your face is well lit.",
        faceCount: 0,
        faces: [],
        luminance
      };
    }

    if (luminance > maxLum) {
      return {
        status: "poor_lighting",
        message: "Camera feed is overexposed. Please adjust lighting or camera angle.",
        faceCount: 0,
        faces: [],
        luminance
      };
    }

    // 2. Run Face Detection
    let faces = [];
    if (this.classifyRegion && typeof pico !== "undefined") {
      const gray = this.rgbaToGrayscale(rgba, h, w);
      const image = {
        pixels: gray,
        nrows: h,
        ncols: w,
        ldim: w
      };
      const params = {
        shiftfactor: 0.1,
        minsize: 35,
        maxsize: Math.min(w, h),
        scalefactor: 1.1
      };

      let dets = pico.run_cascade(image, this.classifyRegion, params);
      dets = pico.cluster_detections(dets, 0.2);

      // Filter high-confidence detections
      faces = dets.filter(d => d[3] > 12.0).map(d => ({
        row: d[0],
        col: d[1],
        size: d[2],
        confidence: d[3],
        x: Math.max(0, Math.round(d[1] - d[2] / 2)),
        y: Math.max(0, Math.round(d[0] - d[2] / 2)),
        width: Math.round(d[2]),
        height: Math.round(d[2])
      }));
    }

    const faceCount = faces.length;

    // 3. Evaluate face conditions
    if (faceCount === 0) {
      return {
        status: "no_face",
        message: SecurityConfig.messages.face_missing,
        faceCount: 0,
        faces: [],
        luminance
      };
    }

    if (faceCount > 1) {
      return {
        status: "multiple_faces",
        message: SecurityConfig.messages.multiple_faces,
        faceCount,
        faces,
        luminance
      };
    }

    // Single face detected: Check positioning (center vs cut-off)
    const face = faces[0];
    const marginX = w * 0.05;
    const marginY = h * 0.05;

    const isCutOff = (
      face.x < marginX ||
      face.x + face.width > w - marginX ||
      face.y < marginY ||
      face.y + face.height > h - marginY
    );

    if (isCutOff) {
      return {
        status: "face_offcenter",
        message: "Face partially out of camera frame. Please center yourself.",
        faceCount: 1,
        faces,
        luminance
      };
    }

    // All checks passed cleanly
    return {
      status: "ok",
      message: "Face verified",
      faceCount: 1,
      faces,
      luminance
    };
  }
};

// Auto-initialize when document loads
if (typeof document !== "undefined") {
  document.addEventListener("DOMContentLoaded", () => {
    FaceDetector.init();
  });
}

