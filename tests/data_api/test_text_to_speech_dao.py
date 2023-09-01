import unittest
from unittest.mock import patch
import requests
import time

# Import the function you want to test
from data_api.text_to_speech_dao import with_retry

# Define a mock function to simulate the behavior of the function being retried
def mock_function(arg):
    if arg == "success":
        return "Success"
    else:
        raise requests.ConnectionError

class TestWithRetry(unittest.TestCase):

    @patch('time.sleep', return_value=None)  # Mock the time.sleep function
    def test_with_retry_success(self, mock_sleep):
        # Test with a function that succeeds on the first try
        result = with_retry(mock_function, "success")
        self.assertEqual(result, "Success")
        # Ensure time.sleep was not called
        self.assertFalse(mock_sleep.called)

    @patch('time.sleep', return_value=None)  # Mock the time.sleep function
    def test_with_retry_failure(self, mock_sleep):
        # Test with a function that fails all retries
        with self.assertRaises(requests.ConnectionError):
            with_retry(mock_function, "failure", retries=2, backoff=0)
        # Ensure time.sleep was called twice
        self.assertEqual(mock_sleep.call_count, 2)

if __name__ == '__main__':
    unittest.main()