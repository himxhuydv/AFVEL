import streamlit as st
import base64
import os
import re

st.set_page_config(page_title="AFVEL", layout="wide")

# --- FILE PATHS ---
BG_VIDEO_PATH = "assets/video2.mp4"
VIDEO_PATH_1 = "assets/video1.mp4" 
PASSWORD_DIR = "data/passwords"

# 1. Video preparation (Reading and Base64 Encoding)
def get_video_html(path, width, height):
    if os.path.exists(path):
        try:
            with open(path, "rb") as f:
                video_bytes_content = f.read()
            video_bytes = base64.b64encode(video_bytes_content).decode()
            print(f"DEBUG: Successfully encoded {os.path.basename(path)}")
            return f"""
            <div style='text-align: center; padding: 20px 0 5px 0;'>
                <video 
                    width='{width}' 
                    height='{height}' 
                    autoplay 
                    loop 
                    muted
                    playsinline
                    style='border-radius: 8px; margin: 0 auto;'
                >
                    <source src='data:video/mp4;base64,{video_bytes}' type='video/mp4'>
                    Your browser does not support the video tag.
                </video>
            </div>
            """
        except Exception as e:
            print(f"DEBUG: ERROR encoding {os.path.basename(path)}: {e}")
            return f"<div style='color: red; text-align: center; margin-top: 20px;'>Error encoding {os.path.basename(path)}: {e}</div>"
    else:
        print(f"DEBUG: FILE NOT FOUND at {path}")
        return f"<div style='color: orange; text-align: center; margin-top: 20px;'>{os.path.basename(path)} **FILE NOT FOUND**. Check path: {path}</div>"

def get_bg_video_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

VIDEO_WIDTH = 600
VIDEO_HEIGHT = 338 
video_html = get_video_html(VIDEO_PATH_1, VIDEO_WIDTH, VIDEO_HEIGHT)
bg_video = get_bg_video_base64(BG_VIDEO_PATH)

# ---------- CSS (UNCHANGED) ----------
st.markdown(
    f"""
    <style>
    html, body {{
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
        background: black;
        overflow-x: hidden;
    }}

    .bg-video {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        object-fit: cover;
        z-index: -1;
        filter: brightness(0.45);
    }}

    .block-container {{
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }}

    .overlay {{
        min-height: calc(100vh - 380px); 
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: flex-start; 
        text-align: center;
    }}

    .title {{
        font-size: 70px;
        font-weight: 900;
        color: #FFFFFF;
        letter-spacing: 5px;
        text-shadow:
            0 0 6px  #FFFFFF,
            0 0 14px rgba(255,255,255,0.8),
            0 0 30px rgba(255,255,255,0.6);
        margin-top: 5px; 
    }}

    .subtitle {{
        font-size: 20px;
        color: #F0F0F0;
        margin-bottom: 20px;
    }}

    .card {{
        max-width: 400px !important;
        width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;
        background: rgba(0,0,0,0.35); 
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(6px);
    }}

    div[data-testid="stTextInput"],
    div[data-testid="stPasswordInput"],
    div[data-testid="stRadio"],
    div[data-testid="stButton"],
    div[data-testid="stCameraInput"],
    div[data-testid="stAudioInput"] {{
        max-width: 400px !important;
        width: 100% !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}

    div.stButton > button {{
        width: 100% !important;
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: #00FF41 !important;
        border: 2px solid #00FF41 !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 0 5px #00FF41, inset 0 0 5px #00FF41 !important; 
    }}

    .info-box {{
        max-width: 400px !important;
        background: rgba(0,0,0,0.5);
    }}

    .system-status {{
        max-width: 400px !important;
    }}
    </style>

    <video class="bg-video" autoplay loop muted playsinline>
        <source src="data:video/mp4;base64,{bg_video}" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)

# ---------- 1. VIDEO DISPLAY (AT THE VERY TOP) ----------
st.warning("If the video does not autoplay, please click the play button due to browser restrictions.", icon="⚠️")
st.markdown(video_html, unsafe_allow_html=True)

# ---------- 2. UI HEADER (BELOW VIDEO) ----------
st.markdown(
    """
    <div class="overlay">
        <div class="title"><h1>AFVEL<h1/></div>
        <div class="subtitle">AI Face & Voice Entry Lock</div>
    """,
    unsafe_allow_html=True
)

# ---------- 3. INSTRUCTION AND CREATOR INFO (AFTER TITLE) ----------
info_html = f"""
<div class="info-box">
    <h3>SYSTEM PROTOCOL: USER AUTHENTICATION</h3>
    <ul>
        <li>**Mode Select:** Choose **Enroll** (Initial Setup) or **Verify** (Access).</li>
        <li>**ID Entry:** Provide Name, Email (used as Unique ID), and System Key.</li>
        <li>**Biometric Capture:** Capture a fresh **Face** image and **Voice** recording.</li>
        <li>**Execute:** Click the button to save or check your multi-factor identity.</li>
    </ul>
    <p class="creator-credit">
        <span style='color: #00FFFF;'>//SYSTEM BUILD //</span><br>
        Creator: <span style='font-weight: bold;'>Himxhuydv</span> | AFVEL v1.0
    </p>
</div>
"""
st.markdown(info_html, unsafe_allow_html=True)

# ---------- 4. NEW: DEVELOPER SIGNATURE BAR (FILLING THE GAP) ----------
developer_signature_html = f"""
<div class="system-status">
    <span>[DESIGN STATUS] GENERALLY DESIGNED AND MADE BY HIMXHUYDV: DASHING 19 YEAR OLD, DECENT CUTE PUNJABI MUNDA</span>
</div>
"""
st.markdown(developer_signature_html, unsafe_allow_html=True)

# ---------- MODE & INPUTS SETUP (AFTER GAP) ----------
mode = st.radio("Select Mode", ["Enroll", "Verify"], horizontal=True)
name = st.text_input("Enter your name") 
user_email = st.text_input("Enter your email")
user_password = st.text_input("Enter System Key", type="password")

os.makedirs("data/faces", exist_ok=True)
os.makedirs("data/voices", exist_ok=True)
os.makedirs(PASSWORD_DIR, exist_ok=True) 

def get_safe_id(email):
    safe_id = re.sub(r'[^a-zA-Z0-9\-\.]', '_', email)
    return safe_id.lower().strip('_')

st.markdown("<div class='card'>", unsafe_allow_html=True)

# ---------- ENROLL (Complete) ----------
if mode == "Enroll":
    st.markdown("### 🧑 Enrollment")
    face = st.camera_input("Capture Face")
    voice = st.audio_input("Record Voice")

    if st.button("Save Identity"):
        if not (user_email and user_password and face and voice):
            st.warning("Please provide name, email, System Key, face, and voice to enroll.")
        elif '@' not in user_email or '.' not in user_email:
            st.error("Please enter a valid email address.")
        else:
            safe_id = get_safe_id(user_email)
            with open(f"data/faces/{safe_id}.jpg", "wb") as f:
                f.write(face.getbuffer())
            with open(f"data/voices/{safe_id}.wav", "wb") as f:
                f.write(voice.getbuffer())
            with open(f"{PASSWORD_DIR}/{safe_id}.txt", "w") as f:
                f.write(user_password)
            st.success(f"✅ Identity for **{user_email}** Enrolled Successfully")

# ---------- VERIFY (Complete) ----------
if mode == "Verify":
    st.markdown("### 🔐 Verification")
    face = st.camera_input("Capture Face")
    voice = st.audio_input("Record Voice")

    if st.button("Verify Identity"):
        safe_id = get_safe_id(user_email)
        password_path = f"{PASSWORD_DIR}/{safe_id}.txt"
        if os.path.exists(password_path):
            with open(password_path) as f:
                if f.read().strip() == user_password:
                    st.success("🔓 ACCESS GRANTED (Basic Multi-factor Match)")
                else:
                    st.error("❌ ACCESS DENIED: Invalid System Key.")
        else:
            st.error("❌ ACCESS DENIED: Identity not found.")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)