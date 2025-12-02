import gradio as gr
from gtts import gTTS
from pydub import AudioSegment
from pydub.effects import normalize
import os
import uuid

# ---------- Generate voice ----------

def generate_voice(text, voice_type, clone_file):
output_file = f"{uuid.uuid4()}.mp3"
output_path = os.path.abspath(output_file)

```
# ---------- Clone voice ----------
if voice_type.lower() == "clone" and clone_file is not None:
    try:
        from TTS.api import TTS

        # FIXED: No espeak required
        tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")

        # Convert to WAV if needed
        if not clone_file.lower().endswith(".wav"):
            temp_wav = f"{uuid.uuid4()}.wav"
            sound = AudioSegment.from_file(clone_file)
            sound.export(temp_wav, format="wav")
            clone_file = temp_wav

        # Generate cloned audio
        tts.tts_to_file(text=text, speaker_wav=clone_file, file_path=output_path)

        if os.path.exists(output_path):
            return output_path
        else:
            print("Clone file not created")
            return None

    except Exception as e:
        print("Clone Error:", e)
        return None

# ---------- Normal Voices ----------
tts = gTTS(text=text, lang="en")
tts.save(output_path)

sound = AudioSegment.from_file(output_path)

# ---------- Voice Effects ----------
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

# Pitch
new_sr = int(sound.frame_rate * (2 ** octaves))
sound = sound._spawn(sound.raw_data, overrides={'frame_rate': new_sr})
sound = sound.set_frame_rate(44100)

# Speed
if speed != 1.0:
    sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * speed)})
    sound = sound.set_frame_rate(44100)

# Effects
if voice_type.lower() == "robot":
    sound = sound.overlay(sound - 6)
elif voice_type.lower() == "sci-fi":
    sound = sound._spawn(sound.raw_data, overrides={'frame_rate': int(sound.frame_rate * 1.02)})
elif voice_type.lower() in ["cinematic", "cartoon"]:
    sound = sound.fade_in(100).fade_out(100)

# Volume normalize
sound = normalize(sound)

sound.export(output_path, format="mp3")
return output_path
```

# ---------- UI ----------

with gr.Blocks() as demo:
gr.Markdown("# 🎤 AI Voice Generator — 8 Styles + Voice Cloning (Fully Fixed)")

```
text_input = gr.Textbox(label="Enter text")

voice_dropdown = gr.Dropdown(
    ["Female", "Male", "Kid", "Old", "Cinematic", "Cartoon", "Robot", "Sci-Fi", "Clone"],
    value="Female",
    label="Select Voice"
)

clone_audio = gr.Audio(
    label="Upload Voice Sample (5–10 sec, WAV preferred)",
    type="filepath"
)

audio_output = gr.Audio(label="Generated Audio", type="filepath")

generate_btn = gr.Button("Generate Voice")
generate_btn.click(
    generate_voice,
    inputs=[text_input, voice_dropdown, clone_audio],
    outputs=audio_output
)
```

demo.launch()
