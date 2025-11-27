import gradio as gr
from gtts import gTTS
from pydub import AudioSegment

def generate_voice(text, voice_type):
    output_file = f"{voice_type.lower()}.mp3"

    # Generate TTS via gTTS
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)

    # Male voice: deeper pitch, normal speed
    if voice_type.lower() == "male":
        sound = AudioSegment.from_file(output_file)
        # Lower pitch only without slowing speed
        octaves = -0.25  # negative → deeper
        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        sound = sound.set_frame_rate(44100)  # keep normal speed
        sound.export(output_file, format="mp3")

    return output_file

# ---------- Gradio UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🎤 HuggingFace TTS — Female + Male (Deeper, Normal Speed)")

    text_input = gr.Textbox(label="Enter text")
    voice_dropdown = gr.Dropdown(["Female", "Male"], value="Female", label="Select Voice")
    audio_output = gr.Audio(label="Generated Voice", type="filepath")

    generate_btn = gr.Button("Generate")
    generate_btn.click(generate_voice, inputs=[text_input, voice_dropdown], outputs=audio_output)

# Launch app with public link for multiple users
demo.launch(share=True)
