import os
import unittest
from unittest.mock import Mock, patch
from audio_io.recorder import Recorder

class TestRecorder(unittest.TestCase):
    SPEECH = b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00\x04\x00\x00\x00\x04\x00\x00\x01\x00\x08\x00data\x00\x00\x00\x00'

    @patch("pyaudio.PyAudio")
    def test_init(self, mock_PyAudio):
        recorder = Recorder()
        self.assertEqual(recorder.format, recorder.DEFAULT_FORMAT)
        self.assertEqual(recorder.channels, recorder.DEFAULT_CHANNELS)
        self.assertEqual(recorder.rate, recorder.DEFAULT_RATE)
        self.assertEqual(recorder.input, recorder.DEFAULT_INPUT)
        self.assertEqual(recorder.frames_per_buffer, recorder.DEFAULT_FRAMES_PER_BUFFER)

    @unittest.skip("Fix the recording, it goes in an infinite loop")
    @patch('audio_io.recorder.pyaudio.PyAudio')
    @patch('audio_io.recorder.time.sleep')
    @patch('audio_io.recorder.deque')
    def test_record(self, mock_deque, mock_sleep, mock_pyaudio):
        # Create an instance of MyAudioRecorder
        audio_recorder = Recorder()

        # Mock the PyAudio instance
        mock_pyaudio_instance = mock_pyaudio.return_value
        mock_pyaudio_instance.open.return_value = Mock()
        mock_pyaudio_instance.get_sample_size.return_value = 2

        # Mock the deque instance
        mock_deque_instance = mock_deque.return_value
        mock_deque_instance.copy.return_value = [b'audio_data']
        mock_deque_instance.popleft.return_value = b'prepend_audio_data'
        mock_deque_instance.pop.return_value = b'append_audio_data'

        # Mock the stream read method
        audio_data = b'some_audio_data'
        mock_stream = mock_pyaudio_instance.open.return_value
        mock_stream.read.side_effect = [audio_data, audio_data, audio_data, b'']

        # Mock the speech_detected method
        audio_recorder.speech_detected = Mock(side_effect=[True, True, True, False])

        # Call the record method
        result = audio_recorder.record()

        # Assertions
        self.assertEqual(result, 'filename.wav')
        mock_pyaudio_instance.open.assert_called_once()
        mock_pyaudio_instance.get_sample_size.assert_called_once_with(audio_recorder.format)
        mock_deque.assert_called_once()
        mock_stream.read.assert_called_with(audio_recorder.frames_per_buffer)
        self.assertEqual(mock_pyaudio_instance.terminate.call_count, 1)

    @unittest.skip("Fix the recording, it goes in an infinite loop")
    @patch('audio_io.recorder.pyaudio.PyAudio')
    @patch('audio_io.recorder.time.sleep')
    @patch('audio_io.recorder.deque')
    def test_record_and_save(self, mock_deque, mock_sleep, mock_pyaudio):
        # Create an instance of MyAudioRecorder
        audio_recorder = Recorder()

        # Mock the PyAudio instance
        mock_pyaudio_instance = mock_pyaudio.return_value
        mock_pyaudio_instance.open.return_value = Mock()
        mock_pyaudio_instance.get_sample_size.return_value = 2

        # Mock the deque instance
        mock_deque_instance = mock_deque.return_value
        mock_deque_instance.copy.return_value = [b'audio_data']
        mock_deque_instance.popleft.return_value = b'prepend_audio_data'
        mock_deque_instance.pop.return_value = b'append_audio_data'

        # Mock the stream read method
        audio_data = b'some_audio_data'
        mock_stream = mock_pyaudio_instance.open.return_value
        mock_stream.read.side_effect = [audio_data, audio_data, audio_data, b'']

        # Mock the speech_detected method
        audio_recorder.speech_detected = Mock(side_effect=[True, True, True, False])

        # Call the record_and_save method
        result = audio_recorder.record_and_save(mock_stream, 2, mock_deque_instance)

        # Assertions
        self.assertEqual(result, 'filename.wav')
        mock_stream.read.assert_called_with(audio_recorder.frames_per_buffer)
        mock_deque_instance.append.assert_called_with(b'audio_data')
        self.assertEqual(mock_stream.write.call_count, 3)

    def test_speech_detected_true(self):
        window = [100, 200, 300, 400, 600]
        threshold = 250
        result = Recorder.speech_detected(window, threshold)
        self.assertTrue(result)

    def test_speech_detected_false(self):
        window = [100, 200, 300, 400, 600]
        threshold = 700
        result = Recorder.speech_detected(window, threshold)
        self.assertFalse(result)

    def test_get_rms(self):
        data = self.SPEECH
        width = 2
        result = Recorder.get_rms(data, width=width)
        self.assertIsInstance(result, float)

if __name__ == '__main__':
    unittest.main()