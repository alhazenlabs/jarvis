import time
import requests

from utils.logger import LOG


class UnsupportedExtenstion(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MicrophoneError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class AiError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class DbError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class SttError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def with_retry(function, *args, retries=3, backoff=1):
    for _ in range(retries):
        try:
            return function(*args)
        except requests.ConnectionError as e:
            LOG.info("connection error. retrying in a moment.")
            time.sleep(backoff)
    
    LOG.info("max retries exceeded. translation failed")
    raise requests.ConnectionError("max retries exceeded. translation failed")