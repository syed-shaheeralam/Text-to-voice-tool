from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from TTS.api import TTS
import uuid

app = FastAPI()

# Multi-voice model (VCTK, requires espeak backend)
tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False)

@app.post("/generate")
async def generate_voice(text: str = Form(...), speaker: str = Form("p226")):
    """
    Generate TTS audio
    - 'text': text to convert
    - 'speaker': choose from tts.speakers (boys, girls, kids, old, cinematic)
    """
    file_name = f"{uuid.uuid4()}.wav"
    tts.tts_to_file(text=text, speaker=speaker, file_path=file_name)
    return FileResponse(file_name, media_type="audio/wav", filename=file_name)

# Run: uvicorn app:app --reload --port 8000
