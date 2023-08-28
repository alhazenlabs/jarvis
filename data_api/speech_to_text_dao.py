"""
A module providing data access methods for transcribing speech using the Google Cloud Speech-to-Text API.
"""

from google.cloud import speech_v1p1beta1 as speech
import io

class SpeechToTextDao(object):
    """
    A class providing methods for transcribing speech using the Google Cloud Speech-to-Text API.
    """

    INPUT_LANGUAGE_CODE = "en-IN"
    DEFAULT_RATE = 16000

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

        response = client.recognize(config=config, audio=audio)

        highest_confidence_result = ''
        highest_confidence = 0

        for result in response.results:
            transcript = result.alternatives[0].transcript
            confidence = result.alternatives[0].confidence

            print("Transcript: {}".format(transcript))
            
            if confidence > highest_confidence:
                highest_confidence_result = transcript
                highest_confidence = confidence

        return highest_confidence_result
