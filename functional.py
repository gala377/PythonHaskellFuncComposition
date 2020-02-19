import inspect

from types import FrameType
from typing import (
    Optional,
    Callable,
)


def expand(func):
    return Function(func)


class Function:

    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __getattr__(self, item):
        for frame_info in inspect.stack()[1:]:
            if f := self.__lookup_item(frame_info.frame, item):
                return Function(lambda *args, **kwargs: self(f(*args, **kwargs)))
            if frame_info.function == '<module>':
                break
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'")

    @staticmethod
    def __lookup_item(frame: FrameType, item: str) -> Optional[Callable]:
        for attr in ("f_locals", "f_globals", "f_builtins"):
            if f := getattr(frame, attr).get(item):
                return f
        return None
