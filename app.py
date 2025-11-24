from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from TTS.api import TTS
import uuid
import os

app = FastAPI()

# Load model (once, global)
tts = TTS(model_name="tts_models/en/vctk/vits")

@app.post("/generate")
async def generate_voice(text: str = Form(...), voice: str = Form("default")):
    """
    Generate voice for given text.
    voice can be: "default", "p225", "f121", etc. (depends on model)
    """
    file_name = f"{uuid.uuid4()}.wav"
    tts.tts_to_file(text=text, speaker=voice, file_path=file_name)
    return FileResponse(file_name, media_type="audio/wav", filename=file_name)

# To run: uvicorn app:app --reload --port 8000
