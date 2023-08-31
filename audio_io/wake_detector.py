import os
import struct
import pyaudio
import pvporcupine
from utils.constants import Constants


# AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)


# Parameters for PyAudio
pa = None
audio_stream = None
pa_format = pyaudio.paInt16
pa_channels = 1
pa_rate = 16000
pa_frames_per_buffer = 512

class WakeDetector(object):
    
    PC = pvporcupine.create(
        access_key=Constants.PORCUPINE_ACCESS_KEY, 
        keywords=Constants.DEFAULT_WAKE_KEYWORDS,  
        sensitivities=Constants.DEFAULT_WAKE_SENSITIVITIES
        )
    DEFAULT_FRAMES_PER_BUFFER = Constants.DEFAULT_FRAMES_PER_BUFFER # Porcupine complains when frames per buffer is greater than 512

    @classmethod
    def detect(cls, frames):
        pcm = struct.unpack_from("h" * cls.DEFAULT_FRAMES_PER_BUFFER, frames)
        keyword_index = cls.PC.process(pcm)
        return keyword_index >= 0


if __name__== "__main__":
    print("Listening... Press Ctrl+C to exit")

    pa = pyaudio.PyAudio()

    # Open audio stream
    audio_stream = pa.open(
        rate=pa_rate,
        channels=pa_channels,
        format=pa_format,
        input=True,
        frames_per_buffer=pa_frames_per_buffer,
    )

    try:
        while True:
            frames = audio_stream.read(pa_frames_per_buffer)
            if WakeDetector.detect(frames):
                print("jarvis detected")
                print("application logic should be below")
    except KeyboardInterrupt:
        print("Stopping... the application")
    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()