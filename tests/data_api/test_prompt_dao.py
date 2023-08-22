import unittest

from data_api.prompt_dao import PromptDao
from utils.db import terminating_sn


class TestPromptDao(unittest.TestCase):

    def testAddPrompt(self):
        role = "system"
        context = "your name is jarvis"
        message = "what are the elemental composition of air on earth"

        with terminating_sn() as session:
            PromptDao.addPrompt(session, role, context, message)
            session.commit()

            fetched_prompt = PromptDao.getPrompt(session, message)

            self.assertEqual(fetched_prompt.role, role)
            self.assertEqual(fetched_prompt.context, context)

