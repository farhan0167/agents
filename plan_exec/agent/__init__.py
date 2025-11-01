from langgraph.graph import StateGraph, START, END

from .nodes import (
    planner_node,
    exec_node,
    tool_node,
    llm_node,
    should_continue
)

from .schemas import State

def create_agent():
    agent = StateGraph(State)

    # Add nodes
    agent.add_node("planner_node", planner_node)
    agent.add_node("exec_node", exec_node)
    agent.add_node("llm_node", llm_node)
    agent.add_node("tool_node", tool_node)

    # Add Edges
    agent.add_edge(START, "planner_node")
    agent.add_edge("planner_node", "exec_node")
    agent.add_edge("exec_node", "llm_node")
    agent.add_conditional_edges(
        "llm_node",
        should_continue,
        ["tool_node", "exec_node", END]
    )
    agent.add_edge("tool_node", "llm_node")

    agent_compiled = agent.compile()
    return agent_compiled