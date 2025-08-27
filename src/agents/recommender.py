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
    """You are a world-class university planning expert. Create comprehensive university recommendation reports.

Your job is to:
1. Analyze the user's query and preferences
2. Review the university data provided
3. Generate a detailed, helpful report
4. Include any tables or structured data in your response
5. Make clear recommendations

Write in a clear, engaging way that helps the user make informed decisions."""),
    
    ("human", 
    """Create a university recommendation report.

User Query: {query}
All Available Data: {all_data}

Generate a comprehensive report that directly addresses the user's query and helps them make an informed decision.""")
])

chain = prompt | client

def recommender_agent(state: Dict) -> Dict:
    """Generate university recommendation report using LLM."""
    print("Generating recommendation report...")
    
    # Let LLM handle all the data processing
    response = chain.invoke({
        "query": state.get("query", ""),
        "all_data": state
    })
    
    return {**state, "report": response.content}