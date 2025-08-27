import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

# Shared LLM client for the entire application
shared_llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"), 
    model="llama-3.1-8b-instant"
)

def get_shared_llm():
    """Get the shared LLM client"""
    return shared_llm
