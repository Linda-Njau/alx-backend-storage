#!/usr/bin/env python3
"""cache class definiton"""

import redis
from typing import Union, Callable, Optional
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Counts the number of calls for the given method""" 
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Wrapper function for counting calls"""
        self._redis.incr(key)
        return method(*args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """ history of call input and outputs"""
    input_list = method.__qualname__ + ":inputs"
    output_list = method.__qualname__ + ":outputs"

    @wraps(method)
    def wrapper(self, *args) -> bytes:
        """wrapper method for call_history"""
        self._redis.rpush(input_list, str(args))
        output = method(self, *args)
        self._redis.rpush(output_list, output)
        return output
    return wrapper


class Cache:
    def __init__(self):
        """Constructor for redis instance"""
        self._redis = redis.Redis()
        self._redis.flushdb()
   
    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the input data in the redis database"""
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key
    
    def get(self, key: str, fn: Optional[Callable] = None) -> Union[str, bytes, int, float]:
        """Get the value of data for a given key"""
        data = self._redis.get(key)
        return fn(data) if fn else data
  
    def get_str(self, data: str) -> str:
        """Returns a string representation of the given data"""
        return self.get(key, str)

    def get_int(self, data: str) -> int:
        """Returns a int representation of the given data"""
        return self.get(key, int)