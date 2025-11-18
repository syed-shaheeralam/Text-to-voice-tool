import gradio as gr
from bark import SAMPLE_RATE, generate_audio
import scipy.io.wavfile as wav
import os

# Predefined Bark speaker voices
voices = {
    "Female": "v2/en_speaker_6",
    "Male": "v2/en_speaker_1",
    "Old Man": "v2/en_speaker_9",
    "Kid": "v2/en_speaker_5",
    "Cinematic": "v2/en_speaker_8"
}

def tts_generate(text, voice):
    try:
        if not text.strip():
            return "Error: Please enter some text."
        audio = generate_audio(text, history_prompt=voices[voice])
        filename = os.path.join(os.getcwd(), "output.wav")
        wav.write(filename, SAMPLE_RATE, audio)
        return filename
    except Exception as e:
        return f"Error: {e}"

app = gr.Interface(
    fn=tts_generate,
    inputs=[
        gr.Textbox(lines=4, placeholder="Type text here...", label="Enter Text"),
        gr.Dropdown(list(voices.keys()), label="Choose Voice")
    ],
    outputs=gr.Audio(type="filepath", label="Generated Audio"),
    title="Unlimited Voiceover Tool",
    description="CPU-friendly, multiple voices simulated, play and download audio."
)

app.launch()
