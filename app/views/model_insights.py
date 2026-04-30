"""
Model Insights Page — Performance Metrics + ARIA Guide
========================================================
"""

import os
import streamlit as st
import joblib
import numpy as np

from config import PROJECT_ROOT, MODEL_DIR
from aria import aria_component, step_guide, bottom_banner, ARIA_MESSAGES


@st.cache_data
def _load_metadata():
    path = os.path.join(MODEL_DIR, 'model_metadata.pkl')
    if os.path.exists(path):
        return joblib.load(path)
    return None


def render():
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.5rem;">
        <div class="app-title">🤖 Model Insights</div>
        <div class="app-subtitle">Performance metrics, confusion matrix &amp; model comparison</div>
    </div>
    <div class="gradient-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown(aria_component(ARIA_MESSAGES['model']), unsafe_allow_html=True)

    meta = _load_metadata()
    if meta is None:
        st.markdown(aria_component(
            "Model metadata not found. Run <code>python train.py</code> first!",
            "danger"
        ), unsafe_allow_html=True)
        st.stop()

    # ═══════════════════════════════════════════════════════════════
    # ── Spam Detection Model ──
    # ═══════════════════════════════════════════════════════════════
    st.markdown(f"""
    <div class="glass-card" style="text-align:center;">
        <div style="font-family:'Orbitron',monospace;font-size:1.3rem;font-weight:700;
             color:var(--text);margin-bottom:0.3rem;">
            Spam Detection Model:
            <span style="color:var(--primary);">{meta['model_name']}</span>
        </div>
        <div style="color:var(--subtext);font-size:0.8rem;">Email/SMS spam classification</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    for col, name, val, color in [
        (c1, "Accuracy", meta['accuracy'], "green"),
        (c2, "Precision", meta['precision'], "blue"),
        (c3, "Recall", meta['recall'], "cyan"),
        (c4, "F1-Score", meta['f1_score'], "purple"),
    ]:
        pct = val * 100
        glow = "#00FF88" if pct >= 90 else "#ffb74d" if pct >= 80 else "#FF4757"
        col.markdown(f"""
        <div class="stat-card {color}">
            <div class="stat-number" style="color:{glow};">{pct:.1f}%</div>
            <div class="stat-label">{name}</div>
            <div style="margin-top:0.5rem;">
                <div style="background:rgba(255,255,255,0.06);border-radius:6px;height:8px;overflow:hidden;">
                    <div style="width:{pct}%;height:100%;background:{glow};border-radius:6px;"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # ── Confusion matrix + comparison images ──
    cm_path = os.path.join(MODEL_DIR, 'confusion_matrices.png')
    comp_path = os.path.join(MODEL_DIR, 'model_comparison.png')

    img1, img2 = st.columns(2)
    with img1:
        st.markdown('<div class="glass-card"><h3>📊 Confusion Matrices</h3></div>',
                    unsafe_allow_html=True)
        if os.path.exists(cm_path):
            st.image(cm_path, use_container_width=True)
        else:
            st.info("Confusion matrix image not found.")
    with img2:
        st.markdown('<div class="glass-card"><h3>📈 Model Comparison</h3></div>',
                    unsafe_allow_html=True)
        if os.path.exists(comp_path):
            st.image(comp_path, use_container_width=True)
        else:
            st.info("Model comparison image not found.")

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    # ── Metric Definitions ──
    st.markdown("""
    <div class="glass-card">
        <h3 style="margin-bottom:0.8rem;">📖 Metric Definitions</h3>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:1rem;">
            <div class="metric-card">
                <strong style="color:var(--primary);">Accuracy</strong>
                <p style="color:var(--subtext);font-size:0.85rem;margin-top:0.3rem;">
                    Percentage of all predictions that were correct.</p>
            </div>
            <div class="metric-card">
                <strong style="color:var(--primary);">Precision</strong>
                <p style="color:var(--subtext);font-size:0.85rem;margin-top:0.3rem;">
                    Of messages flagged as spam, how many actually were spam.</p>
            </div>
            <div class="metric-card">
                <strong style="color:var(--primary);">Recall</strong>
                <p style="color:var(--subtext);font-size:0.85rem;margin-top:0.3rem;">
                    Of all actual spam messages, how many were correctly caught.</p>
            </div>
            <div class="metric-card">
                <strong style="color:var(--primary);">F1-Score</strong>
                <p style="color:var(--subtext);font-size:0.85rem;margin-top:0.3rem;">
                    Harmonic mean of precision and recall — balanced metric.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── TF-IDF Vocabulary ──
    vec_path = os.path.join(MODEL_DIR, 'tfidf_vectorizer.pkl')
    if os.path.exists(vec_path):
        vec = joblib.load(vec_path)
        vocab_size = len(vec.vocabulary_)
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <h3>🔤 TF-IDF Vectorizer</h3>
            <div class="stat-number" style="color:var(--primary);">{vocab_size:,}</div>
            <div class="stat-label">features in vocabulary</div>
            <div style="color:var(--subtext);font-size:0.85rem;margin-top:0.5rem;">
                n-gram range: {vec.ngram_range} &nbsp;|&nbsp;
                max features: {vec.max_features or 'unlimited'}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ═══════════════════════════════════════════════════════════════
    # ── Phishing URL Model ──
    # ═══════════════════════════════════════════════════════════════
    phishing_meta_path = os.path.join(MODEL_DIR, 'phishing_model_metadata.pkl')
    if os.path.exists(phishing_meta_path):
        pmeta = joblib.load(phishing_meta_path)

        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
            <div style="font-family:'Orbitron',monospace;font-size:1.3rem;font-weight:700;
                 color:var(--text);margin-bottom:0.3rem;">
                Phishing URL Model:
                <span style="color:#7B2FFF;">{pmeta['model_name']}</span>
            </div>
            <div style="color:var(--subtext);font-size:0.8rem;">
                Trained on UCI Phishing Websites &mdash;
                11,055 URLs &times; {pmeta['n_features']} features
            </div>
        </div>
        """, unsafe_allow_html=True)

        pc1, pc2, pc3, pc4 = st.columns(4)
        for col, name, val, color in [
            (pc1, "Accuracy",  pmeta['accuracy'], "green"),
            (pc2, "Precision", pmeta['precision'], "blue"),
            (pc3, "Recall",    pmeta['recall'], "cyan"),
            (pc4, "F1-Score",  pmeta['f1_score'], "purple"),
        ]:
            pct = val * 100
            glow = "#00FF88" if pct >= 90 else "#ffb74d" if pct >= 80 else "#FF4757"
            col.markdown(f"""
            <div class="stat-card {color}">
                <div class="stat-number" style="color:{glow};">{pct:.1f}%</div>
                <div class="stat-label">{name}</div>
                <div style="margin-top:0.5rem;">
                    <div style="background:rgba(255,255,255,0.06);border-radius:6px;height:8px;overflow:hidden;">
                        <div style="width:{pct}%;height:100%;background:{glow};border-radius:6px;"></div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if 'cv_mean' in pmeta:
            st.markdown(f"""
            <div style="text-align:center;margin:0.8rem 0;color:var(--subtext);font-size:0.9rem;">
                5-Fold CV: <strong style="color:var(--text);">{pmeta['cv_mean']:.2%}</strong>
                (&plusmn; {pmeta['cv_std']*2:.2%})
            </div>
            """, unsafe_allow_html=True)

        # Report plot
        phishing_plot = os.path.join(MODEL_DIR, 'phishing_model_report.png')
        if os.path.exists(phishing_plot):
            st.markdown('<div class="glass-card"><h3>📊 Phishing Model Report</h3></div>',
                        unsafe_allow_html=True)
            st.image(phishing_plot, use_container_width=True)

        # Top features
        phishing_model_path = os.path.join(MODEL_DIR, 'phishing_rf_model.pkl')
        if os.path.exists(phishing_model_path) and 'feature_names' in pmeta:
            rf_model = joblib.load(phishing_model_path)
            importances = rf_model.feature_importances_
            feat_names = pmeta['feature_names']
            indices = np.argsort(importances)[::-1]

            st.markdown('<div class="glass-card"><h3>🏆 Top 10 Phishing Features</h3></div>',
                        unsafe_allow_html=True)

            for rank, idx in enumerate(indices[:10], 1):
                pct_imp = importances[idx] * 100
                bar_w = min(pct_imp * 3, 100)
                st.markdown(f"""
                <div class="history-row">
                    <span style="color:var(--text);font-size:0.9rem;">
                        <strong style="color:var(--primary);">#{rank}</strong>
                        &nbsp;{feat_names[idx]}
                    </span>
                    <div style="display:flex;align-items:center;gap:0.5rem;">
                        <div style="width:80px;height:8px;background:rgba(255,255,255,0.06);
                                    border-radius:4px;overflow:hidden;">
                            <div style="width:{bar_w}%;height:100%;
                                        background:linear-gradient(90deg,#00D4FF,#7B2FFF);
                                        border-radius:4px;"></div>
                        </div>
                        <span style="color:var(--subtext);font-size:0.8rem;
                                     min-width:45px;text-align:right;">
                            {pct_imp:.1f}%
                        </span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown(bottom_banner(), unsafe_allow_html=True)
