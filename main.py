from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Load and check Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ GEMINI_API_KEY not loaded. Check your environment settings.")
else:
    print("✅ GEMINI_API_KEY loaded:", api_key[:6], "********")

# Configure Gemini
genai.configure(api_key=api_key)

# Create generative model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Initial system prompt and chat history
SYSTEM_PROMPT = (
    "You are a Science Experiment Recommender Chatbot. "
    "You provide science experiments based on user requests. "
    "Always remember previous interactions and continue conversations naturally. "
    "If a user asks an unrelated question, politely say that you only discuss science experiments. "
    "Give structured explanations with Aim, Equipment, Steps, and Precautions when needed."
)
chat_history = [SYSTEM_PROMPT]

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")
        print("🟢 Received message:", user_message)

        chat_history.append(f"User: {user_message}")
        response = model.generate_content("\n".join(chat_history) + "\nChatbot:")
        
        bot_response = response.text.strip()
        print("🟣 Bot Response:", bot_response)

        chat_history.append(f"Chatbot: {bot_response}")
        return jsonify({"response": bot_response})

    except Exception as e:
        print("❌ Error in /chat:", str(e))
        return jsonify({"response": "Oops! Something went wrong. Please try again."})

if __name__ == '__main__':
    app.run(debug=True)
