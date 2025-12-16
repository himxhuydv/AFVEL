import streamlit as st
import base64

st.set_page_config(page_title="AFVEL", layout="wide")

# ---------- PATHS ----------
VIDEO_PATH = r"C:\Users\ashay\OneDrive\Desktop\SACRIFICES OF COMFORT\AFVEL\AFVEL\Foundation\assets\video1.mp4"
LOGO_PATH  = r"C:\Users\ashay\OneDrive\Desktop\SACRIFICES OF COMFORT\AFVEL\AFVEL\Foundation\assets\logo2.jpg"

def to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

video_b64 = to_base64(VIDEO_PATH)
logo_b64  = to_base64(LOGO_PATH)

# ---------- CSS ----------
st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    padding-top: 0 !important;
    background-image: url("data:image/jpeg;base64,{logo_b64}");
    background-size: 26%;
    background-position: 72% 45%;
    background-repeat: no-repeat;
    background-attachment: fixed;
    background-color: #030217;
}}

[data-testid="stHeader"] {{
    height: 0px;
    background: transparent !important;
}}

.block-container {{
    padding-top: 0 !important;
}}

.glowing-title {{
    text-align: center;
    margin: 0;
    font-size: 66px;
    font-weight: 900;
    color: white;
    letter-spacing: 15px;
    text-shadow: 0 0 15px white, 0 0 30px white;
}}

.video-wrapper {{
    position: relative;
    border-radius: 10px;
    overflow: hidden;
    border: 2px solid #00FF41;
}}

.video-wrapper video {{
    width: 100%;
    height: 100%;
    object-fit: cover;
}}

.section-title {{
    color: #9AFF9A;
    font-weight: 800;
    letter-spacing: 2px;
    margin: 14px 0 8px 0;
    font-size: 13px;
}}

.stTextInput label, .stRadio label {{
    color: #FFFFFF !important;
    font-weight: 800 !important;
}}

.stTextInput input {{
    background-color: #0d1117 !important;
    color: white !important;
    border: 1px solid #00FF41 !important;
}}

[data-testid="stAudioInput"] {{
    transform: scale(0.9);
}}

div.stButton > button {{
    width: 100% !important;
    background-color: #00FF41 !important;
    color: #000000 !important;
    font-weight: 900 !important;
    border: none !important;
    padding: 10px !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.markdown('<div class="glowing-title">AFVEL</div>', unsafe_allow_html=True)

# ---------- MAIN LAYOUT ----------
left, right = st.columns([1, 1])

# ---------- LEFT : VIDEO ----------
with left:
    st.markdown(f"""
    <div class="video-wrapper">
        <video autoplay muted loop playsinline>
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        </video>
    </div>
    """, unsafe_allow_html=True)

# ---------- RIGHT : ACCESS + BIOMETRIC ----------
with right:
    st.markdown("<div class='section-title'>ACCESS CONTROL</div>", unsafe_allow_html=True)

    mode = st.radio("MODE", ["Enroll", "Verify"], horizontal=True)

    # ---------- ENROLL (UNCHANGED) ----------
    if mode == "Enroll":
        st.text_input("FULL NAME")
        st.text_input("EMAIL ADDRESS")
        st.text_input("PASSWORD", type="password")

        st.markdown("<div class='section-title'>BIOMETRIC SCANNER</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.camera_input("CAPTURE FACE")
        with c2:
            st.audio_input("CAPTURE VOICE")

        st.button("REGISTER IDENTITY")

    # ---------- VERIFY (EMAIL + PASSWORD + BIOMETRIC) ----------
    if mode == "Verify":
        st.text_input("EMAIL ADDRESS")
        st.text_input("PASSWORD", type="password")

        st.markdown("<div class='section-title'>BIOMETRIC SCANNER</div>", unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            st.camera_input("SCAN FACE")
        with c2:
            st.audio_input("SCAN VOICE")

        st.button("LOGIN")
