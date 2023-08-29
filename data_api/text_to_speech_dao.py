import time
from gtts import gTTS, gTTSError

from utils.constants import Constants
from utils.db import terminating_sn
from utils.file import generateSpeechFileName, getDirectoryforSpeechSave, error_response
from utils.logger import LOG


class TextToSpeechDao(object):
    ACCENT = Constants.DEFAULT_OUTPUT_ACCENT
    LANGUAGE = Constants.DEFAULT_OUTPUT_LANGUAGE
    IS_SLOW = Constants.DEFAULT_OUTPUT_IS_SLOW
    FILE_FORMAT = Constants.DEFAULT_OUTPUT_FILE_FORMAT

    @classmethod
    def synthesize(cls, text):

        tts = gTTS(text=text, lang=cls.LANGUAGE, tld=cls.ACCENT, slow=cls.IS_SLOW)

        try:
            with terminating_sn() as session:
                file = generateSpeechFileName(session, text)
                file_path = getDirectoryforSpeechSave(file) + cls.FILE_FORMAT.format(file)
                tts.save(file_path)
                session.commit()
        except gTTSError as e:
            LOG.exception("error occurred while translating text to speech", e)
            return error_response(Constants.CONSTANT_SERVER_ERROR)

        return file_path
    