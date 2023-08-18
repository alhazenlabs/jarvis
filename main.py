from output.texttospeech import TextToSpeech
from utils.logger import LOG
from utils.db import load_db

text = """
'm not a doctor, but there are several potential causes for kidney pain, including infections, kidney stones, urinary tract infections, kidney disease, or muscle strains. It's important to consult a medical professional to determine the exact cause of your pain and receive appropriate advice and treatment.
"""  

if __name__ == "__main__":
    # Connect to a sqllite-db
    LOG.info(text)
    load_db()

    tt = TextToSpeech(text)
    tt.save_and_play()
