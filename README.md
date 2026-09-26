# 🛡️ ScamShield – Real-Time Digital Scam Detection & Protection Platform
**ALGOTHON’26 Official Submission**

> *"Detect scams before they detect you."*  
> An explainable, AI-powered cybersecurity platform engineered to protect users from fraudulent SMS, WhatsApp phishing, malicious URLs, credential-harvesting attacks, and deceptive screenshots.

---

## 1. Problem Statement
Digital scams and financial fraud have grown exponentially in sophistication. Modern cybercriminals weaponize urgent psychological triggers—threats of immediate bank account deactivation, electricity disconnection, fraudulent lottery/prize winnings, and deceptive work-from-home tasks. 

Ordinary citizens and first-time digital banking users frequently fall victim because:
- Attackers employ subtle brand impersonation (e.g. `sbi-pan-update.top`, `paypa1-account-resolution.xyz`).
- Urgency and threat language force impulsive decision-making before independent verification.
- Traditional anti-spam filters are opaque black boxes that output binary decisions without explaining *why* a message is dangerous or what precautions to take.

---

## 2. The Solution
**ScamShield** is an explainable cyber-defense platform designed for instant verification across multiple media channels:
1. **SMS & WhatsApp Messages**: Identifies OTP theft, financial coercion, urgency, and impersonation.
2. **Suspicious URLs**: Deep heuristic analysis inspecting unencrypted HTTP, typosquatting, high-risk TLDs, IP host abuse, and URL shorteners.
3. **Screenshot OCR**: Extracts text from mobile screenshots and runs it through the threat detection engine.
4. **Explainable AI (XAI)**: Replaces opaque "AI detected this" messages with a transparent **Risk Factor Breakdown** detailing exact point weights (`+25 OTP/password request`, `+20 financial request`, `+15 urgency`).
5. **Community Threat Intelligence**: Crowdsourced reporting to track emerging phishing vectors.

---

## 3. Key Capabilities & Features

| Capability | Description |
| :--- | :--- |
| **Message Scanner** | Analyzes text for urgency, threats, financial requests, OTP theft, and remote access software prompts. Combines ML probability with weighted rule indicators. |
| **URL Scanner** | Inspects domain entropy (DGA), protocol security, high-risk TLDs (`.xyz`, `.top`, `.cc`), typosquatting brand mimicry (`paypa1`), and `@` credential tricks. |
| **Screenshot Scanner** | Optical Character Recognition (OCR) pipeline that extracts text from uploaded images (PNG, JPG, WEBP) and classifies threat severity. Includes built-in demo presets. |
| **Explainable AI Breakdown** | Visual meter (0–100) with calibrated classifications (`SAFE`, `SUSPICIOUS`, `LIKELY SCAM`) and granular point contributions. |
| **Audit Scan History** | Persistent audit log with privacy-safe input previews, filtering by scan type and risk level, and detailed investigation modals. |
| **Community Reports** | User-submitted scam database with categorization (Banking, OTP, Job Scams, Investment Scams, Prize Scams). |
| **ALGOTHON’26 Demo Showcase** | 1-click jury demonstration runner for instant evaluation of competition test cases. |

---

## 4. System Architecture

```text
                               +-----------------------------+
                               |     ScamShield Web UI       |
                               | (Responsive Cybersecurity)  |
                               +--------------+--------------+
                                              |
                          REST API JSON Calls | (Port 5001)
                                              v
                               +-----------------------------+
                               |      Flask App Engine       |
                               |    (backend/routes.py)      |
                               +-------+------+-------+------+
                                       |      |       |
                 +---------------------+      |       +---------------------+
                 |                            |                             |
                 v                            v                             v
    +------------------------+   +------------------------+    +------------------------+
    |    Message Analyzer    |   |      URL Analyzer      |    |       OCR Engine       |
    |  - Explainable Rules   |   |  - Protocol & SSL      |    |  - Image Validation    |
    |  - 12 Weighted Vectors |   |  - Typosquatting / DGA |    |  - Tesseract OCR /     |
    |  - ML Pipeline Blending|   |  - Risky TLDs & Hosts  |    |    Sample Presets      |
    +-----------+------------+   +-----------+------------+    +-----------+------------+
                |                            |                             |
                +----------------------------+-----------------------------+
                                             |
                                             v
                              +-----------------------------+
                              |      Database Storage       |
                              |  - SQLite (Local Zero-Conf) |
                              |  - Supabase / PostgreSQL    |
                              +-----------------------------+
```

---

## 5. Technology Stack

- **Frontend**: Semantic HTML5, Vanilla CSS3 (Custom Cybersecurity Design System with Blue/Indigo accents and light mode palette), Vanilla ES6 JavaScript, [Chart.js](https://www.chartjs.org/) for real-time analytics.
- **Backend**: Python 3, Flask REST API, Werkzeug.
- **AI / Machine Learning**: `scikit-learn` (TF-IDF Vectorizer + Calibrated Logistic Regression), `pandas`, `numpy`, `joblib`.
- **Computer Vision / OCR**: `pytesseract`, `Pillow` (PIL) with graceful dependency detection and fallback sample presets.
- **Database**: SQLite for zero-configuration local execution; fully compatible with Supabase / PostgreSQL via environment connection string.

---

## 6. Project Directory Structure

```text
ScamShield/
│
├── app.py                      # Root launcher script
├── requirements.txt            # Python dependencies
├── .env.example                # Example environment variables
├── .env                        # Local active configuration
├── README.md                   # Full documentation & specifications
│
├── frontend/                   # Frontend assets mirror
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
│
├── backend/                    # Core backend service
│   ├── __init__.py
│   ├── app.py                  # Flask app factory
│   ├── config.py               # Environment configuration
│   ├── routes.py               # REST API endpoints
│   ├── message_analyzer.py     # Hybrid weighted rule & ML scoring engine
│   ├── url_analyzer.py         # Heuristic URL and domain analysis engine
│   └── ocr_engine.py           # Screenshot OCR processor & validation
│
├── ml_model/                   # Machine learning pipeline
│   ├── __init__.py
│   ├── train.py                # Model training script
│   ├── predict.py              # Inference & n-gram feature extraction
│   ├── scam_model.pkl          # Serialized Logistic Regression model
│   ├── tfidf_vectorizer.pkl    # Serialized TF-IDF vectorizer
│   └── metrics.json            # Model evaluation metrics & confusion matrix
│
├── dataset/                    # Training and evaluation data
│   └── messages.csv            # Labeled dataset (Safe vs Scam across 9 categories)
│
├── database/                   # Data layer
│   ├── __init__.py
│   ├── db.py                   # Database queries and connection pool
│   ├── schema.sql              # SQL table definitions
│   ├── seed.py                 # Initial data seeder for jury demo
│   └── scamshield.db           # SQLite database
│
├── static/                     # Flask static assets
│   ├── css/style.css           # Custom cybersecurity styling
│   ├── js/app.js               # Reactive client-side application
│   └── samples/                # High-resolution demo screenshot mocks
│       ├── sample_scam_banking.png
│       ├── sample_scam_lottery.png
│       └── sample_safe_meeting.png
│
├── templates/
│   └── index.html              # Main single-page application template
│
└── tests/
    └── test_scamshield.py      # Automated test suite (12 test cases)
```

---

## 7. Machine Learning Pipeline & Performance

The ML subsystem uses a calibrated TF-IDF + Logistic Regression pipeline trained on a balanced corpus of real-world communications and scam messages:

```text
Raw Input Text
     ↓
Text Standardization (Lowercase, URLs -> URL_TOKEN, Currency -> CURRENCY_TOKEN)
     ↓
TF-IDF N-gram Extraction (Unigrams + Bigrams, sublinear TF scaling)
     ↓
Calibrated Logistic Regression (C=2.0, balanced class weighting)
     ↓
Scam Probability Score + Top Contributing N-grams
```

### Model Performance Metrics
- **Model Type**: TF-IDF + Calibrated Logistic Regression
- **Accuracy**: `95.65%`
- **Precision**: `92.31%`
- **Recall**: `100.0%` (Zero missed scam samples in test set)
- **F1-Score**: `96.0%`
- **Confusion Matrix**: `[[10, 1], [0, 12]]`

To retrain the model at any time:
```bash
python ml_model/train.py
```

---

## 8. Explainable Scoring Rules

| Factor | Points | Description |
| :--- | :---: | :--- |
| **OTP / Credential Request** | `+25` | Requests confidential PIN, OTP, CVV, or password |
| **Financial / Banking Trigger** | `+20` | Mentions wire transfer, debit cards, UPI, or unverified fees |
| **Account Suspension / KYC Threat** | `+20` | Claims account will be blocked or PAN/KYC is expired |
| **Suspicious Link Request** | `+20` | Urges user to visit an external link or shortened URL |
| **Remote Access / Imposter Support** | `+20` | Directs user to install AnyDesk, TeamViewer, or call fake helplines |
| **Job / Investment Scam** | `+18` | Promises unrealistic daily earnings or guaranteed crypto returns |
| **Urgency & Time Pressure** | `+15` | Uses coercive language ("immediately", "today only", "within 24 hours") |
| **Threat / Coercive Language** | `+15` | Threatens legal action, police arrest warrant, or fines |
| **Prize / Lottery Lure** | `+15` | Promises unexpected cash, scratch cards, or lucky draw rewards |
| **Brand Impersonation** | `+15` | References institutions (SBI, HDFC, PayPal, Customs, Police) |

### Risk Level Normalization
- **`0 – 29`**: **SAFE** (Risk Level: `LOW`)
- **`30 – 59`**: **SUSPICIOUS** (Risk Level: `MEDIUM`)
- **`60 – 100`**: **LIKELY SCAM** (Risk Level: `HIGH`)

---

## 9. Installation & How to Run

### Step 1: Clone Repository & Create Virtual Environment
```bash
cd ScamShield
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Default configuration is already set up to run locally using SQLite without needing external API keys.

### Step 4: Seed Database (Optional)
```bash
python database/seed.py
```

### Step 5: Start the Application
```bash
python app.py
```
Open your browser and navigate to:
```text
http://127.0.0.1:5001
```

---

## 10. API Specification

### 1. Analyze Message
`POST /api/analyze/message`
```json
// Request
{
  "message": "Your bank account will be blocked today. Verify your account immediately using this link."
}

// Response
{
  "risk_score": 70,
  "classification": "LIKELY SCAM",
  "risk_level": "HIGH",
  "indicators": [
    "Urgent time-pressure tactics detected",
    "Threatening or punitive language detected",
    "Account suspension / KYC expiry pressure",
    "Prompts user to click or follow an unverified link"
  ],
  "factors": [
    {
      "factor": "Urgency & Coercion",
      "points": 15,
      "reason": "Forces immediate action to prevent rational verification"
    },
    {
      "factor": "Threat / Coercive Language",
      "points": 15,
      "reason": "Threatens account closure, legal penalty, or law enforcement action"
    },
    {
      "factor": "Account / KYC Threat",
      "points": 20,
      "reason": "Claims account will be frozen unless immediate KYC or PAN is provided"
    },
    {
      "factor": "Link Action Request",
      "points": 20,
      "reason": "Pressures user to open an external link for verification or claiming rewards"
    }
  ],
  "recommendation": "Do not click links or provide passwords, OTPs, PINs or banking information. Verify the request through the organization's official website or customer support helpline."
}
```

### 2. Analyze URL
`POST /api/analyze/url`
```json
// Request
{
  "url": "http://sbi-pan-update.top/verify-login?id=82910"
}
```

### 3. Analyze Screenshot (OCR)
`POST /api/analyze/screenshot`  
- Accepts multipart form data with `screenshot` image file, or JSON with `{"sample_name": "sample_scam_banking.png"}`.

### 4. Fetch Scan History
`GET /api/scans?limit=50&scan_type=message&risk_level=high`

### 5. Submit Scam Report
`POST /api/reports`
```json
{
  "category": "Banking",
  "description": "Suspicious SMS claiming debit card blocked.",
  "url": "http://fake-sbi-portal.top",
  "scam_type": "Banking SMS Scam"
}
```

---

## 11. Automated Test Suite

Run the full verification test suite (12 unit and integration tests):
```bash
python -m unittest tests/test_scamshield.py
```
All 12 tests validate API contracts, test cases 1/2/3, database persistence, and URL heuristics.

---

## 12. Evaluation & Demo Test Cases

| Test Case | Input | Expected Result | ScamShield Result |
| :--- | :--- | :---: | :---: |
| **Case 1 (Prize)** | *"Congratulations! You won ₹50,000. Click this link immediately to claim your prize."* | **LIKELY SCAM** | **71/100 (HIGH)** ✅ |
| **Case 2 (Threat)** | *"Your account will be suspended today. Verify your identity using this link."* | **LIKELY SCAM** | **70/100 (HIGH)** ✅ |
| **Case 3 (Safe)** | *"Your appointment with the college office is confirmed for tomorrow at 10 AM."* | **SAFE** | **0/100 (LOW)** ✅ |
| **Case 4 (URL)** | `http://sbi-pan-update.top/verify-login?id=82910` | **LIKELY SCAM** | **95/100 (HIGH)** ✅ |
| **Case 5 (Screenshot)** | `sample_scam_banking.png` (Urgent SBI KYC suspension SMS) | **LIKELY SCAM** | **90/100 (HIGH)** ✅ |

---

## 13. Limitations & Disclaimers

1. **Assistance Tool**: ScamShield is designed as a decision-support advisory tool. It does not provide absolute guarantees of safety or threat status.
2. **URL Heuristics**: URL analysis is based on structural inspection (protocol, TLD, entropy, typosquatting) rather than live browser execution or active crawling, preventing drive-by malware execution.
3. **OCR System Requirement**: For arbitrary custom screenshot uploads, the host system requires Tesseract OCR (`brew install tesseract` on macOS, `sudo apt-get install tesseract-ocr` on Linux). If unavailable, ScamShield provides graceful fallback with informative setup guidance and built-in sample screenshots.

---

## 14. Future Improvements

- Browser extension for real-time in-browser warning overlays on suspicious login pages.
- Native WhatsApp & Telegram bot integration for instant forwarded message scanning.
- LLM agentic verification for multi-turn conversational baiting detection.
- Decentralized threat intelligence sharing with financial institutions and CERT-In.

---

## 15. ALGOTHON’26 Team Information
- **Project**: ScamShield – Real-Time Digital Scam Detection & Protection Platform
- **Track**: Cybersecurity / AI & Machine Learning
- **Hackathon**: ALGOTHON’26
- **Status**: Production-Ready Full-Stack MVP
