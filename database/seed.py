import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.db import init_db, save_scan, save_report, get_analytics
from backend.message_analyzer import analyze_message_content
from backend.url_analyzer import analyze_url_target

def seed():
    init_db()
    analytics = get_analytics()
    if analytics["total_scans"] > 0:
        print(f"Database already has {analytics['total_scans']} scans. Skipping seed.")
        return

    print("Seeding initial demonstration scans and community reports...")

    # Seed Sample Messages
    sample_messages = [
        "Congratulations! You won ₹50,000 in KBC Lucky Draw. Click this link immediately to claim your prize.",
        "Your account will be suspended today. Verify your identity using this link.",
        "Your appointment with the college office is confirmed for tomorrow at 10 AM.",
        "Dear Customer, your electricity power will be disconnected tonight at 9:30 PM because previous month bill was not paid. Contact electricity officer immediately on 9876543210.",
        "Your verification code is 849201 for logging into your Google Account. Never share this OTP with anyone.",
        "URGENT: 6-digit OTP is required to cancel unauthorized debit of ₹49,999 from your HDFC account. Provide OTP to our executive immediately to prevent loss."
    ]

    for msg in sample_messages:
        analysis = analyze_message_content(msg)
        save_scan(
            scan_type="message",
            input_preview=msg,
            risk_score=analysis["risk_score"],
            classification=analysis["classification"],
            risk_level=analysis["risk_level"],
            indicators=analysis["indicators"],
            factors=analysis["factors"],
            recommendation=analysis["recommendation"]
        )

    # Seed Sample URLs
    sample_urls = [
        "http://sbi-pan-update.top/verify-login?id=82910",
        "http://paypa1-account-resolution.xyz/login",
        "https://google.com"
    ]

    for url in sample_urls:
        analysis = analyze_url_target(url)
        save_scan(
            scan_type="url",
            input_preview=url,
            risk_score=analysis["risk_score"],
            classification=analysis["classification"],
            risk_level=analysis["risk_level"],
            indicators=analysis["indicators"],
            factors=analysis["factors"],
            recommendation=analysis["recommendation"]
        )

    # Seed Sample Community Reports
    reports_data = [
        ("Banking", "Received SMS claiming my SBI debit card is blocked and asking to update PAN on an unofficial .top domain.", "http://sbi-pan-update.top", "Banking"),
        ("Prize Scam", "WhatsApp message from unknown number claiming ₹25,00,000 KBC lottery winner with fake certificate attached.", "http://win-kbc-lottery.xyz", "Prize Scam"),
        ("Job Scam", "Telegram contact offering ₹5,000/day for liking YouTube videos, asked for initial registration fee of ₹1,000.", "", "Job Scam"),
        ("OTP", "Caller impersonated bank fraud officer asking for OTP received on SMS to stop unauthorized debit.", "", "OTP"),
        ("Fake Customer Support", "Searched Google for airline refund, called customer care number which asked to install AnyDesk app.", "", "Fake Customer Support")
    ]

    for cat, desc, url, scam_type in reports_data:
        save_report(category=cat, description=desc, url=url, scam_type=scam_type)

    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed()
