import streamlit as st

LIGHT_THEME = {
    "BACKGROUND": "linear-gradient(135deg, #dcfce7 0%, #fef3c7 55%, #fef9c3 100%)",
    "SIDEBAR_BG": "linear-gradient(180deg, #ecfccb 0%, #bbf7d0 100%)",
    "CARD_BG": "linear-gradient(180deg, #f9fde6 0%, #fef3c7 60%, #fff8d6 100%)",
    "PRIMARY": "#16a34a",
    "SECONDARY": "#22c55e",
    "ACCENT": "#facc15",
    "TEXT_PRIMARY": "#134e4a",
    "TEXT_SECONDARY": "#4b5563",
    "BORDER": "rgba(74, 222, 128, 0.18)",
    "SHADOW": "rgba(34, 197, 94, 0.18)",
    "PANEL_BORDER": "rgba(132, 204, 22, 0.22)"
}

DARK_THEME = {
    "BACKGROUND": "#0f172a",
    "SIDEBAR_BG": "#111827",
    "CARD_BG": "#1f2937",
    "PRIMARY": "#60a5fa",
    "SECONDARY": "#38bdf8",
    "ACCENT": "#facc15",
    "TEXT_PRIMARY": "#f8fafc",
    "TEXT_SECONDARY": "#cbd5e1",
    "BORDER": "rgba(96, 165, 250, 0.2)",
    "SHADOW": "rgba(15, 23, 42, 0.65)",
    "PANEL_BORDER": "rgba(56, 189, 248, 0.15)"
}


def init_theme_state():
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False


def toggle_dark_mode():
    init_theme_state()
    with st.sidebar:
        st.markdown("### 🎨 Theme")
        st.caption("Switch the entire app between light and dark mode.")
        st.session_state.dark_mode = st.checkbox(
            "Dark mode 🔘",
            value=st.session_state.dark_mode,
            key="darkmode_toggle"
        )
    return st.session_state.dark_mode


def get_theme(dark_mode: bool) -> dict:
    return DARK_THEME if dark_mode else LIGHT_THEME


def get_theme_css(dark_mode: bool) -> str:
    theme = DARK_THEME if dark_mode else LIGHT_THEME

    return f"""
    <style>
        html, body, main, [data-testid="stAppViewContainer"], [data-testid="stAppContent"], [data-testid="stMain"] {{
            background: {theme['BACKGROUND']} !important;
            color: {theme['TEXT_PRIMARY']};
            font-family: 'Segoe UI', 'Roboto', sans-serif;
            background-attachment: fixed;
        }}
        [data-testid="stAppViewContainer"] > div {{
            background: transparent !important;
        }}
        [data-testid="stSidebar"] {{
            background: {theme['SIDEBAR_BG']} !important;
            color: {theme['TEXT_PRIMARY']};
            border-right: 1px solid {theme['BORDER']};
            box-shadow: inset -2px 0 0 rgba(74, 222, 128, 0.18);
        }}
        [data-testid="stSidebar"] > div {{
            background: transparent !important;
        }}
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            color: {theme['TEXT_PRIMARY']};
        }}
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {{
            color: {theme['TEXT_PRIMARY']};
        }}
        [data-testid="stMetric"] {{
            background: {theme['CARD_BG']};
            color: {theme['TEXT_PRIMARY']};
            padding: 1.4rem;
            border-radius: 20px;
            border: 1px solid {theme['PANEL_BORDER']};
            box-shadow: 0 20px 45px {theme['SHADOW']};
            backdrop-filter: blur(10px);
        }}
        [data-testid="stMetricLabel"] {{
            color: {theme['TEXT_SECONDARY']};
            font-size: 14px;
        }}
        [data-testid="stMetricValue"] {{
            color: {theme['PRIMARY']};
            font-size: 32px;
            font-weight: 700;
        }}
        .stButton>button {{
            background: linear-gradient(90deg, {theme['SECONDARY']} 0%, {theme['ACCENT']} 100%);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.75rem 1.2rem;
            box-shadow: 0 10px 24px rgba(0,0,0,0.12);
        }}
        .stButton>button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 14px 30px rgba(0,0,0,0.18);
        }}
        .css-1lcbmhc.e16nr0p33 {{
            background-color: {theme['CARD_BG']} !important;
        }}
        .stPlotlyChart {{
            border-radius: 18px;
            border: 1px solid {theme['PANEL_BORDER']};
            background: {theme['CARD_BG']};
            padding: 1rem;
            box-shadow: 0 10px 40px {theme['SHADOW']};
        }}
        .metric-card, .info-box {{
            background: {theme['CARD_BG']};
            color: {theme['TEXT_PRIMARY']};
            border-radius: 16px;
            border: 1px solid {theme['PANEL_BORDER']};
            box-shadow: 0 16px 40px {theme['SHADOW']};
        }}
        .info-box {{
            padding: 1rem;
        }}
        hr {{
            border-color: {theme['BORDER']};
            margin: 2rem 0;
        }}
        .stTextInput>div>div>input,
        .stSelectbox>div>div,
        .stDateInput>div>div {{
            background-color: {theme['CARD_BG']};
            color: {theme['TEXT_PRIMARY']};
            border: 1px solid {theme['PANEL_BORDER']};
        }}
    </style>
    """
