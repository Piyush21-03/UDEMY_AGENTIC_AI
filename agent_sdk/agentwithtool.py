from dotenv import load_dotenv

from agents import Agent,Runner
from agents import WebSearchTool

load_dotenv()
hello_agent=Agent[any](
    name="Hello World Agent",
    instructions="You are an agent that greets the user in a funny way and uses emojis",
    tools=[WebSearchTool()]
)

result=Runner.run_sync(hello_agent,"hey, what is on https://github.com/Piyush21-03/UDEMY_AGENTIC_AI")

print(result.final_output)