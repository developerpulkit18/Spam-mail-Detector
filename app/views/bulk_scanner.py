"""
Bulk Scanner Page — CSV Upload & Batch Classification + ARIA Guide
====================================================================
"""

import os
import streamlit as st
import pandas as pd

from config import PROJECT_ROOT
from aria import aria_component, step_guide, bottom_banner, ARIA_MESSAGES

from utils.model_utils import ModelManager
from utils.keyword_scanner import scan_text
from utils.logger import log_prediction


@st.cache_resource
def _load_model():
    mp = os.path.join(PROJECT_ROOT, 'models', 'best_model.pkl')
    vp = os.path.join(PROJECT_ROOT, 'models', 'tfidf_vectorizer.pkl')
    if not os.path.exists(mp) or not os.path.exists(vp):
        return None
    try:
        return ModelManager(mp, vp)
    except Exception:
        return None


def render():
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.5rem;">
        <div class="app-title">📁 Bulk Scanner</div>
        <div class="app-subtitle">Upload a CSV file and classify hundreds of emails in one go</div>
    </div>
    <div class="gradient-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown(aria_component(ARIA_MESSAGES['bulk']), unsafe_allow_html=True)

    st.markdown(step_guide([
        ("📤", "Upload your CSV file"),
        ("⚙️", "Auto-processing begins"),
        ("📥", "Download results"),
    ], 1), unsafe_allow_html=True)

    manager = _load_model()
    if manager is None:
        st.markdown(aria_component(
            "I can't find the ML model. Run <code>python train.py</code> first!",
            "danger"
        ), unsafe_allow_html=True)
        st.stop()

    st.markdown("""
    <div class="glass-card">
        <h3>📤 Upload CSV File</h3>
        <p class="section-desc">CSV should have a column named
            <strong style="color:var(--primary);">message</strong>,
            <strong style="color:var(--primary);">text</strong>, or
            <strong style="color:var(--primary);">email</strong></p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader("Upload CSV", type=['csv'], label_visibility="collapsed")

    if uploaded is not None:
        try:
            df = pd.read_csv(uploaded)
            msg_col = None
            for col in df.columns:
                if col.lower() in ['message', 'text', 'email', 'content', 'body', 'sms']:
                    msg_col = col
                    break
            if msg_col is None:
                st.error("No message column found.")
                return

            with st.spinner(""):
                st.markdown(aria_component(
                    f"Processing {len(df)} messages... hang tight!",
                ), unsafe_allow_html=True)

                rows = []
                prog = st.progress(0)
                for i, msg in enumerate(df[msg_col].astype(str)):
                    r = manager.predict(msg)
                    kw = scan_text(msg)
                    rows.append({
                        'Message': msg[:120],
                        'Prediction': r['prediction'],
                        'Confidence': f"{r['confidence']:.1%}",
                        'Spam %': f"{r['spam_probability']:.1%}",
                        'Keyword Risk': kw['risk_level'],
                    })
                    log_prediction(msg, r['prediction'], r['confidence'],
                                   r['spam_probability'], 'batch')
                    prog.progress((i + 1) / len(df))
                prog.empty()

            rdf = pd.DataFrame(rows)
            spam_n = sum(1 for r in rows if r['Prediction'] == 'Spam')

            # ARIA reaction
            pct = spam_n / len(rows) * 100 if rows else 0
            if pct > 30:
                st.markdown(aria_component(
                    f"🚨 <strong>Alert!</strong> {spam_n} out of {len(rows)} messages "
                    f"({pct:.0f}%) are spam. That's a lot of threats!",
                    "danger"
                ), unsafe_allow_html=True)
            else:
                st.markdown(aria_component(
                    f"✅ Scan complete! Only {spam_n} out of {len(rows)} messages "
                    f"({pct:.0f}%) flagged as spam. Your inbox looks mostly clean!",
                    "success"
                ), unsafe_allow_html=True)

            c1, c2, c3 = st.columns(3)
            for col, n, lbl, color in [
                (c1, len(rows), "Total", "cyan"),
                (c2, spam_n, "Spam", "purple"),
                (c3, len(rows) - spam_n, "Legit", "green"),
            ]:
                col.markdown(f"""
                <div class="stat-card {color}">
                    <div class="stat-number" style="color:var(--text);">{n}</div>
                    <div class="stat-label">{lbl}</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("")
            st.dataframe(rdf, use_container_width=True, height=400)
            st.download_button("📥 Download CSV", rdf.to_csv(index=False),
                               "results.csv", "text/csv")

        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown(bottom_banner(), unsafe_allow_html=True)
