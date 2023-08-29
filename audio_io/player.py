from pydub import AudioSegment
from pydub.playback import play

from utils.constants import Constants
from utils.exceptions import UnsupportedExtenstion

class Player(object):
    """
    A class for playing audio files (mp3 or wav) with adjustable playback speed.
    """

    DEFAULT_RATE = Constants.DEFAULT_PLAYBACK_RATE

    @staticmethod
    def play(filename, rate=DEFAULT_RATE):
        """
        Play an audio file (mp3 or wav) at the specified playback speed.

        Args:
            filename (str): The path to the audio file (mp3 or wav) to be played.
            rate (float): The playback speed adjustment factor (default: 1.0).

        Raises:
            UnsupportedExtenstion: If the file extension is not supported.
        """
        audio = ''
        if '.mp3' in filename:
            audio = AudioSegment.from_mp3(filename)
        elif '.wav' in filename:
            audio = AudioSegment.from_wav(filename)
        else:
            raise UnsupportedExtenstion(f"File {filename} extension not supported currently")
        
        audio = audio.speedup(playback_speed=rate)
        play(audio)
