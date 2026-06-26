import streamlit as st


def apply_theme():
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


    st.markdown("""
    <style>
        /* Momentum 6.1 - clickable dashboard action link */
        .m5-action-link,
        .m5-action-link:visited,
        .m5-action-link:hover,
        .m5-action-link:active {
            color: #FFFDF9 !important;
            text-decoration: none !important;
        }
    </style>
    """, unsafe_allow_html=True)


    st.markdown("""
    <style>
        /* Momentum 6.4 - Premium experience polish */
        .m5-hero, .m5-timeline, .m5-card, .m5-workout-card, .m55-card, .m55-exercise-card, .quote-card {
            animation: momentumFadeUp 0.28s ease-out both;
            transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
        }

        .m5-card:hover, .m5-workout-card:hover, .m55-card:hover, .m55-exercise-card:hover {
            transform: translateY(-1px);
            box-shadow: 0 18px 42px rgba(59,48,36,0.10);
            border-color: rgba(155,28,28,0.18);
        }

        .m5-action {
            transition: transform 0.16s ease, box-shadow 0.16s ease, filter 0.16s ease;
        }

        .m5-action:hover {
            transform: translateY(-1px);
            filter: brightness(1.03);
            box-shadow: 0 16px 34px rgba(155,28,28,0.26);
        }

        .momentum-empty-state {
            background: linear-gradient(135deg, rgba(255,253,249,0.92), rgba(246,240,232,0.78));
            border: 1px dashed rgba(155,28,28,0.22);
            border-radius: 22px;
            padding: 1.05rem 1.1rem;
            color: #7B6A58;
            font-size: 0.92rem;
            box-shadow: 0 10px 24px rgba(59,48,36,0.045);
        }

        .momentum-insight-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 0.75rem;
            margin: 0.75rem 0 1rem;
        }

        .momentum-insight-card {
            background: rgba(255,253,249,0.93);
            border: 1px solid #E4D8C8;
            border-radius: 22px;
            padding: 1rem;
            box-shadow: 0 14px 32px rgba(59,48,36,0.065);
            animation: momentumFadeUp 0.28s ease-out both;
        }

        .momentum-insight-label {
            text-transform: uppercase;
            letter-spacing: 0.11em;
            color: #7B6A58;
            font-size: 0.68rem;
            font-weight: 850;
            margin-bottom: 0.35rem;
        }

        .momentum-insight-value {
            color: #9B1C1C;
            font-size: 1.35rem;
            font-weight: 880;
            letter-spacing: -0.04em;
        }

        .momentum-insight-sub {
            color: #7B6A58;
            font-size: 0.85rem;
            margin-top: 0.2rem;
        }

        @keyframes momentumFadeUp {
            from { opacity: 0; transform: translateY(6px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 900px) {
            .momentum-insight-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """, unsafe_allow_html=True)

