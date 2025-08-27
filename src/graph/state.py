from typing import TypedDict, List, Optional, Dict

class UniversityState(TypedDict):
    """Represents the state of the university planner workflow."""
    query: str  # The user's initial query
    user_persona: Optional[Dict] # Extracted user preferences
    universities: Optional[List[Dict]] # List of matching universities
    courses: Optional[List[Dict]] # Course data for a specific university
    location_details: Optional[Dict] # Weather, transport info
    report: Optional[str] # The final recommendation report
    knowledge_graph: Optional[Dict] # The JSON for the knowledge graph
