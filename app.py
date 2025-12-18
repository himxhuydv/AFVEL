# =======================
# IMPORTS
# =======================
import os
import json
import bcrypt
import streamlit as st
import base64
import re
import cv2
import numpy as np

# =======================
# PAGE CONFIG
# =======================
st.set_page_config(page_title="AFVEL", layout="wide")

# =======================
# PATHS
# =======================
BG_VIDEO_PATH = "assets/video2.mp4"
VIDEO_PATH_1 = "assets/video1.mp4"
FACE_CASCADE_PATH = "assets/haarcascade_frontalface_default.xml"

# =======================
# SESSION STATE
# =======================
if "access_granted" not in st.session_state:
    st.session_state.access_granted = False

if "enroll_success" not in st.session_state:
    st.session_state.enroll_success = False

# =======================
# FACE DETECTOR
# =======================
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

# =======================
# HELPER FUNCTIONS
# =======================
def get_safe_id(email):
    return re.sub(r'[^a-zA-Z0-9\-\.]', '_', email).lower().strip('_')


def extract_face(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return None

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.3, minNeighbors=5
    )

    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]
    face = gray[y:y+h, x:x+w]
    face = cv2.resize(face, (200, 200))
    return face


def save_user(email, password, face, voice):
    user_dir = f"data/users/{get_safe_id(email)}"
    os.makedirs(user_dir, exist_ok=True)

    # Save password (hashed)
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    with open(f"{user_dir}/password.hash", "wb") as f:
        f.write(hashed)

    # Save profile
    with open(f"{user_dir}/profile.json", "w") as f:
        json.dump({"email": email}, f, indent=4)

    # Save face image
    face_path = f"{user_dir}/face.jpg"
    with open(face_path, "wb") as f:
        f.write(face.getbuffer())

    # Extract & save face data
    face_img = extract_face(face_path)
    if face_img is not None:
        np.save(f"{user_dir}/face.npy", face_img)

    # Save voice
    with open(f"{user_dir}/voice.wav", "wb") as f:
        f.write(voice.getbuffer())


def verify_password(email, password):
    user_dir = f"data/users/{get_safe_id(email)}"
    path = f"{user_dir}/password.hash"
    if not os.path.exists(path):
        return False
    with open(path, "rb") as f:
        return bcrypt.checkpw(password.encode(), f.read())


def verify_face(email, live_face):
    user_dir = f"data/users/{get_safe_id(email)}"
    saved_face_path = f"{user_dir}/face.npy"

    if not os.path.exists(saved_face_path):
        return False

    temp_path = f"{user_dir}/temp_face.jpg"
    with open(temp_path, "wb") as f:
        f.write(live_face.getbuffer())

    live_face_img = extract_face(temp_path)
    if live_face_img is None:
        return False

    saved_face = np.load(saved_face_path)
    diff = np.mean(np.abs(saved_face - live_face_img))

    return diff < 40   # threshold


def get_video_html(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    return f"""
    <div style="text-align:center;">
        <video autoplay loop muted playsinline width="600">
            <source src="data:video/mp4;base64,{b64}" type="video/mp4">
        </video>
    </div>
    """


def get_bg_video_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# =======================
# VIDEO
# =======================
video_html = get_video_html(VIDEO_PATH_1)
bg_video = get_bg_video_base64(BG_VIDEO_PATH)

# =======================
# CSS
# =======================
st.markdown(
    f"""
    <style>
    body {{ background:black; }}
    .bg-video {{
        position:fixed;
        top:0; left:0;
        width:100vw; height:100vh;
        object-fit:cover;
        z-index:-1;
        filter:brightness(0.4);
    }}
    .card {{
        max-width:420px;
        margin:auto;
        background:rgba(0,0,0,0.6);
        padding:20px;
        border-radius:12px;
    }}
    div.stButton > button {{
        width:100%;
        background:black;
        color:#00FF41;
        border:2px solid #00FF41;
        font-weight:bold;
    }}
    </style>

    <video class="bg-video" autoplay loop muted>
        <source src="data:video/mp4;base64,{bg_video}" type="video/mp4">
    </video>
    """,
    unsafe_allow_html=True
)

# =======================
# UI
# =======================
st.markdown(video_html, unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;color:white;'>AFVEL</h1>", unsafe_allow_html=True)
st.markdown("<div class='card'>", unsafe_allow_html=True)

mode = st.radio("Select Mode", ["Enroll", "Verify"], horizontal=True)

# Reset message when leaving Enroll
if mode != "Enroll":
    st.session_state.enroll_success = False

# =======================
# ENROLL
# =======================
if mode == "Enroll":
    email = st.text_input("Email")
    password = st.text_input("System Key", type="password")
    face = st.camera_input("Capture Face")
    voice = st.audio_input("Record Voice")

    if st.button("Register Identity"):
        if not email:
            st.warning("❌ Email required")
        elif not password:
            st.warning("❌ System Key required")
        elif face is None:
            st.warning("❌ Capture your face")
        elif voice is None:
            st.warning("❌ Record your voice")
        else:
            save_user(email, password, face, voice)
            st.session_state.enroll_success = True

if st.session_state.enroll_success:
    st.success("✅ Your identity has been successfully saved!")
    st.toast("Enrollment successful 🎉", icon="✅")

# =======================
# VERIFY
# =======================
if mode == "Verify":
    email = st.text_input("Email")
    password = st.text_input("System Key", type="password")
    face = st.camera_input("Scan Face")

    if st.button("Verify Identity"):
        if verify_password(email, password):
            if verify_face(email, face):
                st.session_state.access_granted = True
                st.success(f"🔓 ACCESS GRANTED — Welcome {email}")
            else:
                st.error("❌ Face does not match")
        else:
            st.error("❌ Invalid password")

# =======================
# POST LOGIN
# =======================
if st.session_state.access_granted:
    st.markdown("### 🎁 You have a gift")
    if st.button("OPEN GIFT"):
        st.image("assets/qr.png", caption="Scan QR to Continue")

st.markdown("</div>", unsafe_allow_html=True)
