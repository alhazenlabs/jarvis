import os

from utils.constants import Constants
from data_api.sftt_dao import SfttDao
from utils.logger import LOG

DIRECTORY = Constants.MEDIA_FOLDER + "shard{}/"
SHARD_LENGTH = 2000


def getSpeechFileFromText(session, text, is_input=0):
    # is_input is the parameter to denote if the speech is user generated(1) or system generated(0)
    return SfttDao.addText(session, text, is_input).id

def getDirectoryforSpeechSave(id):
    LOG.debug("checking the id if it classifies for any shards")
    shard = id // SHARD_LENGTH
    output_dir = DIRECTORY.format(shard)
    if not os.path.exists(output_dir):
        LOG.debug(f"shard {shard} output directory doesn't exist, creating it...")
        os.mkdir(output_dir)
    return output_dir
