import gradio as gr
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import normalize

# For voice cloning (NEW)
from TTS.api import TTS
import tempfile


# -------------------- YOUR ORIGINAL FUNCTION (UNCHANGED) --------------------
def generate_voice(text, voice_type):
    output_file = f"{voice_type.lower()}.mp3"

    tts = gTTS(text=text, lang="en")
    tts.save(output_file)

    sound = AudioSegment.from_file(output_file)

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

    new_sample_rate = int(sound.frame_rate * (2 ** octaves))
    sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sample_rate})
    sound = sound.set_frame_rate(44100)

    if speed != 1.0:
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * speed)})
        sound = sound.set_frame_rate(44100)

    if voice_type.lower() == "robot":
        sound = sound.overlay(sound - 6)
    elif voice_type.lower() == "sci-fi":
        sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * 1.02)})
    elif voice_type.lower() in ["cinematic", "cartoon"]:
        sound = sound.fade_in(100).fade_out(100)

    sound = normalize(sound)
    sound.export(output_file, format="mp3")
    return output_file


# -------------------- NEW: VOICE CLONING FUNCTION --------------------
def clone_voice(text, input_audio):
    if input_audio is None:
        return None

    temp_dir = tempfile.mkdtemp()
    input_path = f"{temp_dir}/input.wav"
    output_path = f"{temp_dir}/cloned.wav"

    input_audio.save(input_path)

    # Load XTTS model
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

    # Generate cloned voice
    tts.tts_to_file(
        text=text,
        speaker_wav=input_path,
        language="en",
        file_path=output_path
    )

    return output_path


# -------------------- GRADIO UI --------------------
with gr.Blocks() as demo:

    gr.Markdown("# 🎤 AI Voice Suite — TTS + Voice Cloning")

    with gr.Tabs():

        # TAB 1 — Your ORIGINAL voices (unchanged)
        with gr.TabItem("🎙️ Normal Voices"):
            text_input = gr.Textbox(label="Enter text")
            voice_dropdown = gr.Dropdown(
                ["Female", "Male", "Kid", "Old", "Cinematic", "Cartoon", "Robot", "Sci-Fi"],
                value="Female", label="Select Voice"
            )
            audio_output = gr.Audio(label="Generated Voice", type="filepath")
            generate_btn = gr.Button("Generate")
            generate_btn.click(generate_voice, [text_input, voice_dropdown], audio_output)

        # TAB 2 — NEW Voice Cloning
        with gr.TabItem("🧬 Voice Cloning (XTTS v2)"):
            clone_text = gr.Textbox(label="Enter text to speak")
            clone_audio = gr.Audio(label="Upload voice sample (5–10 sec)", type="file")
            clone_output = gr.Audio(label="Cloned Voice", type="filepath")
            clone_btn = gr.Button("Clone Voice")
            clone_btn.click(clone_voice, [clone_text, clone_audio], clone_output)


demo.launch(share=True)
