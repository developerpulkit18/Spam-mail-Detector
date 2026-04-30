"""
Domain Detection Module for Spam Mail & Threat Intelligence System
===================================================================
Extracts URLs from text, analyzes them for suspicious characteristics,
assigns risk scores, and classifies each domain as Safe or Suspicious.

Two scoring methods:
  1. Heuristic Analysis — rule-based feature scoring (always available)
  2. ML Prediction — Random Forest trained on UCI Phishing Websites
     dataset (96.6% accuracy, 30 features). Used when the model is loaded.

The final classification merges both signals.
"""

import os
import re
from urllib.parse import urlparse

import joblib
import numpy as np


# ─── Paths ────────────────────────────────────────────────────────────────────
_MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_MODULE_DIR)
_MODEL_DIR = os.path.join(_PROJECT_ROOT, 'models')

# ─── Suspicious keyword list ─────────────────────────────────────────────────
SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'bank', 'secure', 'update', 'free', 'win',
    'account', 'password', 'confirm', 'click', 'urgent', 'suspend',
    'alert', 'prize', 'reward', 'offer', 'gift', 'lucky', 'claim',
    'paypal', 'ebay', 'netflix', 'apple', 'microsoft', 'amazon',
]

# ─── ML Model (lazy-loaded singleton) ────────────────────────────────────────
_phishing_model = None
_phishing_features = None
_phishing_metadata = None


def _load_phishing_model():
    """Load the Random Forest phishing model (once)."""
    global _phishing_model, _phishing_features, _phishing_metadata

    if _phishing_model is not None:
        return True  # already loaded

    model_path = os.path.join(_MODEL_DIR, 'phishing_rf_model.pkl')
    feat_path = os.path.join(_MODEL_DIR, 'phishing_feature_names.pkl')
    meta_path = os.path.join(_MODEL_DIR, 'phishing_model_metadata.pkl')

    if not os.path.exists(model_path) or not os.path.exists(feat_path):
        return False

    try:
        _phishing_model = joblib.load(model_path)
        _phishing_features = joblib.load(feat_path)
        if os.path.exists(meta_path):
            _phishing_metadata = joblib.load(meta_path)
        return True
    except Exception:
        return False


def get_phishing_model_metadata() -> dict:
    """Return metadata for the loaded phishing model, or None."""
    _load_phishing_model()
    return _phishing_metadata


# ─── URL extraction ──────────────────────────────────────────────────────────

def extract_urls(text: str) -> list:
    """
    Extract all URLs from the given text.

    Supports http://, https://, and www. prefixed URLs.
    """
    url_pattern = re.compile(
        r'(?:https?://[^\s<>"\']+|www\.[^\s<>"\']+)',
        re.IGNORECASE
    )
    urls = url_pattern.findall(text)
    cleaned = []
    for url in urls:
        url = url.rstrip('.,;:!?)]}>\'\"')
        if url:
            cleaned.append(url)
    return cleaned


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _is_ip_address(hostname: str) -> bool:
    """Check if the hostname is a raw IPv4 address."""
    ipv4 = re.compile(r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$')
    m = ipv4.match(hostname)
    return bool(m) and all(0 <= int(g) <= 255 for g in m.groups())


def _encode_feature(value: bool, invert: bool = False) -> int:
    """Encode a boolean feature to -1 (phishing) / 1 (legitimate).
    The UCI dataset uses: -1 = phishing indicator, 1 = legitimate.
    If `invert` is True, True maps to 1 (legitimate)."""
    if invert:
        return 1 if value else -1
    return -1 if value else 1


def _extract_ml_features(url: str) -> dict:
    """
    Extract the 30 features expected by the phishing RF model from a URL.

    Many features require page-level inspection (DOM, SSL certificate,
    WHOIS, etc.) which we cannot do from a URL string alone. For those
    features we use 0 (suspicious / unknown) as a neutral default so
    the model still works meaningfully with the URL-level features we
    *can* extract.

    Features we CAN compute from the URL string:
      - having_IPhaving_IP_Address
      - URLURL_Length
      - having_At_Symbol
      - Prefix_Suffix (hyphen in domain)
      - having_Sub_Domain
      - HTTPS_token (https in domain part)
      - double_slash_redirecting
      - Shortining_Service

    All others default to 0 (unknown).
    """
    normalized = url if url.startswith(('http://', 'https://')) else 'http://' + url
    try:
        parsed = urlparse(normalized)
        domain = parsed.hostname or ''
        path = parsed.path or ''
    except Exception:
        domain = ''
        path = ''

    # --- Compute extractable features ---

    # 1. IP address in URL
    has_ip = -1 if _is_ip_address(domain) else 1

    # 2. URL length: >75 chars = -1, 54-75 = 0, <54 = 1
    length = len(url)
    url_len_feat = -1 if length > 75 else (0 if length > 54 else 1)

    # 3. Shortening service
    shorteners = ['bit.ly', 'tinyurl', 'goo.gl', 't.co', 'ow.ly',
                  'is.gd', 'buff.ly', 'j.mp', 'rebrand.ly']
    is_shortened = -1 if any(s in url.lower() for s in shorteners) else 1

    # 4. @ symbol
    has_at = -1 if '@' in url else 1

    # 5. Double-slash redirecting (// after position 7)
    dbl_slash = -1 if '//' in url[7:] else 1

    # 6. Prefix-Suffix (hyphen in domain)
    has_hyphen = -1 if '-' in domain else 1

    # 7. Sub-domain count: 1 dot = 1 (legit), 2 = 0, 3+ = -1
    dot_count = domain.count('.') if domain else 0
    sub_domain_feat = 1 if dot_count <= 1 else (0 if dot_count == 2 else -1)

    # 8. HTTPS token in domain part (not scheme)
    https_in_domain = -1 if 'https' in domain.lower() else 1

    # Build full 30-feature vector in dataset order
    feature_vector = {
        'having_IPhaving_IP_Address': has_ip,
        'URLURL_Length': url_len_feat,
        'Shortining_Service': is_shortened,
        'having_At_Symbol': has_at,
        'double_slash_redirecting': dbl_slash,
        'Prefix_Suffix': has_hyphen,
        'having_Sub_Domain': sub_domain_feat,
        'SSLfinal_State': 0,                   # cannot determine from URL
        'Domain_registeration_length': 0,       # needs WHOIS
        'Favicon': 0,                           # needs page load
        'port': 0,                              # assume standard
        'HTTPS_token': https_in_domain,
        'Request_URL': 0,                       # needs page load
        'URL_of_Anchor': 0,                     # needs page load
        'Links_in_tags': 0,                     # needs page load
        'SFH': 0,                               # needs page load
        'Submitting_to_email': 0,               # needs page load
        'Abnormal_URL': 0,                      # needs WHOIS
        'Redirect': 0,                          # needs HTTP follow
        'on_mouseover': 0,                      # needs DOM
        'RightClick': 0,                        # needs DOM
        'popUpWidnow': 0,                       # needs DOM
        'Iframe': 0,                            # needs DOM
        'age_of_domain': 0,                     # needs WHOIS
        'DNSRecord': 0,                         # needs DNS
        'web_traffic': 0,                       # needs Alexa/API
        'Page_Rank': 0,                         # needs API
        'Google_Index': 0,                       # needs API
        'Links_pointing_to_page': 0,            # needs backlink API
        'Statistical_report': 0,                # needs report DB
    }

    return feature_vector


def _predict_phishing(url: str) -> dict:
    """
    Run the ML phishing model on a single URL.

    Returns dict with ml_prediction, ml_confidence, ml_probability,
    ml_features used, or None if model is unavailable.
    """
    if not _load_phishing_model():
        return None

    features_dict = _extract_ml_features(url)

    # Build vector in the same column order as training
    vector = np.array(
        [features_dict.get(f, 0) for f in _phishing_features],
        dtype=float
    ).reshape(1, -1)

    prediction = _phishing_model.predict(vector)[0]
    probas = _phishing_model.predict_proba(vector)[0]
    phishing_prob = float(probas[1])  # class 1 = phishing
    legit_prob = float(probas[0])     # class 0 = legitimate
    confidence = float(max(probas))

    return {
        'ml_prediction': 'Phishing' if prediction == 1 else 'Legitimate',
        'ml_label': int(prediction),
        'ml_phishing_prob': round(phishing_prob, 4),
        'ml_legit_prob': round(legit_prob, 4),
        'ml_confidence': round(confidence, 4),
        'ml_features_used': features_dict,
    }


# ─── Main analysis ──────────────────────────────────────────────────────────

def analyze_url(url: str) -> dict:
    """
    Analyze a single URL with both heuristic scoring and ML prediction.

    Returns a dict combining:
      - Heuristic features (url_length, dots, @, hyphen, IP, keywords)
      - Heuristic risk_score (0-100)
      - ML prediction (Phishing / Legitimate / N/A)
      - ML confidence & probabilities
      - Final merged classification
    """
    # ── Parse URL ──
    normalized = url if url.startswith(('http://', 'https://')) else 'http://' + url
    try:
        parsed = urlparse(normalized)
        domain = parsed.hostname or ''
    except Exception:
        domain = ''

    # ── Heuristic feature extraction ──
    url_length = len(url)
    num_dots = url.count('.')
    has_at_symbol = '@' in url
    has_hyphen = '-' in domain
    uses_ip = _is_ip_address(domain)

    url_lower = url.lower()
    suspicious_keywords_found = [
        kw for kw in SUSPICIOUS_KEYWORDS if kw in url_lower
    ]

    # ── Heuristic risk score (0-100) ──
    risk_score = 0.0

    if url_length > 75:
        risk_score += 15
    elif url_length > 54:
        risk_score += 8

    if num_dots > 4:
        risk_score += 20
    elif num_dots > 3:
        risk_score += 10

    if has_at_symbol:
        risk_score += 20

    if has_hyphen:
        risk_score += 10

    if uses_ip:
        risk_score += 25

    risk_score += min(len(suspicious_keywords_found) * 8, 30)

    if not url.startswith('https://'):
        risk_score += 5

    risk_score = min(max(risk_score, 0), 100)

    # ── ML prediction ──
    ml_result = _predict_phishing(url)

    # ── Merge heuristic + ML into final classification ──
    heuristic_suspicious = risk_score >= 40

    if ml_result:
        ml_phishing = ml_result['ml_label'] == 1
        ml_conf = ml_result['ml_confidence']

        # If ML is confident (>70%), trust ML; otherwise blend
        if ml_conf >= 0.70:
            final_classification = 'Phishing' if ml_phishing else 'Legitimate'
        else:
            # Both agree → use that; disagree → "Suspicious"
            if ml_phishing and heuristic_suspicious:
                final_classification = 'Phishing'
            elif not ml_phishing and not heuristic_suspicious:
                final_classification = 'Legitimate'
            else:
                final_classification = 'Suspicious'

        # Adjust risk_score with ML probability
        ml_risk_component = ml_result['ml_phishing_prob'] * 100
        combined_score = round(0.4 * risk_score + 0.6 * ml_risk_component, 1)
        combined_score = min(max(combined_score, 0), 100)
    else:
        final_classification = 'Suspicious' if heuristic_suspicious else 'Safe'
        combined_score = round(risk_score, 1)

    result = {
        'url': url,
        'domain': domain,
        'url_length': url_length,
        'num_dots': num_dots,
        'has_at_symbol': has_at_symbol,
        'has_hyphen': has_hyphen,
        'uses_ip': uses_ip,
        'suspicious_keywords_found': suspicious_keywords_found,
        'heuristic_score': round(risk_score, 1),
        'risk_score': combined_score,
        'classification': final_classification,
    }

    # Attach ML fields if model was used
    if ml_result:
        result['ml_prediction'] = ml_result['ml_prediction']
        result['ml_phishing_prob'] = ml_result['ml_phishing_prob']
        result['ml_legit_prob'] = ml_result['ml_legit_prob']
        result['ml_confidence'] = ml_result['ml_confidence']
    else:
        result['ml_prediction'] = 'N/A'
        result['ml_phishing_prob'] = None
        result['ml_legit_prob'] = None
        result['ml_confidence'] = None

    return result


def analyze_text(text: str) -> dict:
    """
    Extract all URLs from text and analyze each one.

    Returns:
      - urls_found: int
      - results: list of analysis dicts
      - overall_risk: 'Low' / 'Medium' / 'High'
      - ml_model_loaded: bool
    """
    urls = extract_urls(text)
    results = [analyze_url(u) for u in urls]

    if not results:
        overall_risk = 'Low'
    else:
        max_score = max(r['risk_score'] for r in results)
        if max_score >= 60:
            overall_risk = 'High'
        elif max_score >= 40:
            overall_risk = 'Medium'
        else:
            overall_risk = 'Low'

    return {
        'urls_found': len(results),
        'results': results,
        'overall_risk': overall_risk,
        'ml_model_loaded': _phishing_model is not None,
    }
