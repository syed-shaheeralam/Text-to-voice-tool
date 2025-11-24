from TTS.api import TTS
import gradio as gr

model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(model_name)

# Only valid XTTS speakers
voices = [
    "female-en-5",
    "male-en-2",
    "female-en-1",
    "female-en-2",
    "female-en-3",
    "female-en-4",
    "male-en-1",
    "male-en-3",
    "male-en-4"
]

def generate_voice(text, voice):
    output_path = "output.wav"
    tts.tts_to_file(
        text=text,
        speaker=voice,
        language="en",
        file_path=output_path
    )
    return output_path

ui = gr.Interface(
    fn=generate_voice,
    inputs=[
        gr.Textbox(label="Enter your text"),
        gr.Dropdown(voices, label="Select Voice")
    ],
    outputs=gr.Audio(label="Generated Voice"),
    title="Clean Multi-Voice TTS",
    description="Choose a voice and generate clear, noise-free speech."
)

ui.launch()
