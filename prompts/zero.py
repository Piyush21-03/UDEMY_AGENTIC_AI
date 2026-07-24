from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client= OpenAI()

SYSTEM_PROMPT="you are an expert in maths and only answer maths questions"

response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role":"user","content":"hey there my name is piyush"
    },
    {
        "role":"system","content":SYSTEM_PROMPT
    }]
)

print(response.choices[0].message.content)