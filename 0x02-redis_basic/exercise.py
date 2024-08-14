#!/usr/bin/env python3
"""
redis
"""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the history of inputs
    and outputs for a method in Redis
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))

        return output
    return wrapper


class Cache:
    """
    A class for interacting with Redis
    to store and retrieve data, with additional
    functionality for counting method calls
    and recording call history
    """
    def __init__(self):
        """
        Initializes the Cache instance by creating
        a Redis client and flushing the database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a piece of data in Redis and returns a unique key for it
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Optional[Callable] = None,
            ) -> Union[str, bytes, int, float, None]:
        """
        Retrieves data from Redis using the provided key. Optionally applies a
        function to the retrieved data before returning it.
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves a string value from Redis using the provided key.
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves an integer value from Redis using the provided key.
        """
        return self.get(key, fn=int)


def replay(method: Callable):
    """
    Replays the history of inputs and outputs for a method that was decorated
    with the `@call_history` decorator. It prints the number of times the
    method was called, followed by each set of inputs and corresponding output.
    """
    redis_client = redis.Redis()
    method_name = method.__qualname__
    inputs_key = f"{method_name}:inputs"
    outputs_key = f"{method_name}:outputs"

    call_count = int(redis_client.get(method_name) or 0)
    print(f"{method_name} was called {call_count} times:")

    inputs = redis_client.lrange(inputs_key, 0, -1)
    outputs = redis_client.lrange(outputs_key, 0, -1)

    for input_args, output in zip(inputs, outputs):
        input_str = input_args.decode('utf-8')
        output_str = output.decode('utf-8')
        print(f"{method_name}{input_str} -> {output_str}")
