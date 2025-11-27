import gradio as gr
from gtts import gTTS
from pydub import AudioSegment

def generate_voice(text, voice_type):
    output_file = f"{voice_type.lower()}.mp3"

    # gTTS generate
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)

    # Male voice deeper
    if voice_type.lower() == "male":
        sound = AudioSegment.from_file(output_file)
        # extra deep: slow down more (0.7x)
        sound = sound._spawn(sound.raw_data, overrides={
            "frame_rate": int(sound.frame_rate * 0.7)
        }).set_frame_rate(sound.frame_rate)
        sound.export(output_file, format="mp3")

    return output_file

# ---------- Gradio UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🎤 HuggingFace TTS — Female + Extra Deep Male")

    text_input = gr.Textbox(label="Enter text")
    voice_dropdown = gr.Dropdown(["Female", "Male"], value="Female", label="Select Voice")
    audio_output = gr.Audio(label="Generated Voice", type="filepath")

    generate_btn = gr.Button("Generate")
    generate_btn.click(generate_voice, inputs=[text_input, voice_dropdown], outputs=audio_output)

demo.launch(share=True)
