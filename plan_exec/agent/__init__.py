from langgraph.graph import StateGraph, START, END

from .nodes import (
    planner_node,
    tool_node,
    should_continue,
    llm_node
)

from .schemas import State

def create_agent():
    agent = StateGraph(State)
    
    # Add nodes
    agent.add_node("planner_node", planner_node)
    agent.add_node("tool_node", tool_node)
    agent.add_node("llm_node", llm_node)
    
    
    # Add Edges
    agent.add_edge(START, "planner_node")
    agent.add_edge("planner_node", END)

    
    agent_compiled = agent.compile()
    return agent_compiled