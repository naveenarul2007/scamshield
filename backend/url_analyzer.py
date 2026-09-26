import re
import math
from urllib.parse import urlparse
from typing import Dict, Any, List

SUSPICIOUS_TLDS = {
    '.xyz': 25, '.top': 25, '.work': 20, '.click': 20, '.loan': 25,
    '.cc': 20, '.buzz': 20, '.fit': 20, '.gq': 25, '.tk': 25,
    '.ml': 25, '.ga': 25, '.cf': 25, '.surf': 20, '.rest': 20,
    '.cfd': 25, '.club': 15, '.online': 15, '.site': 15, '.info': 15
}

SHORTENER_DOMAINS = {
    'bit.ly', 'tinyurl.com', 'is.gd', 'cutt.ly', 't.co', 'rb.gy',
    'ow.ly', 'buff.ly', 'adf.ly', 'shorturl.at', 'bl.ink'
}

SUSPICIOUS_URL_KEYWORDS = [
    'login', 'signin', 'verify', 'verification', 'secure', 'security',
    'update', 'account', 'banking', 'kyc', 'pan', 'aadhaar', 'claim',
    'reward', 'winner', 'prize', 'refund', 'support', 'bonus', 'wallet',
    'confirm', 'reactivate', 'authenticate', 'billing', 'invoice', 'free'
]

TARGET_BRANDS = [
    'paypal', 'netflix', 'amazon', 'apple', 'microsoft', 'google',
    'sbi', 'hdfc', 'icici', 'axis', 'paytm', 'phonepe', 'whatsapp',
    'facebook', 'instagram', 'chase', 'wellsfargo', 'bankofamerica'
]

# Common typosquatting substitutions (e.g. paypa1, micr0soft)
TYPO_SUBS = {
    '0': 'o', '1': 'l', '3': 'e', '5': 's', '8': 'b', 'v': 'u', '@': 'a'
}

def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy to identify randomly generated domain names (DGA)."""
    if not text:
        return 0.0
    prob = [float(text.count(c)) / len(text) for c in set(text)]
    return - sum([p * math.log(p) / math.log(2.0) for p in prob])

def analyze_url_target(raw_url: str) -> Dict[str, Any]:
    """
    Comprehensive heuristic analyzer for suspicious URLs.
    """
    if not raw_url or not raw_url.strip():
        return {
            "risk_score": 0,
            "classification": "SAFE",
            "risk_level": "LOW",
            "indicators": ["Empty URL provided"],
            "factors": [],
            "recommendation": "Please enter a valid URL to analyze."
        }

    raw_url = raw_url.strip()
    # Normalize protocol if omitted
    has_explicit_scheme = raw_url.startswith(('http://', 'https://'))
    test_url = raw_url if has_explicit_scheme else f"http://{raw_url}"

    try:
        parsed = urlparse(test_url)
    except Exception:
        return {
            "risk_score": 90,
            "classification": "LIKELY SCAM",
            "risk_level": "HIGH",
            "indicators": ["Malformed URL syntax"],
            "factors": [{"factor": "Syntax Error", "points": 90, "reason": "Malformed or unparseable URL"}],
            "recommendation": "Do not attempt to open this malformed link."
        }

    hostname = (parsed.hostname or "").lower()
    path = parsed.path.lower()
    query = parsed.query.lower()
    full_url = raw_url.lower()

    factors: List[Dict[str, Any]] = []
    indicators: List[str] = []
    total_score = 0

    # 1. Protocol / HTTPS check
    # Heuristic note: Lack of HTTPS is a risk factor, but NOT standalone proof of scam
    if not has_explicit_scheme:
        indicators.append("⚠ No protocol specified (defaulting to unencrypted HTTP inspection)")
        total_score += 10
        factors.append({
            "factor": "Missing Scheme",
            "points": 10,
            "reason": "URL lacked https:// prefix"
        })
    elif parsed.scheme == 'http':
        indicators.append("⚠ Unencrypted HTTP protocol (no SSL/TLS encryption)")
        total_score += 20
        factors.append({
            "factor": "Unencrypted HTTP",
            "points": 20,
            "reason": "Connection is unencrypted; transmitted credentials can be intercepted"
        })
    elif parsed.scheme == 'https':
        indicators.append("✓ HTTPS enabled (SSL/TLS transport encryption present)")

    # 2. IP Address check
    ip_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ip_pattern, hostname):
        pts = 40
        total_score += pts
        indicators.append("✗ Direct IP address host instead of registered domain name")
        factors.append({
            "factor": "IP Host Address",
            "points": pts,
            "reason": f"Direct IP host ({hostname}) bypasses DNS reputation and domain registration scrutiny"
        })

    # 3. Suspicious or Free TLD check
    matched_tld = None
    for tld, pts in SUSPICIOUS_TLDS.items():
        if hostname.endswith(tld):
            matched_tld = tld
            total_score += pts
            indicators.append(f"⚠ High-risk / suspicious domain extension ({tld})")
            factors.append({
                "factor": "High-Risk TLD",
                "points": pts,
                "reason": f"Domain uses '{tld}', frequently leveraged by phishing campaigns due to low-cost or anonymous registration"
            })
            break

    # 4. URL Shortener detection
    if hostname in SHORTENER_DOMAINS:
        pts = 25
        total_score += pts
        indicators.append(f"⚠ URL shortening service detected ({hostname})")
        factors.append({
            "factor": "URL Shortener Masking",
            "points": pts,
            "reason": "URL shorteners conceal the true destination hostname and path"
        })

    # 5. @ Symbol abuse (credential trick in URLs)
    if '@' in test_url:
        pts = 35
        total_score += pts
        indicators.append("✗ Contains '@' symbol, which can mask the true destination authority")
        factors.append({
            "factor": "URL Authority Confusion (@ symbol)",
            "points": pts,
            "reason": "Browsers treat text before '@' as user credentials, loading the host after '@'"
        })

    # 6. Excessive Subdomains
    subdomains = hostname.split('.')
    # e.g., if subdomain count > 3 (like a.b.c.example.com)
    if len(subdomains) > 3 and not re.match(ip_pattern, hostname):
        pts = 18
        total_score += pts
        indicators.append(f"⚠ Multiple subdomains detected ({len(subdomains)-2} levels deep)")
        factors.append({
            "factor": "Excessive Subdomains",
            "points": pts,
            "reason": f"Host '{hostname}' uses deep nested subdomains commonly used to mimic legitimate infrastructure"
        })

    # 7. Brand Impersonation / Typosquatting in hostname
    found_brand = None
    for brand in TARGET_BRANDS:
        # Check direct substring in hostname (excluding genuine domain)
        if brand in hostname:
            # Check if it's the actual legitimate domain
            if hostname == f"{brand}.com" or hostname.endswith(f".{brand}.com"):
                continue  # legitimate brand domain
            else:
                found_brand = brand
                pts = 30
                total_score += pts
                indicators.append(f"✗ Potential brand impersonation detected for '{brand.upper()}'")
                factors.append({
                    "factor": "Brand Impersonation in Hostname",
                    "points": pts,
                    "reason": f"Hostname '{hostname}' embeds brand name '{brand}' on an unofficial domain"
                })
                break
        
        # Check leetspeak / typosquatting (e.g. paypa1, micr0soft)
        normalized_host = hostname
        for char, repl in TYPO_SUBS.items():
            normalized_host = normalized_host.replace(char, repl)
        
        if brand in normalized_host and brand not in hostname:
            pts = 35
            total_score += pts
            indicators.append(f"✗ Typosquatting / character substitution mimicking '{brand.upper()}'")
            factors.append({
                "factor": "Typosquatting Mimicry",
                "points": pts,
                "reason": f"Host uses lookalike character substitutions to deceive visitors"
            })
            break

    # 8. Suspicious security / banking keywords in URL
    matched_keywords = [kw for kw in SUSPICIOUS_URL_KEYWORDS if kw in (path + query or hostname)]
    if matched_keywords:
        # If combined with unofficial domain or high-risk TLD, assign points
        pts = min(25, len(matched_keywords) * 10)
        total_score += pts
        indicators.append(f"⚠ Suspicious action keywords in URL: {', '.join(matched_keywords[:4])}")
        factors.append({
            "factor": "Phishing Keywords in Path",
            "points": pts,
            "reason": "URL targets sensitive authentication or verification workflows",
            "matches": matched_keywords[:4]
        })

    # 9. Length checks
    if len(raw_url) > 75:
        pts = 10
        total_score += pts
        indicators.append(f"⚠ Unusually long URL ({len(raw_url)} characters)")
        factors.append({
            "factor": "Excessive URL Length",
            "points": pts,
            "reason": f"URL length ({len(raw_url)} chars) exceeds normal threshold (>75 chars)"
        })

    # 10. Shannon Entropy / DGA domain check
    domain_part = subdomains[-2] if len(subdomains) >= 2 else hostname
    entropy = calculate_entropy(domain_part)
    if len(domain_part) >= 10 and entropy > 3.8:
        pts = 15
        total_score += pts
        indicators.append(f"⚠ High algorithmic randomness in domain name (Entropy: {entropy:.2f})")
        factors.append({
            "factor": "Domain Generation Algorithm (DGA) Heuristic",
            "points": pts,
            "reason": "Domain name displays unusually high character randomness typical of automated malware infrastructure"
        })

    # Normalize score
    final_score = min(100, max(0, total_score))

    # Classification
    if final_score >= 60:
        classification = "LIKELY SCAM"
        risk_level = "HIGH"
        recommendation = (
            "Do NOT visit this link or input any personal or login credentials. "
            "The destination exhibits critical characteristics of a malicious phishing or credential-harvesting page."
        )
    elif final_score >= 30:
        classification = "SUSPICIOUS"
        risk_level = "MEDIUM"
        recommendation = (
            "Caution advised. This URL exhibits suspicious attributes (such as unencrypted HTTP, atypical TLD, or redirection). "
            "Verify the official website independently before proceeding."
        )
    else:
        classification = "SAFE"
        risk_level = "LOW"
        recommendation = (
            "No high-risk phishing indicators or malicious URL patterns were detected. "
            "Always inspect the browser address bar to ensure you are on the intended website."
        )

    return {
        "url": raw_url,
        "hostname": hostname,
        "risk_score": final_score,
        "classification": classification,
        "risk_level": risk_level,
        "indicators": indicators,
        "factors": factors,
        "recommendation": recommendation,
        "heuristic_notice": "Heuristic analysis evaluates domain structure, security attributes, and behavioral patterns."
    }
