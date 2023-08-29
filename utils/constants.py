import os

class Constants(object):
    API_KEY = os.environ.get("API_KEY")
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_CONTEXT = "Your name is Jarvis"

    MEDIA_FOLDER = "media/"


    DEFAULT_INPUT_LANGUAGE_CODE = "en-IN"
    DEFAULT_RATE = 16000
    DEFAULT_FRAMES_PER_BUFFER = 1024

    DEFAULT_OUTPUT_ACCENT = "co.uk" # British Accent
    DEFAULT_OUTPUT_LANGUAGE = "en"
    DEFAULT_OUTPUT_IS_SLOW = False
    DEFAULT_OUTPUT_FILE_FORMAT = "{}.mp3"

    DEFAULT_PLAYBACK_RATE = 1.2

    CONSTANT_SERVER_ERROR = "server_error"