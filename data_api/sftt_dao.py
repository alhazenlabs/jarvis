"""
A module providing data access methods for the SpeechFileToText model.
"""

from data_api.models import SpeechFileToText

class SfttDao(object):
    """
    A class providing data access methods for the SpeechFileToText model.
    """

    @staticmethod
    def add_text(session, text, is_input=0):
        """
        Adds a new speech-to-text record to the database.

        Args:
            session (Session): The SQLAlchemy session.
            text (str): The converted text from the speech file.
            is_input (int, optional): Indicator if the text is input (1) or not (0). Default is 0.

        Returns:
            SpeechFileToText: The added SpeechFileToText instance.
        """
        sftt = SpeechFileToText(text, is_input)
        session.add(sftt)
        session.flush()
        return sftt

    @staticmethod
    def get_speech_file(session, text):
        """
        Retrieves a speech file record from the database based on the provided text.

        Args:
            session (Session): The SQLAlchemy session.
            text (str): The text content to search for.

        Returns:
            SpeechFileToText: The retrieved SpeechFileToText instance, or None if not found.
        """
        return session.query(SpeechFileToText).filter(SpeechFileToText.text == text).first()
