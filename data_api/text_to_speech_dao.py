from google.cloud import texttospeech

from utils.constants import Constants
from utils.db import terminating_sn
from utils.file import generateSpeechFileName, getDirectoryforSpeechSave, error_response
from utils.logger import LOG


class TextToSpeechDao(object):
    """
    A class for converting text to speech using the Google Text-to-Speech API.

    Attributes:
        ACCENT (str): The accent of the generated speech.
        LANGUAGE (str): The language of the generated speech.
        FILE_FORMAT (str): The default file format for saving generated speech.
        client (texttospeech.TextToSpeechClient): The Google Text-to-Speech client instance.
        voice (texttospeech.VoiceSelectionParams): The voice selection parameters.
        audio_config (texttospeech.AudioConfig): The audio configuration for generated speech.

    Methods:
        synthesize(text): Converts the provided text into speech and saves it to a file.

    Usage:
        tts_dao = TextToSpeechDao()
        file_path = tts_dao.synthesize("Hello, how are you?")
    """
     
    ACCENT = Constants.DEFAULT_OUTPUT_ACCENT
    FILE_FORMAT = Constants.DEFAULT_OUTPUT_FILE_FORMAT

    client = texttospeech.TextToSpeechClient()

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code=Constants.DEFAULT_OUTPUT_LANGUAGE, ssml_gender=Constants.DEFAULT_OUTPUT_ACCENT
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
        # speaking_rate, sample_rate_hertz 
    )

    @classmethod
    def synthesize(cls, text):
        """
        Converts the provided text into speech and saves it to a file.

        Args:
            text (str): The text to be converted into speech.

        Returns:
            str: The file path where the generated speech is saved.

        Raises:
            Exception: If an error occurs during the conversion.
        """
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
    