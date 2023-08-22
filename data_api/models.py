"""
A file to store all the DB Models
"""

from sqlalchemy import Column, Index
from sqlalchemy.dialects.sqlite import INTEGER, TEXT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class SpeechFileToText(Base):
    __tablename__ = 'sftt' # Shot form for Speech file to text
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
        return f"File Name={self.id} Is Input={self.is_input} Text={self.text}"
    
class Prompt(Base):
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
        return f"Id={self.id} role={self.role} context={self.context} message={self.message}"
