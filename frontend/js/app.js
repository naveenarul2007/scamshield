/**
 * ScamShield - Real-Time Digital Scam Detection & Protection Platform
 * ALGOTHON'26 Full-Stack Application Logic
 */

// Application State
const state = {
  currentView: 'dashboard',
  selectedScreenshotFile: null,
  charts: {
    classificationChart: null,
    categoriesChart: null
  },
  cachedScans: [],
  cachedStats: null
};

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  initNavigation();
  initDashboard();
  initMessageScanner();
  initUrlScanner();
  initScreenshotScanner();
  initScanHistory();
  initReports();
  initDemoTour();
  checkBackendHealth();
});

// ==========================================
// 1. Navigation & View Routing
// ==========================================
function initNavigation() {
  const navLinks = document.querySelectorAll('[data-view-target]');
  navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetView = link.getAttribute('data-view-target');
      switchView(targetView);

      // Close mobile sidebar if open
      document.querySelector('.sidebar').classList.remove('mobile-open');
    });
  });

  // Mobile menu toggle
  const mobileBtn = document.getElementById('mobileMenuBtn');
  if (mobileBtn) {
    mobileBtn.addEventListener('click', () => {
      document.querySelector('.sidebar').classList.toggle('mobile-open');
    });
  }
}

function switchView(viewName) {
  state.currentView = viewName;

  // Update nav menu active states
  document.querySelectorAll('.nav-link').forEach(link => {
    if (link.getAttribute('data-view-target') === viewName) {
      link.classList.add('active');
    } else {
      link.classList.remove('active');
    }
  });

  // Switch view sections
  document.querySelectorAll('.view-section').forEach(sec => {
    sec.classList.remove('active-view');
  });

  const targetSection = document.getElementById(`view-${viewName}`);
  if (targetSection) {
    targetSection.classList.add('active-view');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // Refresh view data
  if (viewName === 'dashboard') {
    fetchStatsAndRefreshDashboard();
  } else if (viewName === 'history') {
    fetchAndRenderHistory();
  } else if (viewName === 'reports') {
    fetchAndRenderReports();
  }
}

// ==========================================
// 2. Health & Status
// ==========================================
async function checkBackendHealth() {
  try {
    const res = await fetch('/api/health');
    const data = await res.json();
    const statusMeta = document.getElementById('sidebarStatusMeta');
    if (statusMeta) {
      statusMeta.innerText = data.ocr_available 
        ? 'ML Engine & Native OCR Active' 
        : 'ML Active • Sample OCR Fallback';
    }
  } catch (err) {
    console.warn('Backend health check warning:', err);
  }
}

// ==========================================
// 3. Dashboard & Analytics
// ==========================================
function initDashboard() {
  fetchStatsAndRefreshDashboard();
}

async function fetchStatsAndRefreshDashboard() {
  try {
    const res = await fetch('/api/stats');
    if (!res.ok) throw new Error('Failed to load stats');
    const data = await res.json();
    state.cachedStats = data;

    // Update Counter values
    const a = data.analytics || {};
    document.getElementById('statTotalScans').innerText = a.total_scans ?? 0;
    document.getElementById('statSafeScans').innerText = a.safe_scans ?? 0;
    document.getElementById('statSuspiciousScans').innerText = a.suspicious_scans ?? 0;
    document.getElementById('statScamScans').innerText = a.scam_scans ?? 0;

    // Update ML model badge
    const model = data.model_info || {};
    const mlBadge = document.getElementById('mlModelBadge');
    if (mlBadge) {
      if (model.status === 'TRAINED') {
        mlBadge.innerHTML = `<strong>Active Model:</strong> ${model.model_type} (${model.accuracy}% Acc, ${model.f1_score}% F1)`;
      } else {
        mlBadge.innerHTML = `<strong>Active:</strong> Rule-based Explainable Engine`;
      }
    }

    // Render Charts
    renderClassificationChart(a);
    renderCategoryChart(a.top_reported_categories || []);

    // Load recent scans preview
    loadRecentScansPreview();
  } catch (err) {
    console.error('Error updating dashboard stats:', err);
  }
}

function renderClassificationChart(analytics) {
  const ctx = document.getElementById('chartClassification');
  if (!ctx) return;

  const safe = analytics.safe_scans || 0;
  const suspicious = analytics.suspicious_scans || 0;
  const scam = analytics.scam_scans || 0;
  const total = safe + suspicious + scam;

  const dataValues = total === 0 ? [1, 0, 0] : [safe, suspicious, scam];
  const labels = total === 0 ? ['No Scans Yet', '', ''] : ['Safe Content', 'Suspicious', 'Likely Scam'];

  if (state.charts.classificationChart) {
    state.charts.classificationChart.destroy();
  }

  state.charts.classificationChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: labels,
      datasets: [{
        data: dataValues,
        backgroundColor: total === 0 ? ['#E2E8F0', '#E2E8F0', '#E2E8F0'] : ['#059669', '#D97706', '#DC2626'],
        borderWidth: 2,
        borderColor: '#FFFFFF',
        hoverOffset: 4
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom',
          labels: { font: { family: "'Plus Jakarta Sans', sans-serif", size: 12 }, padding: 16 }
        }
      },
      cutout: '70%'
    }
  });
}

function renderCategoryChart(categories) {
  const ctx = document.getElementById('chartCategories');
  if (!ctx) return;

  const defaultCategories = [
    { category: 'Banking', count: 4 },
    { category: 'Prize/Lottery', count: 3 },
    { category: 'Phishing', count: 2 },
    { category: 'Job Scam', count: 2 },
    { category: 'OTP Theft', count: 1 }
  ];

  const activeCategories = (categories && categories.length > 0) ? categories : defaultCategories;
  const labels = activeCategories.map(c => c.category);
  const data = activeCategories.map(c => c.count);

  if (state.charts.categoriesChart) {
    state.charts.categoriesChart.destroy();
  }

  state.charts.categoriesChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Reports / Detections',
        data: data,
        backgroundColor: '#3B82F6',
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true,
          ticks: { stepSize: 1, font: { family: "'Plus Jakarta Sans', sans-serif" } },
          grid: { color: '#F1F5F9' }
        },
        x: {
          grid: { display: false },
          ticks: { font: { family: "'Plus Jakarta Sans', sans-serif", size: 11 } }
        }
      },
      plugins: {
        legend: { display: false }
      }
    }
  });
}

async function loadRecentScansPreview() {
  const tbody = document.getElementById('recentScansTableBody');
  if (!tbody) return;

  try {
    const res = await fetch('/api/scans?limit=5');
    const data = await res.json();
    const scans = data.scans || [];

    if (scans.length === 0) {
      tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; color: var(--text-muted); padding: 24px;">No scans recorded yet. Perform your first scan above!</td></tr>`;
      return;
    }

    tbody.innerHTML = scans.map(s => `
      <tr>
        <td style="font-size: 0.8rem; color: var(--text-muted);">${formatDate(s.created_at)}</td>
        <td><span class="badge-pill" style="background:#EFF6FF; color:#1D4ED8; font-size:0.75rem; font-weight:700; text-transform:uppercase;">${s.scan_type}</span></td>
        <td style="max-width: 280px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 0.85rem;" title="${escapeHtml(s.input_preview)}">${escapeHtml(s.input_preview)}</td>
        <td><strong>${s.risk_score}</strong> / 100</td>
        <td>${getRiskBadgeHtml(s.classification, s.risk_level)}</td>
      </tr>
    `).join('');
  } catch (err) {
    console.error('Error loading recent scans:', err);
  }
}

// ==========================================
// 4. Message Scanner
// ==========================================
function initMessageScanner() {
  const textarea = document.getElementById('messageInput');
  const countDisplay = document.getElementById('messageCharCount');
  const btnAnalyze = document.getElementById('btnAnalyzeMessage');
  const form = document.getElementById('messageScanForm');

  if (textarea && countDisplay) {
    textarea.addEventListener('input', () => {
      const chars = textarea.value.length;
      const words = textarea.value.trim() ? textarea.value.trim().split(/\s+/).length : 0;
      countDisplay.innerText = `${chars} characters (${words} words)`;
    });
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const message = textarea.value.trim();
      if (!message) {
        showToast('Please paste or type a message to analyze.', 'error');
        return;
      }

      setButtonLoading(btnAnalyze, true, 'Analyzing Message...');
      try {
        const res = await fetch('/api/analyze/message', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Analysis failed');

        renderScanResults('messageResultsPanel', data);
        showToast('Analysis completed successfully!', 'success');
        fetchStatsAndRefreshDashboard();
      } catch (err) {
        showToast(err.message, 'error');
      } finally {
        setButtonLoading(btnAnalyze, false, 'ANALYZE MESSAGE');
      }
    });
  }

  // Demo chips for message
  document.querySelectorAll('[data-fill-message]').forEach(btn => {
    btn.addEventListener('click', () => {
      const text = btn.getAttribute('data-fill-message');
      if (textarea) {
        textarea.value = text;
        textarea.dispatchEvent(new Event('input'));
        textarea.focus();
      }
    });
  });
}

// ==========================================
// 5. URL Scanner
// ==========================================
function initUrlScanner() {
  const input = document.getElementById('urlInput');
  const btnAnalyze = document.getElementById('btnAnalyzeUrl');
  const form = document.getElementById('urlScanForm');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const url = input.value.trim();
      if (!url) {
        showToast('Please enter a URL to scan.', 'error');
        return;
      }

      setButtonLoading(btnAnalyze, true, 'Scanning URL...');
      try {
        const res = await fetch('/api/analyze/url', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ url })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Scan failed');

        renderScanResults('urlResultsPanel', data, 'url');
        showToast('URL analysis completed!', 'success');
        fetchStatsAndRefreshDashboard();
      } catch (err) {
        showToast(err.message, 'error');
      } finally {
        setButtonLoading(btnAnalyze, false, 'SCAN URL');
      }
    });
  }

  // Demo chips for URL
  document.querySelectorAll('[data-fill-url]').forEach(btn => {
    btn.addEventListener('click', () => {
      const url = btn.getAttribute('data-fill-url');
      if (input) {
        input.value = url;
        input.focus();
      }
    });
  });
}

// ==========================================
// 6. Screenshot Scanner
// ==========================================
function initScreenshotScanner() {
  const dropzone = document.getElementById('screenshotDropzone');
  const fileInput = document.getElementById('screenshotFileInput');
  const previewContainer = document.getElementById('screenshotPreviewContainer');
  const previewImg = document.getElementById('screenshotPreviewImg');
  const previewFilename = document.getElementById('screenshotPreviewFilename');
  const previewSize = document.getElementById('screenshotPreviewSize');
  const btnRemove = document.getElementById('btnRemoveScreenshot');
  const btnAnalyze = document.getElementById('btnAnalyzeScreenshot');
  const form = document.getElementById('screenshotScanForm');

  if (fileInput) {
    fileInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleSelectedFile(e.target.files[0]);
      }
    });
  }

  if (dropzone) {
    ['dragenter', 'dragover'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropzone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
      });
    });

    dropzone.addEventListener('drop', (e) => {
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleSelectedFile(e.dataTransfer.files[0]);
      }
    });
  }

  function handleSelectedFile(file) {
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      showToast('Please upload a valid image (PNG, JPG, JPEG, WEBP).', 'error');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      showToast('File size exceeds 10MB limit.', 'error');
      return;
    }

    state.selectedScreenshotFile = file;
    state.selectedSampleName = null;

    if (previewFilename) previewFilename.innerText = file.name;
    if (previewSize) previewSize.innerText = `${(file.size / 1024).toFixed(1)} KB`;
    if (previewImg) {
      const reader = new FileReader();
      reader.onload = (e) => { previewImg.src = e.target.result; };
      reader.readAsDataURL(file);
    }

    if (previewContainer) previewContainer.style.display = 'flex';
  }

  if (btnRemove) {
    btnRemove.addEventListener('click', () => {
      state.selectedScreenshotFile = null;
      state.selectedSampleName = null;
      if (fileInput) fileInput.value = '';
      if (previewContainer) previewContainer.style.display = 'none';
    });
  }

  // Sample screenshot presets
  document.querySelectorAll('[data-sample-screenshot]').forEach(btn => {
    btn.addEventListener('click', () => {
      const sampleFile = btn.getAttribute('data-sample-screenshot');
      state.selectedSampleName = sampleFile;
      state.selectedScreenshotFile = null;

      if (previewFilename) previewFilename.innerText = `[Built-in Sample] ${sampleFile}`;
      if (previewSize) previewSize.innerText = 'High-Resolution Mock SMS';
      if (previewImg) previewImg.src = `/static/samples/${sampleFile}`;
      if (previewContainer) previewContainer.style.display = 'flex';
      showToast(`Loaded sample screenshot: ${sampleFile}`, 'info');
    });
  });

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      if (!state.selectedScreenshotFile && !state.selectedSampleName) {
        showToast('Please select a screenshot or click a sample preset.', 'error');
        return;
      }

      setButtonLoading(btnAnalyze, true, 'Running OCR & Analyzing...');

      try {
        let res;
        if (state.selectedSampleName) {
          // Analyze preset sample
          res = await fetch('/api/analyze/screenshot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sample_name: state.selectedSampleName })
          });
        } else {
          // Upload file
          const formData = new FormData();
          formData.append('screenshot', state.selectedScreenshotFile);
          res = await fetch('/api/analyze/screenshot', {
            method: 'POST',
            body: formData
          });
        }

        const data = await res.json();
        if (!res.ok) {
          if (data.ocr_available === false) {
            showOcrMissingModal(data.error);
            return;
          }
          throw new Error(data.error || 'Screenshot analysis failed');
        }

        renderScanResults('screenshotResultsPanel', data, 'screenshot');
        showToast('Screenshot text extracted and analyzed!', 'success');
        fetchStatsAndRefreshDashboard();
      } catch (err) {
        showToast(err.message, 'error');
      } finally {
        setButtonLoading(btnAnalyze, false, 'ANALYZE SCREENSHOT');
      }
    });
  }
}

function showOcrMissingModal(errorMessage) {
  const modal = document.getElementById('detailsModal');
  const title = document.getElementById('modalTitle');
  const body = document.getElementById('modalBody');

  if (modal && title && body) {
    title.innerText = 'Tesseract OCR Dependency Notice';
    body.innerHTML = `
      <div style="background:#FFFBEB; border:1px solid #FDE68A; color:#92400E; padding:16px; border-radius:8px; margin-bottom:16px;">
        <h4 style="margin-bottom:6px; font-weight:700;">OCR Engine Not Detected On Server</h4>
        <p style="font-size:0.9rem; line-height:1.5;">${escapeHtml(errorMessage)}</p>
      </div>
      <p style="font-size:0.88rem; color:var(--text-muted); margin-bottom:16px;">
        <strong>Hackathon Testing Shortcut:</strong> You can immediately test the screenshot pipeline using our 3 built-in sample screenshots (e.g. <em>SBI KYC Expiry SMS</em> or <em>KBC Prize Notification</em>) with 1 click above!
      </p>
      <button class="btn-primary" onclick="closeModal()" style="width:100%;">Got it, Continue</button>
    `;
    modal.classList.add('active');
  }
}

// ==========================================
// 7. Results Renderer (Explainable AI Engine)
// ==========================================
function renderScanResults(panelId, result, scanType = 'message') {
  const panel = document.getElementById(panelId);
  if (!panel) return;

  const score = result.risk_score || 0;
  const classification = result.classification || 'SAFE';
  const riskLevel = result.risk_level || 'LOW';
  const indicators = result.indicators || [];
  const factors = result.factors || [];
  const recommendation = result.recommendation || '';
  const extractedText = result.extracted_text || '';

  // Determine stroke color
  let strokeColor = '#059669';
  let badgeClass = 'badge-safe';
  if (score >= 60) {
    strokeColor = '#DC2626';
    badgeClass = 'badge-scam';
  } else if (score >= 30) {
    strokeColor = '#D97706';
    badgeClass = 'badge-suspicious';
  }

  // Calculate SVG stroke offset
  // Circumference = 2 * PI * r = 2 * 3.14159 * 36 ≈ 226.2
  const circumference = 226.2;
  const strokeOffset = circumference - (score / 100) * circumference;

  let ocrSectionHtml = '';
  if (extractedText) {
    ocrSectionHtml = `
      <div style="margin-bottom: 20px;">
        <div class="section-subhead">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path></svg>
          Extracted Text from Screenshot
        </div>
        <div class="ocr-text-box">${escapeHtml(extractedText)}</div>
      </div>
    `;
  }

  // Build Factors table
  let factorsTableHtml = '';
  if (factors.length > 0) {
    const rows = factors.map(f => `
      <tr>
        <td style="font-weight:600; color:var(--text-main);">${escapeHtml(f.factor)}</td>
        <td><span class="factor-badge ${f.points > 0 ? 'positive' : 'neutral'}">+${f.points}</span></td>
        <td style="color:var(--text-muted); font-size:0.82rem;">${escapeHtml(f.reason)}</td>
      </tr>
    `).join('');

    factorsTableHtml = `
      <div style="margin-bottom: 22px;">
        <div class="section-subhead">
          <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
          Explainable Risk Breakdown
        </div>
        <table class="factors-breakdown-table">
          <thead>
            <tr>
              <th>Risk Factor</th>
              <th>Weight</th>
              <th>Reason & Detection Detail</th>
            </tr>
          </thead>
          <tbody>
            ${rows}
          </tbody>
        </table>
      </div>
    `;
  }

  // Indicators HTML
  const indicatorsHtml = indicators.map(ind => `
    <div class="indicator-tag-item ${score >= 30 ? 'warning' : 'neutral'}">
      <span>${score >= 30 ? '⚠' : '✓'}</span>
      <span>${escapeHtml(ind)}</span>
    </div>
  `).join('');

  // ML Analysis info if available
  let mlInfoHtml = '';
  if (result.ml_analysis) {
    const ml = result.ml_analysis;
    const tokens = (ml.key_features || []).join(', ');
    mlInfoHtml = `
      <div style="font-size:0.78rem; background:#F8FAFC; border:1px solid #E2E8F0; padding:10px 14px; border-radius:8px; margin-bottom:18px; color:var(--text-muted);">
        <strong>ML Classifier Probability:</strong> ${(ml.ml_probability * 100).toFixed(1)}% | 
        <strong>Significant N-grams:</strong> <code>${tokens || 'None'}</code>
      </div>
    `;
  }

  panel.innerHTML = `
    <div class="score-hero-container">
      <div class="score-meter-wrap">
        <div class="circular-gauge">
          <svg viewBox="0 0 88 88">
            <circle class="gauge-bg" cx="44" cy="44" r="36" />
            <circle class="gauge-progress" cx="44" cy="44" r="36" 
              style="stroke-dasharray: ${circumference}; stroke-dashoffset: ${strokeOffset}; stroke: ${strokeColor};" />
          </svg>
          <div class="gauge-center-text">
            <div class="gauge-number">${score}</div>
            <div class="gauge-max">/100</div>
          </div>
        </div>
        <div>
          <div class="risk-classification-tag ${badgeClass}">${classification}</div>
          <div class="risk-level-sub">Risk Level: <strong>${riskLevel}</strong></div>
        </div>
      </div>
      <div>
        <button class="btn-tool" onclick="copyResultText(${score}, '${classification}', '${escapeQuotes(recommendation)}')">
          <svg width="15" height="15" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
          Copy Result
        </button>
      </div>
    </div>

    ${ocrSectionHtml}

    <div class="indicators-section">
      <div class="section-subhead">
        <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        Detected Warning Indicators
      </div>
      <div class="indicator-tags-wrap">
        ${indicatorsHtml}
      </div>
    </div>

    ${factorsTableHtml}
    ${mlInfoHtml}

    <div class="action-box">
      <div class="action-box-title">
        <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        Recommended Security Action
      </div>
      <p>${escapeHtml(recommendation)}</p>
    </div>

    <div class="result-toolbar">
      <button class="btn-tool" onclick="switchView('reports')">
        <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>
        Report to Community
      </button>
      <button class="btn-tool" onclick="switchView('history')">
        <svg width="14" height="14" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
        View in History
      </button>
    </div>
  `;

  panel.style.display = 'block';
  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// ==========================================
// 8. Scan History
// ==========================================
function initScanHistory() {
  const typeFilter = document.getElementById('historyTypeFilter');
  const riskFilter = document.getElementById('historyRiskFilter');
  const btnClear = document.getElementById('btnClearHistory');

  if (typeFilter) typeFilter.addEventListener('change', fetchAndRenderHistory);
  if (riskFilter) riskFilter.addEventListener('change', fetchAndRenderHistory);

  if (btnClear) {
    btnClear.addEventListener('click', async () => {
      if (!confirm('Are you sure you want to clear all scan history? This action cannot be undone.')) return;
      try {
        await fetch('/api/scans/clear', { method: 'POST' });
        showToast('All scan history cleared.', 'info');
        fetchAndRenderHistory();
        fetchStatsAndRefreshDashboard();
      } catch (err) {
        showToast('Failed to clear history.', 'error');
      }
    });
  }
}

async function fetchAndRenderHistory() {
  const tbody = document.getElementById('historyTableBody');
  if (!tbody) return;

  const typeFilter = document.getElementById('historyTypeFilter')?.value || 'all';
  const riskFilter = document.getElementById('historyRiskFilter')?.value || 'all';

  let url = `/api/scans?limit=100`;
  if (typeFilter !== 'all') url += `&scan_type=${encodeURIComponent(typeFilter)}`;
  if (riskFilter !== 'all') url += `&risk_level=${encodeURIComponent(riskFilter)}`;

  try {
    const res = await fetch(url);
    const data = await res.json();
    const scans = data.scans || [];
    state.cachedScans = scans;

    if (scans.length === 0) {
      tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:32px; color:var(--text-muted);">No scan records matching current filter.</td></tr>`;
      return;
    }

    tbody.innerHTML = scans.map(s => `
      <tr>
        <td style="font-size:0.8rem; color:var(--text-muted);">${formatDate(s.created_at)}</td>
        <td><span class="badge-pill" style="background:#EFF6FF; color:#1D4ED8; font-size:0.75rem; font-weight:700; text-transform:uppercase;">${s.scan_type}</span></td>
        <td style="max-width:320px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:0.85rem;" title="${escapeHtml(s.input_preview)}">${escapeHtml(s.input_preview)}</td>
        <td><strong>${s.risk_score}</strong> / 100</td>
        <td>${getRiskBadgeHtml(s.classification, s.risk_level)}</td>
        <td>
          <div class="row-actions">
            <button class="btn-action-icon" title="View Details" onclick="showScanDetails(${s.id})">
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg>
            </button>
            <button class="btn-action-icon delete" title="Delete Scan" onclick="deleteScanItem(${s.id})">
              <svg width="16" height="16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
            </button>
          </div>
        </td>
      </tr>
    `).join('');
  } catch (err) {
    tbody.innerHTML = `<tr><td colspan="6" style="text-align:center; padding:24px; color:var(--risk-scam);">Error loading scan history.</td></tr>`;
  }
}

async function showScanDetails(scanId) {
  try {
    const res = await fetch(`/api/scans/${scanId}`);
    if (!res.ok) throw new Error('Scan not found');
    const scan = await res.json();

    const modal = document.getElementById('detailsModal');
    const title = document.getElementById('modalTitle');
    const body = document.getElementById('modalBody');

    title.innerText = `Scan Details #${scan.id} (${scan.scan_type.toUpperCase()})`;

    const indicatorsList = (scan.indicators || []).map(i => `<li>${escapeHtml(i)}</li>`).join('');
    const factorsList = (scan.factors || []).map(f => `
      <div style="display:flex; justify-content:space-between; padding:6px 0; border-bottom:1px solid #F1F5F9; font-size:0.85rem;">
        <div><strong>${escapeHtml(f.factor)}</strong> - <span style="color:var(--text-muted);">${escapeHtml(f.reason)}</span></div>
        <span class="factor-badge positive">+${f.points}</span>
      </div>
    `).join('');

    body.innerHTML = `
      <div style="margin-bottom:16px;">
        <div style="font-size:0.8rem; color:var(--text-muted); margin-bottom:4px;">Date: ${formatDate(scan.created_at)}</div>
        <div style="font-size:0.88rem; background:#F8FAFC; padding:10px 14px; border-radius:6px; border:1px solid #E2E8F0; font-family:var(--font-mono);">
          ${escapeHtml(scan.input_preview)}
        </div>
      </div>

      <div style="display:flex; align-items:center; gap:16px; margin-bottom:18px;">
        <div><strong>Score:</strong> ${scan.risk_score}/100</div>
        <div><strong>Classification:</strong> ${getRiskBadgeHtml(scan.classification, scan.risk_level)}</div>
      </div>

      ${indicatorsList ? `
        <div style="margin-bottom:16px;">
          <h4 style="font-size:0.85rem; text-transform:uppercase; color:var(--text-muted); margin-bottom:6px;">Warning Indicators</h4>
          <ul style="padding-left:18px; font-size:0.85rem; color:var(--text-main); line-height:1.6;">${indicatorsList}</ul>
        </div>
      ` : ''}

      ${factorsList ? `
        <div style="margin-bottom:16px;">
          <h4 style="font-size:0.85rem; text-transform:uppercase; color:var(--text-muted); margin-bottom:6px;">Factor Breakdown</h4>
          <div>${factorsList}</div>
        </div>
      ` : ''}

      <div class="action-box">
        <div class="action-box-title">Security Recommendation</div>
        <p>${escapeHtml(scan.recommendation)}</p>
      </div>
    `;

    modal.classList.add('active');
  } catch (err) {
    showToast(err.message, 'error');
  }
}

async function deleteScanItem(scanId) {
  if (!confirm(`Delete scan record #${scanId}?`)) return;
  try {
    const res = await fetch(`/api/scans/${scanId}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Delete failed');
    showToast(`Scan #${scanId} deleted.`, 'info');
    fetchAndRenderHistory();
    fetchStatsAndRefreshDashboard();
  } catch (err) {
    showToast(err.message, 'error');
  }
}

// ==========================================
// 9. Community Reports ("Report Scam")
// ==========================================
function initReports() {
  const form = document.getElementById('reportScamForm');
  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const category = document.getElementById('reportCategory').value;
      const description = document.getElementById('reportDescription').value.trim();
      const url = document.getElementById('reportUrl').value.trim();
      const scamType = document.getElementById('reportScamType').value.trim();

      if (!category || !description) {
        showToast('Category and Description are required.', 'error');
        return;
      }

      try {
        const res = await fetch('/api/reports', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ category, description, url, scam_type: scamType })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Failed to submit report');

        showToast('Report submitted for community threat intelligence.', 'success');
        form.reset();
        fetchAndRenderReports();
        fetchStatsAndRefreshDashboard();
      } catch (err) {
        showToast(err.message, 'error');
      }
    });
  }
}

async function fetchAndRenderReports() {
  const container = document.getElementById('reportsListContainer');
  if (!container) return;

  try {
    const res = await fetch('/api/reports?limit=20');
    const data = await res.json();
    const reports = data.reports || [];

    if (reports.length === 0) {
      container.innerHTML = `<div style="text-align:center; padding:32px; color:var(--text-muted);">No reports submitted yet. Submit a report using the form!</div>`;
      return;
    }

    container.innerHTML = reports.map(r => `
      <div style="background:#FFFFFF; border:1px solid var(--border-light); border-radius:var(--radius-md); padding:16px; margin-bottom:12px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <span class="badge-pill" style="background:#EFF6FF; color:#1D4ED8; font-weight:700; font-size:0.75rem;">${escapeHtml(r.category)}</span>
          <span style="font-size:0.75rem; color:var(--text-muted);">${formatDate(r.created_at)}</span>
        </div>
        <p style="font-size:0.88rem; color:var(--text-main); margin-bottom:8px; line-height:1.4;">${escapeHtml(r.description)}</p>
        ${r.url ? `<div style="font-size:0.78rem; color:var(--primary); font-family:var(--font-mono); word-break:break-all;">Target URL: ${escapeHtml(r.url)}</div>` : ''}
        <div style="margin-top:8px; font-size:0.75rem; color:#D97706; font-weight:600;">Status: ${escapeHtml(r.status)}</div>
      </div>
    `).join('');
  } catch (err) {
    container.innerHTML = `<div style="color:var(--risk-scam); padding:16px;">Failed to load reports.</div>`;
  }
}

// ==========================================
// 10. Jury Demo Tour (ALGOTHON'26 Showcase)
// ==========================================
function initDemoTour() {
  const btnTour = document.getElementById('btnDemoTour');
  if (btnTour) {
    btnTour.addEventListener('click', showDemoTourModal);
  }
}

function showDemoTourModal() {
  const modal = document.getElementById('detailsModal');
  const title = document.getElementById('modalTitle');
  const body = document.getElementById('modalBody');

  title.innerText = "ALGOTHON'26 Demo Showcase Tour";
  body.innerHTML = `
    <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:20px;">
      Welcome Jury! Quickly test ScamShield's hybrid ML + Explainable Rule engine using official test cases from the competition specification:
    </p>

    <div style="display:flex; flex-direction:column; gap:12px; margin-bottom:24px;">
      <div style="background:#FEF2F2; border:1px solid #FECACA; padding:14px; border-radius:8px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
          <strong style="color:#991B1B; font-size:0.88rem;">Test Case 1: Lottery / Prize Scam</strong>
          <span class="table-badge badge-scam">LIKELY SCAM</span>
        </div>
        <p style="font-size:0.82rem; color:#7F1D1D; margin-bottom:8px;">"Congratulations! You won ₹50,000. Click this link immediately to claim your prize."</p>
        <button class="btn-primary" style="padding:6px 14px; font-size:0.8rem;" onclick="runDemoCase('case-1')">Run Test Case 1</button>
      </div>

      <div style="background:#FEF2F2; border:1px solid #FECACA; padding:14px; border-radius:8px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
          <strong style="color:#991B1B; font-size:0.88rem;">Test Case 2: Account Suspension Threat</strong>
          <span class="table-badge badge-scam">LIKELY SCAM</span>
        </div>
        <p style="font-size:0.82rem; color:#7F1D1D; margin-bottom:8px;">"Your account will be suspended today. Verify your identity using this link."</p>
        <button class="btn-primary" style="padding:6px 14px; font-size:0.8rem;" onclick="runDemoCase('case-2')">Run Test Case 2</button>
      </div>

      <div style="background:#ECFDF5; border:1px solid #A7F3D0; padding:14px; border-radius:8px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
          <strong style="color:#065F46; font-size:0.88rem;">Test Case 3: Legitimate Campus Notice</strong>
          <span class="table-badge badge-safe">SAFE</span>
        </div>
        <p style="font-size:0.82rem; color:#064E3B; margin-bottom:8px;">"Your appointment with the college office is confirmed for tomorrow at 10 AM."</p>
        <button class="btn-primary" style="background:#059669; padding:6px 14px; font-size:0.8rem;" onclick="runDemoCase('case-3')">Run Test Case 3</button>
      </div>

      <div style="background:#FFFBEB; border:1px solid #FDE68A; padding:14px; border-radius:8px;">
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
          <strong style="color:#92400E; font-size:0.88rem;">Test Case 4: Banking Phishing URL</strong>
          <span class="table-badge badge-scam">LIKELY SCAM</span>
        </div>
        <p style="font-size:0.82rem; color:#78350F; margin-bottom:8px;">"http://sbi-pan-update.top/verify-login?id=82910"</p>
        <button class="btn-primary" style="background:#D97706; padding:6px 14px; font-size:0.8rem;" onclick="runDemoCase('case-url')">Run URL Test Case</button>
      </div>
    </div>

    <button class="btn-tool" onclick="closeModal()" style="width:100%;">Close Demo Showcase</button>
  `;
  modal.classList.add('active');
}

function runDemoCase(caseId) {
  closeModal();
  if (caseId === 'case-1') {
    switchView('message');
    const textarea = document.getElementById('messageInput');
    textarea.value = "Congratulations! You won ₹50,000. Click this link immediately to claim your prize.";
    textarea.dispatchEvent(new Event('input'));
    document.getElementById('messageScanForm').dispatchEvent(new Event('submit'));
  } else if (caseId === 'case-2') {
    switchView('message');
    const textarea = document.getElementById('messageInput');
    textarea.value = "Your account will be suspended today. Verify your identity using this link.";
    textarea.dispatchEvent(new Event('input'));
    document.getElementById('messageScanForm').dispatchEvent(new Event('submit'));
  } else if (caseId === 'case-3') {
    switchView('message');
    const textarea = document.getElementById('messageInput');
    textarea.value = "Your appointment with the college office is confirmed for tomorrow at 10 AM.";
    textarea.dispatchEvent(new Event('input'));
    document.getElementById('messageScanForm').dispatchEvent(new Event('submit'));
  } else if (caseId === 'case-url') {
    switchView('url');
    const input = document.getElementById('urlInput');
    input.value = "http://sbi-pan-update.top/verify-login?id=82910";
    document.getElementById('urlScanForm').dispatchEvent(new Event('submit'));
  }
}

// ==========================================
// 11. Utilities & Helpers
// ==========================================
function setButtonLoading(btn, isLoading, text) {
  if (!btn) return;
  btn.disabled = isLoading;
  if (isLoading) {
    btn.innerHTML = `<span class="spinner"></span> <span>${text}</span>`;
  } else {
    btn.innerHTML = text;
  }
}

function getRiskBadgeHtml(classification, riskLevel) {
  let badgeClass = 'badge-safe';
  if (classification === 'LIKELY SCAM') badgeClass = 'badge-scam';
  else if (classification === 'SUSPICIOUS') badgeClass = 'badge-suspicious';
  return `<span class="table-badge ${badgeClass}">${classification} (${riskLevel})</span>`;
}

function copyResultText(score, classification, recommendation) {
  const text = `ScamShield Security Analysis:
Risk Score: ${score}/100
Classification: ${classification}
Recommendation: ${recommendation}
Analyzed by ScamShield (ALGOTHON'26)`;
  navigator.clipboard.writeText(text).then(() => {
    showToast('Result copied to clipboard!', 'success');
  }).catch(() => {
    showToast('Failed to copy to clipboard.', 'error');
  });
}

function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  let icon = 'ℹ️';
  if (type === 'success') icon = '✅';
  if (type === 'error') icon = '❌';

  toast.innerHTML = `<span>${icon}</span> <span>${escapeHtml(message)}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function closeModal() {
  const modal = document.getElementById('detailsModal');
  if (modal) modal.classList.remove('active');
}

function formatDate(isoString) {
  if (!isoString) return '-';
  try {
    const d = new Date(isoString);
    return d.toLocaleDateString('en-US', { day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit' });
  } catch {
    return isoString;
  }
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function escapeQuotes(str) {
  if (!str) return '';
  return String(str).replace(/'/g, "\\'").replace(/"/g, '\\"');
}
