from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client= OpenAI()

SYSTEM_PROMPT='''
you are an expert in coding and only answer codind questions if someone asks some other question you say sorry

examples:
question:give the sum of 2+3.
answer:sorry 

question: what is coding?
answer:Coding is the process of translating human intentions into specific, structured instructions that computers can understand and execute
'''

response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role":"user","content":"what is square of 2"
    },
    {
        "role":"system","content":SYSTEM_PROMPT
    }]
)

print(response.choices[0].message.content)