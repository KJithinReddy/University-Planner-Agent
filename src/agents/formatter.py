import os
from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from src.utils.shared_llm import get_shared_llm
from dotenv import load_dotenv

load_dotenv()

# Use shared LLM client
client = get_shared_llm()

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert at creating knowledge graphs from university reports. 
    
Create a knowledge graph with nodes and edges representing universities, programs, locations, and relationships.

Output ONLY valid JSON in this format:
{{
  "nodes": [
    {{"data": {{"id": "unique_id", "label": "TYPE", "name": "display_name", "description": "detailed_description"}}}}
  ],
  "edges": [
    {{"data": {{"id": "edge_id", "source": "node_id", "target": "node_id", "label": "RELATIONSHIP", "description": "relationship_description"}}}}
  ]
}}

Extract universities, majors, locations, costs, and relationships. Use meaningful labels and unique IDs."""),
    
    ("human", """
University Report:
{report}

Create a knowledge graph JSON. Output only the JSON.
""")
])

chain = prompt | client

def formatter_agent(state: Dict) -> Dict:
    """Generate a knowledge graph JSON from university report"""
    
    print("Generating knowledge graph...")
    
    # Let LLM handle everything including JSON generation
    response = chain.invoke({"report": state.get("report", "")})
    
    # Let the LLM handle the response format - no hardcoded parsing
    return {**state, "knowledge_graph": response.content}


