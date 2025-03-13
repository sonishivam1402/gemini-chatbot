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
My name is Shivam Soni. I am a Full-Stack Developer with expertise in .NET, React, and backend development. 
I hold a B.Tech in Computer Science Engineering from Navrachana University, Vadodara, with a CGPA of 8.57/10.

I currently work as a Full Stack Developer at UCI India, where I enhance RESTful APIs using .NET, optimize SQL 
stored procedures, and build AI-powered products. Previously, I worked as a Backend Developer at DECGamingStudio, 
where I led the development of an immersive AR Farming Game using Unity and Vuforia.

Some key projects I have worked on include:
- **Timesheet Management System (TMS):** Developed enterprise-grade backend services using .NET Core, C#, SQL Server, 
  and Azure DevOps, enabling efficient tracking and approval of employee work hours.
- **Learn-X: Fun Learning Through AR:** Designed interactive AR-based educational mobile applications, leveraging Unity, 
  C#, and Vuforia to enhance learning experiences for children.

I am proficient in **C#, SQL, JavaScript, HTML, CSS, C, and C++**, with experience in **.NET Core, React, jQuery, 
Azure Cloud, SQL Server, and REST API development**. 

I am certified in:
- **AZ-104 Microsoft Certified: Azure Administrator Associate**
- **AZ-900 Microsoft Certified: Azure Fundamentals**
- **AWS Academy Graduate – Machine Learning Foundations**
- **AWS Academy Graduate – Cloud Foundations**

Beyond my professional work, I actively mentor teams in mobile and MERN stack development, sharing my knowledge and 
guiding them through new technologies.
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
