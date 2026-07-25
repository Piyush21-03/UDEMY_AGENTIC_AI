from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client=OpenAI()

response=client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {
            "role":"user",
            "content":[
                {"type":"text","text":"generate a caption for this iamge in about 50 words"},
                {"type":"image_url","image_url":{"url":"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS7zDMYnGheNT1l7pEW3R5N3Uf4--yCjRprCG9W5WQ58g&s=10"}}
            ]
        }
    ]
)

print("Response:",response.choices[0].message.content)