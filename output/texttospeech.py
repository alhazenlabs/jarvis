import time
from gtts import gTTS
from pygame import mixer

from utils.db import terminating_sn
from utils.file import getSpeechFileFromText, getDirectoryforSpeechSave
from utils.logger import LOG


ACCENT = "co.uk"
LANGUAGE = "en"
IS_SLOW = False
FILE_FORMAT = "{}.mp3"


class TextToSpeech(object):
    def __init__(self, text):
        self.text = text
        self.mixer = mixer
        self.tts = gTTS(text=self.text, lang=LANGUAGE, tld=ACCENT, slow=IS_SLOW)
        self.mixer.init()
    
    def _save(self):
        with terminating_sn() as session:
            id = getSpeechFileFromText(session, self.text)
            file_path = getDirectoryforSpeechSave(id) + FILE_FORMAT.format(id)
            LOG.debug(f"saving the file to speech file to: {file_path}")
            self.tts.save(file_path)
            session.commit()
        return file_path

    def save_and_play(self):
        file = self._save()
        LOG.debug(f"loading and playing the speech file: {file}")
        self.mixer.music.load(file)
        self.mixer.music.play()
        while self.mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)
        LOG.debug(f"speech file was played successfully...")

