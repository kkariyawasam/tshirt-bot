import streamlit as st

def init_state():
    defaults = {
        "shirt_id": None,
        "placement": None,
        "logo_id": None,
        "mockup_filename": None,
        "mockup_url": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v
