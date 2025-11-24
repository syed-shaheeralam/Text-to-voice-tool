from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from TTS.api import TTS
import os

app = FastAPI()

# Load TTS model once when app starts
tts = TTS(model_name="tts_models/en/vctk/vits")

@app.post("/generate")
async def generate_voice(text: str = Form(...)):
    out_path = "output.wav"
    tts.tts_to_file(text=text, file_path=out_path)
    return FileResponse(out_path)

@app.get("/")
def home():
    return {"message": "Voiceover API is running"}
