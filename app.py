import gradio as gr
from TTS.api import TTS

# Load lightweight CPU-friendly TTS model
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")  # CPU compatible

# Dropdown UI voices (single speaker model, just for UI)
voices = {
    "Female": None,
    "Male": None
}

def tts_generate(text, voice):
    try:
        if not text.strip():
            return "Error: Please enter some text."
        filename = "output.wav"
        tts.tts_to_file(text=text, file_path=filename)
        return filename
    except Exception as e:
        return f"Error: {e}"

app = gr.Interface(
    fn=tts_generate,
    inputs=[
        gr.Textbox(lines=4, placeholder="Enter your text here...", label="Enter Text"),
        gr.Dropdown(list(voices.keys()), label="Choose Voice")
    ],
    outputs=gr.Audio(type="filepath", label="Generated Audio"),  # <-- fixed
    title="Unlimited Voiceover Tool",
    description="Enter text and get audio output. Play and download the audio easily."
)

app.launch()
