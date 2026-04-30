"""
ARIA — AI Risk Intelligence Assistant
=======================================
Reusable character component rendered via HTML/CSS/SVG.
Provides: avatar, chat bubble, reaction states, and step guides.
"""

import textwrap


def aria_avatar_svg(state: str = "default") -> str:
    """Return the ARIA face as inline HTML.
    state: 'default', 'danger', 'success'"""
    face_class = state if state in ("danger", "success") else ""
    return (
        '<div class="aria-avatar">'
        '<div class="aria-ring"></div>'
        f'<div class="aria-face {face_class}">'
        '<div class="aria-antenna"></div>'
        '<div class="aria-eye left"></div>'
        '<div class="aria-eye right"></div>'
        '<div class="aria-mouth"></div>'
        '</div></div>'
    )


def aria_component(message: str, state: str = "default") -> str:
    """Full ARIA component with avatar + chat bubble.
    Returns HTML string ready for st.markdown(unsafe_allow_html=True)."""
    avatar = aria_avatar_svg(state)
    return (
        '<div class="aria-container">'
        f'{avatar}'
        '<div class="aria-bubble">'
        '<div class="aria-name">ARIA &mdash; AI RISK INTELLIGENCE ASSISTANT</div>'
        f'<div class="aria-text">{message}</div>'
        '</div></div>'
    )


def aria_sidebar_mini() -> str:
    """Small ARIA avatar for sidebar with online indicator."""
    return textwrap.dedent("""\
    <div class="sidebar-aria-mini">
    <svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg">
    <defs><radialGradient id="sg" cx="50%" cy="50%">
    <stop offset="0%" style="stop-color:#1A1A3E"/>
    <stop offset="100%" style="stop-color:#0D0D2B"/>
    </radialGradient></defs>
    <circle cx="40" cy="40" r="36" fill="url(#sg)" stroke="#00D4FF" stroke-width="1.5" opacity="0.9"/>
    <line x1="40" y1="8" x2="40" y2="2" stroke="#00D4FF" stroke-width="2"/>
    <circle cx="40" cy="1" r="3" fill="#00D4FF"/>
    <ellipse cx="28" cy="36" rx="5" ry="6" fill="#00D4FF" opacity="0.9">
    <animate attributeName="ry" values="6;0.5;6" dur="3.5s" repeatCount="indefinite"/></ellipse>
    <ellipse cx="52" cy="36" rx="5" ry="6" fill="#00D4FF" opacity="0.9">
    <animate attributeName="ry" values="6;0.5;6" dur="3.5s" repeatCount="indefinite"/></ellipse>
    <rect x="30" y="52" width="20" height="3" rx="1.5" fill="#00D4FF" opacity="0.5"/>
    </svg>
    <div class="aria-online"><div class="dot"></div><span>ARIA Online</span></div>
    </div>
    """)


def step_guide(steps: list, active_step: int = 1) -> str:
    """Render numbered step cards.
    steps: list of (emoji, text) tuples.
    active_step: 1-indexed current step. Steps below active are 'done'."""
    cards = []
    for i, (emoji, text) in enumerate(steps, 1):
        if i < active_step:
            cls = "done"
            badge = "&#x2705;"
        elif i == active_step:
            cls = "active"
            badge = f"STEP {i}"
        else:
            cls = ""
            badge = f"STEP {i}"
        cards.append(
            f'<div class="step-card {cls}">'
            f'<div class="step-num">{badge}</div>'
            f'<div>{emoji} {text}</div>'
            f'</div>'
        )
    return '<div class="steps-row">' + ''.join(cards) + '</div>'


def bottom_banner() -> str:
    """Full-width bottom banner."""
    return (
        '<div class="bottom-banner">'
        '<div class="banner-logo">&#x1f6e1;&#xfe0f; Threat Intel System</div>'
        '<div class="banner-center">Powered by Machine Learning &amp; AI</div>'
        '<div class="banner-right">'
        'Built with &#x2764;&#xfe0f; by Pulkit, Raushan, Mahesh, Khushi &amp; Mahi'
        '</div></div>'
    )


# ─── Page-specific ARIA messages ─────────────────────────────────────────────
ARIA_MESSAGES = {
    'home': (
        "Hello! I am <strong>ARIA</strong>, your personal threat intelligence "
        "assistant. Paste any email or message below and I will analyze it for "
        "spam and threats instantly!"
    ),
    'domain': (
        "Suspicious about a website? Paste any URL below and I will scan it "
        "for phishing patterns, risky keywords and threat indicators!"
    ),
    'bulk': (
        "Have multiple emails to check? Upload your CSV file and I will scan "
        "all of them at once and give you a full report!"
    ),
    'analytics': (
        "Here are all the insights from your previous scans. I have analyzed "
        "the patterns and visualized them for you!"
    ),
    'model': (
        "Want to know how I think? Here are my accuracy metrics and the "
        "features I use to detect threats!"
    ),
}
