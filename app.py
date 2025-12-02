import gradio as gr
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import normalize
import os
import uuid
import espeakng   # FIX: HuggingFace Clone Voice ERROR Solved

# ---------- Generate voice function ----------
def generate_voice(text, voice_type, clone_file):
    # Unique filename per request to avoid conflicts
    output_file = f"{uuid.uuid4()}.mp3"
    output_path = os.path.abspath(output_file)

    # ---------- Clone voice ----------
    if voice_type.lower() == "clone" and clone_file is not None:
        try:
            from TTS.api import TTS

            # Load Coqui model
            tts = TTS(model_name="tts_models/en/vctk/vits", progress_bar=False, gpu=False)

            # Ensure WAV input
            if not clone_file.lower().endswith(".wav"):
                temp_wav = f"{uuid.uuid4()}.wav"
                sound = AudioSegment.from_file(clone_file)
                sound.export(temp_wav, format="wav")
                clone_file = temp_wav

            # Generate cloned voice
            tts.tts_to_file(text=text, speaker_wav=clone_file, file_path=output_path)

            if os.path.exists(output_path):
                return output_path
            else:
                print("Error: cloned file not created")
                return None

        except Exception as e:
            print("Error in clone generation:", e)
            return None

    # ---------- Generate TTS (Normal Voices) ----------
    tts = gTTS(text=text, lang="en")
    tts.save(output_path)

    sound = AudioSegment.from_file(output_path)

    # ---------- Voice Transformations ----------
    voice_settings = {
        "male": (-0.25, 1.0),
        "female": (0.0, 1.0),
        "kid": (0.35, 1.05),
        "old": (-0.6, 0.95),
        "cinematic": (-0.2, 1.08),
        "cartoon": (0.5, 1.07),
        "robot": (-0.15, 1.0),
        "sci-fi": (0.25, 1.08)
    }
    octaves, speed = voice_settings.get(voice_type.lower(), (0.0, 1.0))

    # Change pitch
    new_sample_rate = int(sound.frame_rate * (2 ** octaves))
    sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    sound = sound.set_frame_rate(44100)

    # Adjust speed
    if speed != 1.0:
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * speed)})
        sound = sound.set_frame_rate(44100)

    # Optional effects
    if voice_type.lower() == "robot":
        sound = sound.overlay(sound - 6)
    elif voice_type.lower() == "sci-fi":
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * 1.02)})
    elif voice_type.lower() in ["cinematic", "cartoon"]:
        sound = sound.fade_in(100).fade_out(100)

    # Normalize
    sound = normalize(sound)

    # Export final audio
    sound.export(output_path, format="mp3")
    return output_path


# ---------- Gradio UI ----------
with gr.Blocks() as demo:
    gr.Markdown("# 🎤 Professional TTS — Multiple Voices + Voice Cloning")

    text_input = gr.Textbox(label="Enter text")

    voice_dropdown = gr.Dropdown(
        ["Female", "Male", "Kid", "Old", "Cinematic", "Cartoon", "Robot", "Sci-Fi", "Clone"],
        value="Female",
        label="Select Voice"
    )

    clone_audio = gr.Audio(
        label="Upload voice sample (5–10 sec, .wav preferred)",
        type="filepath"
    )

    audio_output = gr.Audio(label="Generated Voice", type="filepath")

    generate_btn = gr.Button("Generate Voice")
    generate_btn.click(
        generate_voice,
        inputs=[text_input, voice_dropdown, clone_audio],
        outputs=audio_output
    )

demo.launch()
