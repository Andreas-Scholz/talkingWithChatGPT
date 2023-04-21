import os
import stt
import openai
from settings import chatgpt_model

openai.api_key = os.getenv("OPENAI_API_KEY")

def main():
    transcription = stt.transcribe()
    print("Transcription: " + transcription)

    transcription_without_keyword = stt.strip_keyword(transcription)
    print("Keyword removed: " + transcription_without_keyword)

    input("Press enter if you want to send this to ChatGPT... (otherwise please quit as this costs money):")
    response = talk_to_chatgpt(transcription_without_keyword)
    print(response.content)


def talk_to_chatgpt(message):
    completion = openai.ChatCompletion.create(
        model=chatgpt_model,
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return completion.choices[0].message


if __name__ == '__main__':
    main()

