import gradio as gr
from gtts import gTTS
from pydub import AudioSegment

def generate_voice(text, voice_type):
    output_file = f"{voice_type.lower()}.mp3"

    # Generate TTS via gTTS
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)

    # ---------- Voice Transformations ----------

    # Male: deeper, normal speed
    if voice_type.lower() == "male":
        sound = AudioSegment.from_file(output_file)
        octaves = -0.25
        new_sample_rate = int(sound.frame_rate * (2 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        sound = sound.set_frame_rate(44100)
        sound.export(output_file, format="mp3")

    # Female: default gTTS → natural
    # Kids: higher pitch, slightly faster
    if voice_type.lower() == "kids":
        sound = AudioSegment.from_file(output_file)
        octaves = 0.35
        new_sample_rate = int(sound.frame_rate * (2 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        # slightly faster for playful feel
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * 1.05)})
        sound = sound.set_frame_rate(44100)
        sound.export(output_file, format="mp3")

    # Old: deep, slightly slower → realistic elderly
    if voice_type.lower() == "old":
        sound = AudioSegment.from_file(output_file)
        octaves = -0.6
        new_sample_rate = int(sound.frame_rate * (2 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        sound = sound.set_frame_rate(44100)
        sound.export(output_file, format="mp3")

    # Cinematic: slightly deep, slightly faster → dramatic narrator
    if voice_type.lower() == "cinematic":
        sound = AudioSegment.from_file(output_file)
        octaves = -0.2
        new_sample_rate = int(sound.frame_rate * (2 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * 1.08)})
        sound = sound.set_frame_rate(44100)
        sound.export(output_file, format="mp3")

    # Cartoon: very high pitch, faster → playful / exaggerated
    if voice_type.lower() == "cartoon":
        sound = AudioSegment.from_file(output_file)
        octaves = 0.5
        new_sample_rate = int(sound.frame_rate * (2 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * 1.15)})
        sound = sound.set_frame_rate(44100)
        sound.export(output_file, format="mp3")

    # Robot: metallic, slightly deep, overlayed → electronic feel
    if voice_type.lower() == "robot":
        sound = AudioSegment.from_file(output_file)
        octaves = -0.15
        new_sample_rate = int(sound.frame_rate * (2 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        # overlay for metallic effect
        sound = sound.overlay(sound - 6)
        sound = sound.set_frame_rate(44100)
        sound.export(output_file, format="mp3")

    # Sci-Fi: futuristic, slightly high, modulated, slightly faster
    if voice_type.lower() == "sci-fi":
        sound = AudioSegment.from_file(output_file)
        octaves = 0.25
        new_sample_rate = int(sound.frame_rate * (2 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * 1.08)})
        sound = sound.set_frame_rate(44100)
        sound.export(output_file, format="mp3")

    return output_file

# ---------- Gradio UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🎤 HuggingFace TTS — Female, Male, Kids, Old, Cinematic, Cartoon, Robot + Sci-Fi")

    text_input = gr.Textbox(label="Enter text")
    voice_dropdown = gr.Dropdown(
        ["Female", "Male", "Kids", "Old", "Cinematic", "Cartoon", "Robot", "Sci-Fi"],
        value="Female", label="Select Voice"
    )
    audio_output = gr.Audio(label="Generated Voice", type="filepath")

    generate_btn = gr.Button("Generate")
    generate_btn.click(generate_voice, inputs=[text_input, voice_dropdown], outputs=audio_output)

# Launch app
# Use share=True locally for temporary public URL, remove on Hugging Face Spaces
demo.launch(share=True)
