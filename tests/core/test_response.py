import os
import json
import shutil
import unittest

from types import SimpleNamespace
from unittest.mock import patch

import utils.db

TESTS_MEDIA = "tests/media/"
utils.db.DATABASE = TESTS_MEDIA + "jarvis.db"

from core.response import AI

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

class TestAI(unittest.TestCase):

    def setUp(self) -> None:
        print("loading the test database")
        utils.db.load_db()
    
    def tearDown(self) -> None:
        print("deleting the test database")
        delete_contents(TESTS_MEDIA)

    @patch('openai.ChatCompletion')
    def test_get_response(self, MockClass1):
        MockClass1.create.return_value = self.get_ai_response()
        ai = AI()
        response = ai.getResponse("test_response")
        self.assertEqual(self.get_ai_response().choices[0].message.content, response)
        

    def get_ai_response(self, file="tests/response.json"):
        data = json.load(open(file), object_hook=lambda d: SimpleNamespace(**d))
        print(data)
        return data

