from langchain.messages import HumanMessage

from agent import create_agent


def main(user_message):
    agent = create_agent()
    
    state = {
        "messages": [HumanMessage(content=user_message)],
        "todo": []
    }
    
    response = agent.invoke(state)
    
    return response


if __name__ == "__main__":
    user_message = input("What would you like to know? ")
    response = main(user_message)
    print(response)