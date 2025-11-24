from TTS.api import TTS
import gradio as gr

# Load model (best model for HuggingFace)
tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")

def generate_voice(text):
    output_path = "output.wav"
    tts.tts_to_file(text=text, file_path=output_path)
    return output_path

ui = gr.Interface(
    fn=generate_voice,
    inputs=gr.Textbox(label="Type your text here"),
    outputs=gr.Audio(label="Generated Voice"),
    title="AI Voice Generator",
    description="Enter text and get high-quality speech."
)

ui.launch()
