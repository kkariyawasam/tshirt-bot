import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

# ----------------------------
# Page config
# ----------------------------
st.set_page_config(
    page_title="Lux Mockup Studio",
    page_icon="🖤",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------
# Luxury theme (CSS)
# ----------------------------
st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Helpers
# ----------------------------
def api_get(path: str):
    r = requests.get(f"{API_BASE}{path}", timeout=30)
    r.raise_for_status()
    return r.json()

def api_post_json(path: str, payload: dict):
    r = requests.post(f"{API_BASE}{path}", json=payload, timeout=180)
    r.raise_for_status()
    return r.json()

def api_post_file(path: str, file):
    files = {"file": (file.name, file.getvalue(), "image/png")}
    r = requests.post(f"{API_BASE}{path}", files=files, timeout=180)
    r.raise_for_status()
    return r.json()

def lux_card(title: str, subtitle: str | None = None):
    st.markdown(f"<div class='lux-card'><div class='lux-card-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='lux-muted'>{subtitle}</div>", unsafe_allow_html=True)

def end_card():
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------
# Header
# ----------------------------
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

# ----------------------------
# Sidebar: Navigation + API status
# ----------------------------
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
        health = api_get("/health")
        if health.get("ok"):
            st.success("API connected")
        else:
            st.warning("API response unexpected")
    except Exception as e:
        st.error("API not reachable")
        st.caption(f"{e}")
        st.stop()

# ----------------------------
# Load shirts
# ----------------------------
tshirt_data = api_get("/tshirts")
shirts = tshirt_data["shirts"]
shirt_map = {s["display_name"]: s for s in shirts}

# Keep session state
if "logo_id" not in st.session_state:
    st.session_state["logo_id"] = None
if "mockup_filename" not in st.session_state:
    st.session_state["mockup_filename"] = None
if "mockup_url" not in st.session_state:
    st.session_state["mockup_url"] = None

# ----------------------------
# Page 1: Choose Shirt
# ----------------------------
if page.startswith("1"):
    lux_card("Step 1 — Choose a T-shirt", "Select a template from your pre-approved catalog.")
    shirt_choice = st.selectbox("T-shirt Template", list(shirt_map.keys()))
    shirt = shirt_map[shirt_choice]

    placements = list((shirt.get("placements") or {}).keys())
    placement = st.selectbox("Placement", placements)

    st.session_state["shirt_id"] = shirt["id"]
    st.session_state["placement"] = placement

    st.markdown(f"**Selected:** `{shirt['id']}` • Placement: `{placement}`")
    end_card()

# ----------------------------
# Page 2: Add Logo
# ----------------------------
elif page.startswith("2"):
    lux_card("Step 2 — Add a Logo", "Upload your logo or generate a new one with AI.")
    tabs = st.tabs(["Upload Logo", "AI Generate Logo"])

    with tabs[0]:
        st.caption("Upload a transparent PNG for best results.")
        uploaded = st.file_uploader("Choose a PNG logo", type=["png"])
        if st.button("Upload", disabled=(uploaded is None)):
            try:
                res = api_post_file("/logo/upload", uploaded)
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
                # If user wants color, nudge prompt
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
                res = api_post_json("/logo/generate", payload)
                st.session_state["logo_id"] = res["logo_id"]
                st.success(f"AI logo generated ✅  ID: {res['logo_id']}")
                st.caption("Tip: If transparency isn't perfect, we can add background removal next.")
            except Exception as e:
                st.error(f"AI generation failed: {e}")

    if st.session_state["logo_id"]:
        st.markdown(f"**Current logo:** `{st.session_state['logo_id']}`")
        st.markdown(f"[View Logo]({API_BASE}/logos/{st.session_state['logo_id']})")
    else:
        st.info("No logo selected yet.")
    end_card()

# ----------------------------
# Page 3: Preview & Export
# ----------------------------
elif page.startswith("3"):
    lux_card("Step 3 — Preview & Tune", "Adjust size and position before finalizing.")
    shirt_id = st.session_state.get("shirt_id")
    placement = st.session_state.get("placement")
    logo_id = st.session_state.get("logo_id")

    if not shirt_id or not placement:
        st.warning("Please complete Step 1 first (Choose Shirt).")
        end_card()
        st.stop()

    if not logo_id:
        st.warning("Please complete Step 2 first (Add Logo).")
        end_card()
        st.stop()

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
            res = api_post_json("/mockup/generate", payload)
            st.session_state["mockup_filename"] = res["mockup_filename"]
            st.session_state["mockup_url"] = f"{API_BASE}{res['download_url']}"
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

# ----------------------------
# Page 4: Send to Sales
# ----------------------------
else:
    lux_card("Step 4 — Send to Sales", "Send the mockup link to your sales team via n8n email.")
    mockup_filename = st.session_state.get("mockup_filename")
    shirt_id = st.session_state.get("shirt_id")
    placement = st.session_state.get("placement")

    if not mockup_filename:
        st.warning("Generate a mockup in Step 3 first.")
        end_card()
        st.stop()

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
            api_post_json("/send-to-sales", payload)
            st.success("Sent to sales ✅")
            st.caption("Check your sales inbox.")
        except Exception as e:
            st.error(f"Send failed: {e}")

    st.markdown(f"**Mockup file:** `{mockup_filename}`")
    st.markdown(f"[Open mockup]({API_BASE}/mockups/{mockup_filename})")
    end_card()
