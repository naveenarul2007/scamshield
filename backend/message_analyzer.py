import re
from typing import Dict, Any, List
from ml_model.predict import predict_scam_probability

# Configurable rule weights
DEFAULT_WEIGHTS = {
    "otp_credential": 25,
    "financial_request": 20,
    "suspicious_url": 20,
    "urgency": 15,
    "threat_language": 15,
    "account_suspension": 20,
    "prize_reward": 15,
    "fake_support": 20,
    "job_investment_scam": 18,
    "impersonation": 15,
    "excessive_punctuation": 8,
    "all_caps_pressure": 7,
}

# Regex pattern collections
PATTERNS = {
    "otp_credential": [
        r'\b(otp|one[\s-]?time[\s-]?password|pin|cvv|password|passcode|secret code|6[\s-]?digit code)\b',
        r'\b(share|send|provide|verify|enter)\s+(your|the)?\s*(otp|pin|password|cvv|code)\b',
        r'\b(never share|do not share)\b'  # note: we check negative context
    ],
    "financial_request": [
        r'\b(transfer|wire|pay|deposit|send|credit|debit)\s+(money|funds|cash|fees?|amount|crypto|bitcoin|eth)\b',
        r'[₹$€£]\s*\d+([,\.]\d+)?',
        r'\b(rs\.?|inr|usd)\s*\d+',
        r'\b(bank account|credit card|debit card|netbanking|upi|wallet|beneficiary)\b'
    ],
    "urgency": [
        r'\b(immediately|urgent(ly)?|act fast|within\s+\d+\s*(hours?|mins?|minutes?)|right now|today|instant(ly)?|hurry|final notice|last chance|expir(es?|ing))\b',
        r'\b(do not ignore|immediate action required|time is running out)\b'
    ],
    "threat_language": [
        r'\b(suspend(ed)?|block(ed)?|terminat(ed)?|deactivat(ed)?|cancel(led)?|penalty|fine|legal action|arrest warrant|police|court summon|property seizure)\b',
        r'\b(account (will be|has been) (blocked|suspended|frozen|closed))\b'
    ],
    "account_suspension": [
        r'\b(kyc (update|expired|mandatory|verification)|pan (card)?|aadhaar|unauthorized (login|transaction|access)|security alert)\b',
        r'\b(verify (your)? (account|identity|details|profile|phone|email)|update (your)? (kyc|details|profile)|reactivate (your)? account)\b',
        r'\b(account will be (blocked|suspended|terminated|deactivated))\b'
    ],
    "link_prompt": [
        r'\b(click (this|the|here|on)?\s*(link|url|button)|use (this|the)? link|using this link|visit (this|the)? (link|url|website)|open (the|this) link)\b'
    ],
    "prize_reward": [
        r'\b(congratulations|congrats|you (have )?won|winner|lucky draw|lottery|jackpot|cashback|scratch card|reward points|claim your prize|free gift)\b',
        r'\b(selected (as|for)|exclusive reward|claim (now|within|today))\b'
    ],
    "fake_support": [
        r'\b(anydesk|teamviewer|quicksupport|remote access|download app|call (toll[\s-]?free|helpline|support)|customer care officer)\b',
        r'\b(connect with (our)? fraud prevention|security desk)\b'
    ],
    "job_investment_scam": [
        r'\b(work from home|part[\s-]?time (job|work)|daily (income|earning|payout)|earn ₹\s*\d+|guaranteed (returns?|profit)|crypto signals?|vip signals?)\b',
        r'\b(rate hotels|like youtube videos|simple typing|telegram (group|channel)|no experience)\b'
    ],
    "impersonation": [
        r'\b(customs (department|officer)|income tax (department|refund)|rbi|national crime bureau|ncb|police department|cyber cell|irs)\b',
        r'\b(sbi|hdfc|icici|axis bank|paytm|phonepe|netflix|amazon security|apple id|paypal security)\b'
    ]
}

SUSPICIOUS_DOMAINS_REGEX = r'(https?://|www\.)[^\s/$.?#].[^\s]*'
SHORTENER_DOMAINS = ['bit.ly', 'tinyurl.com', 'is.gd', 'cutt.ly', 't.co', 'rb.gy', 't.me', 'wa.me']
SUSPICIOUS_TLDS = ['.xyz', '.top', '.club', '.work', '.click', '.buzz', '.cc', '.info', '.link', '.online']

def analyze_message_content(text: str, weights: Dict[str, int] = None) -> Dict[str, Any]:
    """
    Hybrid analysis engine combining weighted rule detection and ML model probability.
    """
    if not text or not text.strip():
        return {
            "risk_score": 0,
            "classification": "SAFE",
            "risk_level": "LOW",
            "indicators": ["Empty message provided"],
            "factors": [],
            "recommendation": "Provide message text for scam analysis."
        }

    active_weights = dict(DEFAULT_WEIGHTS)
    if weights:
        active_weights.update(weights)

    factors: List[Dict[str, Any]] = []
    indicators: List[str] = []
    text_lower = text.lower()

    raw_rule_score = 0

    # 1. Check for OTP & Credential Requests
    # Note: Check if message is a legitimate bank warning like "Do not share OTP" vs scam "Share OTP"
    has_otp_word = bool(re.search(r'\b(otp|pin|password|cvv|passcode)\b', text_lower))
    is_safe_warning = bool(re.search(r'\b(never share|do not share|never disclose|bank never asks)\b', text_lower))
    
    if has_otp_word:
        if is_safe_warning and not bool(re.search(r'\b(send|provide|reply with|verify your)\s+(otp|pin|cvv)\b', text_lower)):
            # It's an informational or legitimate 2FA warning
            factors.append({
                "factor": "Security OTP Notice",
                "points": 0,
                "reason": "Standard security warning detected ('Never share your OTP')",
                "matches": ["never share OTP"]
            })
        else:
            matches = re.findall(r'\b(otp|pin|password|cvv|passcode|6[\s-]?digit code)\b', text_lower)
            pts = active_weights["otp_credential"]
            raw_rule_score += pts
            indicators.append("Requests confidential credentials (OTP / PIN / Password)")
            factors.append({
                "factor": "Credential / OTP Request",
                "points": pts,
                "reason": "Asks for sensitive security authentication credentials",
                "matches": list(set(matches))
            })

    # 2. Financial / Payment Requests
    fin_matches = []
    for pat in PATTERNS["financial_request"]:
        found = re.findall(pat, text_lower)
        if found:
            fin_matches.extend([m if isinstance(m, str) else m[0] for m in found])
    if fin_matches:
        pts = active_weights["financial_request"]
        raw_rule_score += pts
        indicators.append("Financial transaction / banking terminology detected")
        factors.append({
            "factor": "Financial / Banking Trigger",
            "points": pts,
            "reason": "Contains mentions of money transfers, card details, or banking actions",
            "matches": list(set(fin_matches))[:4]
        })

    # 3. Urgency & Time Pressure
    urgency_matches = []
    for pat in PATTERNS["urgency"]:
        found = re.findall(pat, text_lower)
        if found:
            urgency_matches.extend([m if isinstance(m, str) else m[0] for m in found])
    if urgency_matches:
        pts = active_weights["urgency"]
        raw_rule_score += pts
        indicators.append("Urgent time-pressure tactics detected")
        factors.append({
            "factor": "Urgency & Coercion",
            "points": pts,
            "reason": "Forces immediate action to prevent rational verification",
            "matches": list(set(urgency_matches))[:4]
        })

    # 4. Threats & Punitive Language
    threat_matches = []
    for pat in PATTERNS["threat_language"]:
        found = re.findall(pat, text_lower)
        if found:
            threat_matches.extend([m if isinstance(m, str) else m[0] for m in found])
    if threat_matches:
        pts = active_weights["threat_language"]
        raw_rule_score += pts
        indicators.append("Threatening or punitive language detected")
        factors.append({
            "factor": "Threat / Coercive Language",
            "points": pts,
            "reason": "Threatens account closure, legal penalty, or law enforcement action",
            "matches": list(set(threat_matches))[:4]
        })

    # 5. Account Suspension & KYC Verification
    kyc_matches = []
    for pat in PATTERNS["account_suspension"]:
        found = re.findall(pat, text_lower)
        if found:
            kyc_matches.extend([m if isinstance(m, str) else m[0] for m in found])
    if kyc_matches:
        pts = active_weights["account_suspension"]
        raw_rule_score += pts
        indicators.append("Account suspension / KYC expiry pressure")
        factors.append({
            "factor": "Account / KYC Threat",
            "points": pts,
            "reason": "Claims account will be frozen unless immediate KYC or PAN is provided",
            "matches": list(set(kyc_matches))[:4]
        })

    # 6. Prize, Reward & Lottery Claims
    prize_matches = []
    for pat in PATTERNS["prize_reward"]:
        found = re.findall(pat, text_lower)
        if found:
            prize_matches.extend([m if isinstance(m, str) else m[0] for m in found])
    if prize_matches:
        pts = active_weights["prize_reward"]
        raw_rule_score += pts
        indicators.append("Prize, reward, or lottery claim detected")
        factors.append({
            "factor": "Prize / Lottery Lure",
            "points": pts,
            "reason": "Promises unexpected cash, prizes, or lucky draw rewards to entice clicks",
            "matches": list(set(prize_matches))[:4]
        })

    # 7. Fake Support & Remote Access
    support_matches = []
    for pat in PATTERNS["fake_support"]:
        found = re.findall(pat, text_lower)
        if found:
            support_matches.extend([m if isinstance(m, str) else m[0] for m in found])
    if support_matches:
        pts = active_weights["fake_support"]
        raw_rule_score += pts
        indicators.append("Remote desktop access / Fake customer support prompt")
        factors.append({
            "factor": "Remote Access / Imposter Support",
            "points": pts,
            "reason": "Instructs installation of remote screen-sharing tools like AnyDesk/TeamViewer",
            "matches": list(set(support_matches))[:4]
        })

    # 8. Fake Job & Investment Scam
    job_matches = []
    for pat in PATTERNS["job_investment_scam"]:
        found = re.findall(pat, text_lower)
        if found:
            job_matches.extend([m if isinstance(m, str) else m[0] for m in found])
    if job_matches:
        pts = active_weights["job_investment_scam"]
        raw_rule_score += pts
        indicators.append("Unrealistic job offer or guaranteed investment returns")
        factors.append({
            "factor": "Job / Investment Scheme",
            "points": pts,
            "reason": "Promises unrealistic work-from-home earnings or guaranteed trading returns",
            "matches": list(set(job_matches))[:4]
        })

    # 9. Impersonation of Institutions
    imp_matches = []
    for pat in PATTERNS["impersonation"]:
        found = re.findall(pat, text_lower)
        if found:
            imp_matches.extend([m if isinstance(m, str) else m[0] for m in found])
    if imp_matches and (raw_rule_score > 0):  # Impersonation is alarming when paired with other actions
        pts = active_weights["impersonation"]
        raw_rule_score += pts
        indicators.append("Potential impersonation of known institution or brand")
        factors.append({
            "factor": "Brand / Authority Impersonation",
            "points": pts,
            "reason": "References recognized brands, government departments, or financial institutions",
            "matches": list(set(imp_matches))[:4]
        })

    # 10. Links and URLs within text
    found_urls = re.findall(SUSPICIOUS_DOMAINS_REGEX, text)
    link_prompt_matches = []
    for pat in PATTERNS.get("link_prompt", []):
        found = re.findall(pat, text_lower)
        if found:
            link_prompt_matches.extend([m if isinstance(m, str) else m[0] for m in found])

    if found_urls or link_prompt_matches:
        url_pts = active_weights["suspicious_url"]
        
        # Extra points if URL is shortened or uses suspicious TLD
        is_short = any(s in text_lower for s in SHORTENER_DOMAINS)
        is_susp_tld = any(t in text_lower for t in SUSPICIOUS_TLDS)
        
        if is_short or is_susp_tld:
            url_pts += 5
            indicators.append("Contains shortened or suspicious domain extension (.top, .xyz, bit.ly)")
        elif found_urls:
            indicators.append("Contains external link requesting user click")
        else:
            indicators.append("Prompts user to click or follow an unverified link")

        raw_rule_score += url_pts
        matches_preview = [f[:40] for f in found_urls] if found_urls else link_prompt_matches
        factors.append({
            "factor": "Link Action Request",
            "points": url_pts,
            "reason": "Pressures user to open an external link for verification or claiming rewards",
            "matches": matches_preview[:3]
        })

    # 11. Excessive punctuation / casing
    exclamation_count = text.count('!')
    if exclamation_count >= 3:
        pts = active_weights["excessive_punctuation"]
        raw_rule_score += pts
        factors.append({
            "factor": "Excessive Punctuation",
            "points": pts,
            "reason": "High frequency of exclamation marks indicates emotional manipulation",
            "matches": [f"{exclamation_count} exclamation marks"]
        })

    words = text.split()
    caps_words = [w for w in words if len(w) > 3 and w.isupper() and w.isalpha()]
    if len(caps_words) >= 2:
        pts = active_weights["all_caps_pressure"]
        raw_rule_score += pts
        factors.append({
            "factor": "Aggressive Capitalization",
            "points": pts,
            "reason": "Capitalized words used to create false authority and alarm",
            "matches": caps_words[:4]
        })

    # Query the Machine Learning model
    ml_prob, ml_top_features = predict_scam_probability(text)
    ml_contribution = None
    if ml_prob is not None:
        ml_score = int(round(ml_prob * 100))
        ml_contribution = {
            "ml_probability": round(ml_prob, 3),
            "ml_score": ml_score,
            "key_features": ml_top_features
        }

    # Normalize rule score to max 100
    normalized_rule_score = min(100, raw_rule_score)

    # Hybrid blending:
    # If ML model is available, blend 55% ML + 45% Rule Score, or take maximum if strong scam signals exist
    if ml_prob is not None:
        blended_score = int(round(0.45 * normalized_rule_score + 0.55 * (ml_prob * 100)))
        # Safety floor: if critical rules (like OTP theft or urgency+link) trigger strongly, don't let ML dilute it
        if normalized_rule_score >= 60:
            final_risk_score = max(normalized_rule_score, blended_score)
        elif normalized_rule_score <= 15 and ml_prob < 0.3:
            final_risk_score = min(normalized_rule_score, blended_score)
        else:
            final_risk_score = blended_score
    else:
        final_risk_score = normalized_rule_score

    # Bound 0-100
    final_risk_score = max(0, min(100, final_risk_score))

    # Classification
    if final_risk_score >= 60:
        classification = "LIKELY SCAM"
        risk_level = "HIGH"
        recommendation = (
            "Do not click links or provide passwords, OTPs, PINs or banking information. "
            "Verify the request through the organization's official website or customer support helpline."
        )
    elif final_risk_score >= 30:
        classification = "SUSPICIOUS"
        risk_level = "MEDIUM"
        recommendation = (
            "Exercise caution. This message contains typical promotional or pressure tactics. "
            "Do not disclose confidential personal details or transfer money without independent verification."
        )
    else:
        classification = "SAFE"
        risk_level = "LOW"
        recommendation = (
            "No significant scam or phishing indicators were detected. "
            "Always remain vigilant when receiving unsolicited communications."
        )

    if not indicators:
        indicators.append("No immediate threats or high-risk patterns detected")

    return {
        "risk_score": final_risk_score,
        "classification": classification,
        "risk_level": risk_level,
        "indicators": indicators,
        "factors": factors,
        "ml_analysis": ml_contribution,
        "recommendation": recommendation
    }
