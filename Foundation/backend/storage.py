import os
import json
import uuid
from datetime import datetime

BASE_DIR = "data"
FACE_DIR = os.path.join(BASE_DIR, "faces")
VOICE_DIR = os.path.join(BASE_DIR, "voices")
USER_FILE = os.path.join(BASE_DIR, "users.json")

os.makedirs(FACE_DIR, exist_ok=True)
os.makedirs(VOICE_DIR, exist_ok=True)
os.makedirs(BASE_DIR, exist_ok=True)

# ---------- UTIL ----------
def load_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=4)

# ---------- ENROLL ----------
def enroll_user(name, email, password, face_file, voice_file):
    users = load_users()

    # prevent duplicate email
    for u in users:
        if u["email"] == email:
            return False, "User already exists"

    user_id = str(uuid.uuid4())

    face_path = os.path.join(FACE_DIR, f"{user_id}.jpg")
    voice_path = os.path.join(VOICE_DIR, f"{user_id}.wav")

    # save face
    with open(face_path, "wb") as f:
        f.write(face_file.getbuffer())

    # save voice
    with open(voice_path, "wb") as f:
        f.write(voice_file.getbuffer())

    user_data = {
        "id": user_id,
        "name": name,
        "email": email,
        "password": password,  # ⚠️ plaintext for now (will hash later)
        "face_path": face_path,
        "voice_path": voice_path,
        "created_at": datetime.utcnow().isoformat()
    }

    users.append(user_data)
    save_users(users)

    return True, "Enrollment successful"

# ---------- VERIFY (TEMP) ----------
def verify_user(email, password):
    users = load_users()
    for u in users:
        if u["email"] == email and u["password"] == password:
            return True, u
    return False, None
