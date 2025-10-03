# llm_client.py
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")


# Lazy import groq to fail only when used
def get_groq_client():
    from groq import Groq
    return Groq(api_key=GROQ_API_KEY)

def chat_completion(messages, max_tokens=1000, temperature=0.2):
    """
    messages: list of {"role": "system"/"user"/"assistant", "content": "text"}
    returns: assistant content string
    """
    if not GROQ_API_KEY:
        # Offline fallback for demo/testing without key
        # Compose a simulated reply indicating to set API key.
        return "[Simulated LLM] Set GROQ_API_KEY in .env to use real LLM."
    client = get_groq_client()
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )
    return resp.choices[0].message.content
