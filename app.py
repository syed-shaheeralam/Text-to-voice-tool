import gradio as gr
from TTS.api import TTS

# Load TTS model once (CPU for Hugging Face Spaces)
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

def generate_voice(text):
    out_file = "output.wav"
    tts.tts_to_file(text=text, file_path=out_file)
    return out_file

iface = gr.Interface(
    fn=generate_voice,
    inputs=gr.Textbox(lines=3, placeholder="Type your text here..."),
    outputs=gr.Audio(type="file")
)

iface.launch()
