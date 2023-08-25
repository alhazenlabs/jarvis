import os

class Constants(object):
    API_KEY = os.environ.get("API_KEY")
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_CONTEXT = "Your name is Jarvis"

    MEDIA_FOLDER = "media/"