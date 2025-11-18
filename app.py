import gradio as gr
import torch
from TTS.api import TTS

tts = TTS("tts_models/en/ljspeech/glow-tts").to("cpu")

voices = {
    "Female": "ljspeech",
    "Kids voice": "random-kid",
    "Old man": "random-old",
    "Cinematic": "random-cinematic"
}

def synthesize(text, voice):
    wav = tts.tts(text=text, speaker=voices.get(voice, "ljspeech"))
    file = "output.wav"
    tts.save_wav(wav, file)
    return file

app = gr.Interface(
    fn=synthesize,
    inputs=[
        gr.Textbox(label="Enter text here"),
        gr.Dropdown(list(voices.keys()), label="Choose Voice")
    ],
    outputs=gr.Audio(label="Generated Audio")
)

app.launch()
