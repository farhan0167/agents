from typing import List

from langchain.messages import AnyMessage, HumanMessage

from .schemas import Item

WRITE_TODOS_SYSTEM_PROMPT = """## `write_todo`

You have access to the `write_todos` tool to help you manage and plan complex objectives.
Use this tool for complex objectives to ensure that you are tracking each necessary step and giving the user visibility into your progress.
This tool is very helpful for planning complex objectives, and for breaking down these larger complex objectives into smaller steps.

It is critical that you mark todos as completed as soon as you are done with a step. Do not batch up multiple steps before marking them as completed.
For simple objectives that only require a few steps, it is better to just complete the objective directly and NOT use this tool.
Writing todos takes time and tokens, use it when it is helpful for managing complex many-step problems! But not for simple few-step requests.

## Important To-Do List Usage Notes to Remember
- The `write_todos` tool should never be called multiple times in parallel.
- Don't be afraid to revise the To-Do list as you go. New information may reveal new tasks that need to be done, or old tasks that are irrelevant."""

def format_planner_instruction(user_message):
    prompt = f"""
For the given user question, come up with a simple step by step plan, like a to-do list. The plan
should involve individual items/steps that if executed correctly will yield the correct answer.
Do not add any superfluous steps. It is important that you evaluate whether or not a to-do needs to be
generated as well. For simple questions, no to-do list is required, so leave it blank. However, if a given question will
require you to think and verify, you should generate a to-do list. That is to say, for complex tasks
you should generate a to-do list.

Question: {user_message}
"""
    return prompt

def format_todo_for_llm(step: Item):
    prompt = f"""
For the item in the todo list, derive the answer:

Item: {step.content}
"""
    return prompt

def format_tool_response_for_llm(tool_response, tool_name):
    if tool_name == "write_todo":
        if tool_response:
            prompt = "Updated to-do list:\n"
            todo = "\n".join(
                [
                    f"  - Item: {item.content} Status: {item.status}\n" 
                    for item in tool_response
                ]
            )
            prompt += todo
            return prompt
    # tavily
    else:
        top = tool_response[0]
        title = top['title']
        url = top['url']
        content = top['content']
        
        prompt = f"""
Title: {title}
URL: {url}

Content:

{content} 
"""
        return prompt


def inject_context(
    todo: List[Item] = None,
    past_steps: List[AnyMessage] = None,
):
    last_step = past_steps[-1]
    
    if todo:
        last_step.content += "Todo:\n"
        last_step.content += "\n".join(
            [
                f"  - Item: {item.content} Status: {item.status}" 
                for item in todo
            ]
        )
        
    return past_steps