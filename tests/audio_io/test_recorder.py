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
        mock_PyAudio.assert_called_once()

    @patch("pyaudio.PyAudio")
    def test_record(self, mock_PyAudio):
        recorder = Recorder(frames_per_buffer=2)
        mock_stream = Mock()
        mock_stream.read.return_value = self.SPEECH

        mock_PyAudio.return_value.open.return_value = mock_stream
        mock_PyAudio.return_value.get_sample_size.return_value = 2

        filename = recorder.record(threshold=50000)

        mock_PyAudio.assert_called_once()
        mock_PyAudio.return_value.open.assert_called_once_with(
            format=recorder.format,
            channels=recorder.channels,
            rate=recorder.rate,
            input=recorder.input,
            frames_per_buffer=recorder.frames_per_buffer
        )
        mock_stream.read.assert_called()

        self.assertTrue(filename.endswith(".wav"))
        os.remove(filename)

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
