"""
A module providing data access methods for the Prompt model.
"""

from data_api.models import Prompt

class PromptDao(object):
    """
    A class providing data access methods for the Prompt model.
    """

    @staticmethod
    def add_prompt(session, role, context, message):
        """
        Adds a new prompt to the database.

        Args:
            session (Session): The SQLAlchemy session.
            role (str): The role of the prompt (user or assistant).
            context (str): The context of the prompt.
            message (str): The content of the prompt.
        """
        prompt = Prompt(role, context, message)
        session.add(prompt)
        session.flush()

    @staticmethod
    def get_prompt(session, message):
        """
        Retrieves a prompt from the database based on the provided message.

        Args:
            session (Session): The SQLAlchemy session.
            message (str): The message content to search for.

        Returns:
            Prompt: The retrieved Prompt instance, or None if not found.
        """
        return session.query(Prompt).filter(Prompt.message == message).first()
