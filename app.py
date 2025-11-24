from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from TTS.api import TTS
import uuid

app = FastAPI()

# Pure Python multi-voice model (no espeak)
tts = TTS(model_name="tts_models/multilingual/multi-dataset/vits", progress_bar=False)

@app.post("/generate")
async def generate_voice(text: str = Form(...), speaker: str = Form("p226")):
    """
    Generate TTS audio
    'speaker' can be any available speaker in the model (see tts.speakers)
    """
    file_name = f"{uuid.uuid4()}.wav"
    tts.tts_to_file(text=text, speaker=speaker, file_path=file_name)
    return FileResponse(file_name, media_type="audio/wav", filename=file_name)
