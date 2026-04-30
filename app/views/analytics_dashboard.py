"""
Analytics Dashboard Page — Charts from Prediction Logs + ARIA Guide
=====================================================================
"""

import os
import streamlit as st
import pandas as pd

from config import PROJECT_ROOT
from aria import aria_component, step_guide, bottom_banner, ARIA_MESSAGES

from utils.logger import load_logs, get_log_stats


def render():
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 0.5rem;">
        <div class="app-title">📊 Analytics Dashboard</div>
        <div class="app-subtitle">Visual insights from all prediction history</div>
    </div>
    <div class="gradient-divider"></div>
    """, unsafe_allow_html=True)

    st.markdown(aria_component(ARIA_MESSAGES['analytics']), unsafe_allow_html=True)

    stats = get_log_stats()

    if stats['total'] == 0:
        st.markdown(aria_component(
            "No prediction logs yet! Use the Spam Detector or Bulk Scanner "
            "first to generate data, then come back here for insights.",
        ), unsafe_allow_html=True)
        st.markdown(bottom_banner(), unsafe_allow_html=True)
        return

    # ── Summary cards ──
    c1, c2, c3, c4 = st.columns(4)
    for col, n, lbl, color in [
        (c1, stats['total'], "Total Scans", "cyan"),
        (c2, stats['spam_count'], "Spam Found", "purple"),
        (c3, stats['ham_count'], "Legitimate", "green"),
        (c4, f"{stats['avg_confidence']:.1%}", "Avg Confidence", "blue"),
    ]:
        col.markdown(f"""
        <div class="stat-card {color}">
            <div class="stat-number" style="color:var(--text);">{n}</div>
            <div class="stat-label">{lbl}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

    logs = load_logs()
    df = pd.DataFrame(logs)

    # ── Charts ──
    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown('<div class="glass-card"><h3>🥧 Spam vs Legitimate</h3></div>',
                    unsafe_allow_html=True)
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(5, 4))
        fig.patch.set_facecolor('#050510')
        ax.set_facecolor('#050510')
        labels = ['Spam', 'Legitimate']
        sizes = [stats['spam_count'], stats['ham_count']]
        colors = ['#FF4757', '#00FF88']
        wedges, texts, autotexts = ax.pie(
            sizes, labels=labels, colors=colors, autopct='%1.1f%%',
            startangle=90, textprops={'color': '#FFFFFF', 'fontsize': 11}
        )
        for t in autotexts:
            t.set_color('#FFFFFF')
        ax.axis('equal')
        st.pyplot(fig)
        plt.close(fig)

    with chart2:
        st.markdown('<div class="glass-card"><h3>📈 Scans by Source</h3></div>',
                    unsafe_allow_html=True)
        if stats['by_source']:
            fig2, ax2 = plt.subplots(figsize=(5, 4))
            fig2.patch.set_facecolor('#050510')
            ax2.set_facecolor('#050510')
            sources = list(stats['by_source'].keys())
            counts = list(stats['by_source'].values())
            bar_colors = ['#00D4FF', '#7B2FFF', '#00FF88', '#FF4757'][:len(sources)]
            ax2.bar(sources, counts, color=bar_colors, width=0.5, edgecolor='none')
            ax2.tick_params(colors='#8888AA')
            ax2.spines['bottom'].set_color('#8888AA')
            ax2.spines['left'].set_color('#8888AA')
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            for i, v in enumerate(counts):
                ax2.text(i, v + 0.3, str(v), ha='center', color='#FFFFFF', fontweight='bold')
            st.pyplot(fig2)
            plt.close(fig2)

    # ── Confidence distribution ──
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card"><h3>📉 Confidence Distribution</h3></div>',
                unsafe_allow_html=True)

    if 'confidence' in df.columns:
        fig3, ax3 = plt.subplots(figsize=(8, 3.5))
        fig3.patch.set_facecolor('#050510')
        ax3.set_facecolor('#050510')
        ax3.hist(df['confidence'].astype(float), bins=20,
                 color='#00D4FF', edgecolor='#7B2FFF', alpha=0.85)
        ax3.tick_params(colors='#8888AA')
        ax3.set_xlabel('Confidence', color='#8888AA')
        ax3.set_ylabel('Count', color='#8888AA')
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.spines['bottom'].set_color('#8888AA')
        ax3.spines['left'].set_color('#8888AA')
        st.pyplot(fig3)
        plt.close(fig3)

    # ── Predictions over time ──
    if 'timestamp' in df.columns:
        st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="glass-card"><h3>🕐 Predictions Over Time</h3></div>',
                    unsafe_allow_html=True)
        df['ts'] = pd.to_datetime(df['timestamp'], errors='coerce')
        df_valid = df.dropna(subset=['ts'])
        if not df_valid.empty:
            daily = df_valid.set_index('ts').resample('h')['prediction'].count().reset_index()
            daily.columns = ['Hour', 'Count']
            st.line_chart(daily.set_index('Hour'))

    # ── Recent logs ──
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card"><h3>📜 Recent Predictions</h3></div>',
                unsafe_allow_html=True)
    for log in stats['recent'][:15]:
        emoji = "🔴" if log['prediction'] == 'Spam' else "🟢"
        badge_bg = "rgba(255,71,87,0.15)" if log['prediction'] == 'Spam' else "rgba(0,255,136,0.1)"
        txt_c = "#FF4757" if log['prediction'] == 'Spam' else "#00FF88"
        st.markdown(f"""
        <div class="history-row">
            <span style="color:var(--subtext);font-size:0.85rem;">{emoji} {log['text'][:70]}</span>
            <span style="background:{badge_bg};color:{txt_c};padding:0.2rem 0.8rem;
                  border-radius:20px;font-size:0.78rem;font-weight:600;">
                {log['prediction']} ({log['confidence']:.0%})
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(bottom_banner(), unsafe_allow_html=True)
