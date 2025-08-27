import os
import sqlite3
from typing import List, Dict, Optional
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from src.utils.shared_llm import get_shared_llm
from dotenv import load_dotenv

load_dotenv()

# Use shared LLM client
llm_client = get_shared_llm()

def get_db_connection():
    """Get database connection"""
    db_path = os.getenv("DATABASE_PATH", "data/ipeds_data.db")
    return sqlite3.connect(db_path)

def clean_sql_query(sql_query: str) -> str:
    """Clean SQL query by removing markdown formatting"""
    # Remove markdown code blocks
    sql_query = sql_query.replace("```sql", "").replace("```", "")
    # Remove leading/trailing whitespace
    sql_query = sql_query.strip()
    return sql_query

def execute_sql_and_format(sql_query: str) -> str:
    """Execute SQL query and format results for display"""
    # Clean the SQL query first
    sql_query = clean_sql_query(sql_query)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Get results
        results = cursor.fetchall()
        conn.close()
        
        # Let LLM handle all result processing
        data_results = []
        for row in results:
            data_results.append(dict(zip(columns, row)))
        
        return str(data_results)
        
    except Exception as e:
        return f"Database error: {str(e)}"

# Let LLM handle all SQL generation
sql_prompt = ChatPromptTemplate.from_messages([
    ("system", """Generate a valid SQLite query for university data.

Let the LLM determine the appropriate tables, columns, and query structure based on the requirements.

Output ONLY the SQL query, no markdown formatting
Do NOT include ```sql or ``` tags
Do NOT include any explanations"""),
    ("human", "Generate SQL for: Location: {location}, Major: {major}, Institution: {institution}, Degree Level: {degree_level}")
])

# Let LLM handle all result formatting
format_prompt = ChatPromptTemplate.from_messages([
    ("system", """Format university data into a readable format. Let the LLM determine the best way to present the information.

Make it clear and easy to read."""),
    ("human", "Format this university data: {data}")
])

@tool
def university_search(location: str = "", major: str = "", institution: str = "", degree_level: str = "") -> str:
    """Search for universities based on location, major, institution, or degree level."""
    print("🔍 Searching universities...")
    
    # Let LLM generate SQL
    sql_response = sql_prompt | llm_client
    sql_query = sql_response.invoke({
        "location": location,
        "major": major,
        "institution": institution,
        "degree_level": degree_level
    }).content.strip()
    
    # Execute SQL and get raw results
    raw_results = execute_sql_and_format(sql_query)
    
    # Let LLM format results
    format_response = format_prompt | llm_client
    formatted_results = format_response.invoke({"data": raw_results}).content
    
    return formatted_results

# Let LLM handle cost analysis
cost_sql_prompt = ChatPromptTemplate.from_messages([
    ("system", """Generate a SQLite query focused on university costs and affordability.

Let the LLM determine the appropriate tables, columns, and query structure for cost analysis.

Output ONLY the SQL query, no markdown formatting
Do NOT include ```sql or ``` tags
Do NOT include any explanations"""),
    ("human", "Generate cost analysis SQL for: Location: {location}, Major: {major}, Institution: {institution}, Degree Level: {degree_level}")
])

# Let LLM handle cost formatting
cost_format_prompt = ChatPromptTemplate.from_messages([
    ("system", """Format university cost data into a readable cost analysis. Let the LLM determine the best way to present cost information.

Make it clear and easy to read."""),
    ("human", "Format this cost data: {data}")
])

@tool
def cost_analysis(location: str = "", major: str = "", institution: str = "", degree_level: str = "") -> str:
    """Analyze costs for universities and return a cost comparison table."""
    print("💰 Analyzing costs...")
    
    # Let LLM generate cost-focused SQL
    sql_response = cost_sql_prompt | llm_client
    sql_query = sql_response.invoke({
        "location": location,
        "major": major,
        "institution": institution,
        "degree_level": degree_level
    }).content.strip()
    
    # Execute SQL and get raw results
    raw_results = execute_sql_and_format(sql_query)
    
    # Let LLM format cost results
    format_response = cost_format_prompt | llm_client
    formatted_results = format_response.invoke({"data": raw_results}).content
    
    return formatted_results

@tool
def university_comparison(location: str = "", major: str = "", institution: str = "", degree_level: str = "") -> str:
    """Compare multiple universities and return a comparison table."""
    print("🔄 Comparing universities...")
    
    # Let LLM generate comparison SQL
    comparison_sql_prompt = ChatPromptTemplate.from_messages([
        ("system", """Generate a SQLite query to compare universities. Let the LLM determine the appropriate tables, columns, and query structure for comparison.

Output ONLY the SQL query, no markdown formatting
Do NOT include ```sql or ``` tags
Do NOT include any explanations"""),
        ("human", "Generate comparison SQL for: Location: {location}, Major: {major}, Institution: {institution}, Degree Level: {degree_level}")
    ])
    
    sql_response = comparison_sql_prompt | llm_client
    sql_query = sql_response.invoke({
        "location": location,
        "major": major,
        "institution": institution,
        "degree_level": degree_level
    }).content.strip()
    
    # Execute SQL and get raw results
    raw_results = execute_sql_and_format(sql_query)
    
    # Let LLM format comparison results
    comparison_format_prompt = ChatPromptTemplate.from_messages([
        ("system", """Format university comparison data into a readable comparison table. Let the LLM determine the best way to present comparison information.

Make it clear and easy to read."""),
        ("human", "Format this comparison data: {data}")
    ])
    
    format_response = comparison_format_prompt | llm_client
    formatted_results = format_response.invoke({"data": raw_results}).content
    
    return formatted_results

@tool
def get_weather_data(location: str) -> str:
    """Get weather information for a specific location."""
    print(f"🌤️ Getting weather for {location}...")
    
    try:
        # Use Tavily for weather search
        tavily_tool = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        search_result = tavily_tool.search(f"current weather in {location}")
        
        # Let LLM format weather results
        weather_format_prompt = ChatPromptTemplate.from_messages([
            ("system", """Format weather search results into a readable weather report. Let the LLM determine the best way to present weather information.

Make it clear and informative."""),
            ("human", "Format this weather data for {location}: {data}")
        ])
        
        # Convert search results to string
        weather_data = str(search_result)
        
        format_response = weather_format_prompt | llm_client
        formatted_weather = format_response.invoke({
            "location": location,
            "data": weather_data
        }).content
        
        return formatted_weather
        
    except Exception as e:
        return f"Weather search error: {str(e)}"

# Test function
if __name__ == "__main__":
    print("🧪 Testing Tools with fully LLM-driven everything")
    print("=" * 50)
    
    # Test weather (should work without database)
    print("Testing weather function:")
    result = get_weather_data.invoke({"location": "Boston"})
    print(f"Result: {result}")
    
    print("\n" + "=" * 50)
    print("✅ Tools ready with fully LLM-driven everything!")




