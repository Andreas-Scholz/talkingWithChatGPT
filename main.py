import os
import speech_recognition as sr
import openai


# OpenAI config
openai.api_key = os.getenv("OPENAI_API_KEY")
chatgpt_model = "gpt-3.5-turbo"  # available models via openai.Model.list()

# Google config
r = sr.Recognizer()

# "Wolfgang, wenn gestern Montag war, was wäre dann übermorgen für ein Tag?";  <- ChatGPT 4.0 kann das, 3.5 offenbar nicht
audio_wolfgang_wochentag_wav = "resources/wolfgang-wochentag.wav"
audio_wolfgang_wochentag_mp3 = "resources/wolfgang-wochentag.mp3"

# General settings
tts = "openai"  # the text to speech vendor to use
audio_input_language = "de"


def main():
    transcription = transcribe()
    print(transcription)
    input("Press enter if you want to send this to ChatGPT... (otherwise please quit as this costs money):\n")
    response = talk_to_chatgpt(transcription)

    print(response.content)


def transcribe():
    transcription = ""
    match tts:
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


if __name__ == '__main__':
    main()

