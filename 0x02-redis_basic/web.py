#!/usr/bin/env python3
"""
This module defines the function `get_page` as well as a decorator for keeping
track of calls to `get_page` with a particular url
"""
import redis
import requests
from functools import wraps
from typing import Callable


def access_count(get_page: Callable[[str], str]) -> Callable[[str], str]:
    """Track calls to `get_page` with a particular url """
    @wraps(get_page)
    def wrapper(url: str) -> str:
        key = f"count:{url}"
        store = redis.Redis()
        store.incr(key)
        store.expire(key, 10)
        return get_page(url)
    return wrapper


@access_count
def get_page(url: str) -> str:
    """Obtain and return the HTML content of a particular URL, `url` """
    return requests.get(url).text
