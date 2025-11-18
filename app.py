import gradio as gr
from bark import SAMPLE_RATE, generate_audio
import scipy.io.wavfile as wav

voices = {
    "Female": "v2/en_speaker_6",
    "Male": "v2/en_speaker_1",
    "Old Man": "v2/en_speaker_9",
    "Kid": "v2/en_speaker_5",
    "Cinematic": "v2/en_speaker_8"
}

def tts_generate(text, voice):
    audio = generate_audio(text, history_prompt=voice)
    filename = "output.wav"
    wav.write(filename, SAMPLE_RATE, audio)
    return filename

app = gr.Interface(
    fn=tts_generate,
    inputs=[
        gr.Textbox(label="Enter Text"),
        gr.Dropdown(list(voices.keys()), label="Choose Voice")
    ],
    outputs=gr.Audio(label="Generated Audio"),
    title="Unlimited Voiceover Tool"
)

app.launch()
