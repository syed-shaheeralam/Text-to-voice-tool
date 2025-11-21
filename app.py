import gradio as gr
from TTS.api import TTS

# -------------------------
# FIXED – SUPER ACCURATE VOICES
# -------------------------
VOICE_MODELS = {
    "XTTS v2 Female (Best Urdu+English)": "tts_models/multilingual/multi-dataset/xtts_v2",
    "XTTS v1 Multilingual (Stable)": "tts_models/multilingual/multi-dataset/xtts",
    "English Female – WaveGlow (Super Clear)": "tts_models/en/ljspeech/tacotron2-DDC_ph"
}

# Cache models so HF Space doesn't reload them for every user
loaded_tts = {}

def load_model(model_name):
    if model_name not in loaded_tts:
        loaded_tts[model_name] = TTS(model_name=model_name, gpu=False)
    return loaded_tts[model_name]


def generate_voice(text, voice_selection):
    model_name = VOICE_MODELS[voice_selection]
    tts = load_model(model_name)

    output_path = "output.wav"
    tts.tts_to_file(
        text=text,
        file_path=output_path
    )
    return output_path


# -------------------------
# GRADIO UI
# -------------------------
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
    description="Multiple voice selection, supports Urdu + English, 100% HuggingFace compatible."
)

ui.launch()
