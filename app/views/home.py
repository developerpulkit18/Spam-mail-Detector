"""
Home Page — Spam Detection with ARIA Guide
============================================
"""

import os
import time
import streamlit as st

from config import PROJECT_ROOT
from aria import aria_component, step_guide, bottom_banner, ARIA_MESSAGES

from utils.model_utils import ModelManager
from utils.explainability import explain_prediction
from utils.keyword_scanner import scan_text
from utils.logger import log_prediction
import joblib


@st.cache_resource
def _load_model():
    model_path = os.path.join(PROJECT_ROOT, 'models', 'best_model.pkl')
    vectorizer_path = os.path.join(PROJECT_ROOT, 'models', 'tfidf_vectorizer.pkl')
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        return None
    try:
        return ModelManager(model_path, vectorizer_path)
    except Exception:
        return None


@st.cache_data
def _load_metadata():
    path = os.path.join(PROJECT_ROOT, 'models', 'model_metadata.pkl')
    if os.path.exists(path):
        return joblib.load(path)
    return None


def render():
    """Render the Home page."""

    # ── Hero title ──
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.5rem;">
        <div class="app-title">🛡️ Spam Mail Detector</div>
        <div class="app-subtitle">AI-powered email classification with real-time explainability</div>
    </div>
    <div class="gradient-divider"></div>
    """, unsafe_allow_html=True)

    manager = _load_model()
    metadata = _load_metadata()

    if manager is None:
        st.markdown(aria_component(
            "I couldn't find my ML model files. Please train the model first by "
            "running <code>python train.py</code> and then reload this page!",
            "danger"
        ), unsafe_allow_html=True)
        st.stop()

    # ── ARIA greeting ──
    st.markdown(aria_component(ARIA_MESSAGES['home']), unsafe_allow_html=True)

    # ── Step guide ──
    active = 1
    if 'home_result' in st.session_state:
        active = 3
    elif st.session_state.get('_home_input', ''):
        active = 2
    st.markdown(step_guide([
        ("📋", "Paste your email message"),
        ("🔍", "Click Analyze"),
        ("📊", "View your threat report"),
    ], active), unsafe_allow_html=True)

    # ── Model info badges ──
    if metadata:
        c1, c2, c3, c4 = st.columns(4)
        badges = [
            (c1, "Model", metadata['model_name'], "cyan"),
            (c2, "Accuracy", f"{metadata['accuracy']:.1%}", "green"),
            (c3, "Precision", f"{metadata['precision']:.1%}", "blue"),
            (c4, "F1 Score", f"{metadata['f1_score']:.1%}", "purple"),
        ]
        for col, label, val, color in badges:
            col.markdown(f"""
            <div class="stat-card {color}">
                <div class="stat-label">{label}</div>
                <div style="color:var(--text);font-family:'Orbitron',monospace;
                     font-size:1rem;font-weight:600;margin-top:0.3rem;">{val}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("")

    # ── Quick test samples ──
    with st.expander("🧪 Quick Test Samples — click to auto-fill"):
        spam_samples = [
            "Congratulations! You've won a $1000 gift card! Claim NOW!",
            "URGENT: Your bank account has been compromised. Click link to verify",
            "FREE entry to win iPhone! Text WIN to 80085",
        ]
        ham_samples = [
            "Hey, are we still meeting for lunch tomorrow?",
            "Can you send me the meeting notes from today?",
            "The project deadline has been extended to next Friday",
        ]
        sc1, sc2 = st.columns(2)
        with sc1:
            st.markdown("**🔴 Spam Examples**")
            for s in spam_samples:
                if st.button(f"📝 {s[:50]}…", key=f"qs_{hash(s)}"):
                    st.session_state._home_input = s
        with sc2:
            st.markdown("**🟢 Legitimate Examples**")
            for s in ham_samples:
                if st.button(f"📝 {s[:50]}…", key=f"qh_{hash(s)}"):
                    st.session_state._home_input = s

    # ── Input section ──
    st.markdown("""
    <div class="glass-card">
        <h3>✍️ Enter Your Message</h3>
        <p class="section-desc">
            Paste an email, SMS, or any text message below to check if it's spam
        </p>
    </div>
    """, unsafe_allow_html=True)

    default = st.session_state.pop('_home_input', '')
    user_input = st.text_area(
        "Message Input",
        value=default,
        height=150,
        placeholder="Type or paste your message here…\n\nExample: Congratulations! You've won a free vacation. Click here to claim!",
        label_visibility="collapsed",
    )

    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        check = st.button("🔍  Analyze Message", use_container_width=True)

    # ── Prediction ──
    if check and user_input.strip():
        with st.spinner(""):
            holder = st.empty()
            holder.markdown(aria_component(
                "Scanning your message with AI... please wait.",
            ), unsafe_allow_html=True)
            time.sleep(0.6)
            result = manager.predict(user_input)
            holder.empty()

        # Log prediction
        log_prediction(
            text=user_input,
            prediction=result['prediction'],
            confidence=result['confidence'],
            spam_probability=result['spam_probability'],
            source='single',
        )
        st.session_state.home_result = True

        # ── Result display ──
        is_spam = result['label'] == 1
        css_class = "result-spam" if is_spam else "result-ham"
        icon = "⚠️" if is_spam else "✅"
        label = "THREAT DETECTED" if is_spam else "MESSAGE IS SAFE"
        desc = ("This message has been classified as spam with high confidence."
                if is_spam else "This message appears to be legitimate and safe.")

        bar_color = ("linear-gradient(90deg,#FF4757,#ff6b7a)" if is_spam
                     else "linear-gradient(90deg,#00FF88,#50ffaa)")

        # ARIA reaction
        aria_state = "danger" if is_spam else "success"
        aria_msg = ("🚨 <strong>THREAT DETECTED!</strong> This message contains "
                    "spam indicators. Be careful with any links or requests!"
                    if is_spam
                    else "✅ <strong>ALL CLEAR!</strong> This message appears to be "
                    "safe and legitimate. No threats detected!")

        st.markdown(aria_component(aria_msg, aria_state), unsafe_allow_html=True)

        st.markdown(f"""
        <div class="{css_class}">
            <div class="result-icon">{icon}</div>
            <div class="result-label">{label}</div>
            <p style="color:{'#ff9999' if is_spam else '#88ffcc'};font-size:0.95rem;">{desc}</p>
            <div class="confidence-bar-container">
                <div class="confidence-bar-fill"
                     style="width:{result['confidence']*100}%;background:{bar_color};"></div>
            </div>
            <div class="confidence-text">Confidence: {result['confidence']:.1%}</div>
            <div class="prob-container">
                <div>
                    <div class="prob-value" style="color:var(--danger);">{result['spam_probability']:.1%}</div>
                    <div class="prob-label">Spam Probability</div>
                </div>
                <div>
                    <div class="prob-value" style="color:var(--success);">{result['ham_probability']:.1%}</div>
                    <div class="prob-label">Ham Probability</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Explainability ──
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        exp_col, kw_col = st.columns(2)

        with exp_col:
            st.markdown("""
            <div class="glass-card">
                <h3>🔬 Top Contributing Words</h3>
                <p class="section-desc">TF-IDF features that most influenced the prediction</p>
            </div>
            """, unsafe_allow_html=True)
            try:
                explanation = explain_prediction(
                    user_input, manager.vectorizer, manager.model,
                    manager.preprocessor, result['prediction'],
                )
                for feat in explanation['top_features'][:8]:
                    direction = "🔴" if feat['contribution'] > 0 else "🟢"
                    bar_width = min(abs(feat['contribution']) * 200, 100)
                    bar_bg = ("rgba(255,71,87,0.3)" if feat['contribution'] > 0
                              else "rgba(0,255,136,0.3)")
                    st.markdown(f"""
                    <div class="history-row">
                        <span style="color:var(--text);font-size:0.9rem;">
                            {direction} <strong>{feat['word']}</strong>
                            <span style="color:var(--subtext);font-size:0.78rem;">
                                (TF-IDF: {feat['tfidf_score']:.3f})
                            </span>
                        </span>
                        <div style="width:100px;height:8px;background:rgba(255,255,255,0.06);
                                    border-radius:4px;overflow:hidden;">
                            <div style="width:{bar_width}%;height:100%;background:{bar_bg};
                                        border-radius:4px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            except Exception:
                st.info("Explainability data not available for this model type.")

        with kw_col:
            st.markdown("""
            <div class="glass-card">
                <h3>🔑 Keyword Risk Scan</h3>
                <p class="section-desc">Phishing phrase detection results</p>
            </div>
            """, unsafe_allow_html=True)
            kw_result = scan_text(user_input)
            risk_cls = {
                'High': 'risk-high', 'Medium': 'risk-medium',
                'Low': 'risk-low', 'None': 'risk-none',
            }.get(kw_result['risk_level'], 'risk-none')

            st.markdown(f"""
            <div style="text-align:center;margin:0.5rem 0 1rem;">
                <span class="risk-badge {risk_cls}">
                    Risk Level: {kw_result['risk_level']}
                </span>
                <div style="color:var(--subtext);font-size:0.85rem;margin-top:0.5rem;">
                    Score: {kw_result['total_score']} &nbsp;|&nbsp;
                    Phrases matched: {len(kw_result['matched_phrases'])}
                </div>
            </div>
            """, unsafe_allow_html=True)

            if kw_result['matched_phrases']:
                for mp in kw_result['matched_phrases']:
                    sev_color = {'High': '#FF4757', 'Medium': '#ffb74d', 'Low': '#8888AA'}
                    st.markdown(f"""
                    <div class="history-row">
                        <span style="color:var(--text);font-size:0.9rem;">
                            ⚠️ "{mp['phrase']}"
                        </span>
                        <span style="color:{sev_color.get(mp['severity'], '#8888AA')};
                              font-size:0.8rem;font-weight:600;">
                            {mp['severity']}
                        </span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("✅ No phishing phrases detected!")

    elif check:
        st.warning("⚠️ Please enter a message to analyze.")

    # ── Bottom banner ──
    st.markdown(bottom_banner(), unsafe_allow_html=True)
