import gradio as gr
from gtts import gTTS
import pyttsx3
from pydub import AudioSegment

# ---------- FEMALE VOICE ----------
def female_voice(text):
    tts = gTTS(text=text, lang="en")
    tts.save("female.mp3")
    return "female.mp3"

# ---------- MALE VOICE ----------
def male_voice(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    # Pick first male voice
    for v in voices:
        if "male" in v.name.lower() or "en-us" in v.id.lower():
            engine.setProperty('voice', v.id)
            break

    engine.setProperty('rate', 150)
    engine.save_to_file(text, "male.wav")
    engine.runAndWait()

    sound = AudioSegment.from_wav("male.wav")
    sound.export("male.mp3", format="mp3")
    return "male.mp3"

# ---------- MAIN FUNCTION ----------
def generate(text, voice_type):
    if voice_type == "Female":
        return female_voice(text)
    else:
        return male_voice(text)

# ---------- GRADIO UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🎤 Simple TTS — Female (gTTS) + Male (pyttsx3)")

    text_input = gr.Textbox(label="Enter text")
    voice_dropdown = gr.Dropdown(["Female", "Male"], value="Female", label="Select Voice")
    audio_output = gr.Audio(label="Generated Voice", type="filepath")

    generate_btn = gr.Button("Generate")
    generate_btn.click(fn=generate, inputs=[text_input, voice_dropdown], outputs=audio_output)

demo.launch()
