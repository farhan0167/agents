from typing import Literal, List

from langgraph.graph import END
from langchain.messages import ToolMessage, AIMessage

from .schemas import State, Todo, Item
from .models import llm
from .tools import tools, tools_by_name
from .prompt_templates import (
    format_tool_response_for_llm,
)


def llm_node(state: State):
    """Processes the current task with LLM"""
    llm_with_tool = llm.bind_tools(tools)

    messages = state["messages"]

    try:
        response = llm_with_tool.invoke(messages)
    except Exception as e:
        response = AIMessage(content=f"Something went wrong: {e}")

    return {
        "messages": [response]
    }
    
def tool_node(state: State):
    """Performs the tool call"""
    todo = state["todo"]
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool_name, tool_args = tool_call["name"], tool_call["args"]
        tool = tools_by_name[tool_name]
        tool_response = tool.invoke(tool_args)
        if tool_name == "write_todo":
            todo = tool_response
        formatted_tool_response = format_tool_response_for_llm(tool_response, tool_name)
        result.append(
            ToolMessage(content=formatted_tool_response, tool_call_id=tool_call["id"])
        )

    return {"messages": result, "todo": todo}


def should_continue(state: State) -> Literal["tool_node", END]:
    """Pure routing function - decides next step based on LLM output and todo list"""
    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, execute it
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we're done
    return END

