from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Create model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# System prompt for science experiment recommender
SYSTEM_PROMPT = (
    "You are a Science Experiment Recommender Chatbot. "
    "You provide science experiments based on user requests. "
    "Always remember previous interactions and continue conversations naturally. "
    "If a user asks an unrelated question, politely say that you only discuss science experiments. "
    "Give structured explanations with Aim, Equipment, Steps, and Precautions when needed."
)

# Start a persistent Gemini chat session
chat = model.start_chat(history=[{"role": "user", "parts": [SYSTEM_PROMPT]}])

# Serve the frontend
@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

# Chat endpoint
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "Please enter a valid question."})

    # Send user message to Gemini chat
    response = chat.send_message(user_message)
    bot_response = response.text.strip()

    return jsonify({"response": bot_response})

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
