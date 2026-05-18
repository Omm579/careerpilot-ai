import streamlit as st
from google import genai
import os
import time
import re 

from dotenv import load_dotenv
from utils.pdf_handler import extract_text_from_pdf

from agents.coordinator_agent import (
    run_career_workflow
)

# -----------------------------------
# LOAD ENV VARIABLES
# -----------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error(
        "Missing API key. Set GEMINI_API_KEY or GOOGLE_API_KEY in your .env file."
    )
    st.stop()

client = genai.Client(api_key=api_key)

# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(
    page_title="CareerPilot AI",
    page_icon="🚀",
    layout="wide"
)

# -----------------------------------
# CUSTOM CSS
# -----------------------------------

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

    /* =========================
       CSS VARIABLES
    ========================== */

    :root {
        --bg-void:      #04040a;
        --bg-deep:      #080812;
        --bg-surface:   #0d0d1f;
        --bg-glass:     rgba(13, 13, 31, 0.72);
        --bg-card:      rgba(18, 18, 38, 0.80);

        --accent-gold:  #f0c040;
        --accent-amber: #f97316;
        --accent-teal:  #2dd4bf;
        --accent-lilac: #a78bfa;

        --text-bright:  #f1f0ff;
        --text-mid:     #9896b8;
        --text-dim:     #4e4d6a;

        --border-soft:  rgba(240, 192, 64, 0.10);
        --border-glow:  rgba(240, 192, 64, 0.35);

        --shadow-card:  0 24px 60px rgba(0, 0, 0, 0.55);
        --shadow-glow:  0 0 40px rgba(240, 192, 64, 0.12);
    }

    /* =========================
       GLOBAL RESET
    ========================== */

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        scroll-behavior: smooth;
    }

    /* =========================
       BACKGROUND — DEEP SPACE MESH
    ========================== */

    .stApp {
        background-color: var(--bg-void);
        background-image:
            radial-gradient(ellipse 80% 60% at 15% 10%, rgba(167,139,250,0.07) 0%, transparent 60%),
            radial-gradient(ellipse 60% 50% at 85% 85%, rgba(45,212,191,0.06) 0%, transparent 55%),
            radial-gradient(ellipse 40% 40% at 50% 50%, rgba(240,192,64,0.04) 0%, transparent 60%),
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 80px,
                rgba(255,255,255,0.012) 80px,
                rgba(255,255,255,0.012) 81px
            ),
            repeating-linear-gradient(
                90deg,
                transparent,
                transparent 80px,
                rgba(255,255,255,0.012) 80px,
                rgba(255,255,255,0.012) 81px
            );
        color: var(--text-bright);
    }

    /* Noise grain overlay */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
        pointer-events: none;
        z-index: 0;
        opacity: 1;
    }

    /* =========================
       HEADINGS
    ========================== */

    h1, h2, h3, h4 {
        font-family: 'Syne', sans-serif !important;
        color: var(--text-bright) !important;
        letter-spacing: -0.03em;
    }

    h2 {
        font-size: 1.5rem !important;
        font-weight: 700 !important;
        border-bottom: 1px solid var(--border-soft);
        padding-bottom: 0.5rem;
        margin-bottom: 1.25rem !important;
    }

    p, li {
        color: var(--text-mid);
        line-height: 1.7;
    }

    /* =========================
       SIDEBAR
    ========================== */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                rgba(8, 8, 18, 0.97) 0%,
                rgba(4, 4, 10, 0.99) 100%
            );
        border-right: 1px solid var(--border-soft);
        backdrop-filter: blur(28px);
        box-shadow: 4px 0 40px rgba(0,0,0,0.5);
    }

    section[data-testid="stSidebar"] * {
        color: var(--text-bright) !important;
    }

    section[data-testid="stSidebar"] h3 {
        font-family: 'Syne', sans-serif !important;
        color: var(--accent-gold) !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
        font-weight: 600 !important;
    }

    section[data-testid="stSidebar"] .stSuccess {
        background: rgba(45, 212, 191, 0.08) !important;
        border: 1px solid rgba(45, 212, 191, 0.25) !important;
        border-radius: 10px !important;
        color: var(--accent-teal) !important;
    }

    /* =========================
       AGENT CARDS
    ========================== */

    .agent-card {
        background: var(--bg-card);
        backdrop-filter: blur(20px);
        padding: 28px 20px;
        border-radius: 20px;
        text-align: center;
        border: 1px solid var(--border-soft);
        box-shadow: var(--shadow-card);
        transition: all 0.4s cubic-bezier(0.23, 1, 0.32, 1);
        position: relative;
        overflow: hidden;
    }

    /* top accent line */
    .agent-card::after {
        content: "";
        position: absolute;
        top: 0; left: 10%; right: 10%;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent,
            var(--accent-gold),
            transparent
        );
        opacity: 0.5;
    }

    .agent-card::before {
        content: "";
        position: absolute;
        inset: 0;
        background: radial-gradient(
            circle at 50% 0%,
            rgba(240,192,64,0.08) 0%,
            transparent 65%
        );
        opacity: 0;
        transition: opacity 0.4s ease;
    }

    .agent-card:hover::before {
        opacity: 1;
    }

    .agent-card:hover {
        transform: translateY(-10px) scale(1.03);
        border-color: var(--border-glow);
        box-shadow:
            var(--shadow-card),
            0 0 35px rgba(240, 192, 64, 0.14),
            0 0 80px rgba(240, 192, 64, 0.04);
    }

    .agent-card h3 {
        font-size: 2.2rem;
        margin-bottom: 10px;
    }

    .agent-card h4 {
        font-family: 'Syne', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.05em;
        color: var(--text-bright) !important;
        margin-bottom: 6px;
    }

    .agent-card p {
        font-size: 0.78rem;
        color: var(--text-dim) !important;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    /* =========================
       BUTTONS
    ========================== */

    .stButton > button {
        width: 100%;
        border: 1px solid rgba(240, 192, 64, 0.4) !important;
        border-radius: 14px;
        padding: 15px 22px;
        font-family: 'Syne', sans-serif;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--bg-void) !important;
        background: linear-gradient(
            135deg,
            var(--accent-gold) 0%,
            var(--accent-amber) 100%
        ) !important;
        box-shadow:
            0 8px 28px rgba(240, 192, 64, 0.28),
            inset 0 1px 0 rgba(255,255,255,0.2);
        transition: all 0.3s cubic-bezier(0.23, 1, 0.32, 1);
    }

    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow:
            0 16px 40px rgba(240, 192, 64, 0.40),
            0 0 60px rgba(240, 192, 64, 0.12),
            inset 0 1px 0 rgba(255,255,255,0.25);
        filter: brightness(1.06);
    }

    .stButton > button:active {
        transform: scale(0.97) translateY(0px);
    }

    /* =========================
       INPUTS
    ========================== */

    .stTextInput input {
        background: rgba(8, 8, 18, 0.85) !important;
        border: 1px solid var(--border-soft) !important;
        color: var(--text-bright) !important;
        border-radius: 12px !important;
        padding: 14px 16px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 15px !important;
        transition: all 0.3s ease;
    }

    .stTextInput input::placeholder {
        color: var(--text-dim) !important;
    }

    .stTextInput input:focus {
        border-color: var(--accent-gold) !important;
        box-shadow: 0 0 0 3px rgba(240, 192, 64, 0.15) !important;
        background: rgba(10, 10, 22, 0.95) !important;
    }

    /* =========================
       FILE UPLOADER
    ========================== */

    .stFileUploader {
        background: rgba(8, 8, 18, 0.7);
        border: 1px dashed rgba(167, 139, 250, 0.35);
        padding: 12px;
        border-radius: 16px;
        transition: border-color 0.3s ease;
    }

    .stFileUploader:hover {
        border-color: rgba(167, 139, 250, 0.65);
    }

    /* =========================
       CHECKBOX
    ========================== */

    .stCheckbox label {
        color: var(--text-mid) !important;
        font-size: 14px;
    }

    .stCheckbox [data-testid="stCheckbox"] > label > div:first-child {
        border-color: var(--border-glow) !important;
        background: var(--bg-surface) !important;
    }

    /* =========================
       SELECT BOX
    ========================== */

    .stSelectbox > div > div {
        background: rgba(8, 8, 18, 0.85) !important;
        border: 1px solid var(--border-soft) !important;
        border-radius: 12px !important;
        color: var(--text-bright) !important;
    }

    /* =========================
       TABS
    ========================== */

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(8, 8, 18, 0.6);
        padding: 6px;
        border-radius: 16px;
        border: 1px solid var(--border-soft);
        margin-bottom: 18px;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none !important;
        border-radius: 12px;
        padding: 10px 20px;
        color: var(--text-dim);
        font-family: 'Syne', sans-serif;
        font-size: 13px;
        font-weight: 600;
        letter-spacing: 0.05em;
        transition: all 0.25s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(240, 192, 64, 0.07);
        color: var(--text-mid);
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(
            135deg,
            rgba(240,192,64,0.18),
            rgba(249,115,22,0.12)
        ) !important;
        border: 1px solid rgba(240,192,64,0.30) !important;
        color: var(--accent-gold) !important;
        box-shadow: 0 4px 16px rgba(240,192,64,0.10);
    }

    /* =========================
       METRICS
    ========================== */

    [data-testid="metric-container"] {
        background: var(--bg-card);
        border: 1px solid var(--border-soft);
        padding: 22px 24px;
        border-radius: 18px;
        backdrop-filter: blur(16px);
        box-shadow: var(--shadow-card), var(--shadow-glow);
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease;
    }

    [data-testid="metric-container"]::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 2px;
        background: linear-gradient(
            90deg,
            var(--accent-gold),
            var(--accent-amber)
        );
    }

    [data-testid="metric-container"]:hover {
        transform: translateY(-4px);
    }

    [data-testid="metric-container"] [data-testid="metric-value"] {
        font-family: 'Syne', sans-serif !important;
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: var(--accent-gold) !important;
    }

    [data-testid="metric-container"] label {
        color: var(--text-mid) !important;
        font-size: 12px !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
    }

    /* =========================
       PROGRESS BAR
    ========================== */

    .stProgress > div > div > div > div {
        background: linear-gradient(
            90deg,
            var(--accent-gold) 0%,
            var(--accent-amber) 50%,
            var(--accent-teal) 100%
        );
        border-radius: 999px;
        box-shadow: 0 0 12px rgba(240,192,64,0.4);
    }

    .stProgress > div > div {
        background: rgba(255,255,255,0.05) !important;
        border-radius: 999px !important;
    }

    /* =========================
       ALERTS & SPINNERS
    ========================== */

    .stAlert {
        border-radius: 14px !important;
        border: 1px solid var(--border-soft) !important;
        backdrop-filter: blur(12px) !important;
        background: rgba(8, 8, 18, 0.8) !important;
    }

    .stAlert [data-testid="stAlertContentInfo"] {
        color: var(--accent-teal) !important;
    }

    .stAlert [data-testid="stAlertContentSuccess"] {
        color: #4ade80 !important;
    }

    .stAlert [data-testid="stAlertContentError"] {
        color: #f87171 !important;
    }

    /* =========================
       DOWNLOAD BUTTON
    ========================== */

    .stDownloadButton > button {
        background: transparent !important;
        border: 1px solid var(--border-glow) !important;
        color: var(--accent-gold) !important;
        border-radius: 12px !important;
        font-family: 'Syne', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        transition: all 0.3s ease !important;
    }

    .stDownloadButton > button:hover {
        background: rgba(240,192,64,0.08) !important;
        box-shadow: 0 0 20px rgba(240,192,64,0.15) !important;
        transform: translateY(-2px) !important;
    }

    /* =========================
       DIVIDER
    ========================== */

    hr {
        border: none !important;
        height: 1px !important;
        background: linear-gradient(
            90deg,
            transparent,
            var(--border-soft),
            var(--accent-gold),
            var(--border-soft),
            transparent
        ) !important;
        margin: 2rem 0 !important;
        opacity: 0.6;
    }

    /* =========================
       BLOCK CONTAINER
    ========================== */

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1300px;
    }

    /* =========================
       MARKDOWN CONTENT
    ========================== */

    .stMarkdown h3 {
        color: var(--accent-gold) !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        margin-top: 1.5rem !important;
    }

    .stMarkdown strong {
        color: var(--text-bright) !important;
        font-weight: 600 !important;
    }

    .stMarkdown ul li::marker {
        color: var(--accent-gold);
    }

    /* =========================
       SCROLLBAR
    ========================== */

    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-void); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(
            180deg,
            var(--accent-gold),
            var(--accent-amber)
        );
        border-radius: 999px;
    }

    /* =========================
       FOOTER
    ========================== */

    footer { visibility: hidden; }

    /* =========================
       ANIMATIONS
    ========================== */

    @keyframes pulse-gold {
        0%, 100% { box-shadow: 0 0 8px rgba(240,192,64,0.15); }
        50%       { box-shadow: 0 0 28px rgba(240,192,64,0.40); }
    }

    @keyframes slide-up {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    .agent-card {
        animation: slide-up 0.5s ease forwards;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------------
# SESSION MEMORY
# -----------------------------------

if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------
# CACHE PDF EXTRACTION
# -----------------------------------

@st.cache_data(show_spinner=False)

def cached_pdf_text(file_bytes):

    from io import BytesIO

    pdf_file = BytesIO(file_bytes)

    text = extract_text_from_pdf(pdf_file)

    text = " ".join(text.split())

    return text[:4000]

# -----------------------------------
# CACHE WORKFLOW
# -----------------------------------

@st.cache_data(show_spinner=False)

def cached_workflow(
    resume,
    role
):

    return run_career_workflow(
        client,
        resume,
        role
    )

# -----------------------------------
# SIDEBAR
# -----------------------------------

st.sidebar.title("CareerPilot AI")

st.sidebar.write("""
### Multi-Agent AI Career Assistant

Features:
- Resume Analysis
- Skill Gap Detection
- Interview Preparation
- Career Recommendations
- ATS Optimization
""")

st.sidebar.success(
    "AI Agents Ready"
)

st.sidebar.subheader("Previous Analyses")

if len(st.session_state.history) == 0:

    st.sidebar.caption(
        "No analyses yet."
    )

else:

    for item in st.session_state.history:

        st.sidebar.write(
            f"🎯 {item['role']}"
        )

# -----------------------------------
# MAIN TITLE
# -----------------------------------

st.markdown(
    """
    <div style='
        text-align: center; 
        padding: 3.5rem 2rem; 
        margin: 1rem 0 2.5rem 0;
        background:
            radial-gradient(ellipse 80% 80% at 50% 0%, rgba(240,192,64,0.06) 0%, transparent 70%),
            rgba(8, 8, 18, 0.75);
        border: 1px solid rgba(240, 192, 64, 0.12);
        border-radius: 24px;
        box-shadow:
            0 30px 80px rgba(0,0,0,0.5),
            inset 0 1px 0 rgba(240,192,64,0.08);
        backdrop-filter: blur(12px);
        position: relative;
        overflow: hidden;
    '>
        <div style='
            position: absolute;
            top: 0; left: 30%; right: 30%;
            height: 1px;
            background: linear-gradient(90deg, transparent, rgba(240,192,64,0.6), transparent);
        '></div>
        <p style='
            font-family: "Syne", sans-serif;
            font-size: 0.72rem;
            color: rgba(240,192,64,0.7);
            letter-spacing: 0.35em;
            text-transform: uppercase;
            margin-bottom: 1rem;
            font-weight: 600;
        '>Multi-Agent AI System</p>
        <h1 style='
            font-family: "Syne", sans-serif;
            font-size: min(9vw, 4.2rem); 
            font-weight: 800;
            color: #f1f0ff;
            margin-bottom: 0.6rem;
            letter-spacing: -0.05em;
            line-height: 1;
        '>
            🚀 CareerPilot <span style="
                background: linear-gradient(135deg, #f0c040, #f97316);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            ">AI</span>
        </h1>
        <p style='
            font-family: "DM Sans", sans-serif;
            font-size: min(4vw, 1.15rem); 
            color: #6b6a8a;
            font-weight: 300;
            max-width: 520px;
            margin: 0 auto;
            line-height: 1.6;
            letter-spacing: 0.01em;
        '>
            Precision-engineered career intelligence,<br>powered by four specialized AI agents.
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# -----------------------------------
# DEMO RESUME OPTION
# -----------------------------------

use_sample = st.checkbox(
    "Use Demo Resume"
)

resume = None

sample_resume = None

if use_sample:

    sample_resume = st.selectbox(
        "Choose Demo Resume",
        [
            "Default Resume",
            "AI Engineer Resume",
            "Data Analyst Resume",
            "Frontend Developer Resume"
        ]
    )

# -----------------------------------
# FILE UPLOAD + ROLE INPUT
# -----------------------------------

col1, col2 = st.columns(2)

with col1:

    uploaded_file = st.file_uploader(
        "Upload Your Resume (PDF)",
        type=["pdf"]
    )

    if use_sample:
        
        try:
            
            BASE_DIR = os.path.dirname(
                os.path.abspath(__file__)
            )
            
            if sample_resume == "Default Resume":
                resume_path = os.path.join(
                    BASE_DIR,
                    "data",
                    "sample_resume.txt"
                )
            
            elif sample_resume == "AI Engineer Resume":
                resume_path = os.path.join(
                    BASE_DIR,
                    "data",
                    "demo_resumes",
                    "ai_resume.txt"
                )
            
            elif sample_resume == "Data Analyst Resume":
                resume_path = os.path.join(
                    BASE_DIR,
                    "data",
                    "demo_resumes",
                    "data_analyst_resume.txt"
                )
            
            else:
                
                resume_path = os.path.join(
                    BASE_DIR,
                    "data",
                    "demo_resumes",
                    "frontend_resume.txt"
                )
            
            with open(
                resume_path,
                "r",
                encoding="utf-8"
            ) as file:

                resume = file.read()

            st.success(
                f"{sample_resume} Loaded Successfully"
            )
            
        except Exception as e:
            
            st.error(
                f"Error loading resume: {e}"
            )

    elif uploaded_file is not None:

        file_bytes = uploaded_file.read()

        resume = cached_pdf_text(
            file_bytes
        )

        st.success(
            "Resume Uploaded Successfully"
        )

with col2:

    role = st.text_input(
        "Enter Your Target Role",
        placeholder="Example: AI Engineer"
    )

# -----------------------------------
# RUN BUTTON
# -----------------------------------

if st.button("Run Career Analysis"):

    # -----------------------------------
    # VALIDATION
    # -----------------------------------

    if not resume:

        st.error(
            "Please upload your resume PDF or use the sample."
        )

    elif not role:

        st.error(
            "Please enter your target role."
        )

    else:

        # -----------------------------------
        # TIMER START
        # -----------------------------------

        start_time = time.time()

        # -----------------------------------
        # PROGRESS + STATUS
        # -----------------------------------

        progress = st.progress(0)

        status = st.empty()

        # -----------------------------------
        # AGENT DASHBOARD
        # -----------------------------------

        st.subheader("🤖 AI Agent Activity")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            resume_agent_card = st.empty()
            resume_agent_card.markdown(
                """
                <div class="agent-card">
                    <h3>📄</h3>
                    <h4>Resume Agent</h4>
                    <p>ATS Optimization</p>
                </div>
                """,
                unsafe_allow_html=True
           )

        with col2:
            skill_agent_card = st.empty()
            skill_agent_card.markdown(
                """
                <div class="agent-card">
                    <h3>🧠</h3>
                    <h4>Skill Agent</h4>
                    <p>Gap Analysis</p>
                </div>
                """,
                unsafe_allow_html=True
           )
            
        with col3:
            interview_agent_card = st.empty()
            interview_agent_card.markdown(
                """
                <div class="agent-card">
                    <h3>🎤</h3>
                    <h4>Interview Agent</h4>
                    <p>Question Generation</p>
                </div>
                """,
                unsafe_allow_html=True
           )

        with col4:
            strategy_agent_card = st.empty()
            strategy_agent_card.markdown(
                """
                <div class="agent-card">
                    <h3>🚀</h3>
                    <h4>Strategy Agent</h4>
                    <p>Career Roadmap</p>
                </div>
                """,
                unsafe_allow_html=True
           )

        try:

            with st.spinner(
                "Launching AI Agents..."
            ):

                # -----------------------------------
                # RESUME AGENT
                # -----------------------------------

                status.info(
                    "Resume Agent Analyzing Resume..."
                )

                resume_agent_card.markdown(
                    """
                    <div class="agent-card">
                        <h3>📄</h3>
                        <h4>Resume Agent</h4>
                        <p style='color:#f0c040;'>Working...</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                progress.progress(20)

                time.sleep(0.5)

                # -----------------------------------
                # SKILL AGENT
                # -----------------------------------

                status.info(
                    "Skill Gap Agent Comparing Skills..."
                )

                skill_agent_card.markdown(
                    """
                    <div class="agent-card">
                        <h3>🧠</h3>
                        <h4>Skill Agent</h4>
                        <p style='color:#f0c040;'>Working...</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                progress.progress(45)

                time.sleep(0.5)

                # -----------------------------------
                # INTERVIEW AGENT
                # -----------------------------------

                status.info(
                    "Interview Agent Preparing Questions..."
                )

                interview_agent_card.markdown(
                    """
                    <div class="agent-card">
                        <h3>🎤</h3>
                        <h4>Interview Agent</h4>
                        <p style='color:#f0c040;'>Working...</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                progress.progress(70)

                time.sleep(0.5)

                # -----------------------------------
                # STRATEGY AGENT
                # -----------------------------------

                status.info(
                    "Strategy Agent Building Roadmap..."
                )

                strategy_agent_card.markdown(
                    """
                    <div class="agent-card">
                        <h3>🚀</h3>
                        <h4>Strategy Agent</h4>
                        <p style='color:#f0c040;'>Working...</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                progress.progress(90)

                # -----------------------------------
                # MAIN WORKFLOW
                # -----------------------------------

                (
                    resume_result,
                    skill_result,
                    interview_result,
                    final_summary,
                    final_recommendation
                ) = cached_workflow(
                    resume,
                    role
                )

                progress.progress(100)

                # -----------------------------------
                # COMPLETE STATUS
                # -----------------------------------

                resume_agent_card.markdown(
                    """
                    <div class="agent-card">
                        <h3>📄</h3>
                        <h4>Resume Agent</h4>
                        <p style='color:#2dd4bf;'>Completed ✓</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                skill_agent_card.markdown(
                    """
                    <div class="agent-card">
                        <h3>🧠</h3>
                        <h4>Skill Agent</h4>
                        <p style='color:#2dd4bf;'>Completed ✓</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                interview_agent_card.markdown(
                    """
                    <div class="agent-card">
                        <h3>🎤</h3>
                        <h4>Interview Agent</h4>
                        <p style='color:#2dd4bf;'>Completed ✓</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                strategy_agent_card.markdown(
                    """
                    <div class="agent-card">
                        <h3>🚀</h3>
                        <h4>Strategy Agent</h4>
                        <p style='color:#2dd4bf;'>Completed ✓</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                status.success(
                    "All AI Agents Completed Successfully"
                )

        except Exception as e:

            st.error(
                f"AI Service Error: {e}"
            )

            st.stop()

        # -----------------------------------
        # TIMER END
        # -----------------------------------

        end_time = time.time()

        execution_time = round(
            end_time - start_time,
            2
        )

        st.success(
            f"Analysis Completed in {execution_time} seconds"
        )

        # -----------------------------------
        # STORE HISTORY
        # -----------------------------------

        st.session_state.history.append({
            "role": role,
            "summary": final_summary
        })

        st.divider()

        # -----------------------------------
        # ATS SCORE
        # -----------------------------------

        st.subheader("📊 ATS Optimization Score")

        # Default fallback score
        ats_score = 75
        
        try:
            
            # Search for score pattern like:
            # "85/100"
            # "ATS Score: 85"
            # etc.
            
            match = re.search(
                r"(\d{1,3})\s*/\s*100",
                resume_result
            )

            if match:
                
                ats_score = int(match.group(1))
                
                # Prevent invalid values
                ats_score = max(
                    0,
                    min(ats_score, 100)
                )
        except:
            
            ats_score = 75
            
        ats_col1, ats_col2 = st.columns([1, 3])

        with ats_col1:

            st.metric(
                "ATS Score",
                f"{ats_score}/100"
            )

        with ats_col2:

            st.progress(
                ats_score / 100
            )

        st.divider()

        # -----------------------------------
        # TABS
        # -----------------------------------

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Resume Analysis",
            "Skill Gap",
            "Interview Prep",
            "Final Recommendation",
            "Career Strategy"
        ])

        # -----------------------------------
        # TAB 1
        # -----------------------------------

        with tab1:

            st.markdown(
                resume_result
            )

        # -----------------------------------
        # TAB 2
        # -----------------------------------

        with tab2:

            st.markdown(
                skill_result
            )

        # -----------------------------------
        # TAB 3
        # -----------------------------------

        with tab3:

            st.markdown(
                interview_result
            )

        # -----------------------------------
        # TAB 4
        # -----------------------------------

        with tab4:

            st.markdown(
                final_recommendation
            )

        # -----------------------------------
        # TAB 5
        # -----------------------------------

        with tab5:

            st.markdown(
                final_summary
            )

        # -----------------------------------
        # FINAL REPORT
        # -----------------------------------

        final_report = f"""
CareerPilot AI Report

==================================

TARGET ROLE

{role}

==================================

RESUME ANALYSIS

{resume_result}

==================================

SKILL GAP ANALYSIS

{skill_result}

==================================

INTERVIEW PREPARATION

{interview_result}

==================================

CAREER STRATEGY

{final_summary}

==================================

FINAL RECOMMENDATION

{final_recommendation}

==================================

Generated by CareerPilot AI
"""

        # -----------------------------------
        # DOWNLOAD BUTTON
        # -----------------------------------

        st.download_button(
            label="📥 Download Full Report",
            data=final_report,
            file_name="career_report.txt",
            mime="text/plain"
        )

# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.markdown(
    """
    <p style='text-align:center; color:#2d2c48; font-family:"Syne",sans-serif; font-size:0.75rem; letter-spacing:0.12em; text-transform:uppercase;'>

    Built using Gemini · Streamlit · Multi-Agent Workflow

    </p>
    """,
    unsafe_allow_html=True
)
