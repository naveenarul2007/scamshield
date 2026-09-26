"""
Comprehensive Test Suite for ScamShield Platform
ALGOTHON'26 Verification Suite
"""
import os
import sys
import unittest
import json

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import create_app
from backend.message_analyzer import analyze_message_content
from backend.url_analyzer import analyze_url_target
from database.db import init_db

class TestScamShield(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_01_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("ocr_available", data)

    def test_02_message_test_case_1_prize_scam(self):
        """Case 1: 'Congratulations! You won ₹50,000. Click this link immediately to claim your prize.' -> LIKELY SCAM"""
        msg = "Congratulations! You won ₹50,000. Click this link immediately to claim your prize."
        res = self.client.post("/api/analyze/message", json={"message": msg})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["classification"], "LIKELY SCAM")
        self.assertEqual(data["risk_level"], "HIGH")
        self.assertGreaterEqual(data["risk_score"], 60)
        self.assertIn("factors", data)
        self.assertTrue(len(data["factors"]) > 0)

    def test_03_message_test_case_2_suspension_threat(self):
        """Case 2: 'Your account will be suspended today. Verify your identity using this link.' -> LIKELY SCAM"""
        msg = "Your account will be suspended today. Verify your identity using this link."
        res = self.client.post("/api/analyze/message", json={"message": msg})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["classification"], "LIKELY SCAM")
        self.assertEqual(data["risk_level"], "HIGH")
        self.assertGreaterEqual(data["risk_score"], 60)

    def test_04_message_test_case_3_college_safe(self):
        """Case 3: 'Your appointment with the college office is confirmed for tomorrow at 10 AM.' -> SAFE"""
        msg = "Your appointment with the college office is confirmed for tomorrow at 10 AM."
        res = self.client.post("/api/analyze/message", json={"message": msg})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["classification"], "SAFE")
        self.assertEqual(data["risk_level"], "LOW")
        self.assertLess(data["risk_score"], 30)

    def test_05_url_phishing_analysis(self):
        url = "http://sbi-pan-update.top/verify-login?id=82910"
        res = self.client.post("/api/analyze/url", json={"url": url})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["classification"], "LIKELY SCAM")
        self.assertGreaterEqual(data["risk_score"], 60)
        self.assertTrue(any("sbi" in str(f).lower() for f in data["factors"]))

    def test_06_url_typosquatting_analysis(self):
        url = "http://paypa1-account-resolution.xyz/login"
        res = self.client.post("/api/analyze/url", json={"url": url})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["classification"], "LIKELY SCAM")

    def test_07_url_safe_legitimate(self):
        url = "https://google.com"
        res = self.client.post("/api/analyze/url", json={"url": url})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["classification"], "SAFE")
        self.assertLess(data["risk_score"], 30)

    def test_08_screenshot_sample_pipeline(self):
        res = self.client.post("/api/analyze/screenshot", json={"sample_name": "sample_scam_banking.png"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("extracted_text", data)
        self.assertIn("SBI", data["extracted_text"])
        self.assertEqual(data["classification"], "LIKELY SCAM")

    def test_09_scans_history_and_filters(self):
        res = self.client.get("/api/scans")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("scans", data)
        self.assertGreater(data["count"], 0)

        # Filter by type
        res_msg = self.client.get("/api/scans?scan_type=message")
        self.assertEqual(res_msg.status_code, 200)

    def test_10_reports_submission_and_retrieval(self):
        report_payload = {
            "category": "Banking",
            "description": "SMS claiming debit card block from unknown 10-digit number.",
            "url": "http://fake-sbi-portal.top",
            "scam_type": "Banking SMS Scam"
        }
        res = self.client.post("/api/reports", json=report_payload)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertIn("report", data)
        self.assertEqual(data["report"]["category"], "Banking")

        # Get reports
        get_res = self.client.get("/api/reports")
        self.assertEqual(get_res.status_code, 200)
        reports_data = get_res.get_json()
        self.assertGreater(reports_data["count"], 0)

    def test_11_stats_and_analytics(self):
        res = self.client.get("/api/stats")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("analytics", data)
        self.assertIn("model_info", data)
        self.assertGreater(data["analytics"]["total_scans"], 0)

    def test_12_demo_samples_api(self):
        res = self.client.get("/api/demo-samples")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("messages", data)
        self.assertIn("urls", data)
        self.assertIn("screenshots", data)
        self.assertEqual(len(data["messages"]), 4)

if __name__ == "__main__":
    unittest.main()
