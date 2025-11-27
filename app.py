import gradio as gr
from gtts import gTTS
from pydub import AudioSegment

def generate_voice(text, voice_type):
    output_file = f"{voice_type.lower()}.mp3"

    # Generate TTS via gTTS
    tts = gTTS(text=text, lang="en")
    tts.save(output_file)

    # Male voice: deeper pitch
    if voice_type.lower() == "male":
        sound = AudioSegment.from_file(output_file)
        octaves = -0.25
        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        sound = sound.set_frame_rate(44100)
        sound.export(output_file, format="mp3")

    # Kids voice: higher pitch
    if voice_type.lower() == "kid":
        sound = AudioSegment.from_file(output_file)
        octaves = 0.25
        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        sound = sound.set_frame_rate(44100)
        sound.export(output_file, format="mp3")

    # Old voice: realistic elderly
    if voice_type.lower() == "old":
        sound = AudioSegment.from_file(output_file)
        octaves = -0.45  # deeper → realistic elderly
        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        sound = sound.set_frame_rate(44100)
        sound.export(output_file, format="mp3")

    # Cinematic / Narrator voice
    if voice_type.lower() == "cinematic":
        sound = AudioSegment.from_file(output_file)
        octaves = -0.2  # slightly deep
        new_sample_rate = int(sound.frame_rate * (2.0 ** octaves))
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
        # Slightly slower for dramatic effect
        sound = sound.speedup(playback_speed=0.9)
        sound = sound.set_frame_rate(44100)
        sound.export(output_file, format="mp3")

    return output_file

# ---------- Gradio UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🎤 HuggingFace TTS — Female, Male, Kids, Realistic Old + Cinematic Voice")

    text_input = gr.Textbox(label="Enter text")
    voice_dropdown = gr.Dropdown(["Female", "Male", "Kid", "Old", "Cinematic"], value="Female", label="Select Voice")
    audio_output = gr.Audio(label="Generated Voice", type="filepath")

    generate_btn = gr.Button("Generate")
    generate_btn.click(generate_voice, inputs=[text_input, voice_dropdown], outputs=audio_output)

# Launch app with public link for multiple users
demo.launch(share=True)
