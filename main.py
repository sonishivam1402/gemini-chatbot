from flask import Flask, request, jsonify
import google.generativeai as genai
import os
 
app = Flask(__name__)
 
# Configure API key (no need for Client instantiation)
api_key = "AIzaSyB7LUmSBt01kl-8uCXsGiZQj25on5JF764"
genai.configure(api_key=api_key)  # Correct method to configure API
 
@app.route('/api/ask', methods=['POST'])
def answer_question():
    # Get the question from the request
    data = request.json
    user_question = data.get('question', '')
   
    if not user_question:
        return jsonify({"error": "No question provided"}), 400
   
    # Profile information from your resume
    profile_info = """
    My name is Shivam Soni. I am a Full-Stack Developer with expertise in React, Node.js, and mobile development (React Native).
    I work at a software company and also mentor teams in mobile and MERN web development. I have a BTech in Computer Science and
    Engineering (2024) and have experience working on SaaS projects, SQLite, and API integrations.
    """
   
    # Create the prompt with system instruction and user query
    prompt = f"""
    You are a chatbot that answers questions about Shivam Soni based on the provided information.
   
    {profile_info}
   
    User: {user_question}
    """
   
    try:
        # Use the Gemini model to generate a response
        model = genai.GenerativeModel("gemini-1.5-flash")  # Correct model usage
        response = model.generate_content(prompt)
       
        # Return the response
        return jsonify({"answer": response.text})
   
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
# For local testing
@app.route('/')
def home():
    return "Resume Q&A API is running. Send POST requests to /api/ask"
 
# This is needed for Vercel
if __name__ == '__main__':
    app.run(debug=True)
 
 