"""
ScamShield Entry Point
ALGOTHON'26 - Real-Time Digital Scam Detection & Protection Platform
"""
import os
import sys

# Ensure root is in path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from backend.app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5001))
    print("=" * 65)
    print("  🛡️  ScamShield – Real-Time Scam Detection Platform")
    print(f"  🚀  Server running at: http://127.0.0.1:{port}")
    print("  ⭐  ALGOTHON'26 Production Build")
    print("=" * 65)
    app.run(host="0.0.0.0", port=port, debug=True)
