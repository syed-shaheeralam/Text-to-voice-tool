import gradio as gr
from TTS.api import TTS

# -------------------------
# SUPER-STABLE VOICES
# -------------------------
VOICE_MODELS = {
    "English Female (LJSpeech-DDC)": "tts_models/en/ljspeech/tacotron2-DDC",
    "English Fast (SpeedySpeech)": "tts_models/en/ljspeech/speedy-speech",
    "Multilingual Female (YourTTS – Urdu/English)": "tts_models/multilingual/multi-dataset/your_tts",
    "Premium Multilingual XTTS V2 (Male/Female)": "tts_models/multilingual/multi-dataset/xtts_v2",
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
            value="English Female (LJSpeech-DDC)"
        )
    ],
    outputs=gr.Audio(type="filepath", label="Generated Voice"),
    title="Ultra-Stable Multi-Voice TTS (SAE)",
    description="Multiple voice selection, supports Urdu + English, 100% HuggingFace compatible."
)

ui.launch()
