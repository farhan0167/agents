from typing import Literal, List

from langgraph.graph import END
from langchain.messages import ToolMessage, HumanMessage, AIMessage

from .schemas import State, Todo, Item
from .models import llm
from .tools import tools, tools_by_name
from .prompt_templates import (
    format_planner_instruction,
    format_todo_for_llm,
    format_tool_response_for_llm,
    inject_context
)

def planner_node(state: State):
    user_message = state["user_message"]
    instruction = format_planner_instruction(user_message)
    
    todo_llm = llm.with_structured_output(Todo)
    response = todo_llm.invoke(instruction)
    
    todo = response.todo
    if todo:
        ai_message = AIMessage(content=f"Generated todo list: {todo}\n")
        human_message = HumanMessage(content="For each item in the todo list, derive the answer:\n")
        return {
            "todo": response.todo,
            "past_steps": [ai_message, human_message]
        }
    else:
        past_step = HumanMessage(content=user_message)
        
        return {
            "past_steps": [past_step]
        }


def llm_node(state: State):
    """Processes the current task with LLM"""
    llm_with_tool = llm.bind_tools(tools)
    
    todo = state["todo"]
    past_steps = state["past_steps"]
    messages = state["messages"]
    
    last_step = past_steps[-1]
    
    # If last step wasn't a tool call nor tool message, we need to format it for the LLM
    if isinstance(last_step, HumanMessage):
        formatted_llm_input = inject_context(
            todo=todo,
            past_steps=past_steps,
        )
    else:
        formatted_llm_input = past_steps
        
    try:
        response = llm_with_tool.invoke(formatted_llm_input)
    except Exception as e:
        response = AIMessage(content=f"Something went wrong: {e}")
        
    return {
        "past_steps": [response]
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
        
    return {"past_steps": result, "todo": todo}


def should_continue(state: State) -> Literal["tool_node", "exec_node", END]:
    """Pure routing function - decides next step based on LLM output and todo list"""
    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, execute it
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we're done
    return END

