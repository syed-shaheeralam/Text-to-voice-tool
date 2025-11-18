import gradio as gr
import os
from TTS.api import TTS

# Load lightweight multi-speaker CPU-friendly model
tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)

# Voices available in model
voices = {
    "Female": "p273",
    "Male": "p225",
    "Kid": "p274",
    "Old": "p226",
    "Cinematic": "p272"
}

def tts_generate(text, voice):
    try:
        if not text.strip():
            return "Error: Please enter some text."
        filename = os.path.join(os.getcwd(), "output.wav")
        tts.tts_to_file(text=text, speaker=voices[voice], file_path=filename)
        return filename
    except Exception as e:
        return f"Error: {e}"

app = gr.Interface(
    fn=tts_generate,
    inputs=[
        gr.Textbox(lines=4, placeholder="Type your text here...", label="Enter Text"),
        gr.Dropdown(list(voices.keys()), label="Choose Voice")
    ],
    outputs=gr.Audio(type="filepath", label="Generated Audio"),
    title="Unlimited Voiceover Tool",
    description="Enter text and get audio output. Play and download. Multiple voices supported."
)

app.launch()
