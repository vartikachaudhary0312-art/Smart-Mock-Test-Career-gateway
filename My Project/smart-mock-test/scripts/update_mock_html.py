"""
Updates frontend/mock-test.html Steps 1 & 2
"""
import os

def update():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, "frontend", "mock-test.html")

    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    s1_marker = "<!-- STEP 1: SUBJECT SELECTION -->"
    s3_marker = "<!-- STEP 3: CAMERA PROCTORING PERMISSION CHECK -->"

    idx1 = content.find(s1_marker)
    idx3 = content.find(s3_marker)

    replacement = """<!-- STEP 1: SUBJECT SELECTION -->
          <div class="test-step-view" id="testStep1">
            <div class="mb-3">
              <h4 class="fw-extrabold text-dark mb-1">Step 1: Select Subject Module</h4>
              <p class="text-muted small">Choose the technical subject you wish to attempt for your mock test assessment.</p>
            </div>

            <!-- Subject Search & Counter -->
            <div class="row g-3 align-items-center mb-3">
              <div class="col-md-7">
                <div class="input-group">
                  <span class="input-group-text bg-white border-end-0 text-muted"><i class="bi bi-search"></i></span>
                  <input type="text" class="form-control border-start-0 ps-0" id="mockSubjectSearch" placeholder="Search by subject name, code, or topic (e.g. Python, DSA, SQL, DBMS)...">
                </div>
              </div>
              <div class="col-md-5 text-md-end">
                <span class="badge bg-purple-subtle text-primary border border-primary-subtle px-3 py-2" id="subjectCountBadge">
                  <i class="bi bi-collection me-1"></i> Showing All Subjects
                </span>
              </div>
            </div>

            <!-- Category Filter Tabs -->
            <div class="d-flex gap-2 flex-wrap mb-4" id="mockCategoryTabs">
              <button class="btn btn-sm btn-primary-custom active" data-cat="all">All Modules</button>
              <button class="btn btn-sm btn-outline-custom" data-cat="cat_programming">Programming Languages</button>
              <button class="btn btn-sm btn-outline-custom" data-cat="cat_core_cs">Core Computer Science</button>
              <button class="btn btn-sm btn-outline-custom" data-cat="cat_web_dev">Web Development</button>
              <button class="btn btn-sm btn-outline-custom" data-cat="cat_db_net">Databases & Data</button>
              <button class="btn btn-sm btn-outline-custom" data-cat="cat_technical_mcqs">Emerging Tech & MCQs</button>
              <button class="btn btn-sm btn-outline-custom" data-cat="cat_quant">Quantitative & Aptitude</button>
              <button class="btn btn-sm btn-outline-custom" data-cat="cat_company">Placement Tests</button>
            </div>

            <div class="subject-grid mb-4" id="subjectGridContainer">
              <!-- Injected via JavaScript -->
            </div>

            <div class="d-flex justify-content-between align-items-center border-top pt-3">
              <div class="text-muted small" id="selectedSubjectFeedback">
                <i class="bi bi-info-circle me-1"></i> Select a subject module to proceed.
              </div>
              <button class="btn btn-primary-custom px-4" id="btnStep1Next" disabled>
                Configure Test <i class="bi bi-arrow-right ms-2"></i>
              </button>
            </div>
          </div>

          <!-- STEP 2: TEST CONFIGURATION -->
          <div class="test-step-view" id="testStep2" style="display: none;">
            <div class="mb-3">
              <h4 class="fw-extrabold text-dark mb-1">Step 2: Test Configuration</h4>
              <p class="text-muted small">Customize assessment length, difficulty complexity, and review proctoring requirements.</p>
            </div>

            <!-- Selected Subject Summary Banner -->
            <div class="card-custom p-3 mb-4 bg-surface-subtle border">
              <div class="d-flex align-items-center justify-content-between flex-wrap gap-2">
                <div class="d-flex align-items-center gap-3">
                  <div class="stat-icon-wrapper stat-icon-purple" id="cfgSubjectIconWrap">
                    <i class="bi bi-journal-code fs-4" id="cfgSubjectIcon"></i>
                  </div>
                  <div>
                    <h5 class="fw-bold mb-0 text-dark" id="cfgSubjectName">Select Subject</h5>
                    <div class="d-flex gap-1 mt-1">
                      <span class="badge badge-purple small" id="cfgSubjectCategory">Core Computer Science</span>
                      <span class="badge badge-secondary small ms-1" id="cfgSubjectCode">CS-01</span>
                    </div>
                  </div>
                </div>
                <div class="text-md-end">
                  <span class="text-muted small d-block">Available In Bank</span>
                  <span class="fw-bold fs-5 text-primary" id="cfgSubjectAvailableCount">100 Questions</span>
                </div>
              </div>
            </div>

            <!-- Length Selection -->
            <div class="mb-4">
              <label class="form-label fw-bold text-dark small mb-2"><i class="bi bi-123 me-1 text-primary"></i>Select Number of Questions:</label>
              <div class="row g-2" id="cfgLengthOptions">
                <div class="col-6 col-md">
                  <div class="p-3 border rounded text-center cursor-pointer cfg-len-card selected" data-length="10">
                    <div class="fw-bold fs-5">10 Qs</div>
                    <div class="text-muted x-small">~15 Minutes</div>
                  </div>
                </div>
                <div class="col-6 col-md">
                  <div class="p-3 border rounded text-center cursor-pointer cfg-len-card" data-length="20">
                    <div class="fw-bold fs-5">20 Qs</div>
                    <div class="text-muted x-small">~30 Minutes</div>
                  </div>
                </div>
                <div class="col-6 col-md">
                  <div class="p-3 border rounded text-center cursor-pointer cfg-len-card" data-length="30">
                    <div class="fw-bold fs-5">30 Qs</div>
                    <div class="text-muted x-small">~45 Minutes</div>
                  </div>
                </div>
                <div class="col-6 col-md">
                  <div class="p-3 border rounded text-center cursor-pointer cfg-len-card" data-length="50">
                    <div class="fw-bold fs-5">50 Qs</div>
                    <div class="text-muted x-small">~60 Minutes</div>
                  </div>
                </div>
                <div class="col-12 col-md">
                  <div class="p-3 border rounded text-center cursor-pointer cfg-len-card" data-length="max">
                    <div class="fw-bold fs-5" id="cfgLenMaxLabel">All Available</div>
                    <div class="text-muted x-small">Full Bank</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Difficulty Selection -->
            <div class="mb-4">
              <label class="form-label fw-bold text-dark small mb-2"><i class="bi bi-speedometer2 me-1 text-primary"></i>Select Difficulty Level:</label>
              <div class="row g-2 difficulty-options">
                <div class="col-md-3">
                  <div class="difficulty-card p-3 h-100" data-diff="Easy">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <span class="fw-bold text-success"><i class="bi bi-reception-1 me-1"></i>Easy</span>
                      <span class="badge badge-green small">Basic</span>
                    </div>
                    <p class="text-muted x-small mb-0">Core fundamentals & syntax MCQs.</p>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="difficulty-card selected p-3 h-100" data-diff="Medium">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <span class="fw-bold text-primary"><i class="bi bi-reception-3 me-1"></i>Medium</span>
                      <span class="badge badge-purple small">Recommended</span>
                    </div>
                    <p class="text-muted x-small mb-0">Problem solving & code tracing.</p>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="difficulty-card p-3 h-100" data-diff="Hard">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <span class="fw-bold text-danger"><i class="bi bi-reception-4 me-1"></i>Hard</span>
                      <span class="badge badge-danger small">Advanced</span>
                    </div>
                    <p class="text-muted x-small mb-0">Complex algorithms & edge cases.</p>
                  </div>
                </div>
                <div class="col-md-3">
                  <div class="difficulty-card p-3 h-100" data-diff="Mixed">
                    <div class="d-flex justify-content-between align-items-center mb-1">
                      <span class="fw-bold text-info"><i class="bi bi-shuffle me-1"></i>Mixed</span>
                      <span class="badge bg-info-subtle text-info border border-info-subtle small">Adaptive</span>
                    </div>
                    <p class="text-muted x-small mb-0">Dynamic blend across all levels.</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Dynamic Test Guidelines Box -->
            <div class="card-custom p-4 mb-4">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="fw-bold mb-0"><i class="bi bi-shield-check me-2 text-primary"></i>Examination Guidelines & Proctoring Policy</h6>
                <span class="badge bg-primary-subtle text-primary border border-primary-subtle px-3 py-1" id="cfgDurationBadge">
                  <i class="bi bi-clock-history me-1"></i> Duration: 15 Mins
                </span>
              </div>
              <ul class="text-muted small mb-0 pe-2">
                <li class="mb-2"><strong class="text-dark" id="cfgRuleTiming">Dynamic Duration: 15 minutes allocated for 10 questions.</strong></li>
                <li class="mb-2"><strong>Fullscreen Examination Mode:</strong> Assessment opens in locked fullscreen mode. Exiting fullscreen triggers a security violation.</li>
                <li class="mb-2"><strong>Webcam AI Proctoring:</strong> Face verification is active. Keep your face centered in the camera feed; multiple faces or camera disconnections trigger warnings.</li>
                <li class="mb-2"><strong>Integrity Lockdown:</strong> Copy, cut, paste, right-click context menu, and tab switching are blocked and logged. Exceeding 6 violations triggers auto-submission.</li>
                <li class="mb-0"><strong>Instant Solution Review:</strong> Comprehensive question explanations and score analytics are displayed upon final submission.</li>
              </ul>
            </div>

            <div class="d-flex justify-content-between border-top pt-3">
              <button class="btn btn-outline-custom" id="btnStep2Back"><i class="bi bi-arrow-left me-2"></i>Back</button>
              <button class="btn btn-primary-custom px-4" id="btnStep2Next">Proceed to Camera Check <i class="bi bi-arrow-right ms-2"></i></button>
            </div>
          </div>\n\n          """

    new_content = content[:idx1] + replacement + content[idx3:]
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated mock-test.html successfully!")

if __name__ == "__main__":
    update()
