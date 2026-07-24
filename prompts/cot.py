from dotenv import load_dotenv
from openai import OpenAI
import json
load_dotenv()

client= OpenAI()


SYSTEM_PROMPT='''
you are an expert in coding and only answer codind questions if someone asks some other question you say sorry

rules:
-strictly follow the given json output format
-only run one step at a time
-the sequence of the step is START(where the user gives an input),PLAN (that can be multiple) and OUTPUT (that will be displayed to the user)

output JSON format:
{"step":"START"| "PLAN"|"OUTPUT","content":"string"}

examples:
START:hey,can you solve 2+3*5/10
PLAN:{"step":"PLAN",:"content":"seems like user is interested in maths problem"}
PLAN:{"step":"PLAN",:"content":"looking at the problem this needs to be solved by BODMAS rule"}
PLAN:{"step":"PLAN",:"content":"yes the bodmas rule is correct thing to use in this"}
PLAN:{"step":"PLAN",:"content":"first we multiply the 3*5 and we get the product as 15"}
PLAN:{"step":"PLAN",:"content":"now the new equation is 2+15/10"}
PLAN:{"step":"PLAN",:"content":"next thing to do is 15/10 which becomes 1.5"}
PLAN:{"step":"PLAN",:"content":"new equation becomes 2+1.5"}
PLAN:{"step":"PLAN",:"content":"the final answer becomes 3.5"}
'''

print("\n\n")


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
    response=client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type":"json_object"},
        messages=message_history
    )

    raw_result=response.choices[0].message.content
    message_history.append({"role":"assistant","content":raw_result})
    parsed_result=json.loads(raw_result)

    if parsed_result.get("step")=="START":
        print("➡️", parsed_result.get("content"))
        continue
    
    if parsed_result.get("step")=="PLAN":
        print("🔥", parsed_result.get("content"))
        continue

    if parsed_result["step"] == "OUTPUT":
        print("🤖", parsed_result["content"])
        break

print("\n\n")


