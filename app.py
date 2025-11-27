import gradio as gr
from gtts import gTTS
import pyttsx3
import os
from pydub import AudioSegment

# ---------- FEMALE VOICE (gTTS) ----------
def female_voice(text):
    tts = gTTS(text=text, lang="en")
    tts.save("female_output.mp3")
    return "female_output.mp3"

# ---------- MALE VOICE (pyttsx3) ----------
def male_voice(text):
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    
    # try to pick a male voice
    male = None
    for v in voices:
        if "male" in v.name.lower() or "alex" in v.name.lower():
            male = v.id
            break

    engine.setProperty("voice", male if male else voices[0].id)
    engine.save_to_file(text, "male_output.mp3")
    engine.runAndWait()
    return "male_output.mp3"

# ---------- MAIN FUNCTION ----------
def generate_voice(text, voice_type):
    if not text.strip():
        return None

    if voice_type == "Female":
        output = female_voice(text)
    else:
        output = male_voice(text)

    return output

# ---------- GRADIO UI ----------
with gr.Blocks(title="Simple TTS App") as demo:
    gr.Markdown("# 🎙️ Text to Speech Generator")
    gr.Markdown("Select a voice & enter your text to generate speech.")

    text_input = gr.Textbox(label="Enter text here", placeholder="Type anything...")
    voice_dropdown = gr.Dropdown(["Female", "Male"], value="Female", label="Select Voice")

    output_audio = gr.Audio(label="Generated Voice", type="filepath")

    generate_btn = gr.Button("Generate Voice")

    generate_btn.click(
        fn=generate_voice,
        inputs=[text_input, voice_dropdown],
        outputs=output_audio
    )

demo.launch()
