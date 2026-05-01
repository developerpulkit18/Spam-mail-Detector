"""
Complete CSS Design System — Deep Space + ARIA Theme
=====================================================
Cinematic dark theme with animated star background,
ARIA AI assistant character, typewriter effects,
and premium glassmorphism cards.
"""


def inject_css(st):
    """Inject the full CSS design system into the Streamlit page."""
    st.markdown("""
    <style>
    /* ═══════════════════ GOOGLE FONTS ═══════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ═══════════════════ ROOT VARIABLES ═══════════════════ */
    :root {
        --bg-deep: #050510;
        --bg-surface: #0D0D1F;
        --bg-card: #12122A;
        --primary: #00D4FF;
        --secondary: #7B2FFF;
        --success: #00FF88;
        --danger: #FF4757;
        --text: #FFFFFF;
        --subtext: #8888AA;
        --border-glow: rgba(0, 212, 255, 0.15);
        --card-border: rgba(123, 47, 255, 0.2);
    }

    /* ═══════════════════ BASE OVERRIDES ═══════════════════ */
    .stApp, .main .block-container, [data-testid="stAppViewContainer"] {
        background: var(--bg-deep) !important;
        color: var(--text) !important;
        font-family: 'Inter', sans-serif !important;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    .stApp > header { background: transparent !important; }
    /* ── Sidebar panel ── FORCE ALWAYS VISIBLE ── */
    /* ── Sidebar panel ── */
    [data-testid="stSidebar"] {
        background: #0A0A1A !important;
        border-right: 1px solid rgba(0,212,255,0.12) !important;
    }
    [data-testid="stSidebar"] > div:first-child {
        background: #0A0A1A !important;
        width: 100% !important;
    }
    [data-testid="stSidebar"] * {
        color: var(--subtext) !important;
        font-family: 'Inter', sans-serif !important;
    }
    /* ── Radio nav items ── */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.15rem !important;
    }
    [data-testid="stSidebar"] .stRadio label {
        padding: 0.55rem 0.8rem !important;
        border-radius: 10px !important;
        margin: 2px 0 !important;
        transition: all 0.2s ease !important;
        cursor: pointer !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(0,212,255,0.06) !important;
    }
    [data-testid="stSidebar"] .stRadio label span {
        color: #bbb !important;
        font-size: 0.92rem !important;
    }
    [data-testid="stSidebar"] .stRadio label:hover span {
        color: var(--primary) !important;
    }
    /* checked / selected item */
    [data-testid="stSidebar"] .stRadio [data-checked="true"],
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) {
        background: rgba(0,212,255,0.1) !important;
        border-left: 3px solid var(--primary) !important;
    }
    [data-testid="stSidebar"] .stRadio [data-checked="true"] span,
    [data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:has(input:checked) span {
        color: var(--primary) !important;
        font-weight: 600 !important;
    }

    /* hide Streamlit menu & footer */
    #MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }

    /* ═══════════════════ STAR BACKGROUND ═══════════════════ */
    .star-bg {
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        z-index: -1; pointer-events: none; overflow: hidden;
    }
    .star-bg .star {
        position: absolute; border-radius: 50%; background: #fff;
        animation: twinkle linear infinite alternate;
    }
    @keyframes twinkle {
        0% { opacity: 0.1; transform: scale(0.8); }
        100% { opacity: 0.7; transform: scale(1.2); }
    }
    .ambient-glow {
        position: fixed; top: 30%; left: 50%; transform: translate(-50%, -50%);
        width: 600px; height: 600px;
        background: radial-gradient(circle, rgba(123,47,255,0.06) 0%, rgba(0,212,255,0.03) 40%, transparent 70%);
        z-index: -1; pointer-events: none;
    }

    /* ═══════════════════ TYPOGRAPHY ═══════════════════ */
    .app-title {
        font-family: 'Orbitron', monospace !important;
        font-size: 2.6rem; font-weight: 800; text-align: center;
        background: linear-gradient(135deg, #00D4FF, #7B2FFF, #00D4FF);
        background-size: 300% 300%;
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 4s ease infinite;
        margin-bottom: 0.3rem;
    }
    .app-subtitle {
        text-align: center; color: var(--subtext); font-size: 0.95rem;
        animation: fadeInUp 1.2s ease forwards;
        opacity: 0;
    }
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes fadeInUp {
        to { opacity: 1; transform: translateY(0); }
        from { opacity: 0; transform: translateY(12px); }
    }

    /* ═══════════════════ ARIA CHARACTER ═══════════════════ */
    .aria-container {
        display: flex; align-items: flex-start; gap: 1.2rem;
        padding: 1.2rem 1.5rem; margin: 1rem 0;
        background: rgba(13,13,31,0.7);
        border: 1px solid rgba(0,212,255,0.12);
        border-radius: 18px;
        backdrop-filter: blur(8px);
    }
    .aria-avatar {
        flex-shrink: 0; width: 80px; height: 80px;
        position: relative;
    }
    .aria-ring {
        position: absolute; inset: -6px; border-radius: 50%;
        border: 2px solid rgba(0,212,255,0.4);
        animation: ariaRingPulse 3s ease-in-out infinite;
    }
    @keyframes ariaRingPulse {
        0%, 100% { box-shadow: 0 0 8px rgba(0,212,255,0.2); transform: scale(1); }
        50% { box-shadow: 0 0 20px rgba(0,212,255,0.5); transform: scale(1.05); }
    }
    .aria-face {
        width: 80px; height: 80px; border-radius: 50%;
        background: linear-gradient(135deg, #0D0D2B 0%, #1A1A3E 100%);
        border: 2px solid rgba(0,212,255,0.3);
        position: relative; overflow: hidden;
        animation: ariaFloat 4s ease-in-out infinite;
        box-shadow: 0 0 30px rgba(0,212,255,0.15);
    }
    @keyframes ariaFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-6px); }
    }
    .aria-eye {
        position: absolute; width: 10px; height: 12px;
        background: var(--primary); border-radius: 50%;
        top: 30px; box-shadow: 0 0 8px var(--primary);
        animation: ariaBlink 3.5s ease-in-out infinite;
    }
    .aria-eye.left { left: 22px; }
    .aria-eye.right { right: 22px; }
    @keyframes ariaBlink {
        0%, 45%, 55%, 100% { transform: scaleY(1); }
        50% { transform: scaleY(0.05); }
    }
    .aria-mouth {
        position: absolute; bottom: 20px; left: 50%; transform: translateX(-50%);
        width: 22px; height: 3px; background: var(--primary);
        border-radius: 3px; opacity: 0.6;
    }
    .aria-antenna {
        position: absolute; top: -2px; left: 50%; transform: translateX(-50%);
        width: 2px; height: 10px; background: var(--primary);
    }
    .aria-antenna::after {
        content: ''; position: absolute; top: -4px; left: -3px;
        width: 8px; height: 8px; border-radius: 50%;
        background: var(--primary); box-shadow: 0 0 8px var(--primary);
    }
    /* Reaction states */
    .aria-face.danger { border-color: var(--danger); box-shadow: 0 0 30px rgba(255,71,87,0.3); }
    .aria-face.danger .aria-eye { background: var(--danger); box-shadow: 0 0 8px var(--danger); }
    .aria-face.danger .aria-mouth { background: var(--danger); width: 18px; height: 18px;
        border-radius: 50%; bottom: 16px; border: 2px solid var(--danger);
        background: transparent; }
    .aria-face.success { border-color: var(--success); box-shadow: 0 0 30px rgba(0,255,136,0.3); }
    .aria-face.success .aria-eye { background: var(--success); box-shadow: 0 0 8px var(--success); }
    .aria-face.success .aria-mouth { background: var(--success); width: 22px; height: 10px;
        border-radius: 0 0 12px 12px; bottom: 18px; }

    /* Chat bubble */
    .aria-bubble {
        flex: 1; padding: 1rem 1.2rem;
        background: rgba(18,18,42,0.8);
        border: 1px solid rgba(0,212,255,0.1);
        border-radius: 14px 14px 14px 2px;
        position: relative;
    }
    .aria-name {
        font-family: 'Orbitron', monospace; font-size: 0.72rem;
        color: var(--primary); font-weight: 600; letter-spacing: 1.5px;
        margin-bottom: 0.4rem;
    }
    .aria-text {
        color: #ccc; font-size: 0.92rem; line-height: 1.55;
    }

    /* ═══════════════════ STEP CARDS ═══════════════════ */
    .steps-row {
        display: flex; gap: 0.8rem; margin: 0.8rem 0 1.2rem; flex-wrap: wrap;
    }
    .step-card {
        flex: 1; min-width: 160px; padding: 0.8rem 1rem;
        background: var(--bg-card); border: 1px solid rgba(123,47,255,0.15);
        border-radius: 12px; text-align: center; font-size: 0.85rem;
        color: var(--subtext); transition: all 0.3s ease; position: relative;
    }
    .step-card.active {
        border-color: var(--primary);
        box-shadow: 0 0 15px rgba(0,212,255,0.15);
        color: var(--text);
        animation: stepPulse 2s ease-in-out infinite;
    }
    .step-card.done {
        border-color: var(--success); color: var(--success);
    }
    .step-num {
        font-family: 'Orbitron', monospace; font-weight: 700;
        font-size: 0.7rem; color: var(--secondary);
        margin-bottom: 0.3rem; letter-spacing: 1px;
    }
    @keyframes stepPulse {
        0%, 100% { box-shadow: 0 0 10px rgba(0,212,255,0.1); }
        50% { box-shadow: 0 0 25px rgba(0,212,255,0.25); }
    }

    /* ═══════════════════ GLASS CARDS ═══════════════════ */
    .glass-card {
        background: rgba(18, 18, 42, 0.6);
        border: 1px solid rgba(123,47,255,0.15);
        border-radius: 16px; padding: 1.5rem;
        backdrop-filter: blur(10px);
        margin-bottom: 1rem;
    }
    .glass-card h3 {
        font-family: 'Orbitron', monospace !important;
        font-size: 1.1rem; color: var(--text); margin: 0;
    }
    .section-desc {
        color: var(--subtext); font-size: 0.88rem; margin-top: 0.3rem;
    }

    /* ═══════════════════ STAT CARDS ═══════════════════ */
    .stat-card {
        background: var(--bg-card); border-radius: 14px; padding: 1.2rem;
        text-align: center; border: 1px solid rgba(0,212,255,0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .stat-card:hover {
        transform: scale(1.05);
        box-shadow: 0 0 25px rgba(0,212,255,0.15);
    }
    .stat-card.cyan  { border-color: rgba(0,212,255,0.25); }
    .stat-card.green { border-color: rgba(0,255,136,0.25); }
    .stat-card.blue  { border-color: rgba(100,130,255,0.25); }
    .stat-card.purple { border-color: rgba(123,47,255,0.25); }
    .stat-card:hover.cyan  { box-shadow: 0 0 25px rgba(0,212,255,0.2); }
    .stat-card:hover.green { box-shadow: 0 0 25px rgba(0,255,136,0.2); }
    .stat-card:hover.blue  { box-shadow: 0 0 25px rgba(100,130,255,0.2); }
    .stat-card:hover.purple { box-shadow: 0 0 25px rgba(123,47,255,0.2); }
    .stat-number {
        font-family: 'Orbitron', monospace; font-size: 1.8rem; font-weight: 700;
    }
    .stat-label {
        color: var(--subtext); font-size: 0.75rem; text-transform: uppercase;
        letter-spacing: 1.5px; margin-top: 0.3rem; font-weight: 500;
    }

    /* ═══════════════════ GRADIENT DIVIDER ═══════════════════ */
    .gradient-divider {
        height: 2px; margin: 1.5rem 0;
        background: linear-gradient(90deg, transparent, var(--primary), var(--secondary), transparent);
        opacity: 0.4;
    }

    /* ═══════════════════ RESULT CARDS ═══════════════════ */
    .result-spam {
        background: linear-gradient(135deg, rgba(255,71,87,0.12), rgba(255,71,87,0.03));
        border: 1px solid rgba(255,71,87,0.3); border-radius: 16px;
        padding: 2rem; text-align: center; margin: 1rem 0;
        animation: slideInRight 0.5s ease;
    }
    .result-ham {
        background: linear-gradient(135deg, rgba(0,255,136,0.1), rgba(0,255,136,0.02));
        border: 1px solid rgba(0,255,136,0.3); border-radius: 16px;
        padding: 2rem; text-align: center; margin: 1rem 0;
        animation: slideInRight 0.5s ease;
    }
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(40px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .result-icon { font-size: 3rem; margin-bottom: 0.5rem; }
    .result-label {
        font-family: 'Orbitron', monospace; font-size: 1.6rem; font-weight: 800;
        letter-spacing: 2px;
    }
    .result-spam .result-label { color: var(--danger); }
    .result-ham .result-label { color: var(--success); }

    /* Confidence bar */
    .confidence-bar-container {
        width: 80%; max-width: 400px; margin: 1rem auto;
        background: rgba(255,255,255,0.06); border-radius: 8px; height: 10px;
        overflow: hidden;
    }
    .confidence-bar-fill {
        height: 100%; border-radius: 8px;
        transition: width 1s ease;
    }
    .confidence-text {
        color: var(--subtext); font-size: 0.88rem; margin-top: 0.5rem;
    }
    .prob-container {
        display: flex; justify-content: center; gap: 3rem; margin-top: 1rem;
    }
    .prob-value { font-family: 'Orbitron', monospace; font-size: 1.3rem; font-weight: 700; }
    .prob-label { color: var(--subtext); font-size: 0.75rem; text-transform: uppercase;
        letter-spacing: 1px; margin-top: 0.2rem; }

    /* ═══════════════════ FEATURE PILLS ═══════════════════ */
    .feature-pill {
        display: inline-block; padding: 0.3rem 0.8rem; margin: 0.15rem;
        border-radius: 20px; font-size: 0.78rem; font-weight: 500;
        background: rgba(0,212,255,0.08);
        border: 1px solid rgba(0,212,255,0.2);
        color: var(--primary);
    }

    /* ═══════════════════ RISK BADGES ═══════════════════ */
    .risk-badge {
        display: inline-block; padding: 0.35rem 1rem; border-radius: 20px;
        font-weight: 600; font-size: 0.85rem;
    }
    .risk-high { background: rgba(255,71,87,0.15); color: var(--danger);
        border: 1px solid rgba(255,71,87,0.3); }
    .risk-medium { background: rgba(255,183,77,0.15); color: #ffb74d;
        border: 1px solid rgba(255,183,77,0.3); }
    .risk-low { background: rgba(0,255,136,0.12); color: var(--success);
        border: 1px solid rgba(0,255,136,0.3); }
    .risk-none { background: rgba(136,136,170,0.1); color: var(--subtext);
        border: 1px solid rgba(136,136,170,0.2); }

    /* ═══════════════════ METRIC CARDS ═══════════════════ */
    .metric-card {
        background: var(--bg-card); border: 1px solid var(--card-border);
        border-radius: 14px; padding: 1.2rem; margin-bottom: 0.8rem;
    }
    .metric-card-suspicious { border-color: rgba(255,71,87,0.25); }
    .metric-card-safe { border-color: rgba(0,255,136,0.2); }
    .risk-score-circle {
        width: 56px; height: 56px; border-radius: 50%; display: flex;
        align-items: center; justify-content: center;
        font-family: 'Orbitron', monospace; font-weight: 700; font-size: 1rem;
        flex-shrink: 0;
    }

    /* ═══════════════════ HISTORY ROW ═══════════════════ */
    .history-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 0.55rem 0.8rem; margin: 0.2rem 0;
        background: rgba(18,18,42,0.4); border-radius: 8px;
        border: 1px solid rgba(123,47,255,0.06);
        transition: background 0.2s;
    }
    .history-row:hover { background: rgba(18,18,42,0.7); }

    /* ═══════════════════ BOTTOM BANNER ═══════════════════ */
    .bottom-banner {
        margin-top: 2rem; padding: 1rem 1.5rem;
        border-top: 1px solid rgba(0,212,255,0.12);
        display: flex; justify-content: space-between; align-items: center;
        flex-wrap: wrap; gap: 0.5rem;
    }
    .bottom-banner .banner-logo {
        font-family: 'Orbitron', monospace; font-size: 0.85rem;
        color: var(--primary); font-weight: 600;
    }
    .bottom-banner .banner-center {
        color: var(--subtext); font-size: 0.78rem;
    }
    .bottom-banner .banner-right {
        color: #555; font-size: 0.72rem;
    }

    /* ═══════════════════ BUTTONS ═══════════════════ */
    .stButton > button {
        background: linear-gradient(135deg, #00D4FF 0%, #7B2FFF 100%) !important;
        color: white !important; border: none !important;
        border-radius: 12px !important; padding: 0.7rem 2rem !important;
        font-family: 'Orbitron', monospace !important; font-weight: 600 !important;
        font-size: 0.9rem !important; letter-spacing: 0.5px;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        box-shadow: 0 0 25px rgba(0,212,255,0.35) !important;
        transform: translateY(-2px) !important;
    }

    /* ═══════════════════ INPUTS ═══════════════════ */
    .stTextArea textarea {
        background: var(--bg-card) !important; color: var(--text) !important;
        border: 1px solid rgba(0,212,255,0.15) !important;
        border-radius: 12px !important; font-family: 'Inter', sans-serif !important;
    }
    .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 15px rgba(0,212,255,0.12) !important;
    }
    .stFileUploader {
        background: var(--bg-card) !important; border-radius: 12px !important;
    }

    /* ═══════════════════ EXPANDERS ═══════════════════ */
    [data-testid="stExpander"] {
        background: rgba(18,18,42,0.4) !important;
        border: 1px solid rgba(123,47,255,0.1) !important;
        border-radius: 12px !important;
    }

    /* ═══════════════════ SIDEBAR EXTRAS ═══════════════════ */
    .sidebar-aria-mini {
        text-align: center; padding: 0.8rem 0;
    }
    .sidebar-aria-mini svg { width: 48px; height: 48px; }
    .aria-online {
        display: flex; align-items: center; justify-content: center;
        gap: 0.4rem; margin-top: 0.3rem;
    }
    .aria-online .dot {
        width: 8px; height: 8px; background: var(--success); border-radius: 50%;
        animation: blink 2s ease-in-out infinite;
    }
    @keyframes blink {
        0%, 100% { opacity: 1; } 50% { opacity: 0.3; }
    }
    .aria-online span {
        font-size: 0.72rem; color: var(--success) !important;
        font-family: 'Inter', sans-serif; letter-spacing: 0.5px;
    }

    /* ═══════════════════ SIDEBAR TOGGLE — BIG & VISIBLE ═══════════════════ */
    /* Native Streamlit collapsed-sidebar button */
    [data-testid="stSidebarCollapsedControl"] {
        top: 0.6rem !important;
        left: 0.6rem !important;
        z-index: 999999 !important;
    }
    [data-testid="stSidebarCollapsedControl"] button {
        background: rgba(0,212,255,0.15) !important;
        border: 2px solid rgba(0,212,255,0.4) !important;
        border-radius: 12px !important;
        padding: 0.6rem 0.7rem !important;
        color: var(--primary) !important;
        box-shadow: 0 0 15px rgba(0,212,255,0.2) !important;
        transition: all 0.3s ease !important;
    }
    [data-testid="stSidebarCollapsedControl"] button:hover {
        background: rgba(0,212,255,0.25) !important;
        box-shadow: 0 0 25px rgba(0,212,255,0.4) !important;
        transform: scale(1.1) !important;
    }
    [data-testid="stSidebarCollapsedControl"] button svg {
        width: 22px !important;
        height: 22px !important;
        stroke: var(--primary) !important;
    }
    /* Native X close button inside sidebar */
    [data-testid="stSidebar"] button[kind="header"],
    [data-testid="stSidebar"] [data-testid="stSidebarNavCollapseIcon"],
    [data-testid="stSidebarCollapseButton"] button {
        color: var(--primary) !important;
        background: rgba(0,212,255,0.08) !important;
        border: 1px solid rgba(0,212,255,0.2) !important;
        border-radius: 8px !important;
    }

    /* ── Custom floating menu button ── */
    .floating-menu-btn {
        position: fixed;
        left: 14px;
        top: 50%;
        transform: translateY(-50%);
        z-index: 999998;
        background: linear-gradient(135deg, rgba(0,212,255,0.2), rgba(123,47,255,0.2));
        border: 2px solid rgba(0,212,255,0.4);
        border-radius: 14px;
        padding: 10px 12px;
        cursor: pointer;
        color: #00D4FF;
        font-family: 'Orbitron', monospace;
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 1px;
        backdrop-filter: blur(12px);
        box-shadow: 0 0 20px rgba(0,212,255,0.15);
        transition: all 0.3s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 4px;
        writing-mode: horizontal-tb;
    }
    .floating-menu-btn:hover {
        background: linear-gradient(135deg, rgba(0,212,255,0.35), rgba(123,47,255,0.35));
        box-shadow: 0 0 30px rgba(0,212,255,0.35);
        transform: translateY(-50%) scale(1.08);
    }
    .floating-menu-btn .hamburger {
        font-size: 1.4rem;
        line-height: 1;
    }
    .floating-menu-btn .menu-label {
        font-size: 0.55rem;
        letter-spacing: 2px;
    }
    /* Hide floating btn when sidebar is open */
    [data-testid="stSidebar"][aria-expanded="true"] ~ .main .floating-menu-btn,
    body:has([data-testid="stSidebar"][aria-expanded="true"]) .floating-menu-btn {
        opacity: 0;
        pointer-events: none;
    }

    /* ═══════════════════ DATA ELEMENTS ═══════════════════ */
    .stDataFrame { border-radius: 12px !important; overflow: hidden; }
    [data-testid="stMetric"] {
        background: var(--bg-card) !important;
        border: 1px solid rgba(0,212,255,0.08);
        border-radius: 12px; padding: 0.8rem !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Orbitron', monospace !important;
        color: var(--primary) !important;
    }
    [data-testid="stMetricLabel"] {
        color: var(--subtext) !important;
    }

    /* ═══════════════════ RESPONSIVE ═══════════════════ */
    @media (max-width: 768px) {
        .app-title { font-size: 1.5rem; }
        .aria-container { flex-direction: column; align-items: center; text-align: center; }
        .steps-row { flex-direction: column; }
        .bottom-banner { flex-direction: column; text-align: center; }
        .stat-number { font-size: 1.3rem; }
    }
    </style>
    """, unsafe_allow_html=True)


def inject_stars_and_glow(st):
    """Inject animated star background and ambient glow."""
    import random
    stars_html = '<div class="star-bg">'
    for _ in range(60):
        x = random.randint(0, 100)
        y = random.randint(0, 100)
        size = round(random.uniform(1, 2.5), 1)
        dur = round(random.uniform(3, 8), 1)
        delay = round(random.uniform(0, 5), 1)
        stars_html += (
            f'<div class="star" style="left:{x}%;top:{y}%;'
            f'width:{size}px;height:{size}px;'
            f'animation-duration:{dur}s;animation-delay:{delay}s;"></div>'
        )
    stars_html += '</div><div class="ambient-glow"></div>'
    st.markdown(stars_html, unsafe_allow_html=True)
