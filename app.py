import gradio as gr
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import normalize

def generate_voice(text, voice_type):
    output_file = f"{voice_type.lower()}.mp3"

    # ---------- Generate TTS ----------
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)

    sound = AudioSegment.from_file(output_file)

    # ---------- Voice Transformations ----------
    if voice_type.lower() == "male":
        octaves = -0.25
        speed = 1.0
    elif voice_type.lower() == "female":
        octaves = 0.0
        speed = 1.0
    elif voice_type.lower() == "kids":
        octaves = 0.35
        speed = 1.05
    elif voice_type.lower() == "old":
        octaves = -0.6
        speed = 0.95
    elif voice_type.lower() == "cinematic":
        octaves = -0.2
        speed = 1.08
    elif voice_type.lower() == "cartoon":
        octaves = 0.5
        speed = 1.07   # ← ONLY THIS LINE CHANGED (speed reduced)
    elif voice_type.lower() == "robot":
        octaves = -0.15
        speed = 1.0
    elif voice_type.lower() == "sci-fi":
        octaves = 0.25
        speed = 1.08
    else:
        octaves = 0.0
        speed = 1.0

    # Change pitch
    new_sample_rate = int(sound.frame_rate * (2 ** octaves))
    sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    sound = sound.set_frame_rate(44100)

    # Adjust speed
    if speed != 1.0:
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * speed)})
        sound = sound.set_frame_rate(44100)

    # Add optional voice effects
    if voice_type.lower() == "robot":
        sound = sound.overlay(sound - 6)
    elif voice_type.lower() == "sci-fi":
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * 1.02)})
    elif voice_type.lower() in ["cinematic", "cartoon"]:
        sound = sound.fade_in(100).fade_out(100)

    # Normalize volume
    sound = normalize(sound)

    # Export final voice
    sound.export(output_file, format="mp3")
    return output_file

# ---------- Gradio UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🎤 Professional TTS — Female, Male, Kids, Old, Cinematic, Cartoon, Robot + Sci-Fi")

    text_input = gr.Textbox(label="Enter text")
    voice_dropdown = gr.Dropdown(
        ["Female", "Male", "Kids", "Old", "Cinematic", "Cartoon", "Robot", "Sci-Fi"],
        value="Female", label="Select Voice"
    )
    audio_output = gr.Audio(label="Generated Voice", type="filepath")

    generate_btn = gr.Button("Generate")
    generate_btn.click(generate_voice, inputs=[text_input, voice_dropdown], outputs=audio_output)

demo.launch(share=True)
