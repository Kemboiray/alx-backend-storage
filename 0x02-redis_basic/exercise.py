#!/usr/bin/env python3
"""
This module defines a class `Cache` that stores and flushes an instance of the
`Redis` client.
"""
from typing import Union


class Cache:
    """
    Public class method:
        store - Store input data in `Redis` using a randomly generated key
    """
    def __init__(self) -> None:
        """Initialise `Redis` client """
        import redis
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store input data in `Redis` using randomly generated key

        Return: randomly generated key
        """
        from uuid import uuid4
        key = str(uuid4())
        self._redis.set(key, data)
        return key
