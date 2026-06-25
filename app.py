
import streamlit as st
from datetime import date, datetime
from database import *

st.set_page_config(page_title="Momentum 6.0", page_icon="🏋️", layout="wide", initial_sidebar_state="collapsed")
init_db()


def require_password():
    """
    Private access gate.
    Local default password: momentum
    Deployment password: set APP_PASSWORD in Streamlit secrets.
    """
    try:
        expected_password = st.secrets.get("APP_PASSWORD", "momentum")
    except Exception:
        expected_password = "momentum"

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if st.session_state["authenticated"]:
        return

    st.markdown('<div class="momentum-logo">Momentum</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="hero-card">
            <h1>Private Access</h1>
            <p>Enter your password to open Momentum.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    password = st.text_input("Password", type="password")

    if st.button("Enter Momentum"):
        if password == expected_password:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    st.stop()



st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #F6F0E8;
        --panel: #FFFDF9;
        --panel-soft: #F1E6D8;
        --border: #E4D8C8;
        --text: #34281F;
        --muted: #7B6A58;
        --red: #9B1C1C;
        --red-dark: #7F1717;
        --navy: #1F3A5F;
        --gold: #D4A65A;
        --taupe: #BFAE9A;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(212,166,90,0.12), transparent 28%),
            linear-gradient(135deg, #F9F4EC 0%, #F6F0E8 50%, #EFE4D3 100%);
        color: var(--text);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F8F1E7 0%, #EFE4D3 100%);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] * {
        color: var(--text);
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }

    h1 {
        color: var(--text);
        letter-spacing: -0.045em;
        font-weight: 800;
        font-size: 2.4rem;
        margin-bottom: 0.2rem;
    }

    h2, h3 {
        color: var(--text);
        letter-spacing: -0.03em;
        font-weight: 750;
    }

    p, label, .stCaption {
        color: var(--muted);
    }

    div[data-testid="stMetric"] {
        background: rgba(255,253,249,0.92);
        border: 1px solid var(--border);
        padding: 1.05rem 1rem;
        border-radius: 20px;
        box-shadow: 0 12px 30px rgba(59, 48, 36, 0.07);
    }

    div[data-testid="stMetric"] label {
        color: var(--muted) !important;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        font-size: 0.72rem;
        font-weight: 700;
    }

    div[data-testid="stMetricValue"] {
        color: var(--red);
        font-weight: 800;
    }

    div[data-testid="stExpander"] {
        background: rgba(255,253,249,0.78);
        border: 1px solid var(--border);
        border-radius: 18px;
        box-shadow: 0 8px 20px rgba(59,48,36,0.05);
    }

    .stButton > button, .stDownloadButton > button {
        border-radius: 14px;
        border: 1px solid var(--taupe);
        background: #FFFDF9;
        color: var(--text);
        font-weight: 700;
        padding: 0.55rem 1rem;
        box-shadow: 0 6px 16px rgba(59,48,36,0.06);
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color: var(--red);
        color: var(--red);
        background: #FFF8EF;
    }

    div[data-testid="stAlert"] {
        border-radius: 16px;
        border: 1px solid var(--border);
        box-shadow: 0 8px 18px rgba(59,48,36,0.05);
    }

    div[data-testid="stDataFrame"] {
        background: rgba(255,253,249,0.92);
        border-radius: 18px;
        border: 1px solid var(--border);
        padding: 0.4rem;
        box-shadow: 0 8px 22px rgba(59,48,36,0.05);
    }

    .momentum-logo {
        font-size: 0.78rem;
        letter-spacing: 0.28em;
        text-transform: uppercase;
        color: var(--red);
        font-weight: 800;
        margin-bottom: 0.1rem;
    }

    .hero-card {
        background: rgba(255,253,249,0.82);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.4rem 1.5rem;
        box-shadow: 0 16px 35px rgba(59,48,36,0.08);
        margin-bottom: 1rem;
    }

    .section-card {
        background: rgba(255,253,249,0.86);
        border: 1px solid var(--border);
        border-radius: 24px;
        padding: 1.15rem 1.25rem;
        box-shadow: 0 14px 32px rgba(59,48,36,0.07);
        margin: 0.7rem 0 1rem 0;
    }

    .eyebrow {
        text-transform: uppercase;
        font-size: 0.72rem;
        letter-spacing: 0.11em;
        color: var(--muted);
        font-weight: 800;
        margin-bottom: 0.45rem;
    }

    .big-red {
        color: var(--red);
        font-weight: 800;
        font-size: 1.35rem;
    }

    .navy-pill {
        display: inline-block;
        padding: 0.32rem 0.65rem;
        border-radius: 999px;
        background: rgba(31,58,95,0.10);
        color: var(--navy);
        font-weight: 800;
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }

    .quote-card {
        background: rgba(255,253,249,0.75);
        border: 1px solid var(--border);
        border-radius: 18px;
        padding: 1rem;
        color: var(--muted);
        font-size: 0.95rem;
        box-shadow: 0 10px 22px rgba(59,48,36,0.05);
    }

    .primary-action {
        background: linear-gradient(135deg, #9B1C1C 0%, #7F1717 100%);
        color: white;
        border-radius: 16px;
        padding: 0.9rem 1rem;
        text-align: center;
        font-weight: 800;
        margin-top: 1rem;
        box-shadow: 0 10px 25px rgba(155,28,28,0.20);
    }

    .small-muted {
        color: var(--muted);
        font-size: 0.88rem;
    }

    hr {
        border-color: rgba(228,216,200,0.7);
    }
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
    /* v2.1 cleanup */
    @media (max-width: 900px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        div[data-testid="stMetric"] {
            margin-bottom: 0.75rem;
        }

        h1 {
            font-size: 2rem !important;
        }

        .hero-card {
            padding: 1.2rem !important;
        }
    }

    /* Hide empty markdown/card artifacts if any render blank */
    .section-card:empty {
        display: none !important;
    }

    .primary-action-note {
        background: linear-gradient(135deg, #9B1C1C 0%, #7F1717 100%);
        color: white;
        border-radius: 16px;
        padding: 0.9rem 1rem;
        text-align: center;
        font-weight: 800;
        margin-top: 1rem;
        box-shadow: 0 10px 25px rgba(155,28,28,0.20);
    }

    .weeks-left {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 999px;
        background: rgba(155,28,28,0.10);
        color: #9B1C1C;
        font-weight: 800;
        font-size: 0.85rem;
        margin-left: 0.4rem;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
    /* v3.4 bundle polish */
    .power-tile {
        background: rgba(255,253,249,0.92);
        border: 1px solid #E4D8C8;
        border-radius: 20px;
        padding: 1rem;
        margin: 0.75rem 0;
        box-shadow: 0 10px 24px rgba(59,48,36,0.06);
    }

    .power-title {
        color: #9B1C1C;
        font-weight: 800;
        font-size: 1.1rem;
    }

    .power-muted {
        color: #7B6A58;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


st.markdown("""
<style>
    /* Momentum v4.4 Premium UI Bundle */
    .premium-hero {
        background:
            radial-gradient(circle at top right, rgba(212,166,90,0.18), transparent 28%),
            linear-gradient(135deg, rgba(255,253,249,0.95), rgba(246,240,232,0.88));
        border: 1px solid #E4D8C8;
        border-radius: 30px;
        padding: 1.6rem 1.7rem;
        box-shadow: 0 18px 42px rgba(59,48,36,0.10);
        margin-bottom: 1rem;
    }

    .premium-hero h1 {
        margin: 0;
        font-size: 2.55rem;
        letter-spacing: -0.055em;
        color: #34281F;
    }

    .premium-hero-sub {
        color: #7B6A58;
        margin-top: 0.35rem;
        font-size: 1rem;
    }

    .premium-pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        margin-top: 1rem;
    }

    .premium-pill {
        display: inline-block;
        padding: 0.42rem 0.72rem;
        border-radius: 999px;
        background: rgba(31,58,95,0.10);
        color: #1F3A5F;
        font-weight: 800;
        font-size: 0.82rem;
    }

    .premium-pill-red {
        background: rgba(155,28,28,0.11);
        color: #9B1C1C;
    }

    .premium-timeline {
        background: rgba(255,253,249,0.88);
        border: 1px solid #E4D8C8;
        border-radius: 24px;
        padding: 1rem;
        box-shadow: 0 12px 28px rgba(59,48,36,0.07);
        margin: 1rem 0;
    }

    .timeline-grid {
        display: grid;
        grid-template-columns: repeat(12, minmax(42px, 1fr));
        gap: 0.45rem;
    }

    .week-chip {
        text-align: center;
        border-radius: 16px;
        padding: 0.55rem 0.25rem;
        border: 1px solid #E4D8C8;
        background: rgba(246,240,232,0.72);
        color: #7B6A58;
        font-size: 0.78rem;
        font-weight: 800;
    }

    .week-chip.done {
        background: rgba(31,58,95,0.10);
        color: #1F3A5F;
        border-color: rgba(31,58,95,0.18);
    }

    .week-chip.current {
        background: linear-gradient(135deg, #9B1C1C, #7F1717);
        color: white;
        border-color: #7F1717;
        box-shadow: 0 10px 22px rgba(155,28,28,0.18);
    }

    .premium-card {
        background: rgba(255,253,249,0.9);
        border: 1px solid #E4D8C8;
        border-radius: 26px;
        padding: 1.15rem 1.25rem;
        box-shadow: 0 14px 32px rgba(59,48,36,0.075);
        margin: 0.75rem 0 1rem 0;
    }

    .premium-card-title {
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #7B6A58;
        font-size: 0.72rem;
        font-weight: 850;
        margin-bottom: 0.5rem;
    }

    .premium-card-main {
        color: #9B1C1C;
        font-size: 1.45rem;
        font-weight: 850;
        letter-spacing: -0.035em;
    }

    .premium-card-muted {
        color: #7B6A58;
        font-size: 0.92rem;
        margin-top: 0.35rem;
    }

    .premium-action {
        background: linear-gradient(135deg, #9B1C1C 0%, #7F1717 100%);
        color: #FFFDF9;
        border-radius: 18px;
        padding: 0.95rem 1rem;
        text-align: center;
        font-weight: 850;
        margin-top: 1rem;
        box-shadow: 0 12px 28px rgba(155,28,28,0.22);
    }

    @media (max-width: 900px) {
        .premium-hero {
            padding: 1.2rem;
            border-radius: 22px;
        }

        .premium-hero h1 {
            font-size: 2rem;
        }

        .timeline-grid {
            grid-template-columns: repeat(4, 1fr);
        }

        .premium-card {
            border-radius: 22px;
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
    /* Momentum 5.0 - Premium Operating System */

    .m5-hero {
        background:
            radial-gradient(circle at top right, rgba(212,166,90,0.18), transparent 30%),
            linear-gradient(135deg, rgba(255,253,249,0.97), rgba(246,240,232,0.88));
        border: 1px solid #E4D8C8;
        border-radius: 32px;
        padding: 1.65rem 1.75rem;
        box-shadow: 0 18px 44px rgba(59,48,36,0.10);
        margin-bottom: 1rem;
    }

    .m5-hero h1 {
        margin: 0;
        font-size: 2.65rem;
        letter-spacing: -0.06em;
        color: #34281F;
    }

    .m5-hero-sub {
        color: #7B6A58;
        margin-top: 0.4rem;
        font-size: 1rem;
        max-width: 640px;
    }

    .m5-pill-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.55rem;
        margin-top: 1rem;
    }

    .m5-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        padding: 0.42rem 0.76rem;
        border-radius: 999px;
        background: rgba(31,58,95,0.10);
        color: #1F3A5F;
        font-weight: 850;
        font-size: 0.82rem;
    }

    .m5-pill-red {
        background: rgba(155,28,28,0.11);
        color: #9B1C1C;
    }

    .m5-timeline {
        background: rgba(255,253,249,0.90);
        border: 1px solid #E4D8C8;
        border-radius: 26px;
        padding: 1rem;
        box-shadow: 0 12px 30px rgba(59,48,36,0.07);
        margin: 1rem 0 1.1rem;
    }

    .m5-timeline-grid {
        display: grid;
        grid-template-columns: repeat(12, minmax(42px, 1fr));
        gap: 0.45rem;
    }

    .m5-week-chip {
        text-align: center;
        border-radius: 16px;
        padding: 0.55rem 0.25rem;
        border: 1px solid #E4D8C8;
        background: rgba(246,240,232,0.72);
        color: #7B6A58;
        font-size: 0.78rem;
        font-weight: 850;
        min-height: 54px;
    }

    .m5-week-chip.done {
        background: rgba(31,58,95,0.10);
        color: #1F3A5F;
        border-color: rgba(31,58,95,0.18);
    }

    .m5-week-chip.current {
        background: linear-gradient(135deg, #9B1C1C, #7F1717);
        color: white;
        border-color: #7F1717;
        box-shadow: 0 10px 22px rgba(155,28,28,0.18);
    }

    .m5-card {
        background: rgba(255,253,249,0.92);
        border: 1px solid #E4D8C8;
        border-radius: 26px;
        padding: 1.15rem 1.25rem;
        box-shadow: 0 14px 32px rgba(59,48,36,0.075);
        margin: 0.75rem 0 1rem;
    }

    .m5-workout-card {
        background: rgba(255,253,249,0.94);
        border: 1px solid #E4D8C8;
        border-radius: 28px;
        padding: 1.2rem 1.3rem 1.25rem;
        box-shadow: 0 16px 38px rgba(59,48,36,0.08);
        margin: 0.75rem 0 1rem;
    }

    .m5-eyebrow {
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #7B6A58;
        font-size: 0.72rem;
        font-weight: 850;
        margin-bottom: 0.5rem;
    }

    .m5-main {
        color: #9B1C1C;
        font-size: 1.5rem;
        font-weight: 880;
        letter-spacing: -0.04em;
        margin-bottom: 0.35rem;
    }

    .m5-muted {
        color: #7B6A58;
        font-size: 0.92rem;
        margin-top: 0.2rem;
    }

    .m5-exercise-list {
        margin-top: 0.95rem;
        display: grid;
        gap: 0.45rem;
    }

    .m5-exercise-row {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        align-items: center;
        padding: 0.52rem 0.65rem;
        border-radius: 14px;
        background: rgba(246,240,232,0.62);
        border: 1px solid rgba(228,216,200,0.75);
        color: #6E5F50;
        font-size: 0.92rem;
    }

    .m5-exercise-name {
        font-weight: 780;
        color: #34281F;
    }

    .m5-exercise-target {
        color: #7B6A58;
        font-weight: 700;
        white-space: nowrap;
    }

    .m5-action {
        background: linear-gradient(135deg, #9B1C1C 0%, #7F1717 100%);
        color: #FFFDF9;
        border-radius: 18px;
        padding: 0.95rem 1rem;
        text-align: center;
        font-weight: 880;
        margin-top: 1rem;
        box-shadow: 0 12px 28px rgba(155,28,28,0.22);
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 52px;
        width: 100%;
    }

    .m5-recovery-card {
        min-height: 100%;
    }

    .m5-section-gap {
        height: 0.35rem;
    }

    @media (max-width: 900px) {
        .m5-hero {
            padding: 1.2rem;
            border-radius: 22px;
        }

        .m5-hero h1 {
            font-size: 2rem;
        }

        .m5-timeline-grid {
            grid-template-columns: repeat(4, 1fr);
        }

        .m5-card,
        .m5-workout-card {
            border-radius: 22px;
            padding: 1rem;
        }

        .m5-exercise-row {
            flex-direction: column;
            align-items: flex-start;
            gap: 0.15rem;
        }

        .m5-exercise-target {
            white-space: normal;
        }
    }
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
    /* Momentum 5.5 - Premium UI Bundle */

    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at top left, rgba(155,28,28,0.08), transparent 30%),
            linear-gradient(180deg, #FFF8EF 0%, #F1E6D8 100%) !important;
        border-right: 1px solid #E4D8C8 !important;
        box-shadow: 10px 0 30px rgba(59,48,36,0.05);
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #34281F;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 0.35rem;
        display: flex;
        flex-direction: column;
    }

    section[data-testid="stSidebar"] label {
        background: rgba(255,253,249,0.58);
        border: 1px solid rgba(228,216,200,0.86);
        border-radius: 15px;
        padding: 0.55rem 0.65rem;
        margin: 0.08rem 0;
        transition: all 0.18s ease;
        box-shadow: 0 5px 14px rgba(59,48,36,0.035);
    }

    section[data-testid="stSidebar"] label:hover {
        background: rgba(255,253,249,0.95);
        border-color: rgba(155,28,28,0.35);
        transform: translateX(2px);
    }

    section[data-testid="stSidebar"] label:has(input:checked) {
        background: linear-gradient(135deg, rgba(155,28,28,0.12), rgba(255,253,249,0.92));
        border-color: rgba(155,28,28,0.45);
        box-shadow: 0 8px 20px rgba(155,28,28,0.08);
    }

    section[data-testid="stSidebar"] label:has(input:checked) p {
        color: #9B1C1C !important;
        font-weight: 850 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] > label {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin-bottom: 0.6rem !important;
    }

    .m55-sidebar-brand {
        background: rgba(255,253,249,0.82);
        border: 1px solid #E4D8C8;
        border-radius: 22px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 12px 28px rgba(59,48,36,0.07);
    }

    .m55-brand-mark {
        color: #9B1C1C;
        font-weight: 900;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        font-size: 0.85rem;
    }

    .m55-brand-sub {
        color: #7B6A58;
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }

    .m55-card {
        background: rgba(255,253,249,0.93);
        border: 1px solid #E4D8C8;
        border-radius: 26px;
        padding: 1.15rem 1.25rem;
        box-shadow: 0 14px 32px rgba(59,48,36,0.075);
        margin: 0.75rem 0 1rem;
    }

    .m55-title {
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #7B6A58;
        font-size: 0.72rem;
        font-weight: 850;
        margin-bottom: 0.55rem;
    }

    .m55-headline {
        color: #9B1C1C;
        font-size: 1.35rem;
        font-weight: 880;
        letter-spacing: -0.04em;
        margin-bottom: 0.3rem;
    }

    .m55-muted {
        color: #7B6A58;
        font-size: 0.92rem;
    }

    .m55-exercise-card {
        background: rgba(255,253,249,0.92);
        border: 1px solid #E4D8C8;
        border-radius: 22px;
        padding: 1rem;
        margin: 0.85rem 0;
        box-shadow: 0 12px 26px rgba(59,48,36,0.065);
    }

    .m55-exercise-title {
        color: #9B1C1C;
        font-weight: 880;
        font-size: 1.12rem;
        letter-spacing: -0.03em;
    }

    .m55-exercise-meta {
        color: #7B6A58;
        font-size: 0.88rem;
        margin-top: 0.2rem;
    }

    .m55-action-strip {
        background: linear-gradient(135deg, rgba(31,58,95,0.08), rgba(255,253,249,0.88));
        border: 1px solid rgba(31,58,95,0.12);
        border-radius: 18px;
        padding: 0.85rem;
        margin: 0.65rem 0;
        color: #1F3A5F;
        font-weight: 750;
    }

    div[data-testid="stMetricValue"] {
        overflow: visible !important;
        text-overflow: clip !important;
        white-space: nowrap !important;
        font-size: clamp(1.5rem, 2.7vw, 2.45rem) !important;
    }

    div[data-testid="stMetric"] {
        min-height: 128px;
    }

    @media (max-width: 900px) {
        div[data-testid="stMetric"] {
            min-height: auto;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.85rem !important;
        }

        .m55-card,
        .m55-exercise-card {
            border-radius: 20px;
            padding: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)



st.markdown("""
<style>
    /* Momentum 6.0 Core Complete polish */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    div[data-testid="stMetric"] {
        min-height: 124px;
    }

    div[data-testid="stMetricValue"] {
        overflow: visible !important;
        text-overflow: clip !important;
        white-space: nowrap !important;
        font-size: clamp(1.55rem, 2.6vw, 2.35rem) !important;
    }

    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at top left, rgba(155,28,28,0.08), transparent 30%),
            linear-gradient(180deg, #FFF8EF 0%, #F1E6D8 100%) !important;
        border-right: 1px solid #E4D8C8 !important;
        box-shadow: 10px 0 30px rgba(59,48,36,0.05);
    }

    @media (max-width: 900px) {
        .block-container {
            padding-left: 0.9rem;
            padding-right: 0.9rem;
        }

        div[data-testid="stMetric"] {
            min-height: auto;
        }

        div[data-testid="stMetricValue"] {
            font-size: 1.75rem !important;
        }
    }
</style>
""", unsafe_allow_html=True)


# st.title("Momentum v2.1")  # Hidden for premium dashboard layout
st.caption("Training intelligence for progressive overload.")

st.sidebar.markdown(
    """
    <div class="m55-sidebar-brand">
        <div class="m55-brand-mark">Momentum</div>
        <div class="m55-brand-sub">Built for consistency</div>
    </div>
    """,
    unsafe_allow_html=True,
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Today's Workout",
        "Progress Hub",
        "Analytics",
        "Workout Log",
        "Exercise History",
        "Bodyweight Log",
        "Program Manager",
        "Program Editor",
        "Export / Backup",
        "Settings",
    ],
)

def total_reps(reps):
    total = 0
    for part in str(reps).replace(" ", "").split(","):
        try:
            total += float(part)
        except ValueError:
            pass
    return total


def get_personal_records():
    logs = fetch_df("""
        SELECT wl.log_date, e.exercise_name, e.muscle_group, wl.weight, wl.reps
        FROM workout_logs wl
        JOIN exercises e ON wl.exercise_id = e.id
        WHERE wl.weight IS NOT NULL AND wl.weight > 0
    """)

    if logs.empty:
        return logs

    logs["total_reps"] = logs["reps"].apply(total_reps)
    logs["volume"] = logs["weight"] * logs["total_reps"]

    records = []
    for exercise_name, group in logs.groupby("exercise_name"):
        best_weight = group["weight"].max()
        best_reps = group["total_reps"].max()
        best_volume_row = group.loc[group["volume"].idxmax()]

        records.append({
            "Exercise": exercise_name,
            "Muscle Group": best_volume_row["muscle_group"],
            "Best Weight": round(best_weight, 1),
            "Best Total Reps": round(best_reps, 1),
            "Best Volume": round(best_volume_row["volume"], 1),
            "PR Date": best_volume_row["log_date"],
        })

    import pandas as pd
    return pd.DataFrame(records).sort_values("Best Volume", ascending=False)


def get_today_checkin():
    df = fetch_df("SELECT * FROM daily_checkins WHERE checkin_date = ?", (str(date.today()),))
    return None if df.empty else df.iloc[0]

def calculate_momentum_score():
    score = 0
    details = []

    checkin = get_today_checkin()
    completions_today = fetch_df("SELECT * FROM workout_completions WHERE completion_date = ?", (str(date.today()),))

    if not completions_today.empty:
        score += 30
        details.append("Workout completed: +30")
    else:
        details.append("Workout completed: +0")

    if checkin is not None:
        if int(checkin["protein_hit"] or 0) == 1:
            score += 20
            details.append("Protein hit: +20")
        else:
            details.append("Protein hit: +0")

        if int(checkin["steps_hit"] or 0) == 1:
            score += 20
            details.append("Steps hit: +20")
        else:
            details.append("Steps hit: +0")

        if int(checkin["water_hit"] or 0) == 1:
            score += 10
            details.append("Water hit: +10")
        else:
            details.append("Water hit: +0")

        sleep = float(checkin["sleep_hours"] or 0)
        if sleep >= 7:
            score += 20
            details.append("Sleep 7h+: +20")
        elif sleep >= 6:
            score += 10
            details.append("Sleep 6h+: +10")
        else:
            details.append("Sleep below 6h: +0")
    else:
        details.append("No daily check-in yet.")

    return score, details

def smart_progression_plan(exercise, latest_log):
    if latest_log is None:
        return {
            "Next Weight": "Baseline",
            "Target": f"{exercise['target_sets']} sets × {exercise['min_reps']}–{exercise['max_reps']}",
            "Reason": "No previous log exists yet."
        }

    weight, reps_text, rir, notes, log_date = latest_log
    reps = []
    for part in str(reps_text).replace(" ", "").split(","):
        try:
            reps.append(float(part))
        except ValueError:
            pass

    target_sets = int(exercise["target_sets"])
    min_reps = int(exercise["min_reps"])
    max_reps = int(exercise["max_reps"])
    progression_type = exercise["progression_type"]

    if progression_type in ["time", "cardio_time", "steps"]:
        return {
            "Next Weight": "N/A",
            "Target": f"Reach {max_reps} cleanly",
            "Reason": "Progress this exercise by duration, steps, or difficulty."
        }

    if len(reps) < target_sets:
        return {
            "Next Weight": weight,
            "Target": f"Complete all {target_sets} sets",
            "Reason": "Previous log did not include all target sets."
        }

    if all(r >= max_reps for r in reps):
        if rir is not None and float(rir) <= 2:
            suggested = float(weight or 0) + 5
            return {
                "Next Weight": suggested,
                "Target": f"{target_sets} sets × {min_reps}",
                "Reason": "Top rep range reached with low RIR. Increase load next session."
            }
        return {
            "Next Weight": weight,
            "Target": f"{target_sets} sets × {max_reps}",
            "Reason": "Top reps reached, but RIR is still high. Keep load and improve control."
        }

    if any(r < min_reps for r in reps):
        return {
            "Next Weight": weight,
            "Target": f"Rebuild toward {min_reps}+ reps per set",
            "Reason": "Performance fell below the target range."
        }

    return {
        "Next Weight": weight,
        "Target": f"Beat previous reps: {reps_text}",
        "Reason": "Stay at the same load and progress reps first."
    }



def dynamic_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning."
    if hour < 18:
        return "Good afternoon."
    return "Good evening."

def get_recent_workouts(limit=5):
    return fetch_df("""
        SELECT completion_date, day, workout_name
        FROM workout_completions
        ORDER BY id DESC
        LIMIT ?
    """, (int(limit),))

week = current_week()
phase = get_phase(week)
next_workout = get_next_workout()

if page == "Dashboard":
    programs = get_programs()
    active_program_id = get_active_program_id()
    active_program = programs[programs["id"] == active_program_id].iloc[0] if not programs.empty else None

    score, score_details = calculate_momentum_score()
    recovery_status = get_today_recovery().title()
    weeks_left = max(0, 12 - week)
    completed_workouts = len(fetch_df("SELECT * FROM workout_completions"))

    st.markdown('<div class="momentum-logo">Momentum</div>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="m5-hero">
            <h1>{dynamic_greeting()}</h1>
            <div class="m5-hero-sub">Training intelligence for progressive overload, consistency, and execution.</div>
            <div class="m5-pill-row">
                <span class="m5-pill">{str(date.today())}</span>
                <span class="m5-pill m5-pill-red">Week {week} of 12</span>
                <span class="m5-pill">{weeks_left} weeks left</span>
                <span class="m5-pill m5-pill-red">Momentum {score}/100</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    timeline_html = ""
    for i in range(1, 13):
        if i < week:
            timeline_html += f'<div class="m5-week-chip done">W{i}<br>✓</div>'
        elif i == week:
            timeline_html += f'<div class="m5-week-chip current">W{i}<br>●</div>'
        else:
            timeline_html += f'<div class="m5-week-chip">W{i}<br>&nbsp;</div>'

    st.markdown(
        f"""
        <div class="m5-timeline">
            <div class="m5-eyebrow">12 Week Timeline</div>
            <div class="m5-timeline-grid">{timeline_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Week", f"{week}/12")
    m2.metric("Recovery", recovery_status)
    m3.metric("Momentum", f"{score}/100")
    m4.metric("Weeks Left", weeks_left)

    left, right = st.columns([1.05, 1])

    with left:
        upcoming_exercises = (
            get_exercises(next_workout["day"])
            if next_workout["day"] != "No Day"
            else fetch_df("SELECT * FROM exercises WHERE 1=0")
        )

        exercise_rows = ""
        if not upcoming_exercises.empty:
            for _, row in upcoming_exercises.head(7).iterrows():
                exercise_rows += (
                    f'<div class="m5-exercise-row">'
                    f'<span class="m5-exercise-name">{row["exercise_name"]}</span>'
                    f'<span class="m5-exercise-target">{row["target_sets"]}×{row["min_reps"]}–{row["max_reps"]}</span>'
                    f'</div>'
                )

        if upcoming_exercises.empty:
            exercise_rows = '<div class="m5-muted">No exercises yet. Add exercises in Program Manager.</div>'

        st.markdown(
            f"""
            <div class="m5-workout-card">
                <div class="m5-eyebrow">Today's Priority</div>
                <div class="m5-main">{next_workout["day"]} — {next_workout["workout_name"]}</div>
                <div class="m5-muted">Your next workout is ready. Log each exercise from Today’s Workout.</div>
                <div class="m5-exercise-list">
                    {exercise_rows}
                </div>
                <div class="m5-action">Start Today’s Workout</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown('<div class="m5-card m5-recovery-card">', unsafe_allow_html=True)
        st.markdown('<div class="m5-eyebrow">Recovery Overview</div>', unsafe_allow_html=True)

        today_checkin = get_today_checkin()

        if today_checkin is None:
            st.info("No check-in yet today.")
        else:
            sleep_value = float(today_checkin["sleep_hours"] or 0)
            energy_value = float(today_checkin["energy"] or 0)
            stress_value = float(today_checkin["stress"] or 0)

            st.write(f"**Sleep:** {sleep_value:g} / 8 h")
            st.progress(min(sleep_value / 8, 1.0), text=f"{sleep_value:g} hours logged")

            st.write(f"**Energy:** {energy_value:g} / 5")
            st.progress(min(energy_value / 5, 1.0), text=f"{energy_value:g} out of 5")

            st.write(f"**Stress:** {stress_value:g} / 5")
            st.progress(min(stress_value / 5, 1.0), text=f"{stress_value:g} out of 5")

            hydration_label = "Good" if int(today_checkin["water_hit"] or 0) else "Missing"
            nutrition_label = "Good" if int(today_checkin["protein_hit"] or 0) else "Missing"

            st.write(f"**Hydration:** {hydration_label}")
            st.write(f"**Nutrition:** {nutrition_label}")

        st.markdown('<div class="m5-muted">Recovery determines execution quality.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("Log Daily Check-In", expanded=False):
        c1, c2 = st.columns(2)

        body_weight = c1.number_input("Body Weight", min_value=0.0, step=0.5)
        sleep_hours = c1.number_input("Sleep Hours", min_value=0.0, max_value=24.0, step=0.5)
        energy = c2.slider("Energy", 1, 5, 3)
        stress = c2.slider("Stress", 1, 5, 3)

        c3, c4, c5 = st.columns(3)
        protein_hit = c3.checkbox("Protein Hit")
        water_hit = c4.checkbox("Water Hit")
        steps_hit = c5.checkbox("Steps Hit")

        if st.button("Save Daily Check-In"):
            save_checkin(
                str(date.today()),
                body_weight,
                sleep_hours,
                energy,
                stress,
                int(protein_hit),
                int(water_hit),
                int(steps_hit),
            )
            st.success("Daily check-in saved.")

    row1_left, row1_right = st.columns(2)

    with row1_left:
        st.markdown('<div class="m5-card">', unsafe_allow_html=True)
        st.markdown('<div class="m5-eyebrow">Bodyweight Trend</div>', unsafe_allow_html=True)

        weight_logs = fetch_df("""
            SELECT checkin_date, body_weight
            FROM daily_checkins
            WHERE body_weight IS NOT NULL AND body_weight > 0
            ORDER BY checkin_date ASC
        """)

        if weight_logs.empty:
            st.info("No bodyweight data yet.")
        else:
            weight_logs["checkin_date"] = weight_logs["checkin_date"].astype(str)

            current_weight = round(weight_logs["body_weight"].iloc[-1], 1)
            avg_7 = round(weight_logs["body_weight"].tail(7).mean(), 1)
            change = (
                round(weight_logs["body_weight"].iloc[-1] - weight_logs["body_weight"].iloc[0], 1)
                if len(weight_logs) >= 2
                else 0
            )

            w1, w2, w3 = st.columns(3)
            w1.metric("Current", current_weight)
            w2.metric("7-Day Avg", avg_7)
            w3.metric("Trend", f"{change:+.1f}")

            st.line_chart(weight_logs.set_index("checkin_date")["body_weight"])

        st.markdown("</div>", unsafe_allow_html=True)

    with row1_right:
        st.markdown('<div class="m5-card">', unsafe_allow_html=True)
        st.markdown('<div class="m5-eyebrow">Momentum Score</div>', unsafe_allow_html=True)

        st.metric("Today", f"{score}/100", "Consistency")

        with st.expander("Score Breakdown"):
            for item in score_details:
                st.write(item)

        st.markdown('<div class="m5-muted">Consistency compounds quietly.</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    row2_left, row2_right = st.columns([0.9, 1.35])

    with row2_left:
        st.markdown('<div class="m5-card">', unsafe_allow_html=True)
        st.markdown('<div class="m5-eyebrow">Recent Workouts</div>', unsafe_allow_html=True)

        recent = get_recent_workouts(5)

        if recent.empty:
            st.info("No completed workouts yet.")
        else:
            for _, row in recent.iterrows():
                st.write(f"**{row['day']} — {row['workout_name']}**")
                st.caption(row["completion_date"])

        st.markdown("</div>", unsafe_allow_html=True)

    with row2_right:
        st.markdown('<div class="m5-card">', unsafe_allow_html=True)
        st.markdown('<div class="m5-eyebrow">Personal Records</div>', unsafe_allow_html=True)

        prs = get_personal_records()

        if prs.empty:
            st.info("No personal records yet.")
        else:
            st.dataframe(prs.head(6), use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="quote-card">
            “Discipline today. Freedom tomorrow.”
        </div>
        """,
        unsafe_allow_html=True,
    )

elif page == "Today's Workout":
    st.header("Today's Workout")
    st.caption("A cleaner training screen for logging sessions with less visual clutter.")

    days = get_workout_days()

    if days.empty:
        st.warning("No workout days exist for the active program yet. Go to Program Manager to create days and exercises.")
        st.stop()

    day_options = [f"{row.day} — {row.workout_name}" for _, row in days.iterrows()]
    next_label = f"{next_workout['day']} — {next_workout['workout_name']}"
    default_index = day_options.index(next_label) if next_label in day_options else 0

    selected_label = st.selectbox("Workout", day_options, index=default_index)
    selected_day = selected_label.split(" — ")[0]
    selected_row = days[days["day"] == selected_day].iloc[0]

    st.markdown(
        f"""
        <div class="m55-card">
            <div class="m55-title">Current Session</div>
            <div class="m55-headline">{selected_row['day']} — {selected_row['workout_name']}</div>
            <div class="m55-muted">Week {week}/12 · {phase} · Recommended: {next_label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    exercises = get_exercises(selected_day)
    recovery_status = get_today_recovery()

    if exercises.empty:
        st.info("This workout day exists, but it has no exercises yet. Add exercises in Program Manager.")
        st.stop()

    compact_mode = st.toggle("Compact gym mode", value=True)
    st.caption("Use compact mode during gym sessions. Turn it off when you want full notes.")

    for _, ex in exercises.iterrows():
        latest = get_latest_log(int(ex["id"]))
        rec = recommendation(ex, latest, recovery_status)
        plan = smart_progression_plan(ex, latest)

        st.markdown(
            f"""
            <div class="m55-exercise-card">
                <div class="m55-exercise-title">{ex['exercise_name']}</div>
                <div class="m55-exercise-meta">
                    {ex['muscle_group']} · {ex['target_sets']} sets × {ex['min_reps']}–{ex['max_reps']} · {ex['progression_type']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if latest:
            weight, reps, rir, notes, log_date = latest
            st.write(f"**Last:** {weight or 0:g} · reps/time: {reps} · RIR: {rir if rir is not None else 'N/A'} · {log_date}")
        else:
            st.write("**Last:** No previous log. Use today as baseline.")

        if count_stall_sessions(int(ex["id"])):
            st.error("Plateau warning: same result logged for 3 sessions.")

        st.markdown(
            f"""
            <div class="m55-action-strip">
                <strong>Next:</strong> {plan['Next Weight']} · <strong>Target:</strong> {plan['Target']}<br>
                {plan['Reason']}
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not compact_mode:
            st.success(f"Recommendation: {rec}")
            with st.expander("Smart Progression Plan"):
                p1, p2, p3 = st.columns(3)
                p1.metric("Next Weight", plan["Next Weight"])
                p2.metric("Target", plan["Target"])
                p3.write(plan["Reason"])

        with st.form(f"log_{ex['id']}"):
            c1, c2 = st.columns(2)
            weight_input = c1.number_input("Actual Weight / Load", min_value=0.0, step=2.5, key=f"w_{ex['id']}")
            reps_input = c2.text_input("Actual Reps / Time / Steps", placeholder="Example: 8,8,7,6", key=f"r_{ex['id']}")
            rir_input = st.slider("RIR", 0.0, 5.0, 2.0, 0.5, key=f"rir_{ex['id']}")
            notes_input = "" if compact_mode else st.text_area("Notes", key=f"notes_{ex['id']}")

            if st.form_submit_button("Save Exercise Log"):
                if reps_input.strip():
                    save_workout_log(str(date.today()), int(ex["id"]), weight_input, reps_input, rir_input, notes_input)
                    st.success(f"{ex['exercise_name']} saved.")
                else:
                    st.error("Enter reps/time/steps before saving.")

    st.markdown("---")
    if st.button("Mark Workout Complete"):
        mark_workout_complete(selected_row["day"], int(selected_row["day_order"]), selected_row["workout_name"])
        st.success("Workout marked complete. Refresh to see next workout update.")

elif page == "Progress Hub":
    st.header("Progress Hub")
    st.caption("Your current phase, bodyweight trend, personal records, and consistency score.")

    score, score_details = calculate_momentum_score()
    weeks_left = max(0, 12 - week)

    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Current Week", f"{week}/12")
    p2.metric("Weeks Left", weeks_left)
    p3.metric("Momentum Score", f"{score}/100")
    p4.metric("Recovery", get_today_recovery().title())

    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown('<div class="m55-title">Bodyweight Trend</div>', unsafe_allow_html=True)

    weight_logs = fetch_df("""
        SELECT checkin_date, body_weight
        FROM daily_checkins
        WHERE body_weight IS NOT NULL AND body_weight > 0
        ORDER BY checkin_date ASC
    """)

    if weight_logs.empty:
        st.info("No bodyweight data yet.")
    else:
        weight_logs["checkin_date"] = weight_logs["checkin_date"].astype(str)
        current_weight = round(weight_logs["body_weight"].iloc[-1], 1)
        avg_7 = round(weight_logs["body_weight"].tail(7).mean(), 1)
        avg_30 = round(weight_logs["body_weight"].tail(30).mean(), 1)
        trend = round(weight_logs["body_weight"].iloc[-1] - weight_logs["body_weight"].iloc[0], 1) if len(weight_logs) >= 2 else 0

        w1, w2, w3, w4 = st.columns(4)
        w1.metric("Current", current_weight)
        w2.metric("7-Day Avg", avg_7)
        w3.metric("30-Day Avg", avg_30)
        w4.metric("Trend", f"{trend:+.1f}")
        st.line_chart(weight_logs.set_index("checkin_date")["body_weight"])

    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns([1.25, 1])

    with left:
        st.markdown('<div class="m55-card">', unsafe_allow_html=True)
        st.markdown('<div class="m55-title">Personal Records</div>', unsafe_allow_html=True)
        prs = get_personal_records()
        if prs.empty:
            st.info("No personal records yet.")
        else:
            st.dataframe(prs.head(10), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="m55-card">', unsafe_allow_html=True)
        st.markdown('<div class="m55-title">Momentum Score Breakdown</div>', unsafe_allow_html=True)
        for item in score_details:
            st.write(f"• {item}")
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Analytics":
    st.header("Analytics")
    st.caption("Training patterns, exercise frequency, and muscle-group logging summary.")

    summary = get_program_count_summary()
    if not summary.empty:
        a, b, c = st.columns(3)
        a.metric("Active Programs", int(summary["active_programs"].iloc[0] or 0))
        b.metric("Archived Programs", int(summary["archived_programs"].iloc[0] or 0))
        c.metric("Total Programs", int(summary["total_programs"].iloc[0] or 0))

    st.markdown('<div class="m55-card">', unsafe_allow_html=True)
    st.markdown('<div class="m55-title">Workout Frequency</div>', unsafe_allow_html=True)
    weekly = get_weekly_workout_summary()
    if weekly.empty:
        st.info("No completed workout data yet.")
    else:
        weekly["completion_date"] = weekly["completion_date"].astype(str)
        st.line_chart(weekly.set_index("completion_date")["completed_workouts"])
        st.dataframe(weekly, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    left, right = st.columns(2)

    with left:
        st.markdown('<div class="m55-card">', unsafe_allow_html=True)
        st.markdown('<div class="m55-title">Exercise Frequency</div>', unsafe_allow_html=True)
        frequency = get_exercise_frequency()
        if frequency.empty:
            st.info("No exercise logs yet.")
        else:
            st.dataframe(frequency, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="m55-card">', unsafe_allow_html=True)
        st.markdown('<div class="m55-title">Muscle Group Log Summary</div>', unsafe_allow_html=True)
        muscle_summary = get_muscle_volume_summary()
        if muscle_summary.empty:
            st.info("No muscle-group data yet.")
        else:
            st.dataframe(muscle_summary, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif page == "Workout Log":
    st.header("Workout Log")
    logs = fetch_df("""
        SELECT wl.id, wl.log_date, e.day, e.workout_name, e.exercise_name, e.muscle_group, wl.weight, wl.reps, wl.rir, wl.notes
        FROM workout_logs wl
        JOIN exercises e ON wl.exercise_id = e.id
        ORDER BY wl.id DESC
    """)

    if logs.empty:
        st.info("No workouts logged yet.")
    else:
        st.dataframe(logs, use_container_width=True)

        st.subheader("Edit or Delete Log")
        log_id = st.selectbox(
            "Select Log ID",
            logs["id"].tolist(),
            format_func=lambda x: f"ID {x} — {logs.loc[logs['id'] == x, 'exercise_name'].iloc[0]} — {logs.loc[logs['id'] == x, 'log_date'].iloc[0]}"
        )

        selected = logs[logs["id"] == log_id].iloc[0]

        with st.form("edit_workout_log_form"):
            edit_date = st.date_input("Log Date", value=date.fromisoformat(str(selected["log_date"])))
            edit_weight = st.number_input("Weight / Load", min_value=0.0, step=2.5, value=float(selected["weight"] or 0))
            edit_reps = st.text_input("Reps / Time / Steps", value=str(selected["reps"]))
            edit_rir = st.slider("RIR", 0.0, 5.0, float(selected["rir"] if selected["rir"] is not None else 2.0), 0.5)
            edit_notes = st.text_area("Notes", value="" if selected["notes"] is None else str(selected["notes"]))

            save_edit = st.form_submit_button("Save Changes")
            if save_edit:
                if edit_reps.strip():
                    update_workout_log(log_id, str(edit_date), edit_weight, edit_reps, edit_rir, edit_notes)
                    st.success("Workout log updated. Refresh to see changes.")
                else:
                    st.error("Reps/time/steps cannot be blank.")

        st.warning("Delete is permanent for this selected log only.")
        confirm_delete = st.checkbox("I understand this will delete the selected workout log only.")
        if st.button("Delete Selected Log"):
            if confirm_delete:
                delete_workout_log(log_id)
                st.success("Workout log deleted. Refresh to update the table.")
            else:
                st.error("Check the confirmation box before deleting.")

elif page == "Exercise History":
    st.header("Exercise History")
    exercises = get_exercises()
    exercise_name = st.selectbox("Select Exercise", exercises["exercise_name"].unique())
    exercise_ids = exercises.loc[exercises["exercise_name"] == exercise_name, "id"].tolist()
    placeholders = ",".join("?" for _ in exercise_ids)
    logs = fetch_df(f"""
        SELECT wl.log_date, e.day, e.workout_name, wl.weight, wl.reps, wl.rir, wl.notes
        FROM workout_logs wl
        JOIN exercises e ON wl.exercise_id = e.id
        WHERE wl.exercise_id IN ({placeholders})
        ORDER BY wl.id ASC
    """, tuple(exercise_ids))
    if logs.empty:
        st.info("No history for this exercise yet.")
    else:
        logs["total_reps"] = logs["reps"].apply(total_reps)
        logs["volume"] = logs["weight"] * logs["total_reps"]

        st.subheader("Personal Record")
        best_weight = round(logs["weight"].max(), 1)
        best_total_reps = round(logs["total_reps"].max(), 1)
        best_volume_row = logs.loc[logs["volume"].idxmax()]
        best_volume = round(best_volume_row["volume"], 1)
        pr_date = best_volume_row["log_date"]

        p1, p2, p3, p4 = st.columns(4)
        p1.metric("Best Weight", best_weight)
        p2.metric("Best Total Reps", best_total_reps)
        p3.metric("Best Volume", best_volume)
        p4.metric("PR Date", pr_date)

        st.dataframe(logs, use_container_width=True)
        st.subheader("Weight Trend")
        st.line_chart(logs.set_index("log_date")["weight"])
        st.subheader("Volume Trend")
        st.line_chart(logs.set_index("log_date")["volume"])


elif page == "Bodyweight Log":
    st.header("Bodyweight Log")
    st.caption("Use this page to add, edit, or clear bodyweight entries by date.")

    c1, c2 = st.columns(2)
    entry_date = c1.date_input("Date", value=date.today())
    entry_weight = c2.number_input("Body Weight", min_value=0.0, step=0.5)

    if st.button("Save Bodyweight Entry"):
        save_bodyweight_entry(str(entry_date), entry_weight)
        st.success("Bodyweight entry saved.")

    weight_logs = fetch_df("""
        SELECT checkin_date, body_weight
        FROM daily_checkins
        WHERE body_weight IS NOT NULL AND body_weight > 0
        ORDER BY checkin_date DESC
    """)

    if weight_logs.empty:
        st.info("No bodyweight entries yet.")
    else:
        st.subheader("Bodyweight History")
        st.dataframe(weight_logs, use_container_width=True)

        clear_date = st.selectbox("Clear entry for date", weight_logs["checkin_date"].tolist())
        if st.button("Clear Selected Bodyweight Entry"):
            clear_bodyweight_entry(clear_date)
            st.success("Selected bodyweight entry cleared. Refresh to update the table.")



elif page == "Program Manager":
    st.header("Program Manager")
    st.caption("Build and manage training programs. Each program can represent a different specialization block.")

    programs = get_programs()
    active_program_id = get_active_program_id()

    if programs.empty:
        st.warning("No programs found.")
        st.stop()

    program_names = programs["program_name"].tolist()
    program_ids = programs["id"].tolist()
    selected_index = program_ids.index(active_program_id) if active_program_id in program_ids else 0

    selected_program_name = st.selectbox("Program", program_names, index=selected_index)
    selected_program = programs[programs["program_name"] == selected_program_name].iloc[0]
    selected_program_id = int(selected_program["id"])

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Selected Program", selected_program_name)
    with c2:
        st.metric("Duration", f"{int(selected_program['duration_weeks'])} weeks")

    if st.button("Set as Active Program"):
        set_active_program(selected_program_id)
        reset_workout_progress()
        st.success("Active program updated. Workout progress reset so Momentum starts from Day 1 for this program.")

    st.subheader("Available Programs")
    st.dataframe(programs, use_container_width=True)

    st.subheader("Create Program")
    with st.form("create_program_form"):
        new_program_name = st.text_input("Program Name", placeholder="Example: Arm Specialization")
        new_duration = st.number_input("Duration Weeks", min_value=1, max_value=52, value=12)
        new_goal = st.text_area("Goal", placeholder="Example: Prioritize forearms, biceps, and triceps while maintaining lower body.")
        create_button = st.form_submit_button("Create Program")

        if create_button:
            if new_program_name.strip():
                create_program(new_program_name.strip(), new_duration, new_goal)
                st.success("Program created. Refresh to see it in the list.")
            else:
                st.error("Program name is required.")

    st.markdown("---")
    st.subheader("Workout Day Builder")

    with st.form("add_day_form"):
        d1, d2, d3 = st.columns(3)
        day_order = d1.number_input("Day Order", min_value=1, max_value=14, value=1)
        day_label = d2.text_input("Day Label", value=f"Day {day_order}")
        workout_name = d3.text_input("Workout Name", placeholder="Example: Biceps + Forearms")

        add_day = st.form_submit_button("Add Workout Day")
        if add_day:
            if day_label.strip() and workout_name.strip():
                add_workout_day(selected_program_id, day_label.strip(), int(day_order), workout_name.strip())
                st.success("Workout day added.")
            else:
                st.error("Day label and workout name are required.")

    days = get_workout_days()
    if days.empty:
        st.info("No workout days created for the active program yet.")
    else:
        st.subheader("Current Active Program Split")
        st.dataframe(days, use_container_width=True)

    st.markdown("---")
    st.subheader("Exercise Builder")

    program_days = get_program_exercises(selected_program_id)
    visible_days = program_days[["day", "day_order", "workout_name"]].drop_duplicates().sort_values(["day_order", "day"])

    if visible_days.empty:
        st.info("Create at least one workout day before adding exercises.")
    else:
        day_options = [f"{row.day} — {row.workout_name}" for _, row in visible_days.iterrows()]
        selected_day_label = st.selectbox("Add Exercise To", day_options)
        selected_day = selected_day_label.split(" — ")[0]
        selected_day_row = visible_days[visible_days["day"] == selected_day].iloc[0]

        with st.form("add_exercise_form"):
            e1, e2 = st.columns(2)
            exercise_name = e1.text_input("Exercise Name", placeholder="Example: Hammer Curl")
            muscle_group = e2.text_input("Muscle Group", placeholder="Example: Biceps")

            s1, s2, s3 = st.columns(3)
            target_sets = s1.number_input("Target Sets", min_value=1, max_value=10, value=3)
            min_reps = s2.number_input("Min Reps / Time / Steps", min_value=0, max_value=100000, value=8)
            max_reps = s3.number_input("Max Reps / Time / Steps", min_value=0, max_value=100000, value=12)

            progression_type = st.selectbox(
                "Progression Type",
                ["weight", "core_load", "time", "cardio_time", "steps", "reps", "optional_reps", "each_leg"]
            )

            add_exercise = st.form_submit_button("Add Exercise")
            if add_exercise:
                if exercise_name.strip() and muscle_group.strip():
                    add_exercise_to_day(
                        selected_program_id,
                        selected_day,
                        int(selected_day_row["day_order"]),
                        selected_day_row["workout_name"],
                        exercise_name.strip(),
                        muscle_group.strip(),
                        int(target_sets),
                        int(min_reps),
                        int(max_reps),
                        progression_type
                    )
                    st.success("Exercise added.")
                else:
                    st.error("Exercise name and muscle group are required.")

    st.markdown("---")
    st.subheader("Program Exercises")
    all_exercises = get_program_exercises(selected_program_id)

    if all_exercises.empty:
        st.info("No days or exercises for this program yet.")
    else:
        display_exercises = all_exercises.copy()
        display_exercises["exercise_name"] = display_exercises["exercise_name"].replace("__DAY_PLACEHOLDER__", "(day shell)")
        st.dataframe(
            display_exercises[["id", "day", "day_order", "workout_name", "exercise_name", "muscle_group", "target_sets", "min_reps", "max_reps", "progression_type"]],
            use_container_width=True
        )

        st.subheader("Delete")
        delete_options = display_exercises["id"].tolist()
        delete_id = st.selectbox(
            "Select Exercise/Day Shell ID to Delete",
            delete_options,
            format_func=lambda x: f"ID {x} — {display_exercises.loc[display_exercises['id'] == x, 'day'].iloc[0]} — {display_exercises.loc[display_exercises['id'] == x, 'exercise_name'].iloc[0]}"
        )
        confirm_delete_item = st.checkbox("I understand this deletes the selected exercise/day shell only.")
        if st.button("Delete Selected Item"):
            if confirm_delete_item:
                delete_exercise(delete_id)
                st.success("Selected item deleted. Refresh to update.")
            else:
                st.error("Check the confirmation box before deleting.")




elif page == "Program Editor":
    st.header("Program Editor")
    st.caption("Edit programs, workout days, and exercises without touching code.")

    programs = get_programs()

    if programs.empty:
        st.warning("No programs available.")
        st.stop()

    program_name = st.selectbox("Select Program to Edit", programs["program_name"].tolist())
    selected_program = programs[programs["program_name"] == program_name].iloc[0]
    selected_program_id = int(selected_program["id"])

    st.subheader("Program Details")
    with st.form("edit_program_form"):
        edited_program_name = st.text_input("Program Name", value=str(selected_program["program_name"]))
        edited_duration = st.number_input("Duration Weeks", min_value=1, max_value=52, value=int(selected_program["duration_weeks"]))
        edited_goal = st.text_area("Goal", value="" if selected_program["goal"] is None else str(selected_program["goal"]))

        if st.form_submit_button("Save Program Changes"):
            if edited_program_name.strip():
                update_program(selected_program_id, edited_program_name.strip(), edited_duration, edited_goal)
                st.success("Program updated. Refresh to see changes.")
            else:
                st.error("Program name cannot be blank.")


    st.subheader("Archive Program")
    st.caption("Archiving hides nothing yet, but marks programs you are not actively using.")
    archive_col, unarchive_col = st.columns(2)
    if archive_col.button("Archive Selected Program"):
        if selected_program_id == 1:
            st.error("Shoulder Specialization is protected and cannot be archived.")
        else:
            archive_program(selected_program_id)
            st.success("Program archived.")

    if unarchive_col.button("Unarchive Selected Program"):
        unarchive_program(selected_program_id)
        st.success("Program unarchived.")


    st.subheader("Duplicate Program")
    st.info("Option A: duplication copies the full program, including all workout days and exercises.")
    with st.form("duplicate_program_form"):
        duplicate_name = st.text_input("New Program Name", placeholder=f"{program_name} Copy")
        if st.form_submit_button("Duplicate Full Program"):
            if duplicate_name.strip():
                duplicate_program(selected_program_id, duplicate_name.strip())
                st.success("Program duplicated with all days and exercises. Refresh to see the copy.")
            else:
                st.error("New program name is required.")

    st.subheader("Delete Program")
    st.warning("Deleting a program also deletes its workout days and exercise templates. Shoulder Specialization is protected.")
    confirm_delete_program = st.checkbox("I understand this deletes the selected program and its exercises.")
    if st.button("Delete Selected Program"):
        if selected_program_id == 1:
            st.error("Shoulder Specialization is protected and cannot be deleted.")
        elif confirm_delete_program:
            delete_program(selected_program_id)
            reset_workout_progress()
            st.success("Program deleted. Active program reset to Shoulder Specialization if needed.")
        else:
            st.error("Check the confirmation box first.")

    st.markdown("---")
    st.subheader("Workout Day Editor")

    program_exercises = get_program_exercises(selected_program_id)

    if program_exercises.empty:
        st.info("No workout days exist for this program yet. Use Program Manager to create days.")
        st.stop()

    day_table = program_exercises[["day", "day_order", "workout_name"]].drop_duplicates().sort_values(["day_order", "day"])

    if day_table.empty:
        st.info("No workout days found.")
    else:
        day_options = [f"{row.day} — {row.workout_name}" for _, row in day_table.iterrows()]
        selected_day_label = st.selectbox("Select Workout Day", day_options)
        selected_day = selected_day_label.split(" — ")[0]
        selected_day_row = day_table[day_table["day"] == selected_day].iloc[0]

        with st.form("edit_day_form"):
            new_day_order = st.number_input("Day Order", min_value=1, max_value=14, value=int(selected_day_row["day_order"]))
            new_day_label = st.text_input("Day Label", value=str(selected_day_row["day"]))
            new_workout_name = st.text_input("Workout Name", value=str(selected_day_row["workout_name"]))

            if st.form_submit_button("Save Workout Day Changes"):
                if new_day_label.strip() and new_workout_name.strip():
                    update_workout_day(
                        selected_program_id,
                        selected_day,
                        new_day_label.strip(),
                        int(new_day_order),
                        new_workout_name.strip()
                    )
                    st.success("Workout day updated. Refresh to see changes.")
                else:
                    st.error("Day label and workout name are required.")

    st.markdown("---")
    st.subheader("Exercise Editor")

    editable_exercises = program_exercises[program_exercises["exercise_name"] != "__DAY_PLACEHOLDER__"]

    if editable_exercises.empty:
        st.info("No editable exercises exist for this program yet.")
    else:
        exercise_id = st.selectbox(
            "Select Exercise",
            editable_exercises["id"].tolist(),
            format_func=lambda x: f"ID {x} — {editable_exercises.loc[editable_exercises['id'] == x, 'day'].iloc[0]} — {editable_exercises.loc[editable_exercises['id'] == x, 'exercise_name'].iloc[0]}"
        )

        selected_exercise = editable_exercises[editable_exercises["id"] == exercise_id].iloc[0]

        with st.form("edit_exercise_form"):
            e1, e2 = st.columns(2)
            edited_exercise_name = e1.text_input("Exercise Name", value=str(selected_exercise["exercise_name"]))
            edited_muscle_group = e2.text_input("Muscle Group", value=str(selected_exercise["muscle_group"]))

            s1, s2, s3 = st.columns(3)
            edited_sets = s1.number_input("Target Sets", min_value=0, max_value=10, value=int(selected_exercise["target_sets"]))
            edited_min_reps = s2.number_input("Min Reps / Time / Steps", min_value=0, max_value=100000, value=int(selected_exercise["min_reps"]))
            edited_max_reps = s3.number_input("Max Reps / Time / Steps", min_value=0, max_value=100000, value=int(selected_exercise["max_reps"]))

            progression_options = ["weight", "core_load", "time", "cardio_time", "steps", "reps", "optional_reps", "each_leg", "placeholder"]
            current_progression = str(selected_exercise["progression_type"])
            progression_index = progression_options.index(current_progression) if current_progression in progression_options else 0
            edited_progression_type = st.selectbox("Progression Type", progression_options, index=progression_index)

            if st.form_submit_button("Save Exercise Changes"):
                if edited_exercise_name.strip() and edited_muscle_group.strip():
                    update_exercise_template(
                        exercise_id,
                        edited_exercise_name.strip(),
                        edited_muscle_group.strip(),
                        int(edited_sets),
                        int(edited_min_reps),
                        int(edited_max_reps),
                        edited_progression_type
                    )
                    st.success("Exercise updated. Refresh to see changes.")
                else:
                    st.error("Exercise name and muscle group are required.")

        st.markdown("---")
        st.subheader("Move / Duplicate Exercise")

        move_day_options = [f"{row.day} — {row.workout_name}" for _, row in day_table.iterrows()]

        if not move_day_options:
            st.info("No target days available.")
        else:
            target_day_label = st.selectbox("Target Day", move_day_options)
            target_day = target_day_label.split(" — ")[0]
            target_day_row = day_table[day_table["day"] == target_day].iloc[0]

            m1, m2 = st.columns(2)

            if m1.button("Move Exercise to Target Day"):
                move_exercise_to_day(
                    exercise_id,
                    target_day,
                    int(target_day_row["day_order"]),
                    str(target_day_row["workout_name"])
                )
                st.success("Exercise moved. Refresh to see changes.")

            if m2.button("Duplicate Exercise to Target Day"):
                duplicate_exercise_to_day(
                    exercise_id,
                    target_day,
                    int(target_day_row["day_order"]),
                    str(target_day_row["workout_name"])
                )
                st.success("Exercise duplicated. Refresh to see changes.")

    st.markdown("---")
    st.subheader("Current Program Template")
    display_table = get_program_exercises(selected_program_id)

    if display_table.empty:
        st.info("No template data.")
    else:
        display_table = display_table.copy()
        display_table["exercise_name"] = display_table["exercise_name"].replace("__DAY_PLACEHOLDER__", "(day shell)")
        st.dataframe(
            display_table[["id", "day", "day_order", "workout_name", "exercise_name", "muscle_group", "target_sets", "min_reps", "max_reps", "progression_type"]],
            use_container_width=True
        )


elif page == "Export / Backup":
    st.header("Export / Backup")
    st.caption("Download your Momentum data as CSV files. This helps protect your logs before future upgrades.")

    tables = get_export_tables()

    for table_name, table_df in tables.items():
        st.subheader(table_name)
        if table_df.empty:
            st.info("No data yet.")
        else:
            st.dataframe(table_df, use_container_width=True)
            csv = table_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"Download {table_name}.csv",
                data=csv,
                file_name=f"{table_name}.csv",
                mime="text/csv"
            )


elif page == "Settings":
    st.header("Settings")

    st.subheader("Access")
    if st.button("Log Out"):
        st.session_state["authenticated"] = False
        st.rerun()

    st.subheader("Deployment / Data")
    st.code(f"Database: {get_database_path()}")
    st.code(f"Latest Backup: {get_latest_backup()}")

    if st.button("Create Database Backup"):
        backup_path = create_database_backup()
        if backup_path:
            st.success(f"Backup created: {backup_path}")
        else:
            st.error("No database file found yet.")

    st.subheader("Phase Settings")
    current_start = get_setting("phase_start_date", str(date.today()))
    start_date = st.date_input("Phase Start Date", value=date.fromisoformat(current_start))
    if st.button("Save Phase Start Date"):
        set_setting("phase_start_date", str(start_date))
        st.success("Phase start date saved.")

    st.subheader("Reset Test Data")
    st.warning("Deletes workout logs, check-ins, and completion history only. Keeps exercise templates.")
    confirm_reset = st.checkbox("I understand this deletes logged test data only.")
    if st.button("Reset Test Data"):
        if confirm_reset:
            reset_test_data()
            st.success("Test data reset complete.")
        else:
            st.error("Check the confirmation box first.")

    st.subheader("Version")
    st.code("Momentum 6.0 - Core Complete")
