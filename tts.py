import pyttsx3
from settings import tts_language, tts_speed

# Setup text to speech engine
tts = pyttsx3.init()
tts.setProperty('voice', tts.getProperty('voices')[tts_language].id)
tts.setProperty('rate', tts_speed)


def speak(text: str):
    tts.say(text)
    tts.runAndWait()
    tts.stop()
