-- ScamShield Database Schema
-- Compatible with SQLite and PostgreSQL / Supabase

CREATE TABLE IF NOT EXISTS scans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scan_type VARCHAR(32) NOT NULL,
    input_preview TEXT,
    risk_score INTEGER NOT NULL,
    classification VARCHAR(32) NOT NULL,
    risk_level VARCHAR(16) NOT NULL,
    indicators TEXT,         -- JSON encoded array of warning indicators
    factors TEXT,            -- JSON encoded array of factor score breakdowns
    recommendation TEXT
);

CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    category VARCHAR(64) NOT NULL,
    description TEXT NOT NULL,
    url VARCHAR(512),
    scam_type VARCHAR(64),
    status VARCHAR(32) DEFAULT 'Pending Verification'
);

CREATE INDEX IF NOT EXISTS idx_scans_created_at ON scans(created_at);
CREATE INDEX IF NOT EXISTS idx_scans_type ON scans(scan_type);
CREATE INDEX IF NOT EXISTS idx_scans_classification ON scans(classification);
CREATE INDEX IF NOT EXISTS idx_reports_category ON reports(category);
