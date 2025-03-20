import google.generativeai as genai
import streamlit as st
import speech_recognition as sr
import tempfile
from gtts import gTTS
from streamlit_webrtc import webrtc_streamer, WebRtcMode, AudioProcessorBase
import av

# Configure API Key
genai.configure(api_key="YOUR_API_KEY")

# AI Persona
persona_context = """
You are an AI version of Shreya, a passionate developer and problem solver.
Your intermediate level includes blockchain, AI, UI/UX, and frontend frameworks like React.js.
You're highly adaptable, love challenges, and constantly push your boundaries.
You also have a basic knowledge of cybersecurity.
Your tone is confident, knowledgeable, and sometimes humorous. You enjoy guiding others.
"""

# AI Model
model = genai.GenerativeModel('gemini-1.5-pro-latest')

class AudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        try:
            text = self.recognizer.recognize_google(audio)
            st.session_state["user_input"] = text
        except sr.UnknownValueError:
            st.session_state["user_input"] = "Could not understand audio."
        except sr.RequestError:
            st.session_state["user_input"] = "Speech recognition service error."
        return frame
PORT = int(os.environ.get("PORT", 8501))  # Default to 8501 if no port is assigned
st.set_page_config(page_title="Live Mic AI Bot", page_icon="🎤")

st.write("# 🎙️ Live Microphone AI Chatbot")

st.write(f"Running on port {PORT} 🚀")

webrtc_ctx = webrtc_streamer(
    key="speech-to-text",
    mode=WebRtcMode.SENDRECV,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"video": False, "audio": True}
)

if "user_input" in st.session_state:
    user_input = st.session_state["user_input"]
    st.write(f"**You:** {user_input}")

    # Get AI response
    ai_response = model.generate_content(f"{persona_context}\n\n{user_input}").text
    st.write(f"**AI (You):** {ai_response}")

    # Convert AI response to speech
    tts = gTTS(text=ai_response, lang="en")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        st.audio(temp_audio.name, format="audio/mp3")

