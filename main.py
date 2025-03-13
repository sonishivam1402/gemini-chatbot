from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os

# Initialize FastAPI app
app = FastAPI()

# Load API key from environment variable
API_KEY = "AIzaSyB7LUmSBt01kl-8uCXsGiZQj25on5JF764"  # Set this in Render
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from environment variables")

genai.configure(api_key=API_KEY)

# Define request model
class QuestionRequest(BaseModel):
    question: str

# Root route for health check
@app.get("/")
def home():
    return {"message": "Resume Q&A API is running. Send POST requests to /api/ask"}

# API endpoint to handle questions
@app.post("/api/ask")
def answer_question(request: QuestionRequest):
    user_question = request.question

    if not user_question:
        raise HTTPException(status_code=400, detail="No question provided")

    # Profile information
    profile_info = """
    My name is Shivam Soni. I am a Full-Stack Developer with expertise in React, Node.js, and mobile development (React Native).
    I work at a software company and also mentor teams in mobile and MERN web development. I have a BTech in Computer Science and
    Engineering (2024) and have experience working on SaaS projects, SQLite, and API integrations.
    """

    # Construct the prompt
    prompt = f"""
    You are a chatbot that answers questions about Shivam Soni based on the provided information.

    {profile_info}

    User: {user_question}
    """

    try:
        # Use Gemini model to generate response
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)

        return {"answer": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
