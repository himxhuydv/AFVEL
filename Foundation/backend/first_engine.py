from deepface import DeepFace
import os

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

        # result is a list, we take first face
        return result[0]["embedding"]

    except Exception as e:
        print("Face embedding error:", e)
        return None
