"""
A module containing the database models for speech-to-text data and prompts.
"""

from sqlalchemy import Column, Index
from sqlalchemy.dialects.sqlite import INTEGER, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SpeechFileToText(Base):
    """
    Represents a speech file converted to text and stored in the database.

    Attributes:
        id (int): Primary key for the table.
        text (str): The converted text from the speech file.
        is_input (int): Indicator if the text is input (1) or not (0).

    __tablename__ = 'sftt'
    """

    __tablename__ = 'sftt'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    text = Column(TEXT)
    is_input = Column(INTEGER)

    __table_args__ = (
        Index('sftt_id_index', 'id'),
        Index('sftt_is_input_index', 'is_input')
    )

    def __init__(self, text, is_input=0):
        self.text = text
        self.is_input = is_input

    def __repr__(self):
        return f"File ID={self.id} Is Input={self.is_input} Text={self.text}"

class Prompt(Base):
    """
    Represents a user or assistant prompt stored in the database.

    Attributes:
        id (int): Primary key for the table.
        role (str): The role of the prompt (user or assistant).
        context (str): The context of the prompt.
        message (str): The message of the prompt (input/output).

    __tablename__ = 'prompt'
    """

    __tablename__ = 'prompt'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    role = Column(TEXT)
    context = Column(TEXT)
    message = Column(TEXT)

    def __init__(self, role, context, message):
        self.role = role
        self.context = context
        self.message = message

    __table_args__ = (
        Index('prompt_id_index', 'id'),
        Index('prompt_context_index', 'context')
    )

    def __repr__(self):
        return f"Prompt ID={self.id} Role={self.role} Context={self.context} Message={self.message}"
