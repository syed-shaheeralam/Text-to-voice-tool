from TTS.api import TTS
import gradio as gr

model_name = "tts_models/multilingual/multi-dataset/xtts_v2"
tts = TTS(model_name)

def generate_voice(text, voice):
    output_path = "output.wav"
    tts.tts_to_file(
        text=text,
        speaker=voice,
        file_path=output_path
    )
    return output_path

voices = ["female-en-5", "male-en-2", "female-child", "old-man", "cinematic"]

ui = gr.Interface(
    fn=generate_voice,
    inputs=[
        gr.Textbox(label="Enter your text"),
        gr.Dropdown(voices, label="Select Voice")
    ],
    outputs=gr.Audio(label="Generated Voice"),
    title="Multi-Voice AI TTS",
    description="Choose a voice and generate clean high-quality speech."
)

ui.launch()
