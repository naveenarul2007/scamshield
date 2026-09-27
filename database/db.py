import os
import json
import sqlite3
from datetime import datetime, timezone

DB_DIR = os.path.dirname(os.path.abspath(__file__))

# Vercel's serverless environment has a read-only filesystem except for /tmp
if os.environ.get("VERCEL") == "1" or os.environ.get("VERCEL_ENV"):
    DEFAULT_SQLITE_PATH = "/tmp/scamshield.db"
else:
    DEFAULT_SQLITE_PATH = os.path.join(DB_DIR, "scamshield.db")

def get_db_connection():
    db_path = os.getenv("SQLITE_PATH", DEFAULT_SQLITE_PATH)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize SQLite database using schema.sql."""
    schema_path = os.path.join(DB_DIR, "schema.sql")
    with open(schema_path, "r") as f:
        schema = f.read()

    conn = get_db_connection()
    try:
        conn.executescript(schema)
        conn.commit()
    finally:
        conn.close()

def save_scan(scan_type: str, input_preview: str, risk_score: int, classification: str,
              risk_level: str, indicators: list, factors: list, recommendation: str) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now(timezone.utc).isoformat()
    
    # Truncate and sanitize input preview
    sanitized_preview = (input_preview[:120] + '...') if len(input_preview) > 120 else input_preview
    
    cursor.execute("""
        INSERT INTO scans (created_at, scan_type, input_preview, risk_score, classification, risk_level, indicators, factors, recommendation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        created_at,
        scan_type,
        sanitized_preview,
        risk_score,
        classification,
        risk_level,
        json.dumps(indicators or []),
        json.dumps(factors or []),
        recommendation
    ))
    scan_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "id": scan_id,
        "created_at": created_at,
        "scan_type": scan_type,
        "input_preview": sanitized_preview,
        "risk_score": risk_score,
        "classification": classification,
        "risk_level": risk_level,
        "indicators": indicators,
        "factors": factors,
        "recommendation": recommendation
    }

def get_all_scans(limit: int = 50, scan_type: str = None, risk_level: str = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM scans WHERE 1=1"
    params = []

    if scan_type and scan_type.lower() != 'all':
        query += " AND lower(scan_type) = ?"
        params.append(scan_type.lower())

    if risk_level and risk_level.lower() != 'all':
        query += " AND lower(risk_level) = ?"
        params.append(risk_level.lower())

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "created_at": r["created_at"],
            "scan_type": r["scan_type"],
            "input_preview": r["input_preview"],
            "risk_score": r["risk_score"],
            "classification": r["classification"],
            "risk_level": r["risk_level"],
            "indicators": json.loads(r["indicators"] or "[]"),
            "factors": json.loads(r["factors"] or "[]"),
            "recommendation": r["recommendation"]
        })
    return results

def get_scan_by_id(scan_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM scans WHERE id = ?", (scan_id,))
    r = cursor.fetchone()
    conn.close()

    if not r:
        return None

    return {
        "id": r["id"],
        "created_at": r["created_at"],
        "scan_type": r["scan_type"],
        "input_preview": r["input_preview"],
        "risk_score": r["risk_score"],
        "classification": r["classification"],
        "risk_level": r["risk_level"],
        "indicators": json.loads(r["indicators"] or "[]"),
        "factors": json.loads(r["factors"] or "[]"),
        "recommendation": r["recommendation"]
    }

def delete_scan(scan_id: int) -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans WHERE id = ?", (scan_id,))
    rows_affected = cursor.rowcount
    conn.commit()
    conn.close()
    return rows_affected > 0

def clear_all_scans() -> bool:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM scans")
    conn.commit()
    conn.close()
    return True

def save_report(category: str, description: str, url: str = None, scam_type: str = None) -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now(timezone.utc).isoformat()
    cursor.execute("""
        INSERT INTO reports (created_at, category, description, url, scam_type, status)
        VALUES (?, ?, ?, ?, ?, 'Pending Verification')
    """, (created_at, category, description, url or "", scam_type or category))
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return {
        "id": report_id,
        "created_at": created_at,
        "category": category,
        "description": description,
        "url": url,
        "scam_type": scam_type or category,
        "status": "Pending Verification"
    }

def get_all_reports(limit: int = 50):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()

    return [{
        "id": r["id"],
        "created_at": r["created_at"],
        "category": r["category"],
        "description": r["description"],
        "url": r["url"],
        "scam_type": r["scam_type"],
        "status": r["status"]
    } for r in rows]

def get_analytics():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM scans")
    total_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE classification = 'SAFE'")
    safe_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE classification = 'SUSPICIOUS'")
    suspicious_scans = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM scans WHERE classification = 'LIKELY SCAM'")
    scam_scans = cursor.fetchone()[0]

    cursor.execute("SELECT scan_type, COUNT(*) as count FROM scans GROUP BY scan_type")
    type_counts = {r[0]: r[1] for r in cursor.fetchall()}

    cursor.execute("SELECT category, COUNT(*) as count FROM reports GROUP BY category ORDER BY count DESC LIMIT 5")
    top_categories = [{"category": r[0], "count": r[1]} for r in cursor.fetchall()]

    conn.close()

    return {
        "total_scans": total_scans,
        "safe_scans": safe_scans,
        "suspicious_scans": suspicious_scans,
        "scam_scans": scam_scans,
        "type_breakdown": type_counts,
        "top_reported_categories": top_categories
    }
