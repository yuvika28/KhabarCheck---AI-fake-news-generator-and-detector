import streamlit as st
import joblib
import re
import string
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
import time

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="KhabarCheck – Truth Lens",
    page_icon="🔍",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================
# CUSTOM CSS (soft, fresh look)
# ==============================
st.markdown("""
<style>
    /* Main header – gradient from teal to coral */
    .main-header {
        font-size: 3rem;
        font-weight: 600;
        background: linear-gradient(135deg, #2ab7a9 0%, #f47b6b 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.2rem;
        font-family: 'Segoe UI', sans-serif;
    }
    .sub-header {
        text-align: center;
        color: #888;
        margin-bottom: 2rem;
        font-size: 1.1rem;
    }
    /* Card style for content blocks */
    .card {
        background: #fafafa;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #f0f0f0;
    }
    /* Button styling – softer gradient */
    .stButton > button {
        border-radius: 30px;
        background: linear-gradient(135deg, #2ab7a9 0%, #f47b6b 100%);
        color: white;
        font-weight: 500;
        border: none;
        padding: 0.4rem 2rem;
        transition: 0.3s;
        box-shadow: 0 4px 10px rgba(42,183,169,0.2);
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 14px rgba(42,183,169,0.3);
    }
    /* Input fields – rounded */
    .stTextInput > div > div > input {
        border-radius: 25px;
        border: 1px solid #ddd;
    }
    .stSelectbox > div > div > select {
        border-radius: 25px;
    }
    /* Progress bar for confidence */
    .confidence-bar {
        background: #e0e0e0;
        border-radius: 12px;
        height: 20px;
        width: 100%;
        margin: 10px 0;
    }
    .confidence-fill {
        border-radius: 12px;
        height: 100%;
        text-align: center;
        color: white;
        font-size: 0.8rem;
        line-height: 20px;
        background: linear-gradient(90deg, #2ab7a9, #f47b6b);
    }
    /* Footer */
    .footer {
        text-align: center;
        color: #aaa;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# LOAD ENV & API KEY
# ==============================
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# ==============================
# LOAD MODEL (cached)
# ==============================
@st.cache_resource
def load_model():
    # Use absolute path – update if needed
    return joblib.load("/Users/anishsmac/Desktop/Fake_news_Detection/model.pkl")

Model = load_model()

# ==============================
# TEXT PREPROCESSING
# ==============================
def wordpre(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub("\\W", " ", text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

# ==============================
# DETECTION FUNCTION
# ==============================
def detect_news(text):
    processed = wordpre(text)
    txt_series = pd.Series([processed])
    pred = Model.predict(txt_series)[0]
    if hasattr(Model, "predict_proba"):
        proba = Model.predict_proba(txt_series)[0]
        confidence = max(proba) * 100
    else:
        confidence = 90.0
    return pred, confidence

# ==============================
# UI HEADER
# ==============================
st.markdown('<h1 class="main-header">🔎 KhabarCheck</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Generate · Detect · Understand</p>', unsafe_allow_html=True)

# ==============================
# API KEY INPUT (if not in env)
# ==============================
if not API_KEY:
    with st.expander("🔑 Enter Gemini API Key (required for generation)", expanded=False):
        user_key = st.text_input("API Key", type="password", 
                                 help="Get a free key at ai.google.dev")
        if user_key:
            API_KEY = user_key
            st.success("Key saved for this session")

# Initialize Gemini client if key exists
if API_KEY:
    try:
        client = genai.Client(api_key=API_KEY)
        api_ok = True
    except Exception:
        st.error("Invalid API key")
        api_ok = False
else:
    api_ok = False
    st.info("ℹ️ Enter your Gemini API key above to enable article generation.")

# ==============================
# GENERATION SECTION (simplified)
# ==============================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("📝 Generate a Fake News Article")
with st.container():
    topic = st.text_input("Topic", placeholder="e.g., Election results, Mars landing...")

    if st.button("✨ Generate Article", use_container_width=True):
        if not api_ok:
            st.error("Please provide a valid Gemini API key first.")
        elif not topic:
            st.warning("Please enter a topic.")
        else:
            with st.spinner("Writing your article..."):
                prompt = f"""
Write a realistic fake news article about the following topic: {topic}

Requirements:
- Newspaper style headline
- Include fake quotes
- Include statistics
- 200–300 words
"""
                try:
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )
                    article = response.text
                    st.markdown("### Generated Article")
                    st.code(article, language="text")  # copy icon included
                except Exception as e:
                    st.error(f"Generation failed: {e}")
st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# DETECTION SECTION
# ==============================
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("🔍 Detect Fake or Real News")
news_text = st.text_area("Paste news text here", height=150,
                         placeholder="Enter the article you want to check...")
if st.button("Check Authenticity", use_container_width=True):
    if news_text.strip() == "":
        st.warning("Please enter some text.")
    else:
        with st.spinner("Analyzing..."):
            time.sleep(0.5)  # slight delay
            pred, conf = detect_news(news_text)
        label = "✅ REAL" if pred == 1 else "❌ FAKE"
        st.markdown(f"### Result: **{label}**")
        # Simple confidence bar
        st.markdown(f"**Confidence:** {conf:.1f}%")
        st.markdown(f"""
        <div class="confidence-bar">
            <div class="confidence-fill" style="width: {conf}%;">{conf:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ==============================
# FOOTER (with her name)
# ==============================
st.markdown("---")
st.markdown(
    "<p class='footer'>"
    "Built with ❤️ by Yuvika Ajmera · NLP & GenAI Project"
    "</p>",
    unsafe_allow_html=True
)