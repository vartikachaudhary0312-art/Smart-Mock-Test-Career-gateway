import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'mock-test.html')

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings
content_norm = content.replace('\r\n', '\n')

old_block = """            <!-- Length Selection -->
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
            </div>"""

new_block = """            <!-- Length Selection -->
            <div class="mb-4">
              <label class="form-label fw-bold text-dark small mb-2"><i class="bi bi-123 me-1 text-primary"></i>Select Number of Questions:</label>
              <div class="length-options-grid" id="cfgLengthOptions">
                <div class="cfg-len-card selected" data-length="10">
                  <div class="cfg-len-value">10 Qs</div>
                  <div class="cfg-len-time text-muted">~15 Minutes</div>
                </div>
                <div class="cfg-len-card" data-length="20">
                  <div class="cfg-len-value">20 Qs</div>
                  <div class="cfg-len-time text-muted">~30 Minutes</div>
                </div>
                <div class="cfg-len-card" data-length="30">
                  <div class="cfg-len-value">30 Qs</div>
                  <div class="cfg-len-time text-muted">~45 Minutes</div>
                </div>
                <div class="cfg-len-card" data-length="50">
                  <div class="cfg-len-value">50 Qs</div>
                  <div class="cfg-len-time text-muted">~60 Minutes</div>
                </div>
                <div class="cfg-len-card" data-length="max">
                  <div class="cfg-len-value" id="cfgLenMaxLabel">All Available</div>
                  <div class="cfg-len-time text-muted">Full Bank</div>
                </div>
              </div>
            </div>

            <!-- Difficulty Selection -->
            <div class="mb-4">
              <label class="form-label fw-bold text-dark small mb-2"><i class="bi bi-speedometer2 me-1 text-primary"></i>Select Difficulty Level:</label>
              <div class="difficulty-options" id="cfgDifficultyOptions">
                <div class="difficulty-card" data-diff="Easy">
                  <div class="difficulty-card-header">
                    <span class="fw-bold text-success text-nowrap"><i class="bi bi-reception-1 me-1"></i>Easy</span>
                    <span class="badge badge-green small">Basic</span>
                  </div>
                  <p class="difficulty-card-desc mb-0">Core fundamentals & syntax MCQs.</p>
                </div>
                <div class="difficulty-card selected" data-diff="Medium">
                  <div class="difficulty-card-header">
                    <span class="fw-bold text-primary text-nowrap"><i class="bi bi-reception-3 me-1"></i>Medium</span>
                    <span class="badge badge-purple small">Recommended</span>
                  </div>
                  <p class="difficulty-card-desc mb-0">Problem solving & code tracing.</p>
                </div>
                <div class="difficulty-card" data-diff="Hard">
                  <div class="difficulty-card-header">
                    <span class="fw-bold text-danger text-nowrap"><i class="bi bi-reception-4 me-1"></i>Hard</span>
                    <span class="badge badge-danger small">Advanced</span>
                  </div>
                  <p class="difficulty-card-desc mb-0">Complex algorithms & edge cases.</p>
                </div>
                <div class="difficulty-card" data-diff="Mixed">
                  <div class="difficulty-card-header">
                    <span class="fw-bold text-info text-nowrap"><i class="bi bi-shuffle me-1"></i>Mixed</span>
                    <span class="badge bg-info-subtle text-info border border-info-subtle small">Adaptive</span>
                  </div>
                  <p class="difficulty-card-desc mb-0">Dynamic blend across all levels.</p>
                </div>
              </div>
            </div>"""

if old_block in content_norm:
    updated = content_norm.replace(old_block, new_block)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(updated)
    print("SUCCESS: mock-test.html updated with responsive cards structure!")
else:
    print("ERROR: old_block not found in mock-test.html")

