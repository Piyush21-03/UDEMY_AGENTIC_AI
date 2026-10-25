import asyncio
from dotenv import load_dotenv
from openai import OpenAI
from openai import AsyncOpenAI
import speech_recognition as sr
from openai.helpers import LocalAudioPlayer

load_dotenv()
client=OpenAI()
async_client=AsyncOpenAI()

async def tts(speech:str):
    async with async_client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        instructions="Always answer in cheerfull  and happy manner",
        input=speech,
        response_format="pcm"
    ) as response:
        await LocalAudioPlayer().play(response)


def main():
    r=sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold=2

        SYSTEM_PROMPT=f"""
                    You are a helpful and friendly voice assistant.
        
                    Your job is to have natural, clear, and concise conversations with the user.
        
                    Rules:
                    - Speak naturally, like a human assistant.
                    - Keep responses short and easy to understand.
                    - Do not use unnecessary technical terms.
                    - Ask questions when you need more information.
                    - Be polite, helpful, and confident.
                    - Do not repeat the user's question unnecessarily.
                    - If you don't know something, say so honestly.
                    - For simple questions, give simple answers.
                    - Since this is a voice conversation, avoid long lists and complicated formatting.
                    """
        

        messages=[{"role":"system","content":SYSTEM_PROMPT}]

        while True:

            print("Speak Something . . . ")
            audio=r.listen(source)

            print("Processing audio . . .(STT)")
            stt=r.recognize_google(audio)

            print("you said. . . ",stt)

            messages.append({"role":"user","content":stt})
            response=client.chat.completions.create(
                model="gpt-5.6-luna",
                messages=messages
            )

            print("AI response:",response.choices[0].message.content)
            asyncio.run(tts(speech=response.choices[0].message.content))
main()