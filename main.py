from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
import os
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro-latest")

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
    data = request.get_json()
    user_message = data.get("message", "")
    chat_history.append(f"User: {user_message}")
    response = model.generate_content("\n".join(chat_history) + "\nChatbot:")
    bot_response = response.text.strip()
    chat_history.append(f"Chatbot: {bot_response}")
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
    app.run(debug=True)
