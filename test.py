from typing import Callable
from com import *


@expand
def foo(x: int) -> int:
    return x * 2


def bar(x: int) -> int:
    return x + 3


def passing_call(arg: int, func: Callable[[int], int]) -> int:
    return foo.func(arg)


def tests():
    try:
        assert foo(3) == 6
        assert foo.bar(1) == 8

        def inner(x):
            return x + 1

        assert foo.inner(1) == 4
        assert passing_call(1, bar) == 8
        assert foo.bar.inner(1) == 10
    except BaseException as e:
        print(f"Tests failed with exception {type(e)}: {e}")
    else:
        print("All passed")


if __name__ == '__main__':
    tests()
