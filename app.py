import gradio as gr
from gtts import gTTS
import pyttsx3
from pydub import AudioSegment

# ---------- FEMALE (GTTS) ----------
def female_voice(text):
    tts = gTTS(text=text, lang="en")
    tts.save("female.mp3")
    return "female.mp3"

# ---------- MALE (pyttsx3 using espeak inside HF) ----------
def male_voice(text):
    engine = pyttsx3.init()

    voices = engine.getProperty("voices")

    # Select male voice safely
    for v in voices:
        if "male" in v.name.lower() or "en-us" in v.id.lower():
            engine.setProperty("voice", v.id)
            break

    engine.setProperty("rate", 150)

    engine.save_to_file(text, "male.wav")
    engine.runAndWait()

    sound = AudioSegment.from_wav("male.wav")
    sound.export("male.mp3", format="mp3")

    return "male.mp3"

# ---------- MASTER ----------
def generate(text, voice):
    if voice == "Female":
        return female_voice(text)
    else:
        return male_voice(text)

# ---------- UI ----------
with gr.Blocks() as demo:
    gr.Markdown("## 🎤 Simple TTS — Female (gTTS) + Male (pyttsx3)")

    text = gr.Textbox(label="Enter Text")
    voice = gr.Dropdown(["Female", "Male"], label="Select Voice", value="Female")
    out = gr.Audio(label="Generated Voice", type="filepath")

    btn = gr.Button("Generate")
    btn.click(generate, inputs=[text, voice], outputs=out)

demo.launch()
