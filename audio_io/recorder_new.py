import time
import wave
import pyaudio
import struct
import pvporcupine

from utils.constants import Constants

class WakeWordDetector(object):
    def __init__(self):

        self.porcupine = pvporcupine.create(
        access_key=Constants.PORCUPINE_ACCESS_KEY, 
        keywords=Constants.DEFAULT_WAKE_KEYWORDS,  
        sensitivities=Constants.DEFAULT_WAKE_SENSITIVITIES
        )

        self.p = pyaudio.PyAudio()
        self.rate = Constants.DEFAULT_RATE
        self.chunk = Constants.DEFAULT_FRAMES_PER_BUFFER  # Number of frames per buffer
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=Constants.DEFAULT_INPUT_CHANNELS,
                                  rate=self.rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)

    def detect_wake_word(self):
        print("Listening for wake word...")

        while True:
            pcm = self.stream.read(self.chunk, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * self.chunk, pcm)
            keyword_index = self.porcupine.process(pcm)
            
            if keyword_index >= 0:
                print("Wake word detected!")
                self.record_sentence()

    def record_sentence(self):
        print("Recording sentence...")
        
        audio_data = bytearray()
        intensity_threshold = Constants.DEFAULT_INPUT_SPEECH_THRESHOLD  # Adjust this threshold as needed
        silence_counter = 0
        
        while True:
            pcm = self.stream.read(self.chunk, exception_on_overflow=False)
            # pcm = struct.unpack_from("h" * self.chunk, pcm)
            intensity = max(pcm)
            
            audio_data.extend(pcm)
            
            if intensity > intensity_threshold:
                silence_counter = 0
            else:
                silence_counter += 1
                
            if silence_counter >= 10:  # Adjust this threshold as needed
                break

        print(f"audio_data: {audio_data}")
        print("Recording finished.")
        filename = 'output_'+str(int(time.time()))
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(Constants.DEFAULT_INPUT_CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(Constants.DEFAULT_RATE)
        wf.writeframes(audio_data)
        wf.close()
        
        # Process or save the recorded audio data as needed
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

if __name__ == "__main__":
    detector = WakeWordDetector()
    detector.detect_wake_word()