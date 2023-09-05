import os, shutil
import unittest
from unittest.mock import patch, Mock
from data_api.ai_dao import AiDao

import utils.db


TESTS_MEDIA = "tests/media/"
utils.db.DATABASE = TESTS_MEDIA + "jarvis.db"


def delete_contents(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

class TestAiDao(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("loading the test database")
        if not os.path.exists(TESTS_MEDIA):
            os.mkdir(TESTS_MEDIA)
        utils.db.load_db()
        cls.ai = AiDao()
    
    @classmethod
    def tearDownClass(cls) -> None:
        print("deleting the test database")
        delete_contents(TESTS_MEDIA)

    @patch("openai.ChatCompletion.create")
    def test_get_response(self, mock_create):
        mock_create.return_value = Mock(choices=[Mock(message=Mock(content="AI response"))])
        response = self.ai._get_response("Hello")
        self.assertEqual(response, "AI response")
    
    @patch("data_api.prompt_dao.PromptDao.add_prompt")
    def test_add_responses_to_db(self, mock_add_prompt):
        self.ai.context = "Test Context"
        self.ai._save_responses()
        self.assertTrue(mock_add_prompt.called)

    @patch("data_api.ai_dao.AiDao._get_response")
    @patch("data_api.ai_dao.AiDao._save_responses")
    def test_get_and_save_response(self, mock_get, mock_save):
        self.ai.get_and_save_response("test text")
        self.assertTrue(mock_get.called)
        self.assertTrue(mock_save.called)
        
if __name__ == "__main__":
    unittest.main()
