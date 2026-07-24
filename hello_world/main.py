from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client= OpenAI()

response=client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{
        "role":"user","content":"hey-There my name is piyush whats your name"
    },
    {
        "role":"system","content":"you are an expert in maths and only answer maths questions"
    }]
)

print(response.choices[0].message.content)