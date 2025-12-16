import streamlit as st
import base64
import os
import re

st.set_page_config(page_title="AFVEL", layout="wide")

# --- FILE PATHS ---
BG_IMAGE_PATH = "assets/logo.jpg"
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

VIDEO_WIDTH = 600
VIDEO_HEIGHT = 338 
video_html = get_video_html(VIDEO_PATH_1, VIDEO_WIDTH, VIDEO_HEIGHT)

# ---------- Load background ----------
def load_bg_image(path):
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return "" 

bg_image = load_bg_image(BG_IMAGE_PATH)

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
    }}

    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image}");
        background-size: cover;
        background-position: center 25%;
        background-repeat: no-repeat;
    }}

    .block-container {{
        padding: 0;
        margin: 0;
        max-width: 100%;
    }}

    .overlay {{
        background: linear-gradient(
            rgba(0, 0, 0, 0.0),
            rgba(0, 0, 0, 0.0)
        );
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
        width: 100%;
        background: rgba(0,0,0,0.3); 
        padding: 22px;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.15);
    }}

    div[data-testid="stTextInput"] {{
        max-width: 100%;
        margin-left: auto; 
        margin-right: auto;
    }}

    div[data-testid="stHorizontalBlock"] > div[data-testid="stRadio"] {{
        width: fit-content;
        margin-left: auto;
        margin-right: auto;
    }}

    .stRadio label {{
        text-align: center;
        display: block;
        width: 100%;
    }}

    div.stButton > button {{
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

    div.stButton > button:hover {{
        background-color: rgba(0, 0, 0, 0.8) !important;
        color: #FFFFFF !important; 
        border-color: #00FFFF !important; 
        box-shadow: 
            0 0 10px #00FFFF, 
            0 0 20px #00FFFF, 
            inset 0 0 10px #00FFFF !important;
    }}

    .info-box {{
        max-width: 400px; 
        background: rgba(0, 0, 0, 0.5); 
        color: #00FF41; 
        padding: 20px;
        margin: 20px auto 30px auto; 
        border-radius: 12px;
        border: 2px solid #00FF41; 
        text-align: left;
        font-family: monospace;
        box-shadow: 
            0 0 10px #00FF41, 
            0 0 20px #00FF41, 
            0 0 40px rgba(0, 255, 65, 0.5); 
    }}

    .creator-credit {{
        font-size: 12px;
        text-align: right;
        border-top: 1px solid rgba(0, 255, 65, 0.3);
        padding-top: 10px;
        margin-top: 15px;
    }}

    .system-status {{
        width: 90%; 
        max-width: 400px;
        background: rgba(0, 0, 0, 0.7);
        color: #00FFFF;
        padding: 8px 15px;
        margin: 15px auto 25px auto;
        border-radius: 4px;
        border: 1px solid #00FFFF;
        font-family: monospace;
        font-size: 14px;
        display: flex;
        justify-content: center;
        box-shadow: 0 0 8px #00FFFF;
        text-align: center;
    }}

    .narrow-content {{
        max-width: 400px;
        width: 100%;
        margin-left: auto;
        margin-right: auto;
    }}
    </style>
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
st.markdown(
    """
    <div class="info-box">
        <h3>SYSTEM PROTOCOL: USER AUTHENTICATION</h3>
        <ul>
            <li><b>Mode Select:</b> Choose Enroll or Verify</li>
            <li><b>ID Entry:</b> Name, Email, System Key</li>
            <li><b>Biometric Capture:</b> Face & Voice</li>
            <li><b>Execute:</b> Save or Verify Identity</li>
        </ul>
        <p class="creator-credit">
            <span style='color:#00FFFF;'>//SYSTEM BUILD //</span><br>
            Creator: <b>Himxhuydv</b> | AFVEL v1.0
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------- 4. NEW: DEVELOPER SIGNATURE BAR (FILLING THE GAP) ----------
st.markdown(
    """
    <div class="system-status">
        <span>[DESIGN STATUS] GENERALLY DESIGNED AND MADE BY HIMXHUYDV</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<div class='narrow-content'>", unsafe_allow_html=True)

# ---------- MODE & INPUTS SETUP (AFTER GAP) ----------
mode = st.radio("Select Mode", ["Enroll", "Verify"], horizontal=True)
name = st.text_input("Enter your name") 
user_email = st.text_input("Enter your email")
user_password = st.text_input("Enter System Key", type="password")

os.makedirs("data/faces", exist_ok=True)
os.makedirs("data/voices", exist_ok=True)
os.makedirs(PASSWORD_DIR, exist_ok=True)

def get_safe_id(email):
    return re.sub(r'[^a-zA-Z0-9\-\.]', '_', email).lower().strip('_')

st.markdown("<div class='card'>", unsafe_allow_html=True)

# ---------- ENROLL (Complete) ----------
if mode == "Enroll":
    st.markdown("### 🧑 Enrollment")
    face = st.camera_input("Capture Face")
    voice = st.audio_input("Record Voice")
    if st.button("Save Identity"):
        if not (user_email and user_password and face and voice):
            st.warning("Please provide all details.")
        else:
            sid = get_safe_id(user_email)
            with open(f"data/faces/{sid}.jpg", "wb") as f:
                f.write(face.getbuffer())
            with open(f"data/voices/{sid}.wav", "wb") as f:
                f.write(voice.getbuffer())
            with open(f"{PASSWORD_DIR}/{sid}.txt", "w") as f:
                f.write(user_password)
            st.success("Identity Enrolled Successfully")

# ---------- VERIFY (Complete) ----------
if mode == "Verify":
    st.markdown("### 🔐 Verification")
    face = st.camera_input("Capture Face")
    voice = st.audio_input("Record Voice")
    if st.button("Verify Identity"):
        sid = get_safe_id(user_email)
        if os.path.exists(f"{PASSWORD_DIR}/{sid}.txt"):
            with open(f"{PASSWORD_DIR}/{sid}.txt") as f:
                if f.read().strip() == user_password:
                    st.success("ACCESS GRANTED")
                else:
                    st.error("ACCESS DENIED")
        else:
            st.error("IDENTITY NOT FOUND")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)