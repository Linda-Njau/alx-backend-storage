#!/usr/bin/env python3
"""cache class definiton"""

import redis
from typing import Union, Callable
import uuid
from functools import wraps

def count_calls(method: Callable) -> Callable:
    key = method.__qualname__
    
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(key)
        return method(*args, **kwargs)
    return wrapper

def call_history(method: Callable) -> Callable:
    input_list = method.__qualname__ + ":inputs"
    output_list = method.__qualname__ + ":outputs"
    
    @wraps(method)
    def wrapper(self, *args) -> bytes:
        self._redis.rpush(input_list, str(args))
        output = method(self, *args)
        self._redis.rpush(output_list, output)
        return output
    return wrapper
        
class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
    def get(self, key: str, fn: callable) -> Union[str, bytes, int, float]:
        value = self._redis.get(key)
        if value is not None and fn is not None:
            return fn(value)
        return value
    def get_str(self, key: str) -> str:
        return self._redis.get(key, str)
    
    def get_int(self, key: str) -> int:
        return self._redis.get(key, int)
    
    
