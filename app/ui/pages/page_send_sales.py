import streamlit as st
from ui.styles import lux_card, end_card

def render(api, api_base: str):
    lux_card("Step 4 — Send to Sales", "Send the mockup link to your sales team via n8n email.")

    mockup_filename = st.session_state.get("mockup_filename")
    shirt_id = st.session_state.get("shirt_id")
    placement = st.session_state.get("placement")

    if not mockup_filename:
        st.warning("Generate a mockup in Step 3 first.")
        end_card()
        return

    customer_name = st.text_input("Customer name", value="John Smith")
    customer_email = st.text_input("Customer email", value="john@example.com")

    if st.button("Send Email to Sales"):
        try:
            payload = {
                "customer_name": customer_name,
                "customer_email": customer_email,
                "shirt_id": shirt_id,
                "placement": placement,
                "mockup_filename": mockup_filename,
            }
            api.post_json("/send-to-sales", payload)
            st.success("Sent to sales ✅")
            st.caption("Check your sales inbox.")
        except Exception as e:
            st.error(f"Send failed: {e}")

    st.markdown(f"**Mockup file:** `{mockup_filename}`")
    st.markdown(f"[Open mockup]({api_base}/mockups/{mockup_filename})")

    end_card()
