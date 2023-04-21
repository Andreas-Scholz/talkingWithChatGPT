import re
import openai
import speech_recognition as sr
from settings import stt, keyword_stripping_pattern, audio_input_language, audio_wolfgang_wochentag_mp3, audio_wolfgang_wochentag_wav

# Setup stt Google
r = sr.Recognizer()


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


def strip_keyword(text: str):
    try:
        stripped_text = re.search(keyword_stripping_pattern, text).group(1)
        return stripped_text.capitalize()  # capitalize the first letter
    except:
        return text