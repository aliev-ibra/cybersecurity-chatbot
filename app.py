from flask import Flask, render_template, request, jsonify
import requests
import cybersecurity_content
import data_handler

import os

from pathlib import Path

# Set the base directory
BASE_DIR = Path(__file__).resolve().parent

# Initialize datasets
data_handler.initialize_datasets()
data_handler.check_and_update_datasets()

app = Flask(__name__, 
            static_folder=os.path.join(BASE_DIR, 'static'),
            template_folder=os.path.join(BASE_DIR, 'templates'))

# Deepseek API configuration
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
API_KEY = "your-api-key-here"  # Replace with actual API key

@app.route('/')
def index():
    initial_message = cybersecurity_content.get_initial_message()
    return render_template('index.html', initial_message=initial_message)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    # Prepare the request to Deepseek API
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": cybersecurity_content.get_system_prompt()},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        bot_response = response.json()['choices'][0]['message']['content']
        return jsonify({"response": bot_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
