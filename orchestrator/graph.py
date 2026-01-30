from langgraph.graph import StateGraph
from agents.collector import collector_agent
from agents.extractor import extractor_agent
from agents.impact import impact_agent
from agents.writer import writer_agent
from mcp_server import tools

def build_graph():
    graph = StateGraph(dict)

    graph.add_node("collector", lambda s: collector_agent(s, tools.__dict__))
    graph.add_node("extractor", lambda s: extractor_agent(s, tools.__dict__))
    graph.add_node("impact", lambda s: impact_agent(s, tools.__dict__))
    graph.add_node("writer", lambda s: writer_agent(s, tools.__dict__))

    graph.set_entry_point("collector")
    graph.add_edge("collector", "extractor")
    graph.add_edge("extractor", "impact")
    graph.add_edge("impact", "writer")
    graph.set_finish_point("writer")

    return graph.compile()
