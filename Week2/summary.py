from agents import Agent, function_tool
import json
from pprint import pprint
from agents import Runner
import asyncio

runner = Runner()

assistant_instructions = """
You're a helpful assistant that helps answer user questions.
"""
def agentassistant(page_content):
    assistant = Agent(
        name='assistant',
        tools=[function_tool(page_content)],
        instructions=assistant_instructions,
        model='gpt-4o-mini'
    )
    return assistant



def summarize(page_content):
    answer = agentassistant(page_content)
    user_prompt = "Summarize the content of https://openai.github.io/openai-agents-python/"
    result = asyncio.run(runner.run(answer, input=user_prompt))
    print(type(result))
    pprint(vars(result))