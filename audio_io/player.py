from pydub import AudioSegment
from pydub.playback import play

from utils.constants import Constants
from utils.exceptions import UnsupportedExtenstion

DEFAULT_RATE = Constants.DEFAULT_PLAYBACK_RATE


def play_audio(filename, rate=DEFAULT_RATE):
    print(filename, type(filename))
    audio = ''
    if '.mp3' in filename:
        audio = AudioSegment.from_mp3(filename)
    elif '.wav' in filename:
        audio = AudioSegment.from_wav(filename)
    else:
        raise UnsupportedExtenstion(f"file {filename} extension not supported currently")
    
    audio = audio.speedup(playback_speed=rate)
    play(audio)


# if __name__ == "__main__":
    # wav_filename = "your_audio.wav"
    # mp3_filename = "your_audio.mp3"
    # playback_rate = 1.5  # Change this to adjust the playback speed
    
    # play_wav_pyaudio(wav_filename, playback_rate)

    # audio_player = play_audio("output_1692858036.wav", rate=1.2)
    # audio_player = play_audio("media/standard/help.mp3", rate=1.2)
