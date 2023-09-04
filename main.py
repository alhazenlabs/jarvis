import os
from collections import deque
import pyaudio
from audio_io.recorder import Recorder
from audio_io.player import Player
from audio_io.wake_detector import WakeDetector
from data_api.speech_to_text_dao import SpeechToTextDao
from data_api.ai_dao import AiDao
from data_api.text_to_speech_dao import TextToSpeechDao
from utils.logger import LOG
from utils.db import load_db
from utils.constants import Constants
from utils.file import mapInputSpeechToText, error_response
from utils.exceptions import SttError


def callable():
    load_db()
    r = Recorder()
    ai = AiDao()
    pa = pyaudio.PyAudio()

    # Open audio stream
    audio_stream = pa.open(
        rate=Constants.DEFAULT_RATE,
        channels=Constants.DEFAULT_INPUT_CHANNELS,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=Constants.DEFAULT_FRAMES_PER_BUFFER,
    )

    prepend_audio = deque(maxlen=min(Constants.DEFAULT_RATE // Constants.DEFAULT_FRAMES_PER_BUFFER, 7))
    
    print("Listening... Press Ctrl+C to exit")
    try:
        while True:
            frame = audio_stream.read(Constants.DEFAULT_FRAMES_PER_BUFFER)

            prepend_audio.append(frame)
            if WakeDetector.detect(frame):  # after detecting the wake word, the last frame misses the wake audio, 
                                               # possibility is that porcupine is modifying it, check
                print("jarvis detected")
                LOG.info(f"frame length of wake detection {len(frame)}")


                LOG.info("0. Begin")
                filename = r.record_and_save(audio_stream, pa.get_sample_size(pyaudio.paInt16), prepend_audio)
                LOG.info(f"1. Recorded the audio for transcription file:{filename}")

                try:
                    transcript = SpeechToTextDao.transcribe_speech(filename)
                    LOG.info(f"2. recorded transcript input is :{transcript}")

                    file = mapInputSpeechToText(transcript, filename)
                    LOG.info(f"3. mapped input speech to text {file}")

                    response = ai.get_and_save_response(transcript)
                    LOG.info(f"4. recieved ai response is :{response}")

                    output_audio = TextToSpeechDao.synthesize(response)
                    LOG.info(f"5. synthesized text to speech in file:{output_audio}")
                except SttError:
                    output_audio = error_response(Constants.CONSTANT_SPEECH_ERROR)
                
                os.remove(filename)
                Player.play(output_audio)

    except KeyboardInterrupt:
        print("Stopping... the application")
    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()

if __name__== "__main__":
    callable()
