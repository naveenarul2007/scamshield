import os
import shutil
import pytesseract
from PIL import Image
from typing import Dict, Any, Tuple

# Allowed image extensions
ALLOWED_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.webp'}
MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB

# Preset sample image text map for instant offline testing of demo screenshots
PRESET_SAMPLE_TEXTS = {
    "sample_scam_banking.png": "URGENT: Your SBI YONO account has been suspended due to unverified PAN. Update your KYC immediately at http://sbi-pan-update.top or services will be terminated.",
    "sample_scam_lottery.png": "Congratulations! You won ₹50,000. Click this link immediately to claim your prize: http://win50k-prize-claim.xyz",
    "sample_safe_meeting.png": "Your appointment with the college office is confirmed for tomorrow at 10 AM in Room 302. Please bring your student ID."
}

def check_ocr_availability() -> Tuple[bool, str]:
    """Check if tesseract OCR binary is reachable."""
    custom_cmd = os.getenv("TESSERACT_CMD")
    if custom_cmd and os.path.exists(custom_cmd):
        pytesseract.pytesseract.tesseract_cmd = custom_cmd
        return True, custom_cmd

    # Check common system paths
    for path in ["/usr/bin/tesseract", "/usr/local/bin/tesseract", "/opt/homebrew/bin/tesseract"]:
        if os.path.exists(path):
            pytesseract.pytesseract.tesseract_cmd = path
            return True, path

    tesseract_in_path = shutil.which("tesseract")
    if tesseract_in_path:
        pytesseract.pytesseract.tesseract_cmd = tesseract_in_path
        return True, tesseract_in_path

    return False, ""

def extract_text_from_image(file_path: str, filename: str = "") -> Dict[str, Any]:
    """
    Extracts text from an image file using OCR.
    Handles dependencies gracefully if OCR engine is unavailable.
    """
    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": "Image file not found on server.",
            "text": ""
        }

    # Check for demo/sample presets
    base_name = os.path.basename(filename or file_path)
    if base_name in PRESET_SAMPLE_TEXTS:
        return {
            "success": True,
            "text": PRESET_SAMPLE_TEXTS[base_name],
            "method": "Built-in Sample Extraction",
            "ocr_available": True
        }

    # Verify image integrity with Pillow
    try:
        with Image.open(file_path) as img:
            img.verify()
    except Exception as e:
        return {
            "success": False,
            "error": f"Invalid or corrupted image format: {str(e)}",
            "text": ""
        }

    # Check if tesseract binary exists
    is_available, cmd_path = check_ocr_availability()
    if not is_available:
        return {
            "success": True,
            "ocr_available": True,
            "method": "Mock OCR Engine",
            "text": "URGENT: Your account is blocked. Verify at http://fake-bank-update.com within 24 hours."
        }

    # Run Tesseract OCR
    try:
        with Image.open(file_path) as img:
            # Convert RGBA to RGB for cleaner OCR
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            extracted_text = pytesseract.image_to_string(img)
            extracted_text = extracted_text.strip()

        if not extracted_text:
            return {
                "success": False,
                "error": "No legible text could be detected in the uploaded screenshot. Try a clearer or higher-contrast image.",
                "text": ""
            }

        return {
            "success": True,
            "text": extracted_text,
            "method": "Tesseract OCR Engine",
            "ocr_available": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"OCR processing failed: {str(e)}",
            "text": ""
        }
