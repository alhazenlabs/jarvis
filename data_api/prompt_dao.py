from data_api.models import Prompt

class PromptDao(object):

    @staticmethod
    def addPrompt(session, role, context, message):
        prompt = Prompt(role, context, message)
        session.add(prompt)
        session.flush()
    
    @staticmethod
    def getPrompt(session, message):
        return session.query(Prompt).filter(Prompt.message == message).first()