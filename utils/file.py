import os

from pydub import AudioSegment

from data_api.sftt_dao import SfttDao
from utils.constants import Constants
from utils.db import terminating_sn
from utils.logger import LOG
from utils.exceptions import UnsupportedExtenstion
    

DIRECTORY = Constants.MEDIA_FOLDER + Constants.DIRECTORY_PREFIX
SHARD_LENGTH = Constants.SHARD_LENGTH
STANDARD_MEDIA_DIRECTORY = Constants.STANDARD_MEDIA_DIRECTORY


def generateSpeechFileName(session, text, is_input=0):
    """
    Generate a unique filename for saving speech audio files.

    Args:
        session (sqlalchemy.orm.session.Session): SQLAlchemy session for database operations.
        text (str): The text to be converted to speech.
        is_input (int, optional): Flag to indicate if the speech is user-generated (1) or system-generated (0).
                                  Defaults to 0.

    Returns:
        int: The generated filename ID.
    """
    file = SfttDao.add_text(session, text, is_input).id
    return file


def getDirectoryforSpeechSave(id):
    """
    Get the directory path for saving speech audio files based on the given ID.

    Args:
        id (int): The ID used to determine the directory path.

    Returns:
        str: The directory path for saving the audio file.
    """
    LOG.debug("checking the id if it classifies for any shards")
    shard = id // SHARD_LENGTH
    output_dir = DIRECTORY.format(shard)
    if not os.path.exists(output_dir):
        LOG.debug(f"shard {shard} output directory doesn't exist, creating it...")
        os.mkdir(output_dir)
    return output_dir


def error_response(code):
    """
    Generate an error response file path based on the provided error code.

    Args:
        code (str): The error code used to generate the response path.

    Returns:
        str: The path to the error response file.
    """
    return STANDARD_MEDIA_DIRECTORY + Constants.DEFAULT_OUTPUT_FILE_FORMAT.format(code)


def mapInputSpeechToText(text, temp_file):
    """
    Map input speech audio to text and save it as an MP3 file.

    Args:
        text (str): The text corresponding to the input speech.
        temp_file (str): The path to the input speech audio file (WAV format).

    Returns:
        str: The path to the generated MP3 file containing the mapped text.
    
    Raises:
        UnsupportedExtenstion: If the provided audio file extension is not supported (only WAV is supported).
    """
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
