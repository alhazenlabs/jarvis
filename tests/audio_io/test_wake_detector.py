import os
import unittest
from unittest.mock import Mock
from audio_io.wake_detector import WakeDetector

class TestWakeDetector(unittest.TestCase):    
    @classmethod
    def setUpClass(cls):
        # Create a mock Porcupine instance and set it for the WakeDetector
        cls.mock_porcupine = Mock()
        cls.mock_porcupine.process.return_value = -1
        cls.original_porcupine = WakeDetector.PC
        WakeDetector.PC = cls.mock_porcupine

    @classmethod
    def tearDownClass(cls):
        # Restore the original Porcupine instance
        WakeDetector.PC = cls.original_porcupine

    def test_detect_wake_keyword_returns_false(self):
        # Generate random binary data for the audio frame
        self.mock_porcupine.process.return_value = -1

        # Act
        result = WakeDetector.detect(os.urandom(1024))

        # Assert
        self.assertFalse(result)

    def test_detect_wake_keyword_returns_true(self):
        self.mock_porcupine.process.return_value = 0

        # Act
        result = WakeDetector.detect(os.urandom(1024))

        # Assert
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
