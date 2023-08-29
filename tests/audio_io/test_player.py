import time
import unittest
import threading
from unittest.mock import Mock, patch

from audio_io.player import Player

class TestVariableRateAudioPlayer(unittest.TestCase):

    def setUp(self):
        self.audio_player = Player("test_audio.wav", rate=1.5)

    @patch("pyaudio.PyAudio")
    def test_play_and_stop(self, mock_pyaudio):
        mock_pyaudio_instance = Mock()
        mock_pyaudio.return_value = mock_pyaudio_instance

        mock_stream_instance = Mock()
        mock_pyaudio_instance.open.return_value = mock_stream_instance

        mock_wf_instance = Mock()
        mock_wf_instance.readframes.side_effect = [b"audio_data", None]
        mock_wave_open = Mock(return_value=mock_wf_instance)
        with patch("wave.open", mock_wave_open):
            # Start playing the audio in a separate thread
            audio_thread = threading.Thread(target=self.audio_player.play)
            audio_thread.start()

            # Let it play for a short time
            time.sleep(1)

            # Stop the audio playback
            self.audio_player.stop()
            audio_thread.join()

            mock_pyaudio_instance.open.assert_called_once()
            mock_stream_instance.stop_stream.assert_called_once()
            mock_stream_instance.close.assert_called_once()
            mock_wf_instance.readframes.assert_called()
    
    @patch("pyaudio.PyAudio")
    def test_play_stopped_immediately(self, mock_pyaudio):
        mock_pyaudio_instance = Mock()
        mock_pyaudio.return_value = mock_pyaudio_instance

        mock_stream_instance = Mock()
        mock_pyaudio_instance.open.return_value = mock_stream_instance

        mock_wf_instance = Mock()
        mock_wf_instance.readframes.return_value = None  # Simulate empty audio file
        mock_wave_open = Mock(return_value=mock_wf_instance)
        with patch("wave.open", mock_wave_open):
            # Start playing the audio in a separate thread
            audio_thread = threading.Thread(target=self.audio_player.play)
            audio_thread.start()

            # Stop the audio playback immediately
            self.audio_player.stop()
            audio_thread.join()

            mock_pyaudio_instance.open.assert_called_once()
            mock_stream_instance.stop_stream.assert_not_called()
            mock_stream_instance.close.assert_not_called()
            mock_wf_instance.readframes.assert_called()

if __name__ == "__main__":
    unittest.main()
