import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data_api.models import Base, Prompt
from data_api.prompt_dao import PromptDao

class TestPromptDao(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        self.Session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def test_add_prompt(self):
        session = self.Session()
        PromptDao.add_prompt(session, role="user", context="Context", message="User's message")
        session.commit()

        result = session.query(Prompt).first()
        self.assertEqual(result.role, "user")
        self.assertEqual(result.context, "Context")
        self.assertEqual(result.message, "User's message")

    def test_get_prompt(self):
        session = self.Session()
        prompt = Prompt(role="user", context="Context", message="User's message")
        session.add(prompt)
        session.commit()

        result = PromptDao.get_prompt(session, message="User's message")
        self.assertEqual(result.role, "user")
        self.assertEqual(result.context, "Context")
        self.assertEqual(result.message, "User's message")

        result_not_found = PromptDao.get_prompt(session, message="Non-existing message")
        self.assertIsNone(result_not_found)

if __name__ == "__main__":
    unittest.main()
