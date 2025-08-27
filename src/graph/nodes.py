from src.graph.state import UniversityState
from src.agents.planner import planner_agent
from src.agents.gatherer import gatherer_agent
from src.agents.recommender import recommender_agent
from src.agents.formatter import formatter_agent

def plan_node(state: UniversityState) -> UniversityState:
    print("Running planner_node")
    return planner_agent(state)

def gather_node(state: UniversityState) -> UniversityState:
    print("Running gather_node")
    return gatherer_agent(state)

def recommend_node(state: UniversityState) -> UniversityState:
    print("Running recommender_node")
    return recommender_agent(state)

def format_node(state: UniversityState) -> UniversityState:
    print("Running formatter_node")
    return formatter_agent(state)
