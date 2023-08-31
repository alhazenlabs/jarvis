import os

def get_openai_key():
    key = os.environ.get("API_KEY")

    if not key:
        raise KeyError("missing Open AI api key. Login to OPEN AI, generate key and update API_KEY environment variable")
    
    return key

def get_porcupine_access_key():
    key = os.environ.get("PICOVOICE_KEY")

    if not key:
        raise KeyError("missing porcupine access key, signup on https://console.picovoice.ai/, and update PICOVOICE_KEY env varaible")

    return key

def get_input_speech_threshold():
    # TODO make this function such that it calculates the speech threshold on the fly
    threshold = int(os.environ.get("DEFAULT_INPUT_SPEECH_THRESHOLD", 600))
    return threshold

class Constants(object):
    API_KEY = get_openai_key()
    DEFAULT_INPUT_SPEECH_THRESHOLD = get_input_speech_threshold()
    PORCUPINE_ACCESS_KEY = get_porcupine_access_key()

    # AI CONSTANTS
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_CONTEXT = "Your name is Jarvis"

    # MEDIA OUTPUT CONSTANTS
    MEDIA_FOLDER = "media/"

    # WAKE CONSTANTS
    DEFAULT_WAKE_KEYWORDS = ['jarvis']
    DEFAULT_WAKE_SENSITIVITIES = [0.5]

    # RECORDER CONSTANTS
    DEFAULT_INPUT_SLEEP_SECONDS = 2
    DEFAULT_INPUT_AUDIO_WIDTH = 4 # 4 bit width, using 2 bit width will given threshold < 10, this makes silence detection harder
    DEFAULT_INPUT_CHANNELS = 1 # Signifies number of channels on the microphone, using 2 channels(stereo) 
                               # will cause a sound sample to be represent in 2 dimension, requiring more memory
    
    DEFAULT_INPUT_LANGUAGE_CODE = "en-IN"
    DEFAULT_RATE = 16000 # Sample rate of the audio stream. Defines the number of audio samples recorded
                         # or played back per second. Common sample rates include 44100 Hz (CD quality)
                         # and 48000 Hz. Higher sample rates allow the capture of higher-frequency audio
                         # but also require more data
    DEFAULT_FRAMES_PER_BUFFER = 1024
    DEFAULT_INPUT_SAMPLES = 50 # This number of samples will be used to calculate the avg intensity of the mic to measure speech threshold
    DEFAULT_SILENCE_LIMIT = 1
    DEFAULT_PERCENTAGE = 1 # 100 %

    # SYNTHESIZE CONSTANTS
    DEFAULT_OUTPUT_ACCENT = "co.uk" # British Accent
    DEFAULT_OUTPUT_LANGUAGE = "en"
    DEFAULT_OUTPUT_IS_SLOW = False
    DEFAULT_OUTPUT_FILE_FORMAT = "{}.mp3"

    # PLAYER CONSTANTS
    DEFAULT_PLAYBACK_RATE = 1.2

    # ERROR
    CONSTANT_SERVER_ERROR = "server_error"
