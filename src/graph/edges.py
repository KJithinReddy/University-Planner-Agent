from langgraph.graph import StateGraph
from src.graph.state import UniversityState
from src.graph.nodes import (
    plan_node,
    gather_node,
    recommend_node,
    format_node,
)

def build_graph():
    graph = StateGraph(state_schema=UniversityState)

    graph.add_node("plan", plan_node)
    graph.add_node("gather", gather_node)
    graph.add_node("recommend", recommend_node)
    graph.add_node("format", format_node)

    graph.set_entry_point("plan")
    graph.set_finish_point("format")

    graph.add_edge("plan", "gather")
    graph.add_edge("gather", "recommend")
    graph.add_edge("recommend", "format")

    return graph.compile()
