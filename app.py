import gradio as gr
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import normalize

# ---------- Generate voice function ----------
def generate_voice(text, voice_type, clone_file):
    output_file = f"{voice_type.lower()}.mp3"

    # ---------- Clone voice ----------
    if voice_type.lower() == "clone" and clone_file is not None:
        try:
            from TTS.api import TTS

            # ✅ Correct voice cloning model
            tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)

            # Generate cloned voice
            tts.tts_to_file(text=text, speaker_wav=clone_file, file_path=output_file)
            return output_file
        except Exception as e:
            print("Error in clone generation:", e)
            return None  # Graceful failure

    # ---------- Generate TTS (Normal Voices) ----------
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
    elif voice_type.lower() == "kid":
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
        speed = 1.07
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

    # Add optional effects
    if voice_type.lower() == "robot":
        sound = sound.overlay(sound - 6)
    elif voice_type.lower() == "sci-fi":
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * 1.02)})
    elif voice_type.lower() in ["cinematic", "cartoon"]:
        sound = sound.fade_in(100).fade_out(100)

    # Normalize volume
    sound = normalize(sound)

    # Export final audio
    sound.export(output_file, format="mp3")
    return output_file

# ---------- Gradio UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🎤 Professional TTS — Female, Male, Kid, Old, Cinematic, Cartoon, Robot, Sci-Fi + Clone Your Voice")

    text_input = gr.Textbox(label="Enter text")

    voice_dropdown = gr.Dropdown(
        ["Female", "Male", "Kid", "Old", "Cinematic", "Cartoon", "Robot", "Sci-Fi", "Clone"],
        value="Female",
        label="Select Voice"
    )

    clone_audio = gr.Audio(
        label="Upload voice sample (5–10 sec)",
        type="filepath"
    )

    audio_output = gr.Audio(label="Generated Voice", type="filepath")

    generate_btn = gr.Button("Generate Voice")
    generate_btn.click(
        generate_voice,
        inputs=[text_input, voice_dropdown, clone_audio],
        outputs=audio_output
    )

demo.launch(share=True)
