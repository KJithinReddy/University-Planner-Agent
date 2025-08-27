import streamlit as st
import json
from src.graph.runner import run_graph
from st_link_analysis import st_link_analysis, NodeStyle, EdgeStyle
from st_link_analysis.component.layouts import LAYOUTS

st.set_page_config(page_title="University Planner Agent", layout="wide")
st.title("University Planner Agent")

# Two-column layout
col1, col2 = st.columns([1, 1])

# Left column - Research Summary
with col1:
    st.subheader("University Recommendations")
    
    query = st.text_input("Enter your university preferences:")

    if st.button("Get Recommendations"):
        if query:
            with st.spinner('Searching for universities...'):
                steps_so_far = []
                steps_placeholder = st.empty()

                def step_callback(step_name):
                    steps_so_far.append(step_name.replace('_', ' ').title())
                    steps_placeholder.markdown("**Steps completed:**\n" + "\n".join([f"- {s}" for s in steps_so_far]))

                initial_state = {"query": query}
                try:
                    final_state = run_graph(initial_state, step_callback=step_callback)
                    st.session_state["final_state"] = final_state
                except Exception as e:
                    st.error(f"Error running graph: {e}")
                    st.stop()

                steps_placeholder.markdown("**All steps completed:**\n" + "\n".join([f"- {s}" for s in steps_so_far]))
                st.success("University recommendations completed!")

                report = final_state.get("report", "No report generated.")
                knowledge_graph = final_state.get("knowledge_graph", {})

                st.session_state["research_report"] = report
                st.session_state["knowledge_graph"] = knowledge_graph
                st.session_state["research_completed"] = True
                
                # Update graph key to force re-render
                st.session_state["graph_key"] = st.session_state.get("graph_key", 0) + 1

                st.subheader("University Recommendations")
                st.markdown(report)

        else:
            st.warning("Please enter your university preferences.")

    elif st.session_state.get("research_completed", False):
        st.markdown("---")
        st.subheader("University Recommendations")

        report = st.session_state.get("research_report", "No report available.")
        st.markdown(report)

# Right column - Knowledge Graph
with col2:
    st.subheader("Knowledge Graph")
    
    # Only show graph if research has been completed
    if not st.session_state.get("research_completed", False):
        st.info("Run university search first to see the knowledge graph.")
    else:
        LAYOUT_NAMES = list(LAYOUTS.keys())

        class DynamicGraph:
            def __init__(self, knowledge_graph):
                self.knowledge_graph = knowledge_graph
                self.load_data()

            def load_data(self):
                try:
                    # Use the knowledge graph from the final state
                    if isinstance(self.knowledge_graph, str):
                        # If it's a string, try to parse as JSON
                        elements = json.loads(self.knowledge_graph)
                    else:
                        # If it's already a dict, use it directly
                        elements = self.knowledge_graph
                    
                    # Ensure proper structure
                    if "nodes" not in elements:
                        elements["nodes"] = []
                    if "edges" not in elements:
                        elements["edges"] = []
                    
                    # Let the data structure handle itself
                    self.all_nodes = elements["nodes"]
                    self.all_edges = elements["edges"]
                    self.nodes = set([n["data"]["id"] for n in self.all_nodes])
                    self.edges = set([e["data"]["id"] for e in self.all_edges])
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    st.warning("No valid knowledge graph data available.")
                    self.all_nodes = []
                    self.all_edges = []
                    self.nodes = set()
                    self.edges = set()

            def get_elements(self):
                return {
                    "nodes": [n for n in self.all_nodes if n["data"]["id"] in self.nodes],
                    "edges": [e for e in self.all_edges if e["data"]["id"] in self.edges],
                }

            def remove(self, node_ids):
                self.nodes -= set(node_ids)
                self._update_edges()

            def expand(self, node_ids):
                new_nodes = set()
                node_ids = set(node_ids)
                for e in self.all_edges:
                    if e["data"]["source"] in node_ids:
                        new_nodes.add(e["data"]["target"])
                    elif e["data"]["target"] in node_ids:
                        new_nodes.add(e["data"]["source"])
                self.nodes |= new_nodes
                self._update_edges()

            def _update_edges(self):
                self.edges = {
                    e["data"]["id"]
                    for e in self.all_edges
                    if e["data"]["source"] in self.nodes and e["data"]["target"] in self.nodes
                }

        COMPONENT_KEY = "NODE_ACTIONS"

        # Create graph from knowledge graph data
        knowledge_graph = st.session_state.get("knowledge_graph", {})
        if not hasattr(st.session_state, "graph"):
            st.session_state.graph = DynamicGraph(knowledge_graph)

        layout = st.selectbox("Try with different layouts", LAYOUT_NAMES, index=LAYOUT_NAMES.index("dagre"))

        def create_dynamic_node_styles(nodes):
            if not nodes:
                return []
            node_labels = {n["data"].get("label", "UNKNOWN") for n in nodes}
            colors = ["#FF7F3E", "#2A629A", "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#FFC107"]
            node_styles = []
            for i, label in enumerate(node_labels):
                color = colors[i % len(colors)]
                node_styles.append(NodeStyle(label, color, "label", "description"))
            return node_styles

        def create_dynamic_edge_styles(edges):
            if not edges:
                return []
            edge_labels = {e["data"].get("label", "RELATED") for e in edges}
            return [EdgeStyle(label, caption='label', directed=True) for label in edge_labels]

        elements = st.session_state.graph.get_elements()
        node_styles = create_dynamic_node_styles(elements["nodes"])
        edge_styles = create_dynamic_edge_styles(elements["edges"])

        def onchange_callback():
            val = st.session_state[COMPONENT_KEY]
            if val["action"] == "remove":
                st.session_state.graph.remove(val["data"]["node_ids"])
            elif val["action"] == "expand":
                st.session_state.graph.expand(val["data"]["node_ids"])

        with st.container(border=True):
            # Use dynamic key to force re-render when new research is completed
            graph_key = f"{COMPONENT_KEY}_{st.session_state.get('graph_key', 0)}"
            vals = st_link_analysis(
                elements,
                layout=layout,
                node_styles=node_styles,
                edge_styles=edge_styles,
                key=graph_key,
                node_actions=['remove', 'expand'],
                on_change=onchange_callback,
            )
            if vals:
                st.markdown("#### Graph Interactions")
                st.json(vals, expanded=True)


