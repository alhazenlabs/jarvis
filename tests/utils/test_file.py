import os
import shutil
import unittest
import utils.db
import utils.file
from unittest.mock import patch, Mock
from pydub import AudioSegment
from data_api.sftt_dao import SfttDao
from utils.constants import Constants
from utils.exceptions import UnsupportedExtenstion

class TestYourModule(unittest.TestCase):
    def setUp(self):
        Constants.MEDIA_FOLDER = "/tmp/test_media_folder/"
        Constants.STANDARD_MEDIA_DIRECTORY = "/tmp/standard_media_directory/"
        os.makedirs(Constants.MEDIA_FOLDER, exist_ok=True)
        os.makedirs(Constants.STANDARD_MEDIA_DIRECTORY, exist_ok=True)
        utils.db.DATABASE = Constants.MEDIA_FOLDER + Constants.SQLITE_DB
        utils.db.load_db()
        utils.file.DIRECTORY = Constants.MEDIA_FOLDER + Constants.DIRECTORY_PREFIX
        utils.file.STANDARD_MEDIA_DIRECTORY = Constants.STANDARD_MEDIA_DIRECTORY

    def tearDown(self):
        shutil.rmtree(Constants.MEDIA_FOLDER)
        shutil.rmtree(Constants.STANDARD_MEDIA_DIRECTORY)

    def test_generateSpeechFileName(self):
        with utils.db.terminating_sn() as session:
            generated_id = utils.file.generateSpeechFileName(session, "Test Speech", is_input=1)
            self.assertEqual(generated_id, 1)

    def test_getDirectoryforSpeechSave(self):
        generated_dir = utils.file.getDirectoryforSpeechSave(150)
        expected_dir = os.path.join(Constants.MEDIA_FOLDER, "shard0/")
        self.assertEqual(generated_dir, expected_dir)

    def test_error_response(self):
        error_code = "500"
        response_path = utils.file.error_response(error_code)
        expected_path = os.path.join(Constants.STANDARD_MEDIA_DIRECTORY, "500.mp3")
        self.assertEqual(response_path, expected_path)

    @patch("utils.file.AudioSegment.from_wav")
    @patch("utils.file.terminating_sn")
    @patch("utils.file.SfttDao.add_text")
    def test_mapInputSpeechToText(self, mock_add_text, mock_terminating_sn, mock_from_wav):
        text = "Test Speech"
        temp_file = "/tmp/test.wav"
        mock_session = Mock()
        mock_add_text.return_value.id = 1
        mock_terminating_sn.return_value.__enter__.return_value = mock_session
        mock_from_wav.return_value = AudioSegment.empty()

        output_file = utils.file.mapInputSpeechToText(text, temp_file)

        expected_output_file = os.path.join(
            Constants.MEDIA_FOLDER, "shard0", "1.mp3"
        )
        self.assertEqual(output_file, expected_output_file)
        mock_add_text.assert_called_with(mock_session, text, 1)

    def test_mapInputSpeechToText_unsupported_extension(self):
        text = "Test Speech"
        temp_file = "/tmp/test.txt"  # Unsupported extension
        with self.assertRaises(UnsupportedExtenstion):
            utils.file.mapInputSpeechToText(text, temp_file)

if __name__ == "__main__":
    unittest.main()
