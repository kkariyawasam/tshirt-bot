import streamlit as st
from ui.styles import lux_card, end_card

def render(shirt_map: dict):
    lux_card("Step 1 — Choose a T-shirt", "Select a template from your pre-approved catalog.")

    shirt_choice = st.selectbox("T-shirt Template", list(shirt_map.keys()))
    shirt = shirt_map[shirt_choice]

    placements = list((shirt.get("placements") or {}).keys())
    placement = st.selectbox("Placement", placements)

    st.session_state["shirt_id"] = shirt["id"]
    st.session_state["placement"] = placement

    st.markdown(f"**Selected:** `{shirt['id']}` • Placement: `{placement}`")
    end_card()
