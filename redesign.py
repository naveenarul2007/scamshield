import os

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ScamShield – Premium Digital Scam Detection</title>
  <meta name="description" content="AI-powered cybersecurity protection against fraudulent SMS, URLs, and screenshots.">
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  
  <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>

  <!-- Sticky Navbar -->
  <nav class="navbar">
    <div class="navbar-container">
      <div class="navbar-brand" data-view-target="dashboard">
        <i data-lucide="shield-check" class="brand-icon"></i>
        <span class="brand-name">SCAMSHIELD</span>
      </div>
      
      <button class="mobile-menu-btn" id="mobileMenuBtn" aria-label="Toggle Menu">
        <i data-lucide="menu"></i>
      </button>

      <ul class="nav-menu sidebar">
        <li><a class="nav-link active" data-view-target="dashboard">Dashboard</a></li>
        <li class="nav-dropdown">
          <a class="nav-link" style="cursor: pointer;">Scan <i data-lucide="chevron-down" style="width: 16px; height: 16px; margin-left: 4px;"></i></a>
          <div class="dropdown-content">
            <a class="nav-link" data-view-target="message"><i data-lucide="message-square"></i> Message</a>
            <a class="nav-link" data-view-target="url"><i data-lucide="link"></i> URL</a>
            <a class="nav-link" data-view-target="screenshot"><i data-lucide="image"></i> Screenshot</a>
          </div>
        </li>
        <li><a class="nav-link" data-view-target="history">History</a></li>
        <li><a class="nav-link" data-view-target="reports">Reports</a></li>
        <li><a class="nav-link" data-view-target="about">About</a></li>
      </ul>
      
      <div class="navbar-cta">
        <button class="btn-primary" data-view-target="message">
          <i data-lucide="search"></i> Scan Now
        </button>
      </div>
    </div>
  </nav>

  <main class="page-viewport">
    
    <!-- DASHBOARD VIEW -->
    <section class="view-section active-view" id="view-dashboard">
      <!-- Premium Hero -->
      <div class="hero-section">
        <div class="hero-content">
          <div class="hero-tag">ENTERPRISE-GRADE PROTECTION</div>
          <h1>Detect scams before they detect you.</h1>
          <p>Analyze suspicious messages, links and screenshots and understand exactly why they may be dangerous.</p>
          <div class="hero-buttons">
            <button class="btn-primary btn-large" data-view-target="message">
              <i data-lucide="search"></i> Scan Now
            </button>
            <button class="btn-secondary btn-large" data-view-target="about">
              How It Works
            </button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="preview-card">
            <div class="preview-header">SECURITY ANALYSIS</div>
            <div class="preview-body">
              <div class="preview-score-box">
                <span class="score-val">87</span>
                <span class="score-max">/ 100</span>
              </div>
              <div class="preview-risk risk-high">🔴 LIKELY SCAM</div>
              <div class="preview-subtitle">HIGH RISK</div>
              <ul class="preview-factors">
                <li><i data-lucide="alert-triangle"></i> Urgent language</li>
                <li><i data-lucide="alert-triangle"></i> Financial request</li>
                <li><i data-lucide="alert-triangle"></i> Suspicious URL</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- How It Works -->
      <div class="how-it-works-section">
        <h2 class="section-title text-center">How ScamShield Works</h2>
        <div class="steps-grid">
          <div class="step-card">
            <div class="step-number">01 &mdash; Paste</div>
            <p>Paste suspicious content from SMS, WhatsApp, or emails.</p>
          </div>
          <div class="step-card">
            <div class="step-number">02 &mdash; Analyze</div>
            <p>ScamShield analyzes warning indicators in real-time.</p>
          </div>
          <div class="step-card">
            <div class="step-number">03 &mdash; Protect</div>
            <p>Understand the risk and take safer action immediately.</p>
          </div>
        </div>
      </div>

      <!-- Dashboard Stats -->
      <div class="dashboard-header">
        <div>
          <h2>Welcome to ScamShield</h2>
          <p class="subtitle">Your digital safety command center.</p>
        </div>
        <div class="status-badge" id="mlModelBadge">
          Active: Rule-based Explainable Engine
        </div>
      </div>

      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-title">TOTAL SCANS (DEMO)</div>
          <div class="stat-value" id="statTotalScans">0</div>
        </div>
        <div class="stat-card safe">
          <div class="stat-title">SAFE (DEMO)</div>
          <div class="stat-value" id="statSafeScans">0</div>
        </div>
        <div class="stat-card suspicious">
          <div class="stat-title">SUSPICIOUS (DEMO)</div>
          <div class="stat-value" id="statSuspiciousScans">0</div>
        </div>
        <div class="stat-card scam">
          <div class="stat-title">SCAMS DETECTED (DEMO)</div>
          <div class="stat-value" id="statScamScans">0</div>
        </div>
      </div>

      <!-- Quick Scan Focus -->
      <div class="quick-scan-focus">
        <h3 class="focus-title">What would you like to check?</h3>
        <div class="focus-grid">
          <div class="focus-card" data-view-target="message">
            <i data-lucide="message-square" class="focus-icon"></i>
            <h4>Message Scanner</h4>
            <p>Analyze suspicious text</p>
            <button class="btn-outline">Scan Message</button>
          </div>
          <div class="focus-card" data-view-target="url">
            <i data-lucide="link" class="focus-icon"></i>
            <h4>URL Scanner</h4>
            <p>Check a suspicious link</p>
            <button class="btn-outline">Scan URL</button>
          </div>
          <div class="focus-card" data-view-target="screenshot">
            <i data-lucide="image" class="focus-icon"></i>
            <h4>Screenshot Scanner</h4>
            <p>Upload and analyze a screenshot</p>
            <button class="btn-outline">Upload Screenshot</button>
          </div>
        </div>
      </div>

      <!-- Charts Area -->
      <div class="charts-section">
        <h3 class="section-title">Analytics Overview (Demo Data)</h3>
        <div class="charts-grid">
          <div class="chart-box">
            <canvas id="chartClassification"></canvas>
          </div>
          <div class="chart-box">
            <canvas id="chartCategories"></canvas>
          </div>
        </div>
      </div>
      
      <!-- Recent Scans (Hidden intentionally for clean SaaS look, but keeping ID for JS) -->
      <table style="display:none;"><tbody id="recentScansTableBody"></tbody></table>

    </section>

    <!-- MESSAGE SCANNER VIEW -->
    <section class="view-section" id="view-message">
      <div class="scanner-container">
        <div class="scanner-header">
          <h2>Message Scanner</h2>
          <p>Paste a suspicious message and we'll explain the warning signs.</p>
        </div>
        
        <div class="scanner-layout">
          <div class="scanner-input-area">
            <form id="messageScanForm">
              <div class="input-card">
                <textarea id="messageInput" class="premium-textarea" placeholder="Paste the suspicious message here..."></textarea>
                <div class="input-footer">
                  <span id="messageCharCount">0 characters (0 words)</span>
                </div>
              </div>
              <button type="submit" class="btn-primary btn-block" id="btnAnalyzeMessage">
                <i data-lucide="search"></i> Analyze Message
              </button>
            </form>
            
            <div class="demo-chips">
              <span class="demo-title">Try a Demo:</span>
              <button type="button" class="chip" data-fill-message="URGENT: 6-digit OTP is required to cancel unauthorized debit of ₹49,999 from your HDFC account. Provide OTP to our executive immediately to prevent loss.">Banking Scam</button>
              <button type="button" class="chip" data-fill-message="Congratulations! You won ₹50,000. Click this link immediately to claim your prize.">Prize Scam</button>
              <button type="button" class="chip" data-fill-message="Work from home! Earn 5000 per day by liking youtube videos. Reply YES to start.">Job Scam</button>
              <button type="button" class="chip" data-fill-message="Your appointment with the college office is confirmed for tomorrow at 10 AM.">Safe Message</button>
            </div>
          </div>
          
          <div class="scanner-results-area" id="messageResultsPanel" style="display:none;">
            <!-- JS Inject -->
          </div>
        </div>
      </div>
    </section>

    <!-- URL SCANNER VIEW -->
    <section class="view-section" id="view-url">
      <div class="scanner-container">
        <div class="scanner-header">
          <h2>Check a suspicious link</h2>
          <p>Analyze links for typosquatting, deceptive mimicry, and structural threats.</p>
        </div>
        
        <div class="scanner-layout">
          <div class="scanner-input-area">
            <form id="urlScanForm">
              <div class="input-card">
                <input type="text" id="urlInput" class="premium-input" placeholder="https://example.com">
              </div>
              <button type="submit" class="btn-primary btn-block" id="btnAnalyzeUrl">
                <i data-lucide="search"></i> Check URL
              </button>
            </form>
            
            <div class="demo-chips">
              <span class="demo-title">Try a Demo:</span>
              <button type="button" class="chip" data-fill-url="http://sbi-pan-update.top/verify-login?id=82910">Phishing Portal</button>
              <button type="button" class="chip" data-fill-url="http://paypa1-account-resolution.xyz/login">Typosquatting</button>
              <button type="button" class="chip" data-fill-url="https://google.com">Safe Domain</button>
            </div>
          </div>
          
          <div class="scanner-results-area" id="urlResultsPanel" style="display:none;">
            <!-- JS Inject -->
          </div>
        </div>
      </div>
    </section>

    <!-- SCREENSHOT SCANNER VIEW -->
    <section class="view-section" id="view-screenshot">
      <div class="scanner-container">
        <div class="scanner-header">
          <h2>Screenshot Scanner</h2>
          <p>Upload a suspicious message screenshot and let ScamShield analyze it.</p>
        </div>
        
        <div class="scanner-layout">
          <div class="scanner-input-area">
            <form id="screenshotScanForm">
              <div class="premium-dropzone" id="screenshotDropzone">
                <i data-lucide="image" class="dropzone-icon"></i>
                <div class="dropzone-text">DROP SCREENSHOT HERE</div>
                <div class="dropzone-subtext">or click to choose image</div>
                <div class="dropzone-formats">Supported: PNG • JPG • JPEG</div>
                <input type="file" id="screenshotFileInput" accept="image/png, image/jpeg, image/jpg, image/webp" class="file-hidden">
              </div>
              
              <div class="preview-box" id="screenshotPreviewContainer" style="display:none;">
                <img src="" id="screenshotPreviewImg" alt="Preview">
                <div class="preview-info">
                  <div id="screenshotPreviewFilename" class="filename">file.png</div>
                  <div id="screenshotPreviewSize" class="filesize">100 KB</div>
                </div>
                <button type="button" class="btn-icon" id="btnRemoveScreenshot"><i data-lucide="x"></i></button>
              </div>

              <div class="demo-chips" style="margin-top:20px;">
                <span class="demo-title">Test Samples:</span>
                <button type="button" class="chip" data-sample-screenshot="sample_scam_banking.png">SBI KYC Scam</button>
                <button type="button" class="chip" data-sample-screenshot="sample_scam_lottery.png">Lottery Scam</button>
                <button type="button" class="chip" data-sample-screenshot="sample_safe_meeting.png">Safe Meeting</button>
              </div>
              
              <button type="submit" class="btn-primary btn-block" id="btnAnalyzeScreenshot" style="margin-top:20px;">
                <i data-lucide="search"></i> Analyze Screenshot
              </button>
            </form>
          </div>
          
          <div class="scanner-results-area" id="screenshotResultsPanel" style="display:none;">
            <!-- JS Inject -->
          </div>
        </div>
      </div>
    </section>

    <!-- HISTORY VIEW -->
    <section class="view-section" id="view-history">
      <div class="page-header">
        <h2>Scan History</h2>
        <p>Your previous analysis records.</p>
      </div>
      
      <div class="history-controls">
        <select id="historyTypeFilter" class="premium-select">
          <option value="all">All Types</option>
          <option value="message">Messages</option>
          <option value="url">URLs</option>
          <option value="screenshot">Screenshots</option>
        </select>
        <select id="historyRiskFilter" class="premium-select">
          <option value="all">All Risks</option>
          <option value="low">Safe</option>
          <option value="medium">Suspicious</option>
          <option value="high">Likely Scam</option>
        </select>
        <button class="btn-outline text-red" id="btnClearHistory">Clear History</button>
      </div>

      <div class="premium-table-container">
        <table class="premium-table">
          <thead>
            <tr>
              <th>DATE</th>
              <th>TYPE</th>
              <th>PREVIEW</th>
              <th>RISK SCORE</th>
              <th>RESULT</th>
              <th>ACTION</th>
            </tr>
          </thead>
          <tbody id="historyTableBody">
            <!-- JS Inject -->
          </tbody>
        </table>
      </div>
    </section>

    <!-- REPORTS VIEW -->
    <section class="view-section" id="view-reports">
      <div class="page-header">
        <h2>Report a Scam</h2>
        <p>Help improve digital safety by reporting suspicious content.</p>
      </div>
      
      <div class="reports-layout">
        <div class="report-form-card">
          <form id="reportScamForm">
            <div class="form-group">
              <label>Scam Category</label>
              <select id="reportCategory" class="premium-select" required>
                <option value="">Select category...</option>
                <option value="Banking">Banking</option>
                <option value="OTP">OTP</option>
                <option value="Job Scam">Job Scam</option>
                <option value="Investment Scam">Investment Scam</option>
                <option value="Prize Scam">Prize Scam</option>
                <option value="Phishing">Phishing</option>
                <option value="Fake Customer Support">Fake Customer Support</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div class="form-group">
              <label>Description</label>
              <textarea id="reportDescription" class="premium-textarea" placeholder="Details about the scam..." required></textarea>
            </div>
            <div class="form-group">
              <label>Optional URL</label>
              <input type="text" id="reportUrl" class="premium-input" placeholder="http://...">
            </div>
            <div class="form-group">
              <label>Specific Mechanism</label>
              <input type="text" id="reportScamType" class="premium-input" placeholder="e.g. Telegram task">
            </div>
            <button type="submit" class="btn-primary btn-block">Submit Report</button>
          </form>
        </div>
        <div class="report-community">
          <h3>Community Reports</h3>
          <div id="reportsListContainer">
            <!-- JS Inject -->
          </div>
        </div>
      </div>
    </section>

    <!-- ABOUT VIEW -->
    <section class="view-section" id="view-about">
      <div class="page-header">
        <h2>About ScamShield</h2>
        <p>Enterprise-grade digital safety.</p>
      </div>
      
      <div class="about-card">
        <h3>The Problem</h3>
        <p>Digital scams have exploded in scale and sophistication. Cybercriminals exploit urgent psychological triggers to deceive victims.</p>
        
        <h3>Our Solution</h3>
        <p>ScamShield provides an instant, unified cyber-defense platform prioritizing <strong>Explainable AI</strong> to provide transparent risk breakdowns.</p>
        
        <h3>How It Works</h3>
        <div class="flow-diagram">
          <div class="flow-node">MESSAGE / URL / SCREENSHOT</div>
          <i data-lucide="arrow-down" class="flow-arrow"></i>
          <div class="flow-node">ANALYSIS</div>
          <i data-lucide="arrow-down" class="flow-arrow"></i>
          <div class="flow-node">RISK DETECTION</div>
          <i data-lucide="arrow-down" class="flow-arrow"></i>
          <div class="flow-node">EXPLANATION</div>
          <i data-lucide="arrow-down" class="flow-arrow"></i>
          <div class="flow-node final">SAFER DECISION</div>
        </div>
        
        <h3>Technology</h3>
        <ul class="tech-list">
          <li>Python / Flask</li>
          <li>Machine Learning (scikit-learn)</li>
          <li>NLP & Heuristics</li>
          <li>OCR (Tesseract)</li>
          <li>JavaScript</li>
          <li>Supabase / PostgreSQL</li>
        </ul>
        
        <div class="alert alert-warning">
          <strong>Limitations:</strong> ScamShield is an assistance tool and cannot guarantee that content is safe or malicious.
        </div>
      </div>
    </section>
  </main>

  <!-- Details Modal -->
  <div class="modal" id="detailsModal">
    <div class="modal-content">
      <div class="modal-header">
        <h3 id="modalTitle">Scan Details</h3>
        <button class="btn-icon" onclick="closeModal()"><i data-lucide="x"></i></button>
      </div>
      <div class="modal-body" id="modalBody"></div>
    </div>
  </div>

  <div id="toastContainer" class="toast-container"></div>
  
  <script src="/static/js/app.js"></script>
  <script>
    // Initialize icons
    lucide.createIcons();
    
    // Add loading overlay functionality to app.js
    window.originalSetButtonLoading = window.setButtonLoading;
    window.setButtonLoading = function(btn, isLoading, text) {
      if(isLoading) {
        btn.disabled = true;
        btn.innerHTML = `<i data-lucide="loader" class="spin"></i> ${text}`;
        lucide.createIcons();
        
        // Find adjacent results panel
        const panel = btn.closest('.scanner-layout').querySelector('.scanner-results-area');
        if(panel) {
          panel.style.display = 'block';
          panel.innerHTML = `
            <div class="loading-state">
              <h3>Analyzing...</h3>
              <div class="loading-step"><i data-lucide="check-circle" class="text-green"></i> Checking language patterns</div>
              <div class="loading-step"><i data-lucide="check-circle" class="text-green"></i> Checking suspicious requests</div>
              <div class="loading-step"><i data-lucide="check-circle" class="text-green"></i> Checking links</div>
              <div class="loading-step active"><i data-lucide="loader" class="spin"></i> Calculating risk</div>
            </div>
          `;
          lucide.createIcons();
        }
      } else {
        btn.disabled = false;
        btn.innerHTML = `<i data-lucide="search"></i> ${text}`;
        lucide.createIcons();
      }
    };

    // Override renderScanResults to match new premium design
    const oldRender = window.renderScanResults;
    window.renderScanResults = function(panelId, result, scanType = 'message') {
      const panel = document.getElementById(panelId);
      if (!panel) return;

      const score = result.risk_score || 0;
      const classification = result.classification || 'SAFE';
      const riskLevel = result.risk_level || 'LOW';
      const indicators = result.indicators || [];
      const factors = result.factors || [];
      const recommendation = result.recommendation || '';
      
      let themeClass = 'safe';
      let icon = 'check-circle';
      if(score >= 60) { themeClass = 'high'; icon = 'alert-triangle'; }
      else if(score >= 30) { themeClass = 'medium'; icon = 'alert-circle'; }

      let factorHtml = factors.map(f => `
        <div class="risk-factor-card">
          <div class="rfc-left">
            <i data-lucide="alert-triangle" class="text-warning"></i>
            <div>
              <strong>${f.factor}</strong>
              <div class="rfc-reason">${f.reason}</div>
            </div>
          </div>
          <div class="rfc-score">+${f.points}</div>
        </div>
      `).join('');

      let recHtml = `
        <div class="recommendation-card">
          <div class="rec-header">
            <i data-lucide="shield"></i> Recommended Action
          </div>
          <div class="rec-body">
            "Do not click suspicious links or provide OTPs, passwords, PINs or banking information. Verify the request through the organization's official website or app."
            <br><br>
            <strong>Specific advice:</strong> ${recommendation}
          </div>
          <div class="rec-actions">
             <button class="btn-outline" onclick="copyResultText(${score}, '${classification}', '${escapeQuotes(recommendation)}')">Copy Result</button>
             <button class="btn-primary" onclick="document.getElementById('${panelId}').style.display='none'">Scan Another</button>
          </div>
        </div>
      `;

      panel.innerHTML = `
        <div class="result-header">Analysis Complete</div>
        <div class="result-score-container ${themeClass}">
          <div class="circular-score">${score}<span class="max">/100</span></div>
          <div class="result-class"><i data-lucide="${icon}"></i> ${classification.toUpperCase()}</div>
          <div class="result-level">${riskLevel.toUpperCase()} RISK</div>
        </div>
        
        <div class="factors-section">
          <h4>Why was this flagged?</h4>
          ${factorHtml || '<p class="text-muted">No significant risk factors detected.</p>'}
        </div>
        
        ${recHtml}
      `;
      lucide.createIcons();
    };
  </script>
</body>
</html>"""

CSS_CONTENT = """/* Premium SaaS Cybersecurity CSS */
:root {
  --bg-main: #F4F7FB;
  --bg-card: #FFFFFF;
  --primary: #0F172A; /* Deep Navy */
  --primary-hover: #1E293B;
  --secondary: #3B82F6; /* Professional Blue */
  --secondary-hover: #2563EB;
  
  --text-dark: #0F172A;
  --text-muted: #64748B;
  --text-light: #94A3B8;
  
  --border: #E2E8F0;
  
  --risk-safe: #059669;
  --risk-safe-bg: #D1FAE5;
  --risk-medium: #D97706;
  --risk-medium-bg: #FEF3C7;
  --risk-high: #DC2626;
  --risk-high-bg: #FEE2E2;
  
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
  
  --font-sans: 'Inter', sans-serif;
  --radius-md: 12px;
  --radius-lg: 16px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: var(--font-sans);
  background: var(--bg-main);
  color: var(--text-dark);
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

a { text-decoration: none; color: inherit; }

/* Navbar */
.navbar {
  position: sticky;
  top: 0;
  background: #FFFFFF;
  border-bottom: 1px solid var(--border);
  z-index: 100;
  box-shadow: var(--shadow-sm);
}
.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.navbar-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 800;
  font-size: 1.25rem;
  color: var(--primary);
  cursor: pointer;
}
.brand-icon { color: var(--secondary); }

.nav-menu {
  display: flex;
  align-items: center;
  gap: 24px;
  list-style: none;
}
.nav-link {
  font-weight: 500;
  color: var(--text-muted);
  transition: color 0.2s;
  display: flex;
  align-items: center;
  cursor: pointer;
}
.nav-link:hover, .nav-link.active {
  color: var(--primary);
}
.nav-dropdown {
  position: relative;
}
.dropdown-content {
  display: none;
  position: absolute;
  top: 100%;
  left: 0;
  background: #FFF;
  box-shadow: var(--shadow-md);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 8px 0;
  min-width: 180px;
}
.nav-dropdown:hover .dropdown-content {
  display: block;
}
.dropdown-content a {
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--text-muted);
  font-size: 0.95rem;
}
.dropdown-content a:hover {
  background: var(--bg-main);
  color: var(--primary);
}
.mobile-menu-btn { display: none; background: none; border: none; cursor: pointer; }

/* Buttons */
.btn-primary {
  background: var(--primary);
  color: #FFF;
  border: none;
  padding: 10px 20px;
  border-radius: var(--radius-md);
  font-weight: 600;
  font-family: inherit;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}
.btn-primary:hover { background: var(--primary-hover); transform: translateY(-1px); }
.btn-secondary {
  background: #FFF;
  color: var(--primary);
  border: 1px solid var(--border);
  padding: 10px 20px;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}
.btn-secondary:hover { background: var(--bg-main); }
.btn-large { padding: 14px 28px; font-size: 1.05rem; }
.btn-block { width: 100%; justify-content: center; padding: 14px; font-size: 1rem; }
.btn-outline {
  background: transparent;
  color: var(--primary);
  border: 1px solid var(--border);
  padding: 8px 16px;
  border-radius: var(--radius-md);
  font-weight: 600;
  cursor: pointer;
}
.btn-outline:hover { background: var(--bg-main); }
.btn-icon { background: none; border: none; cursor: pointer; color: var(--text-muted); }

/* Main Layout */
.page-viewport {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px;
}
.view-section { display: none; animation: fadeIn 0.3s ease; }
.view-section.active-view { display: block; }
@keyframes fadeIn { from{opacity:0; transform:translateY(10px);} to{opacity:1; transform:translateY(0);} }

/* Hero */
.hero-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  align-items: center;
  margin-bottom: 60px;
}
.hero-tag {
  font-size: 0.8rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  color: var(--secondary);
  margin-bottom: 16px;
}
.hero-content h1 {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.1;
  color: var(--primary);
  margin-bottom: 20px;
}
.hero-content p {
  font-size: 1.15rem;
  color: var(--text-muted);
  margin-bottom: 32px;
  max-width: 480px;
}
.hero-buttons { display: flex; gap: 16px; }

.preview-card {
  background: #FFF;
  border: 1px solid var(--border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}
.preview-header {
  background: var(--primary);
  color: #FFF;
  padding: 16px;
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  text-align: center;
}
.preview-body { padding: 32px; text-align: center; }
.preview-score-box { margin-bottom: 16px; }
.score-val { font-size: 3.5rem; font-weight: 800; color: var(--risk-high); line-height: 1; }
.score-max { font-size: 1.5rem; color: var(--text-muted); font-weight: 600; }
.preview-risk {
  display: inline-block;
  background: var(--risk-high-bg);
  color: var(--risk-high);
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: 700;
  margin-bottom: 8px;
}
.preview-subtitle { font-size: 0.9rem; color: var(--text-muted); margin-bottom: 24px; font-weight: 600; }
.preview-factors {
  list-style: none;
  text-align: left;
  border-top: 1px solid var(--border);
  padding-top: 16px;
}
.preview-factors li {
  display: flex;
  align-items: center;
  gap: 12px;
  color: var(--text-dark);
  font-weight: 500;
  margin-bottom: 12px;
}
.preview-factors i { color: var(--risk-high); width: 18px; height: 18px; }

/* How It Works */
.how-it-works-section { margin-bottom: 60px; }
.section-title { font-size: 1.75rem; font-weight: 800; margin-bottom: 32px; color: var(--primary); }
.text-center { text-align: center; }
.steps-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.step-card {
  background: #FFF;
  padding: 32px;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border);
  box-shadow: var(--shadow-sm);
}
.step-number { font-weight: 800; color: var(--secondary); margin-bottom: 12px; font-size: 1.1rem; }

/* Dashboard */
.dashboard-header { margin-bottom: 32px; display: flex; justify-content: space-between; align-items: flex-end; }
.dashboard-header h2 { font-size: 2rem; font-weight: 800; }
.subtitle { color: var(--text-muted); font-size: 1.1rem; }
.status-badge { background: var(--bg-card); border: 1px solid var(--border); padding: 8px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 600; color: var(--secondary); }

.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }
.stat-card { background: #FFF; border: 1px solid var(--border); padding: 24px; border-radius: var(--radius-md); box-shadow: var(--shadow-sm); }
.stat-title { font-size: 0.8rem; font-weight: 700; color: var(--text-muted); margin-bottom: 8px; }
.stat-value { font-size: 2.5rem; font-weight: 800; color: var(--primary); }
.stat-card.safe .stat-value { color: var(--risk-safe); }
.stat-card.suspicious .stat-value { color: var(--risk-medium); }
.stat-card.scam .stat-value { color: var(--risk-high); }

.quick-scan-focus { margin-bottom: 40px; }
.focus-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 20px; }
.focus-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.focus-card {
  background: #FFF;
  border: 1px solid var(--border);
  padding: 32px;
  border-radius: var(--radius-lg);
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: var(--shadow-sm);
}
.focus-card:hover { transform: translateY(-4px); box-shadow: var(--shadow-md); border-color: var(--secondary); }
.focus-icon { width: 48px; height: 48px; color: var(--secondary); margin-bottom: 16px; }
.focus-card h4 { font-size: 1.1rem; font-weight: 700; margin-bottom: 8px; }
.focus-card p { color: var(--text-muted); font-size: 0.9rem; margin-bottom: 20px; }

/* Charts */
.charts-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.chart-box { background: #FFF; border: 1px solid var(--border); padding: 24px; border-radius: var(--radius-lg); height: 300px; }

/* Scanners */
.scanner-container { max-width: 900px; margin: 0 auto; }
.scanner-header { text-align: center; margin-bottom: 32px; }
.scanner-header h2 { font-size: 2rem; font-weight: 800; margin-bottom: 8px; }
.scanner-header p { color: var(--text-muted); font-size: 1.1rem; }

.scanner-layout { display: flex; flex-direction: column; gap: 32px; }
.input-card { background: #FFF; border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 16px; box-shadow: var(--shadow-sm); margin-bottom: 16px; }
.premium-textarea { width: 100%; border: none; min-height: 150px; font-size: 1.05rem; font-family: inherit; color: var(--text-dark); resize: vertical; outline: none; }
.premium-input { width: 100%; border: none; font-size: 1.1rem; font-family: inherit; color: var(--text-dark); outline: none; padding: 8px 0; }
.input-footer { display: flex; justify-content: flex-end; font-size: 0.85rem; color: var(--text-muted); margin-top: 12px; }

.demo-chips { display: flex; align-items: center; gap: 12px; flex-wrap: wrap; margin-top: 24px; }
.demo-title { font-size: 0.85rem; font-weight: 600; color: var(--text-muted); }
.chip { background: #FFF; border: 1px solid var(--border); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 500; cursor: pointer; transition: all 0.2s; }
.chip:hover { background: var(--bg-main); border-color: var(--secondary); color: var(--secondary); }

.premium-dropzone {
  background: #FFF;
  border: 2px dashed var(--border);
  border-radius: var(--radius-lg);
  padding: 60px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  position: relative;
}
.premium-dropzone:hover { border-color: var(--secondary); background: #F8FAFC; }
.dropzone-icon { width: 48px; height: 48px; color: var(--text-muted); margin-bottom: 16px; }
.dropzone-text { font-size: 1.1rem; font-weight: 700; color: var(--primary); margin-bottom: 8px; }
.dropzone-formats { font-size: 0.85rem; color: var(--text-muted); }
.file-hidden { position: absolute; top:0; left:0; width:100%; height:100%; opacity: 0; cursor: pointer; }

.preview-box { display: flex; align-items: center; gap: 16px; background: #FFF; border: 1px solid var(--border); padding: 16px; border-radius: var(--radius-md); margin-top: 16px; }
.preview-box img { width: 60px; height: 60px; object-fit: cover; border-radius: 8px; }
.preview-info { flex: 1; }
.filename { font-weight: 600; font-size: 0.95rem; }
.filesize { font-size: 0.85rem; color: var(--text-muted); }

/* Results */
.scanner-results-area { background: #FFF; border: 1px solid var(--border); border-radius: var(--radius-lg); padding: 32px; box-shadow: var(--shadow-md); animation: fadeIn 0.4s ease; }
.loading-state { text-align: left; }
.loading-state h3 { font-size: 1.25rem; font-weight: 700; margin-bottom: 24px; }
.loading-step { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; font-weight: 500; color: var(--text-muted); }
.loading-step.active { color: var(--primary); font-weight: 600; }
.text-green { color: var(--risk-safe); }
.spin { animation: spin 1s linear infinite; }
@keyframes spin { 100% { transform: rotate(360deg); } }

.result-header { font-size: 0.9rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 24px; text-align: center; }
.result-score-container { text-align: center; margin-bottom: 40px; }
.circular-score { font-size: 4.5rem; font-weight: 800; line-height: 1; margin-bottom: 16px; }
.circular-score .max { font-size: 1.5rem; color: var(--text-muted); }
.result-class { font-size: 1.5rem; font-weight: 800; display: inline-flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.result-level { font-size: 1rem; font-weight: 600; letter-spacing: 0.05em; }

.safe .circular-score, .safe .result-class { color: var(--risk-safe); }
.medium .circular-score, .medium .result-class { color: var(--risk-medium); }
.high .circular-score, .high .result-class { color: var(--risk-high); }

.factors-section h4 { font-size: 1.1rem; font-weight: 700; margin-bottom: 16px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
.risk-factor-card { display: flex; justify-content: space-between; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid #F1F5F9; }
.rfc-left { display: flex; gap: 12px; }
.rfc-left strong { display: block; font-size: 0.95rem; color: var(--primary); }
.rfc-reason { font-size: 0.85rem; color: var(--text-muted); }
.rfc-score { background: #FEE2E2; color: #DC2626; padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; }
.text-warning { color: var(--risk-medium); }

.recommendation-card { background: var(--bg-main); border: 1px solid var(--border); border-radius: var(--radius-md); padding: 24px; margin-top: 32px; }
.rec-header { font-size: 1.1rem; font-weight: 700; color: var(--primary); display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
.rec-body { font-size: 0.95rem; color: var(--text-dark); margin-bottom: 24px; line-height: 1.6; }
.rec-actions { display: flex; gap: 12px; }

/* History & Tables */
.page-header { margin-bottom: 32px; }
.page-header h2 { font-size: 2rem; font-weight: 800; }
.page-header p { color: var(--text-muted); font-size: 1.1rem; }

.history-controls { display: flex; gap: 16px; margin-bottom: 24px; }
.premium-select { padding: 10px 16px; border: 1px solid var(--border); border-radius: var(--radius-md); font-family: inherit; font-size: 0.95rem; background: #FFF; outline: none; }
.text-red { color: var(--risk-high); border-color: var(--risk-high-bg); }

.premium-table-container { background: #FFF; border: 1px solid var(--border); border-radius: var(--radius-lg); overflow: hidden; box-shadow: var(--shadow-sm); }
.premium-table { width: 100%; border-collapse: collapse; text-align: left; }
.premium-table th { background: #F8FAFC; padding: 16px 24px; font-size: 0.8rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; border-bottom: 1px solid var(--border); }
.premium-table td { padding: 16px 24px; border-bottom: 1px solid var(--border); font-size: 0.95rem; }
.premium-table tr:last-child td { border-bottom: none; }

/* Reports & Forms */
.reports-layout { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; }
.report-form-card { background: #FFF; border: 1px solid var(--border); padding: 32px; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); }
.form-group { margin-bottom: 20px; }
.form-group label { display: block; font-weight: 600; font-size: 0.9rem; margin-bottom: 8px; }
.report-community h3 { font-size: 1.25rem; font-weight: 700; margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 12px; }

/* About Page */
.about-card { background: #FFF; border: 1px solid var(--border); padding: 40px; border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); }
.about-card h3 { font-size: 1.35rem; font-weight: 800; color: var(--primary); margin-top: 32px; margin-bottom: 16px; }
.about-card h3:first-child { margin-top: 0; }
.about-card p { font-size: 1.05rem; color: var(--text-muted); margin-bottom: 20px; line-height: 1.7; }
.tech-list { padding-left: 20px; margin-bottom: 32px; color: var(--text-dark); line-height: 1.8; }
.alert-warning { background: var(--risk-medium-bg); color: #92400E; padding: 16px; border-radius: var(--radius-md); font-size: 0.95rem; }

.flow-diagram { display: flex; flex-direction: column; align-items: center; gap: 16px; margin: 40px 0; }
.flow-node { background: var(--bg-main); border: 1px solid var(--border); padding: 12px 24px; border-radius: var(--radius-md); font-weight: 700; font-size: 0.9rem; letter-spacing: 0.05em; color: var(--primary); }
.flow-node.final { background: var(--risk-safe-bg); color: var(--risk-safe); border-color: #A7F3D0; }
.flow-arrow { color: var(--text-muted); }

/* Responsive */
@media (max-width: 768px) {
  .hero-section, .reports-layout, .charts-grid, .steps-grid, .focus-grid, .stats-grid { grid-template-columns: 1fr; }
  .nav-menu { display: none; }
  .mobile-menu-btn { display: block; }
  .nav-menu.mobile-open { display: flex; flex-direction: column; position: absolute; top: 72px; left: 0; width: 100%; background: #FFF; padding: 20px; border-bottom: 1px solid var(--border); box-shadow: var(--shadow-md); }
}
"""

def generate_files():
    with open('/Users/naveenarul/Desktop/ScamShield/templates/index.html', 'w') as f:
        f.write(HTML_CONTENT)
    with open('/Users/naveenarul/Desktop/ScamShield/static/css/style.css', 'w') as f:
        f.write(CSS_CONTENT)

if __name__ == "__main__":
    generate_files()
    print("Files successfully generated.")
