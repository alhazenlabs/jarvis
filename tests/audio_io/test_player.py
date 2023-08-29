import unittest
from unittest.mock import Mock, patch

from audio_io.player import Player, UnsupportedExtenstion

class TestPlayer(unittest.TestCase):

    @patch("pydub.AudioSegment.from_mp3")
    @patch("audio_io.player.play")
    def test_play_mp3(self, mock_play, mock_from_mp3):
        mock_audio = Mock()
        mock_from_mp3.return_value = mock_audio
        # mock_audio.return_value.speedup.return_value.sample_width = 4

        Player.play("audio.mp3", rate=1.5)

        mock_from_mp3.assert_called_once_with("audio.mp3")
        mock_audio.speedup.assert_called_once_with(playback_speed=1.5)
        mock_play.assert_called_once_with(mock_audio.speedup.return_value)
    
    @patch("pydub.AudioSegment.from_wav")
    @patch("audio_io.player.play")
    def test_play_wav(self, mock_play, mock_from_wav):
        mock_audio = Mock()
        mock_from_wav.return_value = mock_audio

        Player.play("audio.wav", rate=2.0)

        mock_from_wav.assert_called_once_with("audio.wav")
        mock_audio.speedup.assert_called_once_with(playback_speed=2.0)
        mock_play.assert_called_once_with(mock_audio.speedup.return_value)

    def test_play_unsupported_extension(self):
        with self.assertRaises(UnsupportedExtenstion):
            Player.play("audio.unknown")
