from langchain.messages import SystemMessage, HumanMessage
from openinference.instrumentation.langchain import LangChainInstrumentor
from phoenix.otel import register

from agent import create_agent
from agent.prompt_templates import AGENT_SYSTEM_PROMPT

tracer_provider = register(project_name="plan_exec")
LangChainInstrumentor().instrument(tracer_provider=tracer_provider)


def main(user_message):
    agent = create_agent()

    state = {
        "todo": [],  # List[Item]
        "messages": [
            SystemMessage(content=AGENT_SYSTEM_PROMPT),
            HumanMessage(content=user_message)
        ]  # List[AnyMessage]
    }

    response = agent.invoke(state)

    return response


if __name__ == "__main__":
    user_message = input("What would you like to know? ")
    response = main(user_message)
    print(response)
    # agent = create_agent()
    # agent.get_graph().draw_mermaid_png(output_file_path="./graph.png")