import gradio as gr
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import normalize
import uuid

def generate_voice(text, voice_type):
    output_file = f"{uuid.uuid4()}.mp3"   # <- properly indented

    # Generate TTS
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)

    # Load audio
    sound = AudioSegment.from_file(output_file)

    # Voice Transformations
    if voice_type.lower() == "male":
        octaves = -0.3
        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={"frame_rate": new_sample_rate})
        sound = sound.set_frame_rate(44100)

    elif voice_type.lower() == "female":
        octaves = 0.3
        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={"frame_rate": new_sample_rate})
        sound = sound.set_frame_rate(44100)

    # Normalize volume
    sound = normalize(sound)

    # Save output
    sound.export(output_file, format="mp3")

    return output_file

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## Voice Generator")
    text = gr.Textbox(label="Enter Text")
    voice_type = gr.Dropdown(["Male", "Female"], label="Voice Type")
    output = gr.Audio(label="Generated Voice")

    btn = gr.Button("Generate Voice")
    btn.click(generate_voice, inputs=[text, voice_type], outputs=[output])

demo.launch()
