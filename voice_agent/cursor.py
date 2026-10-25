import asyncio
from openai import AsyncOpenAI
import speech_recognition as sr
from openai.helpers import LocalAudioPlayer

from dotenv import load_dotenv
from openai import OpenAI
import json,requests
from pydantic import BaseModel,Field
from typing import Optional
import os
load_dotenv()

client= OpenAI()
async_client=AsyncOpenAI()

def run_command(cmd:str):
    result=os.system(cmd)
    return result

def get_weather(city:str):
    url=f"https://wttr.in/{city.lower()}?format=%C+%t"
    response=requests.get(url)
    
    if response.status_code==200:
        return f"the weather in the {city} is {response.text}"
    
    return "something went wrong"

available_tools={
    "get_weather":get_weather,
    "run_command":run_command
}


SYSTEM_PROMPT='''
you are an expert in coding and only answer codind questions if someone asks some other question you say sorry

rules:
-strictly follow the given json output format
-only run one step at a time
-the sequence of the step is START(where the user gives an input),PLAN (that can be multiple) and OUTPUT (that will be displayed to the user)

output JSON format:
{"step":"START"| "PLAN"|"OUTPUT"|"TOOL","content":"string","tool":"string","input":"string"}

Available TOOLS:
-get_weather(city:str):takes the city names as input and return the weather info about the given city
-run_command(cmd:str):takes a system linux command from user and return the output from that command

example 1:
START:hey,can you solve 2+3*5/10
PLAN:{"step":"PLAN",:"content":"seems like user is interested in maths problem"}
PLAN:{"step":"PLAN",:"content":"looking at the problem this needs to be solved by BODMAS rule"}
PLAN:{"step":"PLAN",:"content":"yes the bodmas rule is correct thing to use in this"}
PLAN:{"step":"PLAN",:"content":"first we multiply the 3*5 and we get the product as 15"}
PLAN:{"step":"PLAN",:"content":"now the new equation is 2+15/10"}
PLAN:{"step":"PLAN",:"content":"next thing to do is 15/10 which becomes 1.5"}
PLAN:{"step":"PLAN",:"content":"new equation becomes 2+1.5"}
PLAN:{"step":"PLAN",:"content":"the final answer becomes 3.5"}


example 2:
START:hey,what is the weather of Delhi?
PLAN:{"step":"PLAN",:"content":"seems like user is interested in getting the weather of Delhi"}
PLAN:{"step":"PLAN",:"content":"lets see if we have any available tools in the available tools list"}
PLAN:{"step":"PLAN",:"content":"we have a get_weather tool available for this"}
PLAN:{"step":"PLAN",:"content":"i need to call the get_weather tool for Delhi as an input"}
PLAN:{"step":"TOOL",:"tool":"get_weather","input":"delhi"}
PLAN:{"step":"TOOL",:"tool":"get_weather","output":"the tempertature in delhi is cloudy with 20 C"}
PLAN:{"step":"PLAN",:"content":"Great i got the weather for DELHI"}

'''

print("\n\n")

class MyOutputFormat(BaseModel):
    step:str=Field(..., description="The ID of the step. Example:PLAN,OUTPUT,TOOL,etc")
    content:Optional[str]=Field(None,description="the optional string content for the step")
    tool:Optional[str]=Field(None,description="the ID of the tool to call")
    input:Optional[str]=Field(None,description="the input params for the tool")


message_history=[
    {
        "role":"system","content":SYSTEM_PROMPT
    },
]

user_query = input("👉 ")

message_history.append({
    "role": "user",
    "content": user_query
})

while True:
    response=client.chat.completions.parse(
        model="gpt-4o-mini",
        response_format=MyOutputFormat,
        messages=message_history
    )

    raw_result=response.choices[0].message.content
    message_history.append({"role":"assistant","content":raw_result})
    parsed_result=response.choices[0].message.parsed

    if parsed_result.step=="START":
        print("➡️", parsed_result.content)
        continue

    if parsed_result.step=="TOOL":
        tool_to_call=parsed_result.tool
        tool_input=parsed_result.input
        print(f"🔨 {tool_to_call}({tool_input})")
        tool_response = available_tools [tool_to_call](tool_input)
        print(f"🔨 {tool_to_call}({tool_input})={tool_response}")
        message_history.append({ "role": "developer", "content": json.dumps(
            { "step": "OBSERVE", "tool": tool_to_call, "input": tool_input, "output": tool_response}
        )})
        continue
            
    if parsed_result.step=="PLAN":
        print("🔥", parsed_result.content)
        continue

    if parsed_result.step == "OUTPUT":
        print("🤖", parsed_result.content)
        user_query = input("👉 ")     
        message_history.append({
            "role": "user",
            "content": user_query
        })
        continue
print("\n\n")


