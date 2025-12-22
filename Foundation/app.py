from backend.storage import enroll_user, verify_user
from backend.face_engine import (
    get_face_embedding_from_bytes,
    compare_faces
)

import streamlit as st
import base64

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AFVEL", layout="wide")

VIDEO_PATH = r"C:\Users\ashay\OneDrive\Desktop\SACRIFICES OF COMFORT\AFVEL\AFVEL\Foundation\assets\video1.mp4"
LOGO_PATH  = r"C:\Users\ashay\OneDrive\Desktop\SACRIFICES OF COMFORT\AFVEL\AFVEL\Foundation\assets\logo2.jpg"

def to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

video_b64 = to_base64(VIDEO_PATH)
logo_b64  = to_base64(LOGO_PATH)

# ---------------- CSS ----------------
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

div.stButton > button {{
    width: 100% !important;
    background-color: #00FF41 !important;
    color: #000000 !important;
    font-weight: 900 !important;
    border: none !important;
    padding: 10px !important;
}}

/* ===== CAMERA: SMALL + NO EMPTY SPACE ===== */
[data-testid="stCameraInput"] {{
    transform: scale(0.7);
    transform-origin: top center;
    height: auto !important;
}}

[data-testid="stCameraInput"] > div {{
    margin: 0 auto !important;
}}

[data-testid="stCameraInput"] video {{
    max-height: 220px;   /* adjust: 200–240px if needed */
    height: auto !important;
}}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="glowing-title">AFVEL</div>', unsafe_allow_html=True)

left, right = st.columns([1, 1])

# ---------------- LEFT VIDEO ----------------
with left:
    st.markdown(f"""
    <div class="video-wrapper">
        <video autoplay muted loop playsinline>
            <source src="data:video/mp4;base64,{video_b64}" type="video/mp4">
        </video>
    </div>
    """, unsafe_allow_html=True)

# ---------------- RIGHT PANEL ----------------
with right:
    st.markdown("<div class='section-title'>ACCESS CONTROL</div>", unsafe_allow_html=True)

    mode = st.radio("MODE", ["Enroll", "Verify"], horizontal=True)

    if "logged_user" not in st.session_state:
        st.session_state.logged_user = None

    # -------- ENROLL --------
    if mode == "Enroll":
        name = st.text_input("FULL NAME")
        email = st.text_input("EMAIL ADDRESS")
        password = st.text_input("PASSWORD", type="password")

        st.markdown("<div class='section-title'>FACE SCANNER</div>", unsafe_allow_html=True)

        face_file = st.camera_input("CAPTURE FACE")

        if st.button("REGISTER IDENTITY"):
            if not all([name, email, password, face_file]):
                st.error("All fields are required")
            else:
                success, msg = enroll_user(
                    name=name,
                    email=email,
                    password=password,
                    face_file=face_file
                )
                if success:
                    st.success(msg)
                else:
                    st.error(msg)

    # -------- VERIFY --------
    if mode == "Verify":
        email = st.text_input("EMAIL ADDRESS")
        password = st.text_input("PASSWORD", type="password")

        live_face = st.camera_input("SCAN FACE")

        if st.button("LOGIN"):
            if not live_face:
                st.error("Please scan your face")
            else:
                success, user = verify_user(email, password)

                if not success:
                    st.error("Invalid credentials")
                else:
                    stored_embedding = user["face_embedding"]
                    live_embedding = get_face_embedding_from_bytes(live_face)

                    if live_embedding is None:
                        st.error("Face not detected properly")
                    else:
                        match, distance = compare_faces(
                            stored_embedding,
                            live_embedding
                        )

                        if match:
                            st.session_state.logged_user = user
                            st.success(
                                f"Welcome {user['name']} ✔ Face Verified "
                                f"(distance: {distance:.3f})"
                            )
                        else:
                            st.error(
                                f"Face mismatch ❌ (distance: {distance:.3f})"
                            )
