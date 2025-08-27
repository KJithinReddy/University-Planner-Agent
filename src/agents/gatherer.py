import os
from typing import Dict
from langchain_core.prompts import ChatPromptTemplate
from src.utils.tools import university_search, university_comparison, cost_analysis, get_weather_data
from src.utils.shared_llm import get_shared_llm
from dotenv import load_dotenv

load_dotenv()

# Use shared LLM client
tool_llm = get_shared_llm()

# Let LLM discover tools dynamically
tools = [university_search, university_comparison, cost_analysis, get_weather_data]
tool_llm_with_tools = tool_llm.bind_tools(tools)

# Tool calling prompt
tool_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an intelligent university planning assistant. Based on the user's query and persona, determine which tools to call.

Available tools:
1. university_search - For finding specific universities, program details
2. university_comparison - For comparing multiple universities (returns table)
3. cost_analysis - For detailed cost breakdowns and financial planning
4. get_weather_data - For weather information about locations

CRITICAL RULES:
- For comparisons, call university_comparison ONCE with all universities mentioned
- Do NOT call the same tool multiple times
- Extract all relevant parameters in a single tool call
- If comparing universities, put all university names in the 'institution' parameter
- Be efficient - minimize the number of tool calls

Examples:
- "Compare Harvard and MIT" → university_comparison(institution="Harvard,MIT")
- "Find universities in California" → university_search(location="California")
- "Weather in Boston" → get_weather_data(location="Boston")

Call the most appropriate tool(s) with all relevant parameters."""),
    
    ("human", """User Query: {query}
User Persona: {persona}

Determine which tool(s) to call and extract the relevant parameters. Be efficient and call each tool only once.""")

])

def gatherer_agent(state: Dict) -> Dict:
    """Gather university data using LLM-driven tool calling."""
    query = state.get("query", "")
    persona = state.get("user_persona", {})
    
    print(f"LLM tool calling for query: {query}")
    
    # Let LLM decide which tools to call
    chain = tool_prompt | tool_llm_with_tools
    response = chain.invoke({
        "query": query,
        "persona": persona
    })
    
    print(f"LLM response: {response.content}")
    
    # Let LLM handle tool execution and result processing
    tool_calls = response.tool_calls if hasattr(response, 'tool_calls') else []
    
    # Let LLM handle all tool execution logic
    results = {}
    for tool_call in tool_calls:
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        
        print(f"Executing tool: {tool_name} with args: {tool_args}")
        
        # Let LLM handle tool discovery and execution
        for tool in tools:
            if tool.name == tool_name:
                result = tool.invoke(tool_args)
                results[tool_name] = result
                break
    
    return {**state, **results}
