import struct
import pvporcupine
from utils.constants import Constants

class WakeDetector(object):
    """
    A class for detecting wake keywords using Porcupine keyword spotting.

    Attributes:
        PC (pvporcupine.Porcupine): An instance of Porcupine keyword spotting engine.
        DEFAULT_FRAMES_PER_BUFFER (int): The default number of frames per buffer for audio processing.

    Class Methods:
        detect(frames)
            Detects a wake keyword in the provided audio frames.

    Usage:
        WakeDetector.detect(frames)  # Returns True if a wake keyword is detected, False otherwise.
    """
    
    PC = pvporcupine.create(
        access_key=Constants.PORCUPINE_ACCESS_KEY, 
        keywords=Constants.DEFAULT_WAKE_KEYWORDS,  
        sensitivities=Constants.DEFAULT_WAKE_SENSITIVITIES
        )
    DEFAULT_FRAMES_PER_BUFFER = Constants.DEFAULT_FRAMES_PER_BUFFER # Porcupine complains when frames per buffer is greater than 512

    @classmethod
    def detect(cls, frame):
        """
        Detects a wake keyword in the provided audio frame.

        Args:
            frame (bytes): Audio frame to analyze for wake keyword detection.

        Returns:
            bool: True if a wake keyword is detected, False otherwise.
        """
        pcm = struct.unpack_from("h" * cls.DEFAULT_FRAMES_PER_BUFFER, frame)
        keyword_index = cls.PC.process(pcm)
        return keyword_index >= 0
