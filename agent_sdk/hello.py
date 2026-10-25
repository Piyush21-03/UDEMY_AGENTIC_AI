from dotenv import load_dotenv

from agents import Agent,Runner

load_dotenv()

hello_agent=Agent[any](
    name="Hello World Agent",
    instructions="You are an agent that greets the user in a funny way and uses emojis"

)

result=Runner.run_sync(hello_agent,"Hey There, My name is Piyush Panigrahi")

print(result.final_output)