from dotenv import load_dotenv
from openai import OpenAI
import speech_recognition as sr

load_dotenv()
client=OpenAI()
def main():
    r=sr.Recognizer()

    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold=2

        print("Speak Something . . . ")
        audio=r.listen(source)

        print("Processing audio . . .(STT)")
        stt=r.recognize_google(audio)

        print("you said. . . ",stt)

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


        response=client.chat.completions.create(
            model="gpt-5.6-luna",
            messages=[
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":stt}
            ]
        )

        print("AI response:",response.choices[0].message.content)
main()