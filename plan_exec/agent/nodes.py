from typing import Literal

from langgraph.graph import END
from langchain.messages import ToolMessage

from .schemas import State, Todo
from .models import llm
from .tools import tools, tools_by_name
from .prompt_templates import get_planner_system_prompt

def planner_node(state: State):
    user_message = state["messages"][-1]
    system_prompt = get_planner_system_prompt(user_message)
    
    todo_llm = llm.with_structured_output(Todo)
    response = todo_llm.invoke(system_prompt)
    
    return {
        "todo": response.todo
    }
    

def llm_node(state: State):
    llm_with_tool = llm.bind_tools(tools)
    response = llm_with_tool.invoke(state["messages"])
    
    return {
        "messages": response
    }
    
def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

def should_continue(state: State) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END

