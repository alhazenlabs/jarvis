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
        file = r.save_speech(self.SPEECH)

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

if __name__ == "__main__":
    unittest.main()
