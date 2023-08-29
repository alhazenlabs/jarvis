import os
from audio_io.recorder import Recorder
from audio_io.player import Player
from data_api.speech_to_text_dao import SpeechToTextDao
from data_api.ai_dao import AiDao
from data_api.text_to_speech_dao import TextToSpeechDao
from utils.logger import LOG
from utils.db import load_db
from utils.file import mapInputSpeechToText

text = """
'm not a doctor, but there are several potential causes for kidney pain, including infections, kidney stones, urinary tract infections, kidney disease, or muscle strains. It's important to consult a medical professional to determine the exact cause of your pain and receive appropriate advice and treatment.
"""  

if __name__ == "__main__":
    load_db()

    r = Recorder()
    ai = AiDao()

    LOG.info("0. Begin")
    filename = r.record()
    LOG.info(f"1. Recorded the audio for transcription file:{filename}")
    # filename = "output_1692858036.wav"

    transcript = SpeechToTextDao.transcribe_speech(filename)
    LOG.info(f"2. recorded transcript input is :{transcript}")

    file = mapInputSpeechToText(transcript, filename)
    LOG.info(f"3. mapped input speech to text {file}")
    os.remove(filename)

    response = ai.get_and_save_response(transcript)
    LOG.info(f"4. recieved ai response is :{response}")

    output_audio = TextToSpeechDao.synthesize(response)
    LOG.info(f"5. synthesized text to speech in file:{output_audio}")

    Player.play(output_audio)
    LOG.info(f"6. Audio successfully played:{output_audio}")
    # tts.save_and_play()



