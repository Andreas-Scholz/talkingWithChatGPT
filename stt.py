import re
import sys

import openai
import speech_recognition as sr
from settings import stt_vendor, keyword_stripping_pattern, audio_input_language

# Setup stt Google
r = sr.Recognizer()


def transcribe(audio_source: str, audio_file: str = ""):
    match audio_source:
        case "microphone":
            return __transcribe_microphone()
        case "file":
            return __transcribe_file(audio_file)
        case _:
            raise ValueError("Unknown audio source. Must be either 'microphone' or 'file'.")


def __transcribe_microphone():
    try:
        with sr.Microphone() as source:
            print('listening...')
            r.adjust_for_ambient_noise(source, duration=1)
            voice = r.listen(source)
            transcription = r.recognize_google(voice, language=audio_input_language)
            return transcription
    except:
        print("Detected microphones: " + sr.Microphone.list_microphone_names())
        print("Either no microphone was detected or another error occured. Exiting...")
        sys.exit(1)


def __transcribe_file(audio_file: str):
    transcription = ""
    match stt_vendor:
        case "openai" | "whisper":
            audio_file_stream = open(audio_file, mode="rb")
            transcription = transcribe_with_openai(audio_file_stream)
        case "google":
            with sr.AudioFile(audio_file) as audio_stream:
                audio = r.record(audio_stream)  # listen for the data (load audio to memory)
                transcription = transcribe_with_google(audio)
    return transcription


def transcribe_with_openai(audio):
    transcript = openai.Audio.transcribe(model="whisper-1",
                                         file=audio,
                                         language=audio_input_language)
    return transcript.text


def transcribe_with_google(audio):
    transcript = r.recognize_google(audio, language=audio_input_language)
    return transcript


def strip_keyword(text: str):
    try:
        stripped_text = re.search(keyword_stripping_pattern, text).group(1)
        return stripped_text.capitalize()  # capitalize the first letter
    except:
        return text