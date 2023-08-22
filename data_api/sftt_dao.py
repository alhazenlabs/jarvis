from data_api.models import SpeechFileToText

class SfttDao(object):

    @staticmethod
    def addText(session, text, is_input=0):
        sftt = SpeechFileToText(text, is_input)
        session.add(sftt)
        session.flush()
        return sftt

    @staticmethod
    def getSpeechFile(session, text):
        return session.query(SpeechFileToText).filter(SpeechFileToText.text == text).first()
