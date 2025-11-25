from TTS.api import TTS
import gradio as gr

# AVAILABLE MODELS DICTIONARY
VOICE_MODELS = {
    "Kids Voice": "tts_models/en/vctk/vits",           # kid-like, lightweight
    "Boy / Male Voice": "tts_models/en/vctk/vits",
    "Girl / Female Voice": "tts_models/en/ljspeech/tacotron2-DDC",
    "Old Man Voice": "tts_models/en/vctk/vits",
    "Old Woman Voice": "tts_models/en/ljspeech/tacotron2-DDC",
    "Cinematic Deep Voice": "tts_models/en/vctk/vits"
}

def generate_voice(text, voice_choice):
    # load model based on dropdown choice
    model_name = VOICE_MODELS[voice_choice]
    tts = TTS(model_name)

    output_path = "output.wav"
    tts.tts_to_file(text=text, file_path=output_path)
    return output_path

ui = gr.Interface(
    fn=generate_voice,
    inputs=[
        gr.Textbox(label="Enter Text"),
        gr.Dropdown(
            choices=list(VOICE_MODELS.keys()),
            value="Girl / Female Voice",
            label="Select Voice"
        )
    ],
    outputs=gr.Audio(label="Generated Voice"),
    title="AI Multi-Voice Generator",
    description="Choose Kids, Male, Female, Old or Cinematic voice and generate speech."
)

ui.launch()
