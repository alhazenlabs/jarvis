"""
A module providing data access methods for transcribing speech using the Google Cloud Speech-to-Text API.
"""
import io
from google.cloud import speech_v1p1beta1 as speech

from utils.constants import Constants
from utils.exceptions import SttError
from utils.logger import LOG

class SpeechToTextDao(object):
    """
    A class providing methods for transcribing speech using the Google Cloud Speech-to-Text API.
    """

    INPUT_LANGUAGE_CODE = Constants.DEFAULT_INPUT_LANGUAGE_CODE
    DEFAULT_RATE = Constants.DEFAULT_RATE
    DEFAULT_WAKE_WORDS = Constants.DEFAULT_WAKE_KEYWORDS

    @classmethod
    def transcribe_speech(cls, speech_file_path):
        """
        Transcribes speech from an audio file using the Google Cloud Speech-to-Text API.

        Args:
            speech_file_path (str): The path to the audio file to transcribe.

        Returns:
            str: The transcribed text.
        """
        client = speech.SpeechClient()

        with io.open(speech_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=cls.DEFAULT_RATE,
            language_code=cls.INPUT_LANGUAGE_CODE,
        )

        try:
            response = client.recognize(config=config, audio=audio)
        except Exception as e:
            LOG.exception(f"exception occurred while transcribing audio: {e}")
            raise SttError("transcription of input audio failed")

        highest_confidence_result = ''
        highest_confidence = 0

        for result in response.results:
            transcript = result.alternatives[0].transcript
            confidence = result.alternatives[0].confidence

            print("Transcript: {}".format(transcript))
            
            if confidence > highest_confidence:
                highest_confidence_result = transcript
                highest_confidence = confidence

        return cls.remove_wake_word(highest_confidence_result)

    @classmethod
    def remove_wake_word(cls, sentence):
        if not sentence:
            raise SttError("transcribed sentence is empty")

        for word in cls.DEFAULT_WAKE_WORDS:
            temp_sentence = cls.get_sentence_after(word, sentence)

            if len(temp_sentence) < len(sentence):
                sentence = temp_sentence

        return temp_sentence
    
    @staticmethod
    def get_sentence_after(word, sentence):
        for index in range(len(sentence) - len(word)):
            if word.lower() == sentence[index: index + len(word)].lower():
                return sentence[index + len(word):]
        
        return sentence
