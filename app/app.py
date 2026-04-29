"""
📧 Spam Mail Detector — Interactive Web Application
=====================================================
Agent 3: Frontend / User Interface
Agent 4: Integration & Deployment

A beautiful, modern Streamlit application for real-time spam detection.

Run with:
    streamlit run app/app.py
"""

import os
import sys
import streamlit as st
import pandas as pd
import time

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from utils.model_utils import ModelManager

# ─── Page Configuration ──────────────────────────────────────────────────────

st.set_page_config(
    page_title="Spam Mail Detector — AI-Powered Email Classifier",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS for Premium Design ───────────────────────────────────────────

st.markdown("""
<style>
    /* ── Import Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* ── Global Styles ── */
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 40%, #16213e 100%);
    }
    
    /* ── Hide default Streamlit elements ── */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* ── Hero Section ── */
    .hero-container {
        text-align: center;
        padding: 2rem 1rem 1.5rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.15rem;
        color: #a0aec0;
        font-weight: 400;
        letter-spacing: 0.02em;
    }
    
    /* ── Glassmorphism Card ── */
    .glass-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        border-color: rgba(102, 126, 234, 0.3);
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.1);
    }
    
    /* ── Result Cards ── */
    .result-spam {
        background: linear-gradient(135deg, rgba(255, 56, 56, 0.12) 0%, rgba(255, 100, 100, 0.06) 100%);
        border: 1px solid rgba(255, 56, 56, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        animation: slideUp 0.5s ease-out;
    }
    
    .result-ham {
        background: linear-gradient(135deg, rgba(56, 255, 120, 0.12) 0%, rgba(100, 255, 150, 0.06) 100%);
        border: 1px solid rgba(56, 255, 120, 0.3);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        animation: slideUp 0.5s ease-out;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .result-icon {
        font-size: 4rem;
        margin-bottom: 0.5rem;
    }
    
    .result-label {
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .result-spam .result-label { color: #ff5555; }
    .result-ham .result-label { color: #50fa7b; }
    
    .confidence-bar-container {
        background: rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        height: 12px;
        overflow: hidden;
        margin: 1rem auto;
        max-width: 300px;
    }
    
    .confidence-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease-out;
    }
    
    .confidence-text {
        font-size: 1rem;
        color: #a0aec0;
        margin-top: 0.5rem;
    }
    
    /* ── Stats Cards ── */
    .stat-card {
        background: rgba(255, 255, 255, 0.04);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.3rem;
    }
    
    /* ── Feature Pills ── */
    .feature-pill {
        display: inline-block;
        background: rgba(102, 126, 234, 0.15);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: 50px;
        padding: 0.4rem 1rem;
        margin: 0.3rem;
        font-size: 0.85rem;
        color: #a0aec0;
    }
    
    /* ── Sidebar Styling ── */
    section[data-testid="stSidebar"] {
        background: rgba(15, 12, 41, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06);
    }
    
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3 {
        color: #e2e8f0;
    }
    
    /* ── Text Area Styling ── */
    .stTextArea textarea {
        background: #ffffff !important;
        border: 2px solid rgba(102, 126, 234, 0.4) !important;
        border-radius: 14px !important;
        color: #000000 !important;
        font-size: 1rem !important;
        padding: 1rem !important;
        transition: border-color 0.3s ease !important;
        caret-color: #000000 !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #999999 !important;
        opacity: 1 !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.25) !important;
    }
    
    /* ── Button Styling (main action buttons only) ── */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    
    /* ── Expander styling ── */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.04) !important;
        border-radius: 12px !important;
    }
    
    /* ── Divider ── */
    .gradient-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.5), transparent);
        margin: 1.5rem 0;
        border: none;
    }
    
    /* ── Probabilities ── */
    .prob-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-top: 1rem;
    }
    
    .prob-item {
        text-align: center;
    }
    
    .prob-value {
        font-size: 1.5rem;
        font-weight: 700;
    }
    
    .prob-label {
        font-size: 0.8rem;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    /* ── History table ── */
    .history-row {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 10px;
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
        border: 1px solid rgba(255, 255, 255, 0.06);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    /* ── File uploader — fully reset to avoid conflicts ── */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.06) !important;
        border: 2px dashed rgba(102, 126, 234, 0.4) !important;
        border-radius: 14px !important;
        padding: 1.5rem !important;
        margin-top: 0.5rem !important;
    }
    
    [data-testid="stFileUploader"] section {
        padding: 0 !important;
    }

    /* Override the upload button — explicit props only, NO 'all: revert' */
    [data-testid="stFileUploader"] button {
        background: rgba(102, 126, 234, 0.25) !important;
        border: 1px solid rgba(102, 126, 234, 0.5) !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.45rem 1.2rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: normal !important;
        width: auto !important;
        box-shadow: none !important;
        transform: none !important;
        cursor: pointer !important;
        background-image: none !important;
    }

    /* Hide the duplicate span text inside the upload button.
       Streamlit renders: button > div > span > [span (duplicate text), div > p (real label)]
       We hide the inner span and only show the p element. */
    [data-testid="stFileUploader"] button > div > span > span {
        display: none !important;
    }
    
    [data-testid="stFileUploader"] button p {
        color: #e2e8f0 !important;
        margin: 0 !important;
        font-size: 0.9rem !important;
    }

    [data-testid="stFileUploader"] button:hover {
        background: rgba(102, 126, 234, 0.45) !important;
        border-color: #667eea !important;
        transform: none !important;
        box-shadow: none !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: #a0aec0 !important;
    }
    
    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb {
        background: rgba(102, 126, 234, 0.3);
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Load Model ──────────────────────────────────────────────────────────────

@st.cache_resource
def load_model():
    """Load the trained model and vectorizer (cached)."""
    model_path = os.path.join(PROJECT_ROOT, 'models', 'best_model.pkl')
    vectorizer_path = os.path.join(PROJECT_ROOT, 'models', 'tfidf_vectorizer.pkl')
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        return None
    
    try:
        manager = ModelManager(model_path, vectorizer_path)
        return manager
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

@st.cache_data
def load_model_metadata():
    """Load saved model metadata."""
    metadata_path = os.path.join(PROJECT_ROOT, 'models', 'model_metadata.pkl')
    if os.path.exists(metadata_path):
        import joblib
        return joblib.load(metadata_path)
    return None


# ─── Initialize Session State ────────────────────────────────────────────────

if 'history' not in st.session_state:
    st.session_state.history = []

if 'total_checked' not in st.session_state:
    st.session_state.total_checked = 0

if 'spam_found' not in st.session_state:
    st.session_state.spam_found = 0


# ─── Hero Section ────────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-container">
    <div class="hero-title">📧 Spam Mail Detector</div>
    <div class="hero-subtitle">AI-powered email classification using Natural Language Processing & Machine Learning</div>
</div>
<div class="gradient-divider"></div>
""", unsafe_allow_html=True)


# ─── Sidebar ─────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 🎛️ Control Panel")
    st.markdown("---")
    
    # Model info
    metadata = load_model_metadata()
    if metadata:
        st.markdown("### 🤖 Active Model")
        st.markdown(f"""
        <div class="stat-card">
            <div style="color: #e2e8f0; font-weight: 600; font-size: 1rem;">{metadata['model_name']}</div>
            <div style="color: #a0aec0; font-size: 0.8rem; margin-top: 0.5rem;">
                Accuracy: {metadata['accuracy']:.1%} | F1: {metadata['f1_score']:.1%}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("")
    
    # Session stats
    st.markdown("### 📊 Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.total_checked}</div>
            <div class="stat-label">Checked</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.spam_found}</div>
            <div class="stat-label">Spam Found</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick test samples
    st.markdown("### 🧪 Quick Test Samples")
    
    spam_samples = [
        "Congratulations! You've won a $1000 gift card! Claim NOW!",
        "URGENT: Your bank account has been compromised. Click link to verify",
        "FREE entry to win iPhone! Text WIN to 80085",
        "You've won the lottery! Send $100 processing fee to claim $1M",
    ]
    
    ham_samples = [
        "Hey, are we still meeting for lunch tomorrow?",
        "Can you send me the meeting notes from today?",
        "Don't forget to pick up milk on your way home",
        "The project deadline has been extended to next Friday",
    ]
    
    st.markdown("**🔴 Spam Examples:**")
    for sample in spam_samples:
        if st.button(f"📝 {sample[:45]}...", key=f"spam_{hash(sample)}"):
            st.session_state.sample_text = sample
    
    st.markdown("**🟢 Ham Examples:**")
    for sample in ham_samples:
        if st.button(f"📝 {sample[:45]}...", key=f"ham_{hash(sample)}"):
            st.session_state.sample_text = sample
    
    st.markdown("---")
    
    # Technology used
    st.markdown("### 🛠️ Technology")
    st.markdown("""
    <div style="text-align: center;">
        <span class="feature-pill">Python</span>
        <span class="feature-pill">Scikit-learn</span>
        <span class="feature-pill">NLTK</span>
        <span class="feature-pill">TF-IDF</span>
        <span class="feature-pill">Streamlit</span>
    </div>
    """, unsafe_allow_html=True)


# ─── Main Content ────────────────────────────────────────────────────────────

manager = load_model()

if manager is None:
    st.markdown("""
    <div class="glass-card" style="text-align: center;">
        <div style="font-size: 3rem;">⚠️</div>
        <h2 style="color: #e2e8f0;">Model Not Found</h2>
        <p style="color: #a0aec0;">
            Please train the model first by running:<br>
            <code style="background: rgba(255,255,255,0.1); padding: 0.3rem 0.8rem; border-radius: 8px; color: #667eea;">
                python train.py
            </code>
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ── Input Section ──
st.markdown("""
<div class="glass-card">
    <h3 style="color: #e2e8f0; margin-bottom: 0.5rem;">✍️ Enter Your Message</h3>
    <p style="color: #718096; font-size: 0.9rem;">Paste an email, SMS, or any text message below to check if it's spam</p>
</div>
""", unsafe_allow_html=True)

# Handle sample text from sidebar
default_text = st.session_state.get('sample_text', '')
if default_text:
    del st.session_state.sample_text

user_input = st.text_area(
    "Message Input",
    value=default_text,
    height=150,
    placeholder="Type or paste your message here...\n\nExample: Congratulations! You've won a free vacation. Click here to claim!",
    label_visibility="collapsed"
)

col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    check_button = st.button("🔍  Analyze Message", use_container_width=True)


# ── Prediction ──
if check_button and user_input.strip():
    with st.spinner(""):
        # Show analyzing animation
        progress_placeholder = st.empty()
        progress_placeholder.markdown("""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 2rem;">🔍</div>
            <p style="color: #a0aec0;">Analyzing message with AI...</p>
        </div>
        """, unsafe_allow_html=True)
        
        time.sleep(0.8)  # Brief delay for UX feel
        
        result = manager.predict(user_input)
        progress_placeholder.empty()
    
    # Update stats
    st.session_state.total_checked += 1
    if result['label'] == 1:
        st.session_state.spam_found += 1
    
    # Add to history
    st.session_state.history.insert(0, {
        'message': user_input[:80] + ('...' if len(user_input) > 80 else ''),
        'result': result['prediction'],
        'confidence': result['confidence'],
    })
    # Keep only last 20
    st.session_state.history = st.session_state.history[:20]
    
    # Display result
    if result['label'] == 1:
        # SPAM
        bar_color = "linear-gradient(90deg, #ff5555, #ff7979)"
        st.markdown(f"""
        <div class="result-spam">
            <div class="result-icon">🚫</div>
            <div class="result-label">SPAM DETECTED</div>
            <p style="color: #ff9999; font-size: 0.95rem;">This message has been classified as spam with high confidence.</p>
            <div class="confidence-bar-container">
                <div class="confidence-bar-fill" style="width: {result['confidence']*100}%; background: {bar_color};"></div>
            </div>
            <div class="confidence-text">Confidence: {result['confidence']:.1%}</div>
            <div class="prob-container">
                <div class="prob-item">
                    <div class="prob-value" style="color: #ff5555;">{result['spam_probability']:.1%}</div>
                    <div class="prob-label">Spam Probability</div>
                </div>
                <div class="prob-item">
                    <div class="prob-value" style="color: #50fa7b;">{result['ham_probability']:.1%}</div>
                    <div class="prob-label">Ham Probability</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # HAM
        bar_color = "linear-gradient(90deg, #50fa7b, #69ff94)"
        st.markdown(f"""
        <div class="result-ham">
            <div class="result-icon">✅</div>
            <div class="result-label">NOT SPAM</div>
            <p style="color: #88ffaa; font-size: 0.95rem;">This message appears to be legitimate and safe.</p>
            <div class="confidence-bar-container">
                <div class="confidence-bar-fill" style="width: {result['confidence']*100}%; background: {bar_color};"></div>
            </div>
            <div class="confidence-text">Confidence: {result['confidence']:.1%}</div>
            <div class="prob-container">
                <div class="prob-item">
                    <div class="prob-value" style="color: #ff5555;">{result['spam_probability']:.1%}</div>
                    <div class="prob-label">Spam Probability</div>
                </div>
                <div class="prob-item">
                    <div class="prob-value" style="color: #50fa7b;">{result['ham_probability']:.1%}</div>
                    <div class="prob-label">Ham Probability</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif check_button and not user_input.strip():
    st.warning("⚠️ Please enter a message to analyze.")


# ── Divider ──
st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)


# ── Batch Upload Feature ──
st.markdown("""
<div class="glass-card">
    <h3 style="color: #e2e8f0; margin-bottom: 0.5rem;">📁 Batch Analysis</h3>
    <p style="color: #718096; font-size: 0.9rem;">Upload a CSV file with a 'message' column to classify multiple messages at once</p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload CSV",
    type=['csv'],
    label_visibility="collapsed",
    help="Upload a CSV file with a 'message' column"
)

if uploaded_file is not None:
    try:
        upload_df = pd.read_csv(uploaded_file)
        
        # Find the message column (flexible naming)
        msg_col = None
        for col in upload_df.columns:
            if col.lower() in ['message', 'text', 'email', 'content', 'body', 'sms']:
                msg_col = col
                break
        
        if msg_col is None:
            st.error("❌ Could not find a message column. Please ensure your CSV has a column named 'message', 'text', or 'email'.")
        else:
            with st.spinner("🔍 Analyzing uploaded messages..."):
                results_list = []
                progress_bar = st.progress(0)
                
                for i, msg in enumerate(upload_df[msg_col].astype(str)):
                    result = manager.predict(msg)
                    results_list.append({
                        'Message': msg[:100] + ('...' if len(msg) > 100 else ''),
                        'Prediction': result['prediction'],
                        'Confidence': f"{result['confidence']:.1%}",
                        'Spam %': f"{result['spam_probability']:.1%}",
                        'Ham %': f"{result['ham_probability']:.1%}",
                    })
                    progress_bar.progress((i + 1) / len(upload_df))
                
                progress_bar.empty()
            
            results_df = pd.DataFrame(results_list)
            
            # Summary stats
            spam_count = sum(1 for r in results_list if r['Prediction'] == 'Spam')
            ham_count = len(results_list) - spam_count
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{len(results_list)}</div>
                    <div class="stat-label">Total Messages</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number" style="background: linear-gradient(135deg, #ff5555, #ff7979); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{spam_count}</div>
                    <div class="stat-label">Spam Detected</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number" style="background: linear-gradient(135deg, #50fa7b, #69ff94); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{ham_count}</div>
                    <div class="stat-label">Legitimate</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("")
            st.dataframe(results_df, use_container_width=True, height=400)
            
            # Download results
            csv = results_df.to_csv(index=False)
            st.download_button(
                "📥 Download Results as CSV",
                csv,
                "spam_detection_results.csv",
                "text/csv",
            )
    
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")


# ── History Section ──
if st.session_state.history:
    st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #e2e8f0; margin-bottom: 0.5rem;">📜 Recent History</h3>
        <p style="color: #718096; font-size: 0.9rem;">Your recent classification results this session</p>
    </div>
    """, unsafe_allow_html=True)
    
    for item in st.session_state.history[:10]:
        emoji = "🔴" if item['result'] == 'Spam' else "🟢"
        badge_color = "rgba(255, 56, 56, 0.2)" if item['result'] == 'Spam' else "rgba(56, 255, 120, 0.2)"
        text_color = "#ff5555" if item['result'] == 'Spam' else "#50fa7b"
        
        st.markdown(f"""
        <div class="history-row">
            <span style="color: #a0aec0; font-size: 0.9rem;">{emoji} {item['message']}</span>
            <span style="background: {badge_color}; color: {text_color}; padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600;">
                {item['result']} ({item['confidence']:.0%})
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.session_state.total_checked = 0
        st.session_state.spam_found = 0
        st.rerun()


# ── Footer ──
st.markdown('<div class="gradient-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; padding: 1.5rem 0;">
    <p style="color: #a0aec0; font-size: 0.95rem;">
        Made with ❤️ by <span style="color: #667eea; font-weight: 600;">Pulkit</span>, 
        <span style="color: #764ba2; font-weight: 600;">Raushan</span>, 
        <span style="color: #f093fb; font-weight: 600;">Mahesh</span>, 
        <span style="color: #667eea; font-weight: 600;">Khushi</span> & 
        <span style="color: #764ba2; font-weight: 600;">Mahi</span>
    </p>
    <p style="color: #4a5568; font-size: 0.75rem; margin-top: 0.3rem;">
        Spam Mail Detector — Machine Learning Project
    </p>
</div>
""", unsafe_allow_html=True)
