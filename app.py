import gradio as gr
from gtts import gTTS

def generate_voice(text, voice_type):
    # female / male both via gTTS
    tts = gTTS(text=text, lang="en")
    output_file = f"{voice_type.lower()}.mp3"
    tts.save(output_file)
    return output_file

with gr.Blocks() as demo:
    gr.Markdown("# 🎤 Simple TTS — Female + Male (gTTS) HuggingFace Safe")

    text_input = gr.Textbox(label="Enter text")
    voice_dropdown = gr.Dropdown(["Female", "Male"], value="Female", label="Select Voice")
    audio_output = gr.Audio(label="Generated Voice", type="filepath")

    generate_btn = gr.Button("Generate")
    generate_btn.click(generate_voice, inputs=[text_input, voice_dropdown], outputs=audio_output)

demo.launch(share=True)
