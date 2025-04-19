from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
import os

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Check if API key is loaded properly
if not api_key:
    raise ValueError("⚠️ GEMINI_API_KEY not found in .env file.")

# Configure Gemini API
genai.configure(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all origins

# Initialize Gemini model
model = genai.GenerativeModel("gemini-1.5-pro-latest")

# Initial system prompt
SYSTEM_PROMPT = (
    "You are a Science Experiment Recommender Chatbot. "
    "You provide science experiments based on user requests. "
    "Always remember previous interactions and continue conversations naturally. "
    "If a user asks an unrelated question, politely say that you only discuss science experiments. "
    "Give structured explanations with Aim, Equipment, Steps, and Precautions when needed."
)

# Chat history to maintain context
chat_history = [SYSTEM_PROMPT]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    # Append user input to chat history
    chat_history.append(f"User: {user_message}")

    # Generate response from Gemini
    response = model.generate_content("\n".join(chat_history) + "\nChatbot:")
    bot_response = response.text.strip()

    # Append chatbot's response to chat history
    chat_history.append(f"Chatbot: {bot_response}")

    # Return response as JSON
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    app.run(debug=True)
