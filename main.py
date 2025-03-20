import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import tempfile
import streamlit as st
import os

genai.configure(api_key="AIzaSyAbb6m2hUULstNAyQ4a_loO-JyuSY49XhQ")

persona_context = """
Dont mention in the response that you are AI.Just behave like you are shreya.
You are an AI version of Shreya, a passionate developer and problem solver.
Your intermediate level includes blockchain, AI, UI/UX, and frontend frameworks like React.js.
You're highly adaptable, love challenges, and constantly push your boundaries.
You also have a basic knowledge of cybersecurity.
Your tone is confident, knowledgeable, and sometimes humorous. You enjoy guiding others.
"""

model = genai.GenerativeModel('gemini-1.5-pro-latest')

def speak_text(text):
    """Generate speech using gTTS and return the file path."""
    if not text.strip():
        return None 

    tts = gTTS(text=text, lang='en')
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        audio_path = temp_audio.name
        tts.save(audio_path)  

    return audio_path  

def recognize_speech():
    """Recognize speech using Google Speech API."""
    rec = sr.Recognizer()
    mic = sr.Microphone()
    
    rec.dynamic_energy_threshold = False
    rec.energy_threshold = 400    

    with mic as source:
        rec.adjust_for_ambient_noise(source, duration=0.5)
        st.write("Listening... 🎤")

        try:
            audio = rec.listen(source, timeout=10, phrase_time_limit=15)
            text = rec.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Hmm... I didn't catch that. Try again!"
        except sr.RequestError:
            return "Speech recognition service is down."
        except Exception:
            return "Oops, something went wrong with speech recognition."

def get_ai_response(request):
    """Get AI response in Shreya's persona."""
    full_request = f"{persona_context}\n\n{request}"  

    response = model.generate_content(full_request)
    full_response = response.text.strip()

    return full_response


st.title("🎙️ Voice AI Chatbot")

if st.button("🎤 Speak"):
    user_input = recognize_speech()

    if user_input:
        st.write(f"**You:** {user_input}")

        ai_response = get_ai_response(user_input)
        st.write(f"**Shreya:** {ai_response}")

        audio_path = speak_text(ai_response)

        if audio_path and os.path.exists(audio_path):
            with open(audio_path, "rb") as audio_file:
                st.audio(audio_file, format="audio/mp3")  
        else:
            st.error("Failed to generate audio. Please try again.")
