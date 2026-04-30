"""
Keyword Risk Scanner for Spam Mail & Threat Intelligence System
================================================================
Detects phishing phrases and suspicious keywords in email/message text.
Assigns a risk level (Low / Medium / High) based on the number and
severity of matched phrases.
"""


# ─── Phishing phrase database ────────────────────────────────────────────────
# Each tuple: (phrase, severity_weight)
#   severity_weight: 1 = low, 2 = medium, 3 = high

PHISHING_PHRASES = [
    # High severity (3)
    ("urgent action required", 3),
    ("your account has been compromised", 3),
    ("your account will be suspended", 3),
    ("verify your identity immediately", 3),
    ("unauthorized transaction detected", 3),
    ("confirm your password", 3),
    ("social security number", 3),
    ("bank account details", 3),

    # Medium severity (2)
    ("verify your account", 2),
    ("click below", 2),
    ("click here", 2),
    ("click the link", 2),
    ("update your information", 2),
    ("update your payment", 2),
    ("confirm your account", 2),
    ("reset your password", 2),
    ("unusual activity", 2),
    ("suspicious activity", 2),
    ("limited time offer", 2),
    ("act now", 2),
    ("respond immediately", 2),
    ("failure to respond", 2),
    ("you have been selected", 2),
    ("dear customer", 2),
    ("dear user", 2),

    # Low severity (1)
    ("congratulations", 1),
    ("winner", 1),
    ("free gift", 1),
    ("claim your prize", 1),
    ("no cost", 1),
    ("risk free", 1),
    ("you won", 1),
    ("cash prize", 1),
    ("100% free", 1),
    ("apply now", 1),
    ("sign up free", 1),
    ("exclusive deal", 1),
    ("incredible offer", 1),
    ("special promotion", 1),
    ("unsubscribe", 1),
]


def scan_text(text: str) -> dict:
    """
    Scan text for phishing keywords and phrases.

    Parameters
    ----------
    text : str
        The raw email or message text to scan.

    Returns
    -------
    dict
        - matched_phrases: list of dicts with 'phrase' and 'severity'
        - total_score: int, cumulative severity score
        - risk_level: str, 'Low', 'Medium', or 'High'
        - summary: str, human-readable summary
    """
    text_lower = text.lower()

    matched = []
    total_score = 0

    for phrase, severity in PHISHING_PHRASES:
        if phrase in text_lower:
            severity_label = {1: 'Low', 2: 'Medium', 3: 'High'}[severity]
            matched.append({
                'phrase': phrase,
                'severity': severity_label,
                'weight': severity,
            })
            total_score += severity

    # Determine overall risk level from cumulative score
    if total_score >= 8:
        risk_level = 'High'
    elif total_score >= 4:
        risk_level = 'Medium'
    elif total_score > 0:
        risk_level = 'Low'
    else:
        risk_level = 'None'

    # Build summary
    if not matched:
        summary = "No suspicious phishing phrases detected."
    else:
        summary = (
            f"Detected {len(matched)} suspicious phrase(s) "
            f"with a cumulative severity score of {total_score}. "
            f"Overall risk: {risk_level}."
        )

    return {
        'matched_phrases': matched,
        'total_score': total_score,
        'risk_level': risk_level,
        'summary': summary,
    }
