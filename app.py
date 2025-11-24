from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from TTS.api import TTS
import uuid

app = FastAPI()

# Load Hugging Face model (no espeak needed)
tts = TTS(model_name="tts_models/en/ljspeech/fastspeech2", progress_bar=False)

@app.post("/generate")
async def generate_voice(text: str = Form(...)):
    """Generate TTS audio for given text"""
    file_name = f"{uuid.uuid4()}.wav"
    tts.tts_to_file(text=text, file_path=file_name)
    return FileResponse(file_name, media_type="audio/wav", filename=file_name)

# Run: uvicorn app:app --reload --port 8000
