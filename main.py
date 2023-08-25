from input.recorder import Recorder
from data_api.speech_to_text_dao import SpeechToTextDao
from data_api.ai_dao import AiDao
from output.texttospeech import TextToSpeech
from utils.logger import LOG
from utils.db import load_db

text = """
'm not a doctor, but there are several potential causes for kidney pain, including infections, kidney stones, urinary tract infections, kidney disease, or muscle strains. It's important to consult a medical professional to determine the exact cause of your pain and receive appropriate advice and treatment.
"""  

if __name__ == "__main__":
    load_db()

    r = Recorder()
    ai = AiDao()

    # filename = r.record()
    filename = "output_1692858036.wav"
    transcript = SpeechToTextDao.transcribe_speech(filename)
    print(f"recorded transcript input is :{transcript}")

    response = ai.get_and_save_response(transcript)
    print(f"recieved ai response is :{response}")
    tts = TextToSpeech(response)
    tts.save_and_play()



