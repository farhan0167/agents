

def get_planner_system_prompt(user_message):
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