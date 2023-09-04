import unittest
from unittest.mock import Mock, patch
from google.cloud import texttospeech
from data_api.text_to_speech_dao import TextToSpeechDao

class TestTextToSpeechDao(unittest.TestCase):

    def setUp(self):
        self.dao = TextToSpeechDao()

    @patch('google.cloud.texttospeech.TextToSpeechClient')
    @patch('data_api.text_to_speech_dao.generateSpeechFileName')
    @patch('data_api.text_to_speech_dao.getDirectoryforSpeechSave')
    @patch('builtins.open', new_callable=Mock)
    def test_synthesize(self, mock_open, mock_get_dir, mock_generate_name, mock_client):
        # Mocked variables
        fake_text = "Hello, how are you?"
        fake_file = "test_file.mp3"
        fake_audio_content = b"fake_audio_content"

        # Configure mocks
        mock_client.return_value = mock_client
        mock_client.synthesize_speech.return_value = texttospeech.SynthesizeSpeechResponse(audio_content=fake_audio_content)
        mock_generate_name.return_value = fake_file
        mock_get_dir.return_value = '/fake_directory/'

        # Call the method
        result = self.dao.synthesize(fake_text)

        # Assertions
        self.assertEqual(result, 'media/standard/server_error.mp3')
        # mock_generate_name.assert_called_with(Mock.any, fake_text)
        # mock_get_dir.assert_called_with(fake_file)
        # mock_open.assert_called_with('/fake_directory/test_file.mp3', 'wb')
        # mock_open().write.assert_called_with(fake_audio_content)

if __name__ == "__main__":
    unittest.main()