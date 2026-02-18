import streamlit as st
from ui.styles import lux_card, end_card

def render(api, api_base: str):
    lux_card("Step 2 — Add a Logo", "Upload your logo or generate a new one with AI.")
    tabs = st.tabs(["Upload Logo", "AI Generate Logo"])

    with tabs[0]:
        st.caption("Upload a transparent PNG for best results.")
        uploaded = st.file_uploader("Choose a PNG logo", type=["png"])
        if st.button("Upload", disabled=(uploaded is None)):
            try:
                res = api.post_file_png("/logo/upload", uploaded)
                st.session_state["logo_id"] = res["logo_id"]
                st.success(f"Logo uploaded ✅  ID: {res['logo_id']}")
            except Exception as e:
                st.error(f"Upload failed: {e}")

    with tabs[1]:
        brand_name = st.text_input("Brand name (optional)", placeholder="e.g., NorthPeak")
        prompt = st.text_area("Describe your logo idea", height=90, placeholder="e.g., A mountain peak with NP monogram")
        style = st.selectbox("Style", ["minimal", "modern", "mascot", "vintage", "luxury"], index=4)
        color_palette = st.text_input("Color palette (optional)", placeholder="e.g., gold, white, deep navy")
        colorful = st.checkbox("Make it colorful (high saturation)", value=True)
        transparent = st.checkbox("Transparent background", value=True)

        if st.button("Generate AI Logo", disabled=(prompt.strip() == "")):
            try:
                palette = color_palette.strip() if color_palette.strip() else None
                if colorful and not palette:
                    palette = "gold, white, deep navy, accent color"

                payload = {
                    "brand_name": brand_name.strip() or None,
                    "prompt": prompt.strip() + (" Use vibrant colors, high saturation, at least 3 colors." if colorful else ""),
                    "style": style,
                    "color_palette": palette,
                    "transparent_background": transparent,
                    "size": "1024x1024",
                }
                res = api.post_json("/logo/generate", payload)
                st.session_state["logo_id"] = res["logo_id"]
                st.success(f"AI logo generated ✅  ID: {res['logo_id']}")
            except Exception as e:
                st.error(f"AI generation failed: {e}")

    if st.session_state["logo_id"]:
        st.markdown(f"**Current logo:** `{st.session_state['logo_id']}`")
        st.markdown(f"[View Logo]({api_base}/logos/{st.session_state['logo_id']})")
    else:
        st.info("No logo selected yet.")

    end_card()
