import os
import time
from gtts import gTTS
from db import load_db, terminating_sn
from models import SpeechFileToText
from pygame import mixer

from logger import LOG


ACCENT = "co.uk"
LANGUAGE = "en"
IS_SLOW = False
DIRECTORY = "output/shard{}/"
FILE_FORMAT = "{}.mp3"
SHARD_LENGTH = 2000

# text = "Hello sir, how can i help you today"
text = "Hey there, how are you doing today"

def getSpeechFileFromText(session, text, is_input=0):
    # is_input is the parameter to denote if the speech is user generated(1) or system generated(0)
    sftt = SpeechFileToText(text, is_input)
    session.add(sftt)
    session.flush()
    return sftt.id

def getDirectoryforSpeechSave(id):
    LOG.debug("checking the id if it classifies for any shards")
    shard = id // SHARD_LENGTH
    output_dir = DIRECTORY.format(shard)
    if not os.path.exists(output_dir):
        LOG.debug(f"shard {shard} output directory doesn't exist, creating it...")
        os.mkdir(output_dir)
    return output_dir


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
            self.tts.save(file_path)
            session.commit()
        return file_path

    def save_and_play(self):
        file = self._save()
        self.mixer.music.load(file)
        self.mixer.music.play()
        while self.mixer.music.get_busy():  # wait for music to finish playing
            time.sleep(1)

text = """
During my tenure at Sophos, I spearheaded the development of a comprehensive configuration management service from the ground up. Leveraging GoYang as a yang data model parser, I established a robust system that validated and persisted incoming configuration data into a Postgres database. I meticulously crafted proto message descriptions and RPC calls to facilitate seamless utilization of the configuration management APIs by internal applications. To optimize performance, we implemented Redis for caching less volatile API calls. Our technology stack also featured Loki for application logs, Jaeger for trace persistence across transactions, and Prometheus for resource monitoring. All these components were seamlessly containerized using Docker and seamlessly orchestrated within a cloud environment through Kubernetes.

This initiative not only showcased my proficiency in orchestrating the entire development process but also underscored my ability to implement cutting-edge technologies and leverage containerization and orchestration techniques for efficient deployment and management.
"""  
    

if __name__ == "__main__":
    # Connect to a sqllite-db
    from logger import LOG
    LOG.info(text)
    load_db()

    tt = TextToSpeech(text)
    tt.save_and_play()
    
