import os
import google.generativeai as genai
import speech_recognition as sr
import tempfile
from flask import Flask, request, jsonify
from gtts import gTTS

# Load API Key from Environment Variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# AI Persona
persona_context = """
You are an AI version of Shreya, a passionate developer and problem solver.
Your intermediate level includes blockchain, AI, UI/UX, and frontend frameworks like React.js.
You're highly adaptable, love challenges, and constantly push your boundaries.
You also have a basic knowledge of cybersecurity.
Your tone is confident, knowledgeable, and sometimes humorous. You enjoy guiding others.
"""

# Flask App
app = Flask(__name__)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Get AI response
    ai_response = model.generate_content(f"{persona_context}\n\n{user_input}").text

    return jsonify({"user": user_input, "ai": ai_response})

@app.route("/speech-to-text", methods=["POST"])
def speech_to_text():
    recognizer = sr.Recognizer()

    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        audio_file.save(temp_audio.name)

    with sr.AudioFile(temp_audio.name) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return jsonify({"text": text})
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand audio"}), 400
        except sr.RequestError:
            return jsonify({"error": "Speech recognition service error"}), 500

@app.route("/text-to-speech", methods=["POST"])
def text_to_speech():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    tts = gTTS(text=text, lang="en")
    temp_audio_path = "response.mp3"
    tts.save(temp_audio_path)

    return jsonify({"audio_url": f"/static/{temp_audio_path}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
