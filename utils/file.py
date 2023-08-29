import os

from pydub import AudioSegment

from data_api.sftt_dao import SfttDao
from utils.constants import Constants
from utils.db import terminating_sn
from utils.logger import LOG
from utils.exceptions import UnsupportedExtenstion
    

DIRECTORY = Constants.MEDIA_FOLDER + "shard{}/"
SHARD_LENGTH = 2000
STANDARD_MEDIA_DIRECTORY = "media/standard"

ERROR_TO_PRESET = {
    Constants.CONSTANT_SERVER_ERROR : STANDARD_MEDIA_DIRECTORY + Constants.DEFAULT_OUTPUT_FILE_FORMAT.format(Constants.CONSTANT_SERVER_ERROR)
    }

def generateSpeechFileName(session, text, is_input=0):
    # is_input is the parameter to denote if the speech is user generated(1) or system generated(0)
    file = SfttDao.add_text(session, text, is_input).id
    return file

def getDirectoryforSpeechSave(id):
    LOG.debug("checking the id if it classifies for any shards")
    shard = id // SHARD_LENGTH
    output_dir = DIRECTORY.format(shard)
    if not os.path.exists(output_dir):
        LOG.debug(f"shard {shard} output directory doesn't exist, creating it...")
        os.mkdir(output_dir)
    return output_dir

def error_response(code):
    return ERROR_TO_PRESET[code]

def mapInputSpeechToText(text, temp_file):
    
    with terminating_sn() as session:
        file = SfttDao.add_text(session, text, 1).id

        folder = getDirectoryforSpeechSave(file)

        if '.wav' not in temp_file:
            raise UnsupportedExtenstion("extension not currently supported")
        
        audio = AudioSegment.from_wav(temp_file)
        
        file = folder + Constants.DEFAULT_OUTPUT_FILE_FORMAT.format(file)
        audio.export(file, format="mp3", bitrate="16k")
        session.commit()
    return file
