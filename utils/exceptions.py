
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

