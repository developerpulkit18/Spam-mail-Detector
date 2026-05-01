"""
Spam Mail & Threat Intelligence System — Main Application
===========================================================
Multi-page Streamlit dashboard with ARIA AI assistant.
"""

import os
import sys
import streamlit as st

# ─── Path setup ──────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, APP_DIR)

from styles import inject_css, inject_stars_and_glow
from aria import aria_sidebar_mini

# ─── Page Configuration ─────────────────────────────────────────────────────
st.set_page_config(
    page_title="Spam Mail & Threat Intelligence System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject global CSS + star background
inject_css(st)
inject_stars_and_glow(st)

# ─── Force sidebar open via JS ──────────────────────────────────────────────
# This JS continuously enforces the sidebar to stay expanded using a MutationObserver
import streamlit.components.v1 as components
components.html("""
<script>
(function() {
    var p = window.parent.document;

    function forceOpen() {
        var sb = p.querySelector('[data-testid="stSidebar"]');
        if (!sb) return;
        if (sb.getAttribute('aria-expanded') !== 'true') {
            // Force React state by clicking
            var toggle = p.querySelector('[data-testid="stSidebarCollapsedControl"] button')
                      || p.querySelector('button[aria-label="Open sidebar"]')
                      || p.querySelector('button[kind="header"]');
            if (toggle) {
                toggle.click();
            }
            // CSS Fallbacks
            sb.setAttribute('aria-expanded', 'true');
            sb.style.width = '300px';
            sb.style.minWidth = '300px';
            sb.style.transform = 'none';
            sb.style.marginLeft = '0';
            sb.style.visibility = 'visible';
            sb.style.position = 'relative';
            
            var inner = sb.querySelector('[data-testid="stSidebarContent"]') || sb.firstElementChild;
            if (inner) {
                inner.style.width = '300px';
                inner.style.opacity = '1';
                inner.style.visibility = 'visible';
            }
        }
    }

    forceOpen();
    setInterval(forceOpen, 300); // Polling as fallback

    var observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.attributeName === 'aria-expanded') {
                forceOpen();
            }
        });
    });

    function setupObserver() {
        var sb = p.querySelector('[data-testid="stSidebar"]');
        if (sb) {
            observer.observe(sb, { attributes: true });
        } else {
            setTimeout(setupObserver, 500);
        }
    }
    setupObserver();
    
    // Remove the old floating menu button if it exists
    var oldBtn = p.getElementById('ariaMenuBtn');
    if (oldBtn) oldBtn.remove();

})();
</script>
""", height=0)

# ─── Scans today helper ─────────────────────────────────────────────────────
def _scans_today():
    import pandas as pd
    from datetime import date
    log_path = os.path.join(PROJECT_ROOT, 'data', 'logs.csv')
    if not os.path.exists(log_path):
        return 0
    try:
        df = pd.read_csv(log_path)
        if 'timestamp' in df.columns:
            df['ts'] = pd.to_datetime(df['timestamp'], errors='coerce')
            today = date.today().isoformat()
            return int(df['ts'].dt.date.astype(str).eq(today).sum())
        return len(df)
    except Exception:
        return 0

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    # ARIA mini avatar
    st.markdown(aria_sidebar_mini(), unsafe_allow_html=True)

    st.markdown("---")

    # Shield logo
    st.markdown("""
    <div style="text-align:center;padding:0.3rem 0;">
        <div style="font-family:'Orbitron',monospace;font-size:1.1rem;font-weight:700;
             background:linear-gradient(135deg,#00D4FF,#7B2FFF);
             -webkit-background-clip:text;-webkit-text-fill-color:transparent;
             background-clip:text;">
            THREAT INTEL
        </div>
        <div style="color:#8888AA;font-size:0.72rem;margin-top:0.15rem;letter-spacing:1px;">
            SYSTEM v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Home — Spam Detector",
            "🌐 Domain Analyzer",
            "📁 Bulk Scanner",
            "📊 Analytics Dashboard",
            "🤖 Model Insights",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    # Tech pills
    st.markdown("""
    <div style="text-align:center;">
        <span class="feature-pill">Python</span>
        <span class="feature-pill">Scikit-learn</span>
        <span class="feature-pill">NLTK</span>
        <span class="feature-pill">TF-IDF</span>
        <span class="feature-pill">Random Forest</span>
        <span class="feature-pill">Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Scans today
    scans = _scans_today()
    st.markdown(f"""
    <div style="text-align:center;padding:0.3rem 0;">
        <div style="color:#8888AA;font-size:0.72rem;letter-spacing:1px;text-transform:uppercase;">
            Scans Today
        </div>
        <div style="font-family:'Orbitron',monospace;font-size:1.3rem;
             color:#00D4FF;font-weight:700;margin-top:0.2rem;">
            {scans}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Credits
    st.markdown("""
    <div style="text-align:center;padding:0.3rem 0;">
        <p style="color:#FFF;font-size:0.7rem;">
            Made with ❤️ by
            <span style="color:#00D4FF;">Pulkit</span>,
            <span style="color:#7B2FFF;">Raushan</span>,
            <span style="color:#00FF88;">Mahesh</span>,
            <span style="color:#00D4FF;">Khushi</span> &
            <span style="color:#7B2FFF;">Mahi</span>
        </p>
    </div>
    """, unsafe_allow_html=True)


# ─── Page Router ─────────────────────────────────────────────────────────────

if page.startswith("🏠"):
    from views.home import render
    render()
elif page.startswith("🌐"):
    from views.domain_analyzer import render
    render()
elif page.startswith("📁"):
    from views.bulk_scanner import render
    render()
elif page.startswith("📊"):
    from views.analytics_dashboard import render
    render()
elif page.startswith("🤖"):
    from views.model_insights import render
    render()
