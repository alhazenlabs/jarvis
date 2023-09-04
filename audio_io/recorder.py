import math
import time
import pyaudio
import audioop
import wave

from collections import deque

from utils.constants import Constants
from utils.exceptions import MicrophoneError
from utils.logger import LOG


class Recorder(object):
    """
    A class for recording audio from a microphone using PyAudio and analyzing audio intensity.
    """

    DEFAULT_SLEEP_SECONDS = Constants.DEFAULT_INPUT_SLEEP_SECONDS

    DEFAULT_FRAMES_PER_BUFFER = Constants.DEFAULT_FRAMES_PER_BUFFER  # CHUNKS of bytes to read each time from mic  
    DEFAULT_FORMAT = pyaudio.paInt16
    DEFAULT_WIDTH = Constants.DEFAULT_INPUT_AUDIO_WIDTH # Width parameter specifies the number of bytes used 
                                                        # for a audio sample, (4 = 32 bit) will provide higher variations in threshold
    DEFAULT_CHANNELS = Constants.DEFAULT_INPUT_CHANNELS
    DEFAULT_RATE = Constants.DEFAULT_RATE
    DEFAULT_THRESHOLD = Constants.DEFAULT_INPUT_SPEECH_THRESHOLD # Threshold to signify silence, 
                                                                 # this needs to be calibrated after measuring avg_intensity from a mic
    DEFAULT_INPUT = True # True is for recording the sound

    DEFAULT_SAMPLE = Constants.DEFAULT_INPUT_SAMPLES # Number of samples for measuring audio intensity

    DEFAULT_SILENCE_LIMIT = Constants.DEFAULT_SILENCE_LIMIT # Silence limit in seconds. The max ammount of seconds where
                                                            # only silence is recorded. When this time passes the
                                                            # recording finishes and the file is delivered.

    DEFAULT_PERCENTAGE = Constants.DEFAULT_PERCENTAGE # Percentage of audio to be included while calculating threshold
    MAX_BUFFER_SIZE = 15

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
    
    def record(self, threshold=DEFAULT_THRESHOLD):
        """
        Record audio from the microphone and save it to a WAV file. 
        There is a default sleep of 2 seconds when the stream from microphone is accessed
        This is to make sure that the program doesn't exits before the speaker starts speaking

        Args:
            threshold: The audio intensity threshold for speech detection.
        Returns:
            filename: The filename of the saved WAV file.
        """
        
        pa = pyaudio.PyAudio()
        LOG.info("* listening to microphone. ")
        try:
            stream = pa.open(format=self.format, channels=self.channels, rate=self.rate,
                                        input=self.input, frames_per_buffer=self.frames_per_buffer)
        except Exception as e:
            LOG.exception(f"exception occurred while listening to the microphone: e")
            raise MicrophoneError("unable to open listen to microphone")
        

        time.sleep(self.DEFAULT_SLEEP_SECONDS) 
        # sleeping for 2 seconds to make sure the program doesn't exit before we have started speaking
        filename = self.record_and_save(stream, pa.get_sample_size(self.format), threshold=threshold)

        stream.close()
        pa.terminate()

        return filename

    def record_and_save(self, stream, width, prepend_audio=None, threshold=DEFAULT_THRESHOLD):
        """
        Record audio from a microphone stream and save it to a WAV file.

        Args:
            stream: The PyAudio microphone stream.
            width: The sample width in bytes.
            prepend_audio: Optional audio to prepend to the recorded audio.
            threshold (int): The audio intensity threshold for speech detection.

        Returns:
            filename (str): The filename of the saved WAV file.
        """
        buffers = min(self.rate // self.frames_per_buffer, self.MAX_BUFFER_SIZE)
        window = deque(maxlen=self.DEFAULT_SILENCE_LIMIT * buffers) # when all the samples in the window falls below threshold, we can assume a silence 
        append_audio = window.copy()
        window.append(threshold + 1)

        audio2send = bytearray()
        while prepend_audio:
            pd = prepend_audio.popleft()
            LOG.debug(f"starting frame length {len(pd)}")
            audio2send.extend(pd)

        LOG.info("starting record of phrase")
        while (self.speech_detected(window, threshold)):
            cur_data = stream.read(self.frames_per_buffer)
            window.append(self.get_rms(cur_data)) # Calculating RMS value of the current stream
            LOG.debug(f"current frame length: {len(cur_data)}")
            append_audio.append(cur_data)
            audio2send.extend(cur_data)

        while append_audio:
            ad = append_audio.pop()
            LOG.debug(f"ending frame length {len(ad)}")
            audio2send.extend(ad)

        LOG.info("done recording...")
        filename = self.save_speech(audio2send, width)
        LOG.info(f"saved file {filename}")
        return filename
    
    def save_speech(self, data, width):
        """
        Save recorded audio data to a temporary WAV file.

        Args:
            data: The audio data.
            width: The width of the audio data
        Returns:
            filename: The filename of the saved WAV file.
        """
        filename = 'output_'+str(int(time.time()))
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(self.DEFAULT_CHANNELS)
        wf.setsampwidth(width)
        wf.setframerate(self.DEFAULT_RATE)
        wf.writeframes(data)
        wf.close()
        return filename + '.wav'

    
    @staticmethod
    def speech_detected(window, threshold=DEFAULT_THRESHOLD):
        """
        Check if speech is detected based on the audio intensity window.

        Args:
            window: A deque containing recent audio intensity values.
            threshold: The audio intensity threshold for speech detection.
        Returns:
            True if speech is detected, False otherwise.
        """
        return sum([sound > threshold for sound in window]) > 0
    
    @staticmethod
    def get_rms(data, width=DEFAULT_WIDTH):
        """
        Calculate the Root Mean Square (RMS) value of audio data.

        Args:
            data: The audio data.
            width: The width parameter specifying the number of bytes per sample.
        Returns:
            The RMS value of the audio data.
        """
        return math.sqrt(abs(audioop.avg(data, width)))

    
    def avg_intensity(self, samples=DEFAULT_SAMPLE, percentage=DEFAULT_PERCENTAGE, stream=None):
        """
        Calculate the average audio intensity of the microphone sound. 
        This is a helper function to calculate the threshold of the speaker sound w.r.t the 
        background. Once the threshold is identified, It can be updated in the constants.

        Args:
            samples: Number of audio samples to use for intensity calculation.
            percentage: The percentage of top intensity values to consider.
            stream: Optional audio stream. If not provided, a new stream will be opened.
        Returns:
            intensity: The average audio intensity.
        """

        LOG.info("getting intensity values from mic")
        pa = pyaudio.PyAudio()
        LOG.debug(f"microphone info: {pa.get_default_input_device_info()}")

        if not stream:
            stream = pa.open(format=self.format, channels=self.channels, rate=self.rate, 
                                        input=self.input, frames_per_buffer=self.frames_per_buffer)

        values = [self.get_rms(stream.read(self.frames_per_buffer), self.DEFAULT_WIDTH) for _ in range(samples)] # Calculating the RMS value of the audio stream
        
        values = sorted(values, reverse=True)
        intensity = sum(values[:int(samples * percentage)]) / int(samples * percentage) # Taking the average of top 20% of the sound intensity

        LOG.info(f"average audio intensity is:{intensity}")
        stream.close()
    
        pa.terminate()
        return intensity
    