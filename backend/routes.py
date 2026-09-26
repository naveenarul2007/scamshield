import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename

from backend.message_analyzer import analyze_message_content
from backend.url_analyzer import analyze_url_target
from backend.ocr_engine import extract_text_from_image, check_ocr_availability
from ml_model.predict import get_model_info
from database.db import (
    save_scan, get_all_scans, get_scan_by_id, delete_scan, clear_all_scans,
    save_report, get_all_reports, get_analytics
)

api = Blueprint("api", __name__, url_prefix="/api")

def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@api.route("/health", methods=["GET"])
def health_check():
    ocr_ok, ocr_path = check_ocr_availability()
    return jsonify({
        "status": "healthy",
        "service": "ScamShield API",
        "version": "1.0.0",
        "ocr_available": ocr_ok,
        "ocr_path": ocr_path
    })

@api.route("/analyze/message", methods=["POST"])
def analyze_message_endpoint():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message content cannot be empty."}), 400

    # Analyze message
    analysis = analyze_message_content(message)

    # Save to scan history
    saved = save_scan(
        scan_type="message",
        input_preview=message,
        risk_score=analysis["risk_score"],
        classification=analysis["classification"],
        risk_level=analysis["risk_level"],
        indicators=analysis["indicators"],
        factors=analysis["factors"],
        recommendation=analysis["recommendation"]
    )

    analysis["scan_id"] = saved["id"]
    analysis["created_at"] = saved["created_at"]
    return jsonify(analysis), 200

@api.route("/analyze/url", methods=["POST"])
def analyze_url_endpoint():
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "URL parameter cannot be empty."}), 400

    analysis = analyze_url_target(url)

    saved = save_scan(
        scan_type="url",
        input_preview=url,
        risk_score=analysis["risk_score"],
        classification=analysis["classification"],
        risk_level=analysis["risk_level"],
        indicators=analysis["indicators"],
        factors=analysis["factors"],
        recommendation=analysis["recommendation"]
    )

    analysis["scan_id"] = saved["id"]
    analysis["created_at"] = saved["created_at"]
    return jsonify(analysis), 200

@api.route("/analyze/screenshot", methods=["POST"])
def analyze_screenshot_endpoint():
    # Check if a built-in sample screenshot was requested
    sample_name = request.form.get("sample_name") or (request.get_json(silent=True) or {}).get("sample_name")
    
    if sample_name:
        sample_path = os.path.join(current_app.root_path, "..", "static", "samples", sample_name)
        if not os.path.exists(sample_path):
            sample_path = os.path.join(current_app.root_path, "static", "samples", sample_name)
            
        ocr_result = extract_text_from_image(sample_path, filename=sample_name)
        if not ocr_result["success"]:
            return jsonify({
                "success": False,
                "error": ocr_result.get("error", "Failed to extract text from sample.")
            }), 400
            
        extracted_text = ocr_result["text"]
        analysis = analyze_message_content(extracted_text)
        
        saved = save_scan(
            scan_type="screenshot",
            input_preview=f"[Sample: {sample_name}] " + extracted_text,
            risk_score=analysis["risk_score"],
            classification=analysis["classification"],
            risk_level=analysis["risk_level"],
            indicators=analysis["indicators"],
            factors=analysis["factors"],
            recommendation=analysis["recommendation"]
        )

        analysis["scan_id"] = saved["id"]
        analysis["created_at"] = saved["created_at"]
        analysis["extracted_text"] = extracted_text
        analysis["ocr_method"] = ocr_result.get("method", "Sample Extraction")
        return jsonify(analysis), 200

    # Handle file upload
    if "screenshot" not in request.files:
        return jsonify({"error": "No screenshot file provided in request."}), 400

    file = request.files["screenshot"]
    if file.filename == '':
        return jsonify({"error": "No selected file."}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "error": "Unsupported file format. Please upload PNG, JPG, JPEG, or WEBP image."
        }), 400

    # Save securely
    ext = file.filename.rsplit('.', 1)[1].lower()
    safe_name = f"{uuid.uuid4().hex}.{ext}"
    dest_path = os.path.join(current_app.config['UPLOAD_FOLDER'], safe_name)
    file.save(dest_path)

    try:
        ocr_result = extract_text_from_image(dest_path, filename=file.filename)
        if not ocr_result["success"]:
            return jsonify({
                "success": False,
                "error": ocr_result.get("error", "OCR failed to extract readable text."),
                "ocr_available": ocr_result.get("ocr_available", True)
            }), 400

        extracted_text = ocr_result["text"]
        analysis = analyze_message_content(extracted_text)

        saved = save_scan(
            scan_type="screenshot",
            input_preview=f"[Screenshot] " + extracted_text,
            risk_score=analysis["risk_score"],
            classification=analysis["classification"],
            risk_level=analysis["risk_level"],
            indicators=analysis["indicators"],
            factors=analysis["factors"],
            recommendation=analysis["recommendation"]
        )

        analysis["scan_id"] = saved["id"]
        analysis["created_at"] = saved["created_at"]
        analysis["extracted_text"] = extracted_text
        analysis["ocr_method"] = ocr_result.get("method", "OCR")
        return jsonify(analysis), 200

    finally:
        # Clean up temporary uploaded file to preserve privacy and storage
        if os.path.exists(dest_path):
            try:
                os.remove(dest_path)
            except Exception:
                pass

@api.route("/scans", methods=["GET"])
def get_scans_endpoint():
    limit = request.args.get("limit", default=50, type=int)
    scan_type = request.args.get("scan_type", default=None, type=str)
    risk_level = request.args.get("risk_level", default=None, type=str)

    scans = get_all_scans(limit=limit, scan_type=scan_type, risk_level=risk_level)
    return jsonify({"scans": scans, "count": len(scans)}), 200

@api.route("/scans/<int:scan_id>", methods=["GET"])
def get_scan_detail_endpoint(scan_id: int):
    scan = get_scan_by_id(scan_id)
    if not scan:
        return jsonify({"error": "Scan record not found"}), 404
    return jsonify(scan), 200

@api.route("/scans/<int:scan_id>", methods=["DELETE"])
def delete_scan_endpoint(scan_id: int):
    success = delete_scan(scan_id)
    if not success:
        return jsonify({"error": "Scan record not found or already deleted"}), 404
    return jsonify({"message": f"Scan #{scan_id} deleted successfully."}), 200

@api.route("/scans/clear", methods=["POST"])
def clear_all_scans_endpoint():
    clear_all_scans()
    return jsonify({"message": "All scan history cleared."}), 200

@api.route("/reports", methods=["POST"])
def submit_report_endpoint():
    data = request.get_json(silent=True) or {}
    category = data.get("category", "").strip()
    description = data.get("description", "").strip()
    url = data.get("url", "").strip()
    scam_type = data.get("scam_type", "").strip()

    if not category or not description:
        return jsonify({"error": "Category and description are required fields."}), 400

    report = save_report(
        category=category,
        description=description,
        url=url,
        scam_type=scam_type or category
    )

    return jsonify({
        "message": "Scam report successfully submitted for community review.",
        "report": report
    }), 201

@api.route("/reports", methods=["GET"])
def get_reports_endpoint():
    limit = request.args.get("limit", default=50, type=int)
    reports = get_all_reports(limit=limit)
    return jsonify({"reports": reports, "count": len(reports)}), 200

@api.route("/stats", methods=["GET"])
def get_stats_endpoint():
    analytics = get_analytics()
    model_info = get_model_info()
    return jsonify({
        "analytics": analytics,
        "model_info": model_info
    }), 200

@api.route("/demo-samples", methods=["GET"])
def get_demo_samples():
    """Return pre-configured test cases for hackathon jury evaluation."""
    return jsonify({
        "messages": [
            {
                "id": "case-1",
                "title": "Test Case 1: Lottery / Prize Scam",
                "text": "Congratulations! You won ₹50,000. Click this link immediately to claim your prize.",
                "expected": "LIKELY SCAM",
                "category": "Prize Scam"
            },
            {
                "id": "case-2",
                "title": "Test Case 2: Bank Account Suspension Threat",
                "text": "Your account will be suspended today. Verify your identity using this link.",
                "expected": "LIKELY SCAM",
                "category": "Banking"
            },
            {
                "id": "case-3",
                "title": "Test Case 3: Legitimate University Notice",
                "text": "Your appointment with the college office is confirmed for tomorrow at 10 AM.",
                "expected": "SAFE",
                "category": "Legitimate"
            },
            {
                "id": "case-4",
                "title": "Test Case 4: Urgent Electricity Disconnection",
                "text": "Dear Customer, your electricity power will be disconnected tonight at 9:30 PM because previous month bill was not paid. Contact electricity officer immediately on 9876543210.",
                "expected": "LIKELY SCAM",
                "category": "Utility Scam"
            }
        ],
        "urls": [
            {
                "id": "url-1",
                "title": "Phishing Banking Portal",
                "url": "http://sbi-pan-update.top/verify-login?id=82910",
                "expected": "LIKELY SCAM"
            },
            {
                "id": "url-2",
                "title": "Brand Impersonation / Typosquatting",
                "url": "http://paypa1-account-resolution.xyz/login",
                "expected": "LIKELY SCAM"
            },
            {
                "id": "url-3",
                "title": "Direct IP Login Host",
                "url": "http://192.168.1.50/paypal-security-check",
                "expected": "LIKELY SCAM"
            },
            {
                "id": "url-4",
                "title": "Legitimate Official Domain",
                "url": "https://google.com",
                "expected": "SAFE"
            }
        ],
        "screenshots": [
            {
                "id": "screen-1",
                "title": "SBI KYC Expiry SMS Alert",
                "file": "sample_scam_banking.png",
                "url": "/static/samples/sample_scam_banking.png",
                "expected": "LIKELY SCAM"
            },
            {
                "id": "screen-2",
                "title": "KBC ₹50,000 Prize Winner Notification",
                "file": "sample_scam_lottery.png",
                "url": "/static/samples/sample_scam_lottery.png",
                "expected": "LIKELY SCAM"
            },
            {
                "id": "screen-3",
                "title": "College Office Appointment Confirmation",
                "file": "sample_safe_meeting.png",
                "url": "/static/samples/sample_safe_meeting.png",
                "expected": "SAFE"
            }
        ]
    })
