"""
Domain Analyzer Page — ML Phishing Detection + ARIA Guide
============================================================
"""

import os
import streamlit as st

from config import PROJECT_ROOT
from aria import aria_component, step_guide, bottom_banner, ARIA_MESSAGES

from utils.domain_detector import analyze_text, get_phishing_model_metadata


def render():
    """Render the Domain Analyzer page."""

    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.5rem;">
        <div class="app-title">🌐 Domain Analyzer</div>
        <div class="app-subtitle">ML-powered phishing detection &amp; heuristic URL risk scoring</div>
    </div>
    <div class="gradient-divider"></div>
    """, unsafe_allow_html=True)

    # ── ARIA greeting ──
    st.markdown(aria_component(ARIA_MESSAGES['domain']), unsafe_allow_html=True)

    # ── Step guide ──
    st.markdown(step_guide([
        ("🔗", "Paste text with URLs"),
        ("🔍", "Click Scan URLs"),
        ("📋", "Review threat analysis"),
    ], 1), unsafe_allow_html=True)

    # ── ML model info ──
    meta = get_phishing_model_metadata()
    if meta:
        mc1, mc2, mc3, mc4 = st.columns(4)
        for col, lbl, val, color in [
            (mc1, "ML Model", meta['model_name'], "cyan"),
            (mc2, "Accuracy", f"{meta['accuracy']:.1%}", "green"),
            (mc3, "F1-Score", f"{meta['f1_score']:.1%}", "blue"),
            (mc4, "Features", str(meta['n_features']), "purple"),
        ]:
            col.markdown(f"""
            <div class="stat-card {color}">
                <div class="stat-label">{lbl}</div>
                <div style="color:var(--text);font-family:'Orbitron',monospace;
                     font-size:1rem;font-weight:600;margin-top:0.3rem;">{val}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("")
    else:
        st.warning(
            "ML phishing model not loaded. Run `py train_phishing_model.py` "
            "to train it. Heuristic scoring will still work."
        )

    # ── Input ──
    st.markdown("""
    <div class="glass-card">
        <h3>🔗 Paste Text with URLs</h3>
        <p class="section-desc">Enter any text containing URLs — the system will extract and score each one</p>
    </div>
    """, unsafe_allow_html=True)

    text = st.text_area(
        "URL Input", height=150,
        placeholder="Paste email body or message here...\n\nExample: Please verify your account at http://secure-login.fakebank.com/verify?user=admin",
        label_visibility="collapsed",
    )

    _, btn_col, _ = st.columns([1, 2, 1])
    with btn_col:
        scan = st.button("🔍  Scan URLs", use_container_width=True)

    if scan and text.strip():
        with st.spinner("Scanning URLs with ML model..."):
            analysis = analyze_text(text)

        if analysis['urls_found'] == 0:
            st.markdown(aria_component(
                "I couldn't find any URLs in the text you provided. "
                "Try pasting a full email body or message that contains links!",
            ), unsafe_allow_html=True)
            return

        # ── Summary ──
        risk_cls = {
            'High': 'risk-high', 'Medium': 'risk-medium', 'Low': 'risk-low',
        }.get(analysis['overall_risk'], 'risk-none')

        model_tag = (
            '<span class="feature-pill" style="background:rgba(0,255,136,0.1);'
            'border-color:rgba(0,255,136,0.3);color:#00FF88;">ML Active</span>'
            if analysis['ml_model_loaded']
            else '<span class="feature-pill">Heuristic Only</span>'
        )

        st.markdown(f"""
        <div style="text-align:center;margin:1rem 0;">
            <span class="risk-badge {risk_cls}" style="font-size:1rem;padding:0.5rem 1.5rem;">
                Overall Risk: {analysis['overall_risk']}
            </span>
            <div style="color:var(--subtext);font-size:0.9rem;margin-top:0.6rem;">
                {analysis['urls_found']} URL(s) detected &nbsp;&bull;&nbsp; {model_tag}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ARIA reaction
        if analysis['overall_risk'] == 'High':
            st.markdown(aria_component(
                "🚨 <strong>WARNING!</strong> I detected high-risk phishing indicators "
                "in one or more URLs. Do NOT click these links!",
                "danger"
            ), unsafe_allow_html=True)
        elif analysis['overall_risk'] == 'Low':
            st.markdown(aria_component(
                "✅ <strong>Looking good!</strong> These URLs appear to be safe. "
                "No major phishing indicators detected.",
                "success"
            ), unsafe_allow_html=True)

        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

        # ── Per-URL cards ──
        for i, r in enumerate(analysis['results']):
            cls = r['classification']
            is_danger = cls in ('Phishing', 'Suspicious')
            card_cls = "metric-card-suspicious" if is_danger else "metric-card-safe"
            icon = "🔴" if cls == 'Phishing' else ("🟡" if cls == 'Suspicious' else "🟢")
            score_color = ("#FF4757" if r['risk_score'] >= 60
                           else "#ffb74d" if r['risk_score'] >= 40
                           else "#00FF88")

            ml_badge = ""
            if r.get('ml_prediction') and r['ml_prediction'] != 'N/A':
                ml_color = "#FF4757" if r['ml_prediction'] == 'Phishing' else "#00FF88"
                ml_badge = (
                    f'<span style="background:rgba(255,255,255,0.04);'
                    f'border:1px solid {ml_color};color:{ml_color};'
                    f'padding:0.2rem 0.7rem;border-radius:20px;font-size:0.78rem;'
                    f'font-weight:600;margin-left:0.5rem;">'
                    f'ML: {r["ml_prediction"]} ({r["ml_phishing_prob"]:.0%})</span>'
                )

            st.markdown(f"""
            <div class="metric-card {card_cls}">
                <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;">
                    <div style="flex:1;min-width:200px;">
                        <div style="color:var(--text);font-weight:600;font-size:1rem;word-break:break-all;">
                            {icon} {r['url']}
                        </div>
                        <div style="color:var(--subtext);font-size:0.82rem;margin-top:0.2rem;">
                            Domain: <strong style="color:#ccc;">{r['domain'] or 'N/A'}</strong>
                            {ml_badge}
                        </div>
                    </div>
                    <div class="risk-score-circle" style="border:3px solid {score_color};color:{score_color};">
                        {r['risk_score']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander(f"Details — {r['domain'] or r['url'][:40]}", expanded=False):
                st.markdown("##### Heuristic Features")
                fc1, fc2, fc3 = st.columns(3)
                fc1.metric("URL Length", r['url_length'])
                fc2.metric("Dots (.)", r['num_dots'])
                fc3.metric("Heuristic Score", r['heuristic_score'])

                fc4, fc5, fc6 = st.columns(3)
                fc4.metric("Has @", "Yes" if r['has_at_symbol'] else "No")
                fc5.metric("Has Hyphen", "Yes" if r['has_hyphen'] else "No")
                fc6.metric("Uses IP", "Yes" if r['uses_ip'] else "No")

                if r['suspicious_keywords_found']:
                    kw_pills = " ".join(
                        f'<span class="feature-pill" style="border-color:rgba(255,71,87,0.3);'
                        f'color:#ff9999;">{kw}</span>'
                        for kw in r['suspicious_keywords_found']
                    )
                    st.markdown(f'<div style="margin-top:0.5rem;">'
                                f'<span style="color:var(--subtext);font-size:0.85rem;">'
                                f'Suspicious keywords:</span><br>{kw_pills}</div>',
                                unsafe_allow_html=True)
                else:
                    st.success("No suspicious keywords found.")

                if r.get('ml_prediction') and r['ml_prediction'] != 'N/A':
                    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
                    st.markdown("##### ML Prediction (Random Forest)")
                    ml1, ml2, ml3 = st.columns(3)
                    ml1.metric("Prediction", r['ml_prediction'])
                    ml2.metric("Phishing Prob", f"{r['ml_phishing_prob']:.1%}")
                    ml3.metric("Confidence", f"{r['ml_confidence']:.1%}")

                    phish_pct = r['ml_phishing_prob'] * 100
                    bar_c = "#FF4757" if phish_pct >= 60 else "#ffb74d" if phish_pct >= 40 else "#00FF88"
                    st.markdown(f"""
                    <div style="margin-top:0.5rem;">
                        <div style="display:flex;justify-content:space-between;font-size:0.8rem;color:var(--subtext);">
                            <span>Legitimate ({r['ml_legit_prob']:.0%})</span>
                            <span>Phishing ({r['ml_phishing_prob']:.0%})</span>
                        </div>
                        <div style="background:rgba(255,255,255,0.06);border-radius:6px;height:10px;overflow:hidden;margin-top:0.3rem;">
                            <div style="width:{phish_pct}%;height:100%;background:{bar_c};border-radius:6px;"></div>
                        </div>
                        <div style="margin-top:0.5rem;color:var(--subtext);font-size:0.82rem;">
                            <strong>Combined:</strong> {r['risk_score']} (40% heuristic + 60% ML) &rarr;
                            <strong style="color:var(--text);">{r['classification']}</strong>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    elif scan:
        st.warning("Please paste some text containing URLs.")

    st.markdown(bottom_banner(), unsafe_allow_html=True)
