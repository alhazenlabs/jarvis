import math
import time
import pyaudio
import audioop
import wave

from collections import deque
from utils.logger import LOG


class Recorder(object):
    DEFAULT_SLEEP_SECONDS = 2

    DEFAULT_FRAMES_PER_BUFFER = 1024  # CHUNKS of bytes to read each time from mic
    DEFAULT_FORMAT = pyaudio.paInt16
    DEFAULT_WIDTH = 4 # Width parameter specifies the number of bytes used 
                      # for a audio sample, (4 = 32 bit) will provide higher variations
    DEFAULT_CHANNELS = 1
    DEFAULT_RATE = 16000
    DEFAULT_THRESHOLD = 500
    DEFAULT_INPUT = True # True is for recording the sound

    DEFAULT_SAMPLE = 50 # Number of samples for measuring audio intensity

    DEFAULT_SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                               # only silence is recorded. When this time passes the
                               # recording finishes and the file is delivered.

    DEFAULT_PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                              # is detected, how much of previously recorded audio is
                              # prepended. This helps to prevent chopping the beggining
                              # of the phrase.

    DEFAULT_PERCENTAGE = 1 # Signifies 100%

    def __init__(self, format=DEFAULT_FORMAT, channels=DEFAULT_CHANNELS, rate=DEFAULT_RATE, 
                 input=DEFAULT_INPUT, frames_per_buffer=DEFAULT_FRAMES_PER_BUFFER):
        """
        This function provides an interface to underlying pyaudio library for recording sound.

        :param format: The audio data format. Determines how audio samples are represented.
                    Common formats include paInt16 for 16-bit signed integers, paFloat32 for
                    32-bit floating-point numbers, and others.
        :param channels: Number of audio channels. For example, mono audio has one channel,
                        and stereo audio has two channels. Some systems support more channels
                        for surround sound configurations.
        :param rate: Sample rate of the audio stream. Defines the number of audio samples recorded
                    or played back per second. Common sample rates include 44100 Hz (CD quality)
                    and 48000 Hz. Higher sample rates allow the capture of higher-frequency audio
                    but also require more data.
        :param input: Specifies whether the stream is for input or output. Set it to True for an
                    input (recording) stream and False for an output (playback) stream.
        :param frames_per_buffer: Number of audio frames per buffer. A frame consists of samples
                                from all channels at a given point in time. This parameter affects
                                the buffer size and can impact latency and performance. Smaller
                                buffer sizes may reduce latency but could increase the chance of
                                buffer underruns or overruns.
                                
        """
        self.format =  format
        self.channels = channels
        self.rate = rate
        self.input = input
        self.frames_per_buffer = frames_per_buffer

        self._pyaudio = pyaudio.PyAudio()
    
    def record(self, threshold=DEFAULT_THRESHOLD):

        """
        Listens to Microphone, records in input and saves it to a wav file
        """

        LOG.info("* Listening mic. ")
        stream = self._pyaudio.open(format=self.format, channels=self.channels, rate=self.rate,
                                    input=self.input,frames_per_buffer=self.frames_per_buffer)
        
        buffers = self.rate // self.frames_per_buffer
        window = deque(maxlen=self.DEFAULT_SILENCE_LIMIT * buffers) # when all the samples in the window falls below threshold, we can assume a silence 
        window.append(threshold + 1)
        audio2send = bytearray()

        time.sleep(self.DEFAULT_SLEEP_SECONDS) 
        # sleeping for 2 seconds to make sure the program doesn't exit before we have started speaking

        LOG.info("Starting record of phrase")
        while (self.speech_detected(window, threshold)):
            cur_data = stream.read(self.frames_per_buffer)
            window.append(self.get_rms(cur_data)) # Calculating RMS value of the current stream
            audio2send.extend(cur_data)

        LOG.info("Done recording...")
        filename = self.save_speech(audio2send)
        LOG.info(f"Saved file {filename}")
        stream.close()
        self._pyaudio.terminate()

        return filename
    
    @staticmethod
    def speech_detected(window, threshold=DEFAULT_THRESHOLD):
        return sum([sound > threshold for sound in window]) > 0
    
    @staticmethod
    def get_rms(data, width=DEFAULT_WIDTH):
        # LOG.debug(f"current data for reading the rms: {data}")
        return math.sqrt(abs(audioop.avg(data, width)))

    
    def avg_intensity(self, samples=DEFAULT_SAMPLE, percentage=DEFAULT_PERCENTAGE, stream=None):
        """ 
        Gets average audio intensity of your mic sound.
        """

        LOG.info("Getting intensity values from mic")
        LOG.debug(f"Microphone info: {self._pyaudio.get_default_input_device_info()}")

        if not stream:
            stream = self._pyaudio.open(format=self.format, channels=self.channels, rate=self.rate, 
                                        input=self.input, frames_per_buffer=self.frames_per_buffer)

        values = [self.get_rms(stream.read(self.frames_per_buffer), self.DEFAULT_WIDTH) for _ in range(samples)] # Calculating the RMS value of the audio stream
        
        values = sorted(values, reverse=True)
        intensity = sum(values[:int(samples * percentage)]) / int(samples * percentage) # Taking the average of top 20% of the sound intensity

        LOG.info(f"Average audio intensity is:{intensity}")
        stream.close()
    
        self._pyaudio.terminate()
        return intensity
    
    def save_speech(self, data):
        """ 
        Saves mic data to temporary WAV file. Returns filename of saved 
        file 
        """
        filename = 'output_'+str(int(time.time()))
        # writes data to WAV file
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(self.DEFAULT_CHANNELS)
        wf.setsampwidth(self._pyaudio.get_sample_size(pyaudio.paInt16))
        wf.setframerate(self.DEFAULT_RATE)
        wf.writeframes(data)
        wf.close()
        return filename + '.wav'
    

if __name__ == "__main__":
    r = Recorder()
    # r.avg_intensity()
    r.record()