import gradio as gr
from TTS.api import TTS
import os

VOICE_MODELS = {
    "XTTS v2 Female (Best Urdu+English)": "tts_models/multilingual/multi-dataset/xtts_v2",
    "XTTS v1 Multilingual (Stable)": "tts_models/multilingual/multi-dataset/xtts",
    "English Female – WaveGlow": "tts_models/en/ljspeech/tacotron2-DDC_ph"
}

loaded_tts = {}

def load_model(model_name):
    if model_name not in loaded_tts:
        loaded_tts[model_name] = TTS(
            model_name=model_name,
            gpu=False,
            progress_bar=False
        )
    return loaded_tts[model_name]


def generate_voice(text, voice_selection):
    model_name = VOICE_MODELS[voice_selection]
    tts = load_model(model_name)

    output_path = "output.wav"

    # FIX 1: prevent overwrite crash
    if os.path.exists(output_path):
        os.remove(output_path)

    # FIX 2: HF Spaces CPU crash fix
    audio = tts.tts(text=text)

    # FIX 3: manually save audio
    import soundfile as sf
    sf.write(output_path, audio, 22050)

    return output_path


ui = gr.Interface(
    fn=generate_voice,
    inputs=[
        gr.Textbox(lines=3, label="Enter text"),
        gr.Dropdown(
            label="Choose Voice",
            choices=list(VOICE_MODELS.keys()),
            value="XTTS v2 Female (Best Urdu+English)"
        )
    ],
    outputs=gr.Audio(type="filepath", label="Generated Voice"),
    title="Ultra-Stable Multi-Voice TTS (SAE)",
    description="Multiple voices, Urdu + English, multi-user support."
)

ui.launch()
