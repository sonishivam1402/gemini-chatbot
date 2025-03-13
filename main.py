# api/index.py
from flask import Flask, request, jsonify
from google import genai
import os

app = Flask(__name__)

# Get API key from environment variable (safer than hardcoding)
api_key = "AIzaSyB7LUmSBt01kl-8uCXsGiZQj25on5JF764"
client = genai.Client(api_key=api_key)

@app.route('/api/ask', methods=['POST'])
def answer_question():
    data = request.json
    user_question = data.get('question', '')

    if not user_question:
        return jsonify({"error": "No question provided"}), 400

    profile_info = """
    My name is Shivam Soni. I am a Full-Stack Developer with expertise in React, Node.js, and mobile development (React Native). 
    I work at a software company and also mentor teams in mobile and MERN web development. I have a BTech in Computer Science and 
    Engineering (2024) and have experience working on SaaS projects, SQLite, and API integrations.
    """

    prompt = f"""
    You are a chatbot that answers questions about Shivam Soni based on the provided information.

    {profile_info}

    User: {user_question}
    """

    try:
        # Print API request details for debugging
        print("Sending request to Gemini API...")
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        
        # Print response object
        print("Response received:", response)

        # Check if response contains text
        if hasattr(response, 'text'):
            return jsonify({"answer": response.text})
        else:
            return jsonify({"error": "No valid response from Gemini API"}), 500

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500


# For local testing
@app.route('/')
def home():
    return "Resume Q&A API is running. Send POST requests to /api/ask"

# This is needed for Vercel
if __name__ == '__main__':
    app.run(debug=True)