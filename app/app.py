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
# This JS runs once per page load. It checks if the sidebar is collapsed
# and, if so, clicks the native Streamlit toggle button to expand it.
# It also creates a visible MENU button in the parent DOM as a fallback.
import streamlit.components.v1 as components
components.html("""
<script>
(function() {
    var p = window.parent.document;

    // --- 1. Force-open sidebar on page load ---
    function forceOpen() {
        var sb = p.querySelector('[data-testid="stSidebar"]');
        if (sb && sb.getAttribute('aria-expanded') !== 'true') {
            // Try clicking the native toggle
            var toggle = p.querySelector('[data-testid="stSidebarCollapsedControl"] button')
                      || p.querySelector('button[aria-label="Open sidebar"]');
            if (toggle) {
                toggle.click();
                return;
            }
            // Fallback: directly set styles to force sidebar visible
            sb.setAttribute('aria-expanded', 'true');
            sb.style.width = '300px';
            sb.style.minWidth = '300px';
            sb.style.transform = 'none';
            sb.style.marginLeft = '0';
            // Also show the sidebar content div
            var inner = sb.querySelector('[data-testid="stSidebarContent"]')
                     || sb.firstElementChild;
            if (inner) {
                inner.style.width = '300px';
                inner.style.opacity = '1';
                inner.style.visibility = 'visible';
            }
        }
    }
    forceOpen();
    // Retry a few times (Streamlit renders async)
    setTimeout(forceOpen, 300);
    setTimeout(forceOpen, 800);
    setTimeout(forceOpen, 1500);

    // --- 2. Inject floating MENU button as fallback ---
    if (!p.getElementById('ariaMenuBtn')) {
        var btn = p.createElement('div');
        btn.id = 'ariaMenuBtn';
        btn.innerHTML = '<span style="font-size:1.5rem;line-height:1;">&#9776;</span>'
                      + '<span style="font-size:0.55rem;letter-spacing:2px;">MENU</span>';
        btn.style.cssText =
            'position:fixed;left:14px;top:50%;transform:translateY(-50%);z-index:999998;' +
            'background:linear-gradient(135deg,rgba(0,212,255,0.22),rgba(123,47,255,0.22));' +
            'border:2px solid rgba(0,212,255,0.45);border-radius:14px;padding:12px 14px;' +
            'cursor:pointer;color:#00D4FF;font-family:Orbitron,monospace;font-weight:700;' +
            'letter-spacing:1px;backdrop-filter:blur(12px);' +
            'box-shadow:0 0 22px rgba(0,212,255,0.18);transition:all 0.3s ease;' +
            'display:flex;flex-direction:column;align-items:center;gap:5px;opacity:0;pointer-events:none;';

        btn.onmouseenter = function() {
            btn.style.background = 'linear-gradient(135deg,rgba(0,212,255,0.4),rgba(123,47,255,0.4))';
            btn.style.boxShadow = '0 0 35px rgba(0,212,255,0.4)';
        };
        btn.onmouseleave = function() {
            btn.style.background = 'linear-gradient(135deg,rgba(0,212,255,0.22),rgba(123,47,255,0.22))';
            btn.style.boxShadow = '0 0 22px rgba(0,212,255,0.18)';
        };
        btn.onclick = function() {
            forceOpen();
        };
        p.body.appendChild(btn);

        // Show/hide based on sidebar state
        setInterval(function() {
            var sb = p.querySelector('[data-testid="stSidebar"]');
            if (!sb) return;
            var expanded = sb.getAttribute('aria-expanded');
            if (expanded === 'true') {
                btn.style.opacity = '0';
                btn.style.pointerEvents = 'none';
            } else {
                btn.style.opacity = '1';
                btn.style.pointerEvents = 'auto';
            }
        }, 400);
    }
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
        <p style="color:#555;font-size:0.7rem;">
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
