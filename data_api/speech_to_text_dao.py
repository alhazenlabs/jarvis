from google.cloud import speech_v1p1beta1 as speech
import io

class SpeechToTextDao(object):
    INPUT_LANGUAGE_CODE = "en-IN"
    DEFAULT_RATE = 16000

    @classmethod
    def transcribe_speech(self, speech_file_path):
        client = speech.SpeechClient()

        with io.open(speech_file_path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)

        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self.DEFAULT_RATE,  # Adjust to match your audio file
            language_code=self.INPUT_LANGUAGE_CODE,    # Adjust to match your language
        )

        response = client.recognize(config=config, audio=audio)

        # print(response)
        # print(response.results)
        # for result in response.results:
        #     print("Transcript: {}".format(result.alternatives[0].transcript))

        result = ''
        confidence = 0

        for result in response.results:
            print("Transcript: {}".format(result.alternatives[0].transcript))
            if result.alternatives[0].confidence > confidence:
                result = result.alternatives[0].transcript
                
        return result