"""
A file to translate a given question to response
"""
import os
import openai

from data_api.prompt_dao import PromptDao
from utils.logger import LOG
from utils.db import terminating_sn
    
API_KEY = os.environ.get("API_KEY")
DEFAULT_MODEL = "gpt-3.5-turbo"
DEFAULT_CONTEXT = "Your name is Jarvis" # First message to provide as context

openai.api_key = API_KEY

class AI(object):
    def __init__(self, model=DEFAULT_MODEL, context=DEFAULT_CONTEXT):
        self.model = model
        self.messages = [{"role": "system", "content": context}]
        self.context = None
        self.last_message_index = 0
    
    def getResponse(self, message):
        self.messages.append({"role": "user", "content": message})
        LOG.debug(f"sending the messages to AI as {self.messages}")
        chat = openai.ChatCompletion.create(model=self.model, messages=self.messages)
        LOG.debug(f"recieved chat object is :{chat}")
        reply = chat.choices[0].message.content # Use the first choice reply
        self.messages.append({"role": "assistant", "content": reply})
        LOG.info(f"usage is for this chat is: {chat.usage}")
        self._addResponsesToDB()
        return reply

    def _addResponsesToDB(self):
        with terminating_sn() as session:
            if not self.last_message_index and not self.context:
                PromptDao.addPrompt(session, 
                                    self.messages[self.last_message_index]["role"], 
                                    self.messages[self.last_message_index]["content"],
                                    self.messages[self.last_message_index]["content"],
                                    )
                self.context = self.messages[self.last_message_index]["content"]
                self.last_message_index += 1
    
            for index in range(self.last_message_index, len(self.messages)):
                PromptDao.addPrompt(session, 
                                    self.messages[index]["role"],
                                    self.context, 
                                    self.messages[index]["content"]
                                    )
                self.last_message_index += 1

            session.commit()
            