import os
import speech_recognition as sr
import openai
import re


# OpenAI config
openai.api_key = os.getenv("OPENAI_API_KEY")
chatgpt_model = "gpt-3.5-turbo"  # available models via openai.Model.list()

# Google config
r = sr.Recognizer()

# "Wolfgang, wenn gestern Montag war, was wäre dann übermorgen für ein Tag?";
audio_wolfgang_wochentag_wav = "resources/wolfgang-wochentag.wav"
audio_wolfgang_wochentag_mp3 = "resources/wolfgang-wochentag.mp3"


# General settings
stt = "openai"  # speech to text vendor to use
audio_input_language = "de"
keyword = "Wolfgang"  # the word used to activate chatGPT (instead of alexa) The keyword will be stripped from the beginning of the stt transcript
keyword_stripping_pattern = '^' + keyword + ',?\s*(.*)$'  # strip the keyword from the beginning together with an existing comma and whitespace


def main():
    transcription = transcribe()
    print("Transcription: " + transcription)

    transcription_without_keyword = strip_keyword(transcription)
    print("Keyword removed: " + transcription_without_keyword)

    input("Press enter if you want to send this to ChatGPT... (otherwise please quit as this costs money):")
    response = talk_to_chatgpt(transcription_without_keyword)
    print(response.content)


def transcribe():
    transcription = ""
    match stt:
        case "openai" | "whisper":
            transcription = transcribe_with_openai(audio_wolfgang_wochentag_mp3)
        case "google":
            with sr.AudioFile(audio_wolfgang_wochentag_wav) as source:
                transcription = transcribe_with_google(source)
    return transcription


def transcribe_with_openai(audio_file):
    audio_file_stream = open(audio_file, mode="rb")
    transcript = openai.Audio.transcribe(model="whisper-1",
                                         file=audio_file_stream,
                                         language=audio_input_language)
    return transcript.text


def transcribe_with_google(audio_file):
    audio_data = r.record(audio_file)  # listen for the data (load audio to memory)
    transcript = r.recognize_google(audio_data, language=audio_input_language)
    return transcript


def talk_to_chatgpt(message):
    completion = openai.ChatCompletion.create(
        model=chatgpt_model,
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return completion.choices[0].message


def strip_keyword(text: str):
    try:
        stripped_text = re.search(keyword_stripping_pattern, text).group(1)
        return stripped_text.capitalize()  # capitalize the first letter
    except:
        return text


if __name__ == '__main__':
    main()

