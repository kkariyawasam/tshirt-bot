import streamlit as st

LUXURY_CSS = """
<style>
html, body, [class*="css"]  {
    font-size: 30px !important;
}

/* Page background */
.stApp {
    background: radial-gradient(circle at top left, #111827 0%, #0b0f1a 45%, #05070d 100%);
    color: #E5E7EB;
    font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
}

/* Hide Streamlit default footer */
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b0f1a 0%, #070915 100%);
    border-right: 1px solid rgba(255, 215, 0, 0.10);
}

/* Headings */
h1, h2, h3 {
    letter-spacing: 0.2px;
}

/* Card container */
.lux-card {
    background: rgba(17, 24, 39, 0.60);
    border: 1px solid rgba(255, 215, 0, 0.12);
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
    border-radius: 18px;
    padding: 18px 18px 10px 18px;
    margin-bottom: 16px;
}

.lux-card-title {
    font-size: 15px;
    color: rgba(255,215,0,0.95);
    margin-bottom: 6px;
    font-weight: 600;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}

.lux-muted {
    color: rgba(229, 231, 235, 0.75);
    font-size: 13px;
}

/* Buttons */
div.stButton > button {
    background: linear-gradient(135deg, #C9A227 0%, #F7D774 55%, #C9A227 100%);
    color: #0b0f1a;
    border: 0px;
    border-radius: 14px;
    padding: 0.60em 1.05em;
    font-weight: 700;
    box-shadow: 0 10px 20px rgba(0,0,0,0.35);
    transition: transform 0.05s ease-in-out;
}
div.stButton > button:hover {
    transform: translateY(-1px);
    color: #0b0f1a;
}

/* Inputs */
.stTextInput input, .stSelectbox div, .stTextArea textarea {
    background: rgba(17, 24, 39, 0.55) !important;
    border: 1px solid rgba(255, 215, 0, 0.12) !important;
    border-radius: 12px !important;
    color: #E5E7EB !important;
}

/* Slider */
.stSlider > div {
    background: rgba(17, 24, 39, 0.25);
    border-radius: 12px;
    padding: 10px;
    border: 1px solid rgba(255,215,0,0.08);
}

/* Small badges */
.lux-badge {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(255, 215, 0, 0.10);
    border: 1px solid rgba(255, 215, 0, 0.14);
    color: rgba(255,215,0,0.95);
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.3px;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid rgba(255, 215, 0, 0.10);
    margin: 18px 0;
}
</style>
"""

def apply_luxury_theme():
    st.markdown(LUXURY_CSS, unsafe_allow_html=True)

def header():
    st.markdown(
        """
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom: 14px;">
            <div>
                <div style="font-size:34px; font-weight:800; color:#F7D774; line-height:1;">
                    Mockup Studio
                </div>
                <div style="color:rgba(229,231,235,0.75); margin-top:6px;">
                    Create premium T-shirt mockups from your logo or an AI-generated logo.
                </div>
            </div>
            <div class="lux-badge">Local • FastAPI + Streamlit</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def lux_card(title: str, subtitle: str | None = None):
    st.markdown(f"<div class='lux-card'><div class='lux-card-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='lux-muted'>{subtitle}</div>", unsafe_allow_html=True)

def end_card():
    st.markdown("</div>", unsafe_allow_html=True)
