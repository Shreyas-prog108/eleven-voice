import streamlit as st
import requests
import base64
from dotenv import load_dotenv
import os
# ==========================
# CONFIG - replace with your values
# ==========================
load_dotenv()
API_KEY=os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

# ==========================
# STREAMLIT UI
# ==========================
st.set_page_config(page_title="Voice Narrator", page_icon="🎤")
st.title("🎤 Shreyas's Voice Narrator App")
st.write("Enter a script below and hear it narrated in Shreyas's cloned voice.")

# Text input
text_input = st.text_area("Enter your script:", height=200)
if st.button("Generate Voice"):
    if not text_input.strip():
        st.warning("⚠️ Please enter some text first.")
    else:
        with st.spinner("Generating voice..."):
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": API_KEY
            }
            data = {
                "text": text_input,
                "voice_settings": {
                    "stability": 0.7,
                    "similarity_boost": 0.90
                }
            }
            response = requests.post(API_URL, headers=headers, json=data)
            if response.status_code == 200:
                audio_file = "output.mp3"
                with open(audio_file, "wb") as f:
                    f.write(response.content)

                st.success("✅ Voice generated successfully!")
                st.audio(audio_file, format="audio/mp3")
                b64 = base64.b64encode(response.content).decode()
                href = f'<a href="data:audio/mp3;base64,{b64}" download="narration.mp3">⬇️ Download MP3</a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.error(f"❌ Error: {response.text}")
