# General settings
stt_vendor = "openai" # Speech to text vendor to use: "openai" or "google"
audio_source = "microphone" \
                 # "microphone" or "file"
audio_input_language = "de"
keyword = "Wolfgang"  # the word used to activate chatGPT (instead of alexa) The keyword will be stripped from the beginning of the stt transcript
keyword_stripping_pattern = '^' + keyword + ',?\s*(.*)$'  # strip the keyword from the beginning together with an existing comma and whitespace

# Sample audio files
# "Wolfgang, wenn gestern Montag war, was wäre dann übermorgen für ein Tag?";
audio_wolfgang_wochentag_wav = "resources/wolfgang-wochentag.wav"
audio_wolfgang_wochentag_mp3 = "resources/wolfgang-wochentag.mp3"

# OpenAI config
openai_api_key_environment_var = "OPENAI_API_KEY"
chatgpt_model = "gpt-3.5-turbo"  # available models via openai.Model.list()
answer_max_tokens = 100  # the maximum number of tokens the answer of ChatGPT shall consist of. One token is ~0.75 words.

# text to speech settings
tts_language = 0  # = 0 German, 1 = English
tts_speed = 150  # higher is faster
