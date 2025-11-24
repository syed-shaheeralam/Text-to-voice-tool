import os
from TTS.api import TTS
import gradio as gr

# Load model ONLY once at startup
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")

def generate_voice(text):
    # Save file inside workspace
    output_path = "output.wav"

    # Prevent Empty text crash
    if not text or text.strip() == "":
        return None

    # Generate voice file
    tts.tts_to_file(text=text, file_path=output_path)

    return output_path

# Build clean UI
ui = gr.Interface(
    fn=generate_voice,
    inputs=gr.Textbox(label="Enter text", placeholder="Type something..."),
    outputs=gr.Audio(label="Generated Voice"),
    title="AI Voice Generator (Stable)",
    description="Fast & stable text-to-speech powered by Coqui TTS."
)

# Launch with correct settings for HuggingFace
ui.launch(server_name="0.0.0.0", server_port=7860)
