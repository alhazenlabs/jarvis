import time
from pygame import mixer

from utils.exceptions import UnsupportedExtenstion
from utils.logger import LOG

class Player(object):
    """
    A class for playing audio files (mp3 or wav) with adjustable playback speed.
    """

    mixr = mixer
    # mixr.pre_init(44100, -16, 1, 512) # Use pre_init instead of init to configure output parameters
    mixr.init()

    @classmethod
    def play(cls, filename):
        """
        Play an audio file (mp3 or wav) at the specified playback speed.

        Args:
            filename (str): The path to the audio file (mp3 or wav) to be played.
            rate (float): The playback speed adjustment factor (default: 1.0).

        Raises:
            UnsupportedExtenstion: If the file extension is not supported.
        """
        if ('.mp3' not in filename) and ('.wav' not in filename):
            raise UnsupportedExtenstion(f"File {filename} extension not supported currently")

        LOG.debug(f"loading and playing the audio file: {filename}")
        cls.mixr.music.load(filename)
        cls.mixr.music.play()
        while cls.mixr.music.get_busy():  # wait for music to finish playing
            time.sleep(1)                 # TODO enhance this to play music on a different thread and start listening till the music is playing
        LOG.debug(f"audio file was played successfully.")
