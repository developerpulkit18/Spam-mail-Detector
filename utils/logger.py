"""
Prediction Logger for Spam Mail & Threat Intelligence System
=============================================================
Stores all predictions in a CSV file for analytics and dashboard
visualization.

Log fields:
- timestamp: ISO 8601 datetime of the prediction
- text: the input text (truncated to 200 chars)
- prediction: 'Spam' or 'Not Spam'
- confidence: float, 0-1
- spam_probability: float, 0-1
- source: 'single', 'batch', or 'domain'
"""

import os
import csv
from datetime import datetime

# ─── Configuration ───────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
LOG_FILE = os.path.join(DATA_DIR, 'logs.csv')

LOG_FIELDS = ['timestamp', 'text', 'prediction', 'confidence', 'spam_probability', 'source']


def _ensure_log_file():
    """Create the log file with headers if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
            writer.writeheader()


def log_prediction(text: str, prediction: str, confidence: float,
                   spam_probability: float = 0.0, source: str = 'single'):
    """
    Append a prediction record to the log file.

    Parameters
    ----------
    text : str
        The input text (will be truncated to 200 characters).
    prediction : str
        'Spam' or 'Not Spam'.
    confidence : float
        Prediction confidence (0-1).
    spam_probability : float
        Probability of being spam (0-1).
    source : str
        Source of prediction: 'single', 'batch', or 'domain'.
    """
    _ensure_log_file()

    row = {
        'timestamp': datetime.now().isoformat(),
        'text': text[:200],
        'prediction': prediction,
        'confidence': round(confidence, 4),
        'spam_probability': round(spam_probability, 4),
        'source': source,
    }

    with open(LOG_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=LOG_FIELDS)
        writer.writerow(row)


def load_logs():
    """
    Load all prediction logs from the CSV file.

    Returns
    -------
    list of dict
        Each dict represents one logged prediction.
    """
    _ensure_log_file()

    logs = []
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                row['confidence'] = float(row.get('confidence', 0))
                row['spam_probability'] = float(row.get('spam_probability', 0))
                logs.append(row)
    except Exception:
        pass

    return logs


def get_log_stats():
    """
    Compute summary statistics from prediction logs.

    Returns
    -------
    dict
        - total: int
        - spam_count: int
        - ham_count: int
        - spam_pct: float
        - avg_confidence: float
        - by_source: dict of source -> count
        - recent: list of last 20 logs
    """
    logs = load_logs()

    if not logs:
        return {
            'total': 0,
            'spam_count': 0,
            'ham_count': 0,
            'spam_pct': 0.0,
            'avg_confidence': 0.0,
            'by_source': {},
            'recent': [],
        }

    total = len(logs)
    spam_count = sum(1 for l in logs if l['prediction'] == 'Spam')
    ham_count = total - spam_count
    avg_conf = sum(l['confidence'] for l in logs) / total

    by_source = {}
    for l in logs:
        src = l.get('source', 'single')
        by_source[src] = by_source.get(src, 0) + 1

    return {
        'total': total,
        'spam_count': spam_count,
        'ham_count': ham_count,
        'spam_pct': round(spam_count / total * 100, 1) if total else 0.0,
        'avg_confidence': round(avg_conf, 4),
        'by_source': by_source,
        'recent': logs[-20:][::-1],  # Last 20, newest first
    }
