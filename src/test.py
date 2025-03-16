from __future__ import annotations
from typing import Any, Callable
from functools import wraps

from .exceptions import DuplicateMethodCall, TestFailed


TAMARIN_TEST_LIST = []


def run_tests():
    fails = 0
    for i, test in enumerate(TAMARIN_TEST_LIST):
        print(f"{i + 1}/{len(TAMARIN_TEST_LIST)}: ", end='')
        try:
            test()
            print("TEST OK.")
        except TestFailed as e:
            fails += 1
            print(e)
    print('-' * 75)
    print("OK." if fails == 0 else f"{fails} Fail(s).")

def chain_wrapper(method: Callable[..., None]) -> Callable[..., _Test]:
    @wraps(method)
    def inner(self: _Test, *args, **kwargs) -> _Test:
        if method in self._called:
            raise DuplicateMethodCall(method.__name__)
        self._called.add(method)
        method(self, *args, **kwargs)
        return self
    return inner


def test_wrapper(self: _Test, function: Callable[..., None]) -> Callable[[], None]:
    @wraps(function)
    def inner() -> None:
        try:
            function(**{
                k: v() if callable(v) else v
                for k, v
                in self._params.items()
            })
        except Exception as e:
            raise TestFailed(
                f"TEST FAILED {function.__name__}({self._params}) should {self._desc or ''}: {e}"
            )

    return inner


class Test:

    @staticmethod
    def given(**params) -> _Test:
        return _Test().given(**params)

    @staticmethod
    def should(description: str) -> _Test:
        return _Test().should(description)


class _Test:

    _desc: str | None
    _params: dict[str, Any]
    _called: set[Callable]

    def __init__(self) -> None:
        self._desc = None
        self._params = dict()
        self._called = set()

    @chain_wrapper
    def should(self, description: str) -> None:
        self._desc = description

    @chain_wrapper
    def given(self, **params: dict[str, Any]) -> None:
        self._params.update(params)

    def __call__(self, function: Callable[..., None]) -> Callable[[], None]:
        wrapped = test_wrapper(self, function)
        TAMARIN_TEST_LIST.append(wrapped)
        return wrapped

