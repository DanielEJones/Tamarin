from typing import Any

from .exceptions import TestFailed


class Assert:

    _value: Any

    def __init__(self, value: Any) -> None:
        self._value = value

    def equals(self, value: Any) -> None:
        if self._value != value:
            raise TestFailed(f"{self._value} does not equal {value}")

    def not_equal(self, value: Any) -> None:
        if self._value == value:
            raise TestFailed(f"{self._value} does not equal {value}")

