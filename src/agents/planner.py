import os
from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from src.utils.shared_llm import get_shared_llm
from dotenv import load_dotenv

load_dotenv()

# Use shared LLM client
client = get_shared_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", 
    """You are a university planning assistant. Extract user preferences from queries.

Extract: location, major, budget, campus_size, degree_level, institution, and any other preferences.

Output only valid JSON with these fields."""),
    
    ("human", 
    """Extract preferences from this query: {query}

Output only valid JSON.""")

])

chain = prompt | client

def planner_agent(state: Dict) -> Dict:
    """Extract user preferences using LLM."""
    print("Extracting user preferences...")
    
    # Let LLM handle everything including JSON parsing
    response = chain.invoke({"query": state.get("query", "")})
    
    # Let the LLM handle the response format - no hardcoded parsing
    return {**state, "user_persona": response.content}
