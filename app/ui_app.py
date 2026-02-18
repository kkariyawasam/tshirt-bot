import streamlit as st

from ui.api import ApiClient
from ui.state import init_state
from ui.styles import apply_luxury_theme, header

from ui.pages import page_choose_shirt, page_add_logo, page_preview_export, page_send_sales

API_BASE = "http://127.0.0.1:8000"
api = ApiClient(API_BASE)

# Page config
st.set_page_config(
    page_title="Lux Mockup Studio",
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_luxury_theme()
header()
init_state()

# Sidebar nav + API status
with st.sidebar:
    st.markdown("## 🧭 Navigation")
    page = st.radio(
        "Go to",
        ["1) Choose Shirt", "2) Add Logo", "3) Preview & Export", "4) Send to Sales"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("## 🔌 API Status")
    try:
        health = api.get("/health")
        if health.get("ok"):
            st.success("API connected")
        else:
            st.warning("API response unexpected")
    except Exception as e:
        st.error("API not reachable")
        st.caption(f"{e}")
        st.stop()

# Load shirts once
tshirt_data = api.get("/tshirts")
shirts = tshirt_data["shirts"]
shirt_map = {s["display_name"]: s for s in shirts}

# Render pages
if page.startswith("1"):
    page_choose_shirt.render(shirt_map)
elif page.startswith("2"):
    page_add_logo.render(api, API_BASE)
elif page.startswith("3"):
    page_preview_export.render(api, API_BASE)
else:
    page_send_sales.render(api, API_BASE)
