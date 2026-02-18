import streamlit as st
from ui.styles import lux_card, end_card

def render(api, api_base: str):
    lux_card("Step 3 — Preview & Tune", "Adjust size and position before finalizing.")

    shirt_id = st.session_state.get("shirt_id")
    placement = st.session_state.get("placement")
    logo_id = st.session_state.get("logo_id")

    if not shirt_id or not placement:
        st.warning("Please complete Step 1 first (Choose Shirt).")
        end_card()
        return

    if not logo_id:
        st.warning("Please complete Step 2 first (Add Logo).")
        end_card()
        return

    c1, c2, c3 = st.columns(3)
    with c1:
        scale = st.slider("Scale", 0.2, 2.5, 1.0, 0.05)
    with c2:
        offset_x = st.slider("Offset X", -300, 300, 0, 5)
    with c3:
        offset_y = st.slider("Offset Y", -300, 300, 0, 5)

    if st.button("Generate Preview"):
        try:
            payload = {
                "shirt_id": shirt_id,
                "placement": placement,
                "logo_id": logo_id,
                "scale": float(scale),
                "offset_x": int(offset_x),
                "offset_y": int(offset_y),
            }
            res = api.post_json("/mockup/generate", payload)
            st.session_state["mockup_filename"] = res["mockup_filename"]
            st.session_state["mockup_url"] = f"{api_base}{res['download_url']}"
            st.success("Preview ready ✅")
        except Exception as e:
            st.error(f"Mockup generation failed: {e}")

    mockup_url = st.session_state.get("mockup_url")
    mockup_filename = st.session_state.get("mockup_filename")
    if mockup_url:
        st.image(mockup_url, caption="Mockup Preview", use_container_width=True)
        st.markdown(f"[Open / Download Mockup]({mockup_url})")
        st.caption(f"Filename: {mockup_filename}")
    else:
        st.info("Generate a preview to see the mockup here.")

    end_card()
