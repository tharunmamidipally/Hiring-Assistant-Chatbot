TalentScout AI Hiring Assistant
Project Overview :

TalentScout is an intelligent AI-powered Hiring Assistant designed to streamline the initial technical screening process for candidates. The chatbot collects essential candidate information such as name, email, experience, desired role, location, and tech stack, then generates customized technical questions based on the declared tech stack.

The project demonstrates the use of Large Language Models (LLMs) for prompt engineering, conversational AI, and automated candidate assessment in a real-world recruitment context.

Key Features:

Mobile-first, card-style chatbot interface

Collects candidate information in a structured format

Generates technical questions tailored to each technology

Stores answers securely and allows CSV/JSON download

Simulated data storage for demo purposes

Installation Instructions:


Create a virtual environment

python -m venv venv


Activate the virtual environment

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate


Install dependencies

pip install -r requirements.txt


Configure environment variables

Create a .env file in the project root:

GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama3-8b-8192  # or updated model if deprecated


Run the application

streamlit run app.py

Usage Guide

Open the app in your browser (Streamlit default URL is usually http://localhost:8501).

Fill in the candidate information card (all fields are required).

Submit the form to generate technical questions automatically based on the tech stack.

Answer the questions directly in the mobile-style chat interface.

After completing, click Finish and Download to save your responses as CSV or JSON.

Technical Details

Programming Language: Python 3.11+
Frontend: Streamlit (mobile-first card design)
Backend & AI:

Groq LLaMA-3 API for LLM-powered question generation

Custom Python scripts for input parsing, candidate data handling, and chat management

Architecture:

app.py: Main Streamlit application, handles UI and chat logic

llm_client.py: Manages LLM requests and completions

prompts.py: Contains system and question-generation prompts

storage.py: Handles candidate data saving (simulated/anonymized)

Prompt Design :

The AI prompts are carefully crafted to:

Collect candidate information: Guide the model to extract name, contact, experience, desired role, location, and tech stack in structured format.

Generate technical questions: For each technology in the candidate’s tech stack, generate 3-5 relevant questions covering syntax, concepts, and practical skills.

Maintain context: The chatbot preserves conversation flow, ensuring follow-ups or clarifications can be handled naturally.

Example Prompt Snippet:

Generate 4 technical questions for a candidate named {candidate_name} who knows {technologies}. 
Questions should vary in difficulty and cover practical skills, concepts, and problem-solving.
Provide output in JSON format like:
{
  "Python": [{"question": "...", "difficulty": "easy/medium/hard", "area": "..."}],
  ...
}

Challenges & Solutions 

Mobile-style chat on desktop:

Solution: Used CSS in Streamlit to mimic mobile chat bubbles, cards, and responsive design.

Mandatory candidate information:

Solution: Added validation logic to prevent proceeding without required fields.

Readable assistant messages:

Solution: Updated CSS to improve text contrast and background color.

Handling JSON from LLM responses:

Solution: Implemented robust parsing with fallback to raw text if parsing fails.

User-friendly interaction flow:

Solution: Stepwise chatbot interaction, mobile-first card UI, and single-step question-answering.

Future Enhancements (Optional/Bonus):

One-question-at-a-time interaction for real-time assessment

Sentiment analysis to gauge candidate confidence

Multilingual support

Cloud deployment with live demo link

Author: Bhavya Tharun
GitHub: https://github.com/tharunmamidipally