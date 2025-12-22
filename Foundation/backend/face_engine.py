from deepface import DeepFace
import numpy as np
import os
import tempfile

# -------------------------------------------------
# ENROLL: Generate embedding from saved image path
# -------------------------------------------------
def get_face_embedding(image_path):
    """
    Takes face image path
    Returns face embedding (list of floats) or None
    """

    if not os.path.exists(image_path):
        return None

    try:
        result = DeepFace.represent(
            img_path=image_path,
            model_name="Facenet",
            enforce_detection=True
        )

        # Take first detected face
        return result[0]["embedding"]

    except Exception as e:
        print("Face embedding error:", e)
        return None


# -------------------------------------------------
# VERIFY: Generate embedding from Streamlit camera input
# -------------------------------------------------
def get_face_embedding_from_bytes(uploaded_file):
    """
    Takes Streamlit UploadedFile (camera_input)
    Returns face embedding or None
    """

    try:
        # Save uploaded image temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(uploaded_file.getbuffer())
            temp_path = tmp.name

        result = DeepFace.represent(
            img_path=temp_path,
            model_name="Facenet",
            enforce_detection=True
        )

        # Cleanup temp file
        os.remove(temp_path)

        return result[0]["embedding"]

    except Exception as e:
        print("Live face error:", e)
        return None


# -------------------------------------------------
# FACE COMPARISON
# -------------------------------------------------
def compare_faces(embedding_1, embedding_2, threshold=0.6):
    """
    Compares two face embeddings
    Returns (match: bool, distance: float)
    """

    emb1 = np.array(embedding_1)
    emb2 = np.array(embedding_2)

    distance = np.linalg.norm(emb1 - emb2)

    return distance < threshold, distance
