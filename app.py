import gradio as gr
from gtts import gTTS
import pyttsx3
import os
from pydub import AudioSegment

# ---------- FEMALE VOICE (GTTS) ----------
def female_voice(text):
    tts = gTTS(text=text, lang="en")
    tts.save("female_output.mp3")
    return "female_output.mp3"

# ---------- MALE VOICE (pyttsx3 + espeak-ng) ----------
def male_voice(text):
    engine = pyttsx3.init()

    # force espeak-ng (HuggingFace compatible)
    engine.setProperty("voice", "english-us")
    engine.setProperty("rate", 160)
    engine.setProperty("pitch", 40)

    engine.save_to_file(text, "male_raw.wav")
    engine.runAndWait()

    # convert to mp3
    sound = AudioSegment.from_wav("male_raw.wav")
    sound.export("male_output.mp3", format="mp3")

    return "male_output.mp3"

# ---------- MAIN FUNCTION ----------
def generate_voice(text, voice_type):
    if voice_type == "Female":
        return female_voice(text)
    else:
        return male_voice(text)

# ---------- GRADIO UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🎤 Simple TTS (gTTS + pyttsx3)")

    text = gr.Textbox(label="Enter text")
    voice = gr.Dropdown(["Female", "Male"], value="Female", label="Select Voice")
    audio_out = gr.Audio(label="Generated Voice", type="filepath")

    gen_btn = gr.Button("Generate")

    gen_btn.click(generate_voice, inputs=[text, voice], outputs=audio_out)

demo.launch()
