import os
import soundfile as sf

def load_voice_audio(path):
    if not os.path.exists(path):
        return None, None
    audio, sample_rate = sf.read(path)
    return audio, sample_rate
