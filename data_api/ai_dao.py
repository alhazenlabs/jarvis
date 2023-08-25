"""
A module to translate a given question to a response using OpenAI's GPT-3 model.
"""

import openai

from data_api.prompt_dao import PromptDao
from utils.constants import Constants
from utils.logger import LOG
from utils.db import terminating_sn

openai.api_key = Constants.API_KEY

class AiDao(object):
    """
    AI Data access object class for translating user messages to AI-generated responses using OpenAI's GPT-3 model.

    Args:
        model (str): The GPT-3 model to use. Default is "gpt-3.5-turbo".
        context (str): The initial context message to provide to the AI. Default is "Your name is Jarvis".

    Attributes:
        DEFAULT_MODEL (str): The default GPT-3 model.
        DEFAULT_CONTEXT (str): The default initial context message.
    """

    DEFAULT_MODEL = Constants.DEFAULT_MODEL
    DEFAULT_CONTEXT = Constants.DEFAULT_CONTEXT

    def __init__(self, model=DEFAULT_MODEL, context=DEFAULT_CONTEXT):
        self.model = model
        self.context = None
        self.last_message_index = 0
        self.messages = [{"role": "system", "content": context}] # TODO this can overflow and lead to crashes, use deque

    def _get_response(self, message):
        """
        Translates a user message to an AI-generated response.

        Args:
            message (str): The user's message.

        Returns:
            str: The AI-generated response.
        """
        self.messages.append({"role": "user", "content": message})
        LOG.debug(f"sending the messages to AI as {self.messages}")

        chat = openai.ChatCompletion.create(model=self.model, messages=self.messages)
        LOG.debug(f"received chat object is: {chat}")

        reply = chat.choices[0].message.content
        LOG.info(f"usage for this chat is: {chat.usage}")

        self.messages.append({"role": "assistant", "content": reply})
        return reply

    def _save_responses(self):
        """
        Adds user and assistant responses to the database.
        """
        with terminating_sn() as session:
            if not self.last_message_index and not self.context:
                PromptDao.addPrompt(session,
                                    self.messages[self.last_message_index]["role"],
                                    self.messages[self.last_message_index]["content"],
                                    self.messages[self.last_message_index]["content"])
                self.context = self.messages[self.last_message_index]["content"]
                self.last_message_index += 1

            for index in range(self.last_message_index, len(self.messages)):
                PromptDao.addPrompt(session,
                                    self.messages[index]["role"],
                                    self.context,
                                    self.messages[index]["content"])
                self.last_message_index += 1

            session.commit()
    
    def get_and_save_response(self, message):
        """
        Translates a user message to an AI-generated response and saves it into db

        Args:
            message (str): The user's message.

        Returns:
            str: The AI-generated response.
        """
        response = self._get_response(message)
        self._save_responses()
        return response

