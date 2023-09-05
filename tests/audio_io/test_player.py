# import unittest
# from unittest.mock import patch
# from io import StringIO

# from audio_io.player import Player
# from utils.exceptions import UnsupportedExtenstion

# class TestPlayer(unittest.TestCase):
#     @unittest.skip("ALSA: Couldn't open audio device: No such file or directory")
#     @patch('pygame.mixer.music.load')
#     @patch('pygame.mixer.music.play')
#     @patch('pygame.mixer.music.get_busy', side_effect=[False, True, False])
#     @patch('time.sleep')
#     def test_play_mp3_file_successfully(self, mock_sleep, mock_get_busy, mock_play, mock_load, mock_mixer):
#         # Arrange
#         filename = "test.mp3"
#         expected_output = "audio file was played successfully.\n"

#         # Act
#         with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
#             Player.play(filename)

#         # Assert
#         mock_load.assert_called_once_with(filename)
#         mock_play.assert_called_once()
#         # self.assertEqual(mock_stdout.getvalue(), expected_output)

#     @patch("ALSA: Couldn't open audio device: No such file or directory")
#     @patch('pygame.mixer.music.load')
#     @patch('pygame.mixer.music.play')
#     @patch('pygame.mixer.music.get_busy', side_effect=[False, True, False])
#     @patch('time.sleep')
#     def test_play_wav_file_successfully(self, mock_sleep, mock_get_busy, mock_play, mock_load, mock_mixer):
#         # Arrange
#         filename = "test.wav"
#         expected_output = "audio file was played successfully.\n"

#         # Act
#         with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
#             Player.play(filename)

#         # Assert
#         mock_load.assert_called_once_with(filename)
#         mock_play.assert_called_once()
#         # self.assertEqual(mock_stdout.getvalue(), expected_output)

#     def test_play_unsupported_file_extension_raises_exception(self):
#         # Arrange
#         filename = "test.txt"

#         # Act & Assert
#         with self.assertRaises(UnsupportedExtenstion):
#             Player.play(filename)

# if __name__ == '__main__':
#     unittest.main()