#!/usr/bin/env python3
"""This module defines a class `Cache` """
from typing import Any, Callable, Optional, Union
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Count the number of times a function is called """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        ret = method(self, *args, **kwargs)
        self._redis.incr(key)
        return ret

    return wrapper


def call_history(method: Callable) -> Callable:
    """Store the history of inputs and outputs for a function (`method`) """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        ret = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(ret))
        return ret

    return wrapper


def replay(method: Callable):
    """Display the history of inputs and outputs for a function (`method`) """
    name = method.__qualname__
    self = method.__self__
    input_key = f"{name}:inputs"
    output_key = f"{name}:outputs"
    n_calls = self._redis.get(name)
    print(f"{name} was called {n_calls.decode('utf-8')} times:")
    inputs = self._redis.lrange(input_key, 0, -1)
    outputs = self._redis.lrange(output_key, 0, -1)
    for i, o in zip(inputs, outputs):
        print(f"{name}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")


class Cache:
    """Handle storage and retrieval of data caches using `Redis` """

    def __init__(self) -> None:
        """Initialise `Redis` client """
        import redis
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store input data in `Redis` using randomly generated key

        Return: randomly generated key
        """
        from uuid import uuid4
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """Return the value of `key`, if it exists """
        val = self._redis.get(key)
        if val is not None:
            if fn is not None:
                return fn(val)
            return val

    def get_str(self, key: str) -> Any:
        """Parameterize `Cache.get` with `fn`=`str` """
        return self.get(key, str)

    def get_int(self, key: str) -> Any:
        """Parameterize `Cache.get` with `fn`=`int` """
        return self.get(key, int)


if __name__ == "__main__":
    cache = Cache()
    TEST_CASES = {b"foo": None, 123: int, "bar": lambda d: d.decode("utf-8")}
    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
