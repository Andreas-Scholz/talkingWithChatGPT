import os
import time
import openai
import stt
import tts
from settings import chatgpt_model, audio_source, audio_wolfgang_wochentag_mp3, answer_max_tokens

openai.api_key = os.getenv("OPENAI_API_KEY")

conversation = []

def main():
    while True:
        transcription = stt.transcribe(audio_source, audio_file=audio_wolfgang_wochentag_mp3)
        print("Transcription: " + transcription)

        transcription_without_keyword = stt.strip_keyword(transcription)
        print("Keyword removed: " + transcription_without_keyword)
        add_to_conversation("user", transcription_without_keyword)

        # input("Press enter if you want to send this to ChatGPT... (otherwise please quit):")

        response = talk_to_chatgpt()
        add_to_conversation("assistant", transcription)
        print(response)
        time.sleep(1)
        tts.speak(response)
        time.sleep(1)


def talk_to_chatgpt():
    completion = openai.ChatCompletion.create(
        model=chatgpt_model,
        messages=conversation,
        max_tokens=answer_max_tokens
    )
    return completion.choices[0].message.content


def add_to_conversation(role: str, message: str):
    conversation.append({"role": role, "content": message})


if __name__ == '__main__':
    main()

