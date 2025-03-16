class DuplicateMethodCall(Exception):

    def __init__(self, method: str) -> None:
        super().__init__(
            f"Calling the method '{method}' on the same object multiple times is not supported."
        )

class TestFailed(Exception):

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
