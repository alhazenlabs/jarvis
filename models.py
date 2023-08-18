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
        Index('id_index', 'id'),
        Index('is_input_index', 'is_input')
    )

    def __init__(self, text, is_input=0):
        self.text = text
        self.is_input = is_input

    def __repr__(self):
        return "File Name={} Is Input={} Text={}".format(self.id, self.text, self.is_input)
