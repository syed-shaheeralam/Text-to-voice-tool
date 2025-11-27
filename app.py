from flask import Flask, request, send_file
from gtts import gTTS
import pyttsx3
import os
from pydub import AudioSegment

app = Flask(__name__)

# ---------- FEMALE VOICE (gTTS) ----------
def female_voice(text):
    tts = gTTS(text=text, lang="en")
    tts.save("female_output.mp3")
    return "female_output.mp3"

# ---------- MALE VOICE (pyttsx3) ----------
def male_voice(text):
    engine = pyttsx3.init()
    engine.setProperty("voice", "com.apple.speech.synthesis.voice.Alex" if "darwin" in os.sys.platform else engine.getProperty("voices")[0].id)
    engine.save_to_file(text, "male_output.mp3")
    engine.runAndWait()
    return "male_output.mp3"

@app.route("/tts", methods=["POST"])
def tts():
    text = request.json.get("text")
    voice = request.json.get("voice")

    if not text:
        return {"error": "Text missing"}, 400

    if voice == "female":
        file_path = female_voice(text)
    elif voice == "male":
        file_path = male_voice(text)
    else:
        return {"error": "Invalid voice"}, 400

    return send_file(file_path, as_attachment=True)

@app.route("/")
def home():
    return {
        "message": "TTS API is running",
        "voices": ["female", "male"],
        "usage": "POST /tts {text:'hello', voice:'female'}"
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7860)
