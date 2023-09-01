import time
import requests
from google.cloud import texttospeech
# from gtts import gTTS, gTTSError

from utils.constants import Constants
from utils.db import terminating_sn
from utils.file import generateSpeechFileName, getDirectoryforSpeechSave, error_response
from utils.logger import LOG


# def with_retry(function, *args, retries=3, backoff=1):
#     for _ in range(retries):
#         try:
#             return function(*args)
#         except (requests.ConnectionError, gTTSError) as e:
#             if isinstance(e, gTTSError) and "Failed to connect" not in str(e):
#                 raise e

#             LOG.info("connection error. retrying in a moment.")
#             time.sleep(backoff)
    
#     LOG.info("max retries exceeded. translation failed")
#     raise gTTSError("max retries exceeded. translation failed")



class TextToSpeechDao(object):
    ACCENT = Constants.DEFAULT_OUTPUT_ACCENT
    LANGUAGE = Constants.DEFAULT_OUTPUT_LANGUAGE
    IS_SLOW = Constants.DEFAULT_OUTPUT_IS_SLOW
    FILE_FORMAT = Constants.DEFAULT_OUTPUT_FILE_FORMAT

    client = texttospeech.TextToSpeechClient()

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-GB", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    @classmethod
    def synthesize(cls, text):
        try:
            synthesis_input = texttospeech.SynthesisInput(text=text)
            with terminating_sn() as session:
                file = generateSpeechFileName(session, text)
                file_path = getDirectoryforSpeechSave(file) + cls.FILE_FORMAT.format(file)

                # Perform the text-to-speech request on the text input with the selected voice parameters 
                # and audio file type Set the text input to be synthesized
                response = cls.client.synthesize_speech(
                    input=synthesis_input, voice=cls.voice, audio_config=cls.audio_config
                )

                # The response's audio_content is binary.
                with open(file_path, "wb") as out:
                    # Write the response to the output file.
                    out.write(response.audio_content)
                    LOG.info(f'Audio content written to file {file_path}')

                session.commit()
        except Exception as e:
            LOG.exception("error occurred while translating text to speech", e)
            return error_response(Constants.CONSTANT_SERVER_ERROR)

        return file_path
    