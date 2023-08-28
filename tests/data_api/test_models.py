import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_api.models import Base, SpeechFileToText, Prompt

class TestModels(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def test_speech_file_to_text_model(self):
        session = self.Session()
        sftt = SpeechFileToText(text="Converted text", is_input=1)
        session.add(sftt)
        session.commit()

        result = session.query(SpeechFileToText).first()
        self.assertEqual(result.text, "Converted text")
        self.assertEqual(result.is_input, 1)

    def test_prompt_model(self):
        session = self.Session()
        prompt = Prompt(role="user", context="Context", message="User's message")
        session.add(prompt)
        session.commit()

        result = session.query(Prompt).first()
        self.assertEqual(result.role, "user")
        self.assertEqual(result.context, "Context")
        self.assertEqual(result.message, "User's message")

if __name__ == "__main__":
    unittest.main()
