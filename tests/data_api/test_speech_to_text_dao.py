import os
import unittest
from unittest.mock import Mock, patch

from audio_io.recorder import Recorder
from data_api.speech_to_text_dao import SpeechToTextDao

class TestSpeechToTextDao(unittest.TestCase):
    SPEECH = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00\x04\x00\x00\x00\x04\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00'

    @patch("google.cloud.speech_v1p1beta1.SpeechClient")
    def test_transcribe_speech(self, mock_speech_client):
        r = Recorder()
        file = r.save_speech(self.SPEECH, 2)

        mock_client_instance = Mock()
        mock_speech_client.return_value = mock_client_instance

        mock_response = Mock()
        mock_response.results = [
            Mock(alternatives=[Mock(transcript="Hello", confidence=0.9)]),
            Mock(alternatives=[Mock(transcript="World", confidence=0.8)])
        ]
        mock_client_instance.recognize.return_value = mock_response

        result = SpeechToTextDao.transcribe_speech(file)

        self.assertEqual(result, "Hello")
        mock_speech_client.assert_called_once()
        mock_client_instance.recognize.assert_called_once()

        os.remove(file)

    def test_remove_wake_word(self):
        answer = ", How are you doing today"

        sentence1 = "Hey Jarvis, How are you doing today"
        sentence2 = "Hey JARVIS, How are you doing today"
        sentence3 = "Hey Alexa, How are you doing today"
        sentence4 = "Hey Bumblebee, How are you doing today"

        self.assertEqual(answer, SpeechToTextDao.remove_wake_word(sentence1))
        self.assertEqual(answer, SpeechToTextDao.remove_wake_word(sentence2))
        self.assertEqual(answer, SpeechToTextDao.remove_wake_word(sentence3))
        self.assertEqual(sentence4, SpeechToTextDao.remove_wake_word(sentence4))


if __name__ == "__main__":
    unittest.main()
