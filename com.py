import inspect
import typing
import functools

from types import FrameType
from typing import (
    Optional,
    Callable,
)


def expand(func):
    return Function(func)


def _print_frame_info(frame):
    members = "\n\t\t".join(f"{name=}, {value=}" for name, value in inspect.getmembers(frame.frame))
    print(f"""
Got frame {frame}
    Type of frame:
        {type(frame.frame)}.
    Type of function:
        {type(frame.function)}.

    Frame members:
        {members}
""")


class Function:
    """
    TODO Copy type attributes of the wrapped function to
    TODO the ___call___. Make wrapping work so that
    TODO it is the same function (like functools.wrap).
    TODO Check if composed functions return type is the same as ours input type
    TODO Unpack returned dict, tuple before passing to our function after composition
    """

    def __init__(self, func):
        self._func = func

    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    def __getattr__(self, item):
        for frame_info in inspect.stack()[1:]:
            frame = frame_info.frame
            if (f := self.__lookup_item(frame, item)) is not None:
                def composed(*args, **kwargs):
                    return self(f(*args, **kwargs))
                return Function(composed)
            if frame_info.function == '<module>':
                break

        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{item}'")

    @staticmethod
    def __lookup_item(frame: FrameType, item: str) -> Optional[Callable]:
        if (f := frame.f_locals.get(item)) is not None:
            return f
        elif (f := frame.f_globals.get(item)) is not None:
            return f
        else:
            return frame.f_builtins.get(item)

