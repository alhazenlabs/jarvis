import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_api.models import Base, SpeechFileToText
from data_api.sftt_dao import SfttDao

class TestSfttDao(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def test_add_text(self):
        session = self.Session()
        sftt = SfttDao.add_text(session, text="Converted text", is_input=1)
        session.commit()

        result = session.query(SpeechFileToText).first()
        self.assertEqual(result.text, "Converted text")
        self.assertEqual(result.is_input, 1)
        self.assertEqual(result, sftt)

    def test_get_speech_file(self):
        session = self.Session()
        sftt = SpeechFileToText(text="Converted text", is_input=1)
        session.add(sftt)
        session.commit()

        result = SfttDao.get_speech_file(session, text="Converted text")
        self.assertEqual(result.text, "Converted text")
        self.assertEqual(result.is_input, 1)

        result_not_found = SfttDao.get_speech_file(session, text="Non-existing text")
        self.assertIsNone(result_not_found)

if __name__ == "__main__":
    unittest.main()
