from src.graph.edges import build_graph
from src.graph.state import UniversityState
from typing import Callable

def run_graph(initial_state: UniversityState, step_callback: Callable = None) -> UniversityState:
    """Executes the university planning graph."""
    graph = build_graph()
    
    # LangGraph's stream method allows for step-by-step execution
    final_state = None
    for s in graph.stream(initial_state):
        node_name = list(s.keys())[0] # Get the current node name
        if step_callback:
            step_callback(node_name)
        final_state = s[node_name]
        
    return final_state
