
from dotenv import load_dotenv
from agents import Agent, Runner

load_dotenv()

# Agent that translates to Spanish
spanish_agent = Agent(
    name="Spanish Agent",
    instructions="Translate the user's message into Spanish."
)

# Agent that translates to French
french_agent = Agent(
    name="French Agent",
    instructions="Translate the user's message into French."
)

# Orchestrator agent
orchestrator_agent = Agent(
    name="Orchestrator Agent",
    instructions=(
        "You are a translation assistant. Use the available tools "
        "to translate the user's message. If the user requests "
        "multiple translations, call all relevant tools."
    ),
    tools=[
        spanish_agent.as_tool(
            tool_name="translate_to_spanish",
            tool_description="Translate the user's message into Spanish."
        ),
        french_agent.as_tool(
            tool_name="translate_to_french",
            tool_description="Translate the user's message into French."
        )
    ]
)

result = Runner.run_sync(
    orchestrator_agent,
    input="Say, Hello, how are you in Spanish?"
)

print(result.final_output)
