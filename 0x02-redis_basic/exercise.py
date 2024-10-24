#!/usr/bin/env python3
"""
Exercise module for Redis-based caching.
This module defines a Cache class that
interacts/interfaces with a Redis database.
The Cache class allows storing various
types of data (str, bytes, int, float) in the
Redis database using randomly generated keys.
"""

from functools import wraps
import redis
from typing import Callable, cast, Optional, TypeVar, Union
import uuid

T = TypeVar('T', str, bytes, int, float, None)
UnionOfTypes = Union[str, bytes, int, float, None]


# @staticmethod
def count_calls(method: Callable) -> Callable:
    """
    Decorator to count the number
    of times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method with
        counting functionality.
    """
    # Use wraps to preserve the original method's
    # attributes (name, docstring, etc.)
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the count of method
        calls and returns the original method's result.

        Args:
            self: The instance of the class.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            The return value of the original method.
        """
        # Generate the key for counting based
        # on the method's qualified name
        key = method.__qualname__
        # Increment the count for this method in Redis
        self._redis.incr(key)
        # Call the original method and store the result
        result = method(self, *args, **kwargs)
        # Return the original method's result
        return result

    return wrapper


# @staticmethod
def call_history(method: Callable) -> Callable:
    """
    Decorator to store the history of inputs and outputs
    for a particular function/method in Redis.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function (decorated method)
        with input and output history tracking.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wrapper function that stores
        inputs and outputs in Redis.

        Args:
            self: The instance of the Cache class.
            *args: Positional arguments passed to the method.
            **kwargs: Keyword arguments passed to the method.

        Returns:
            The return value of the method.
        """
        # Define base keys for inputs and outputs
        # using the method's qualified name
        key_inputs = f"{method.__qualname__}:inputs"
        key_outputs = f"{method.__qualname__}:outputs"
        # Store the input arguments as a
        # string in the Redis list for inputs
        self._redis.rpush(key_inputs, str(args))
        # Call the original method and store the output
        output = method(self, *args, **kwargs)
        # Store the output in the Redis list for outputs
        self._redis.rpush(key_outputs, str(output))
        # Return the output
        return output

    return wrapper


class Cache:
    """
    Cache class for storing and retrieving data
    in Redis with optional type conversion.
    """

    def __init__(self):
        """
        Initialize the Cache class by setting up a
        Redis client and flushing the database.
        """
        # Create an instance of the Redis client
        # (Initialize the Redis client) and
        # store it as a private instance variable
        self._redis = redis.Redis()
        # Flush the Redis database to remove any
        # existing data thereby ensuring a clean slate
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the provided input data in
        Redis using a randomly generated key.

        Args:
            data (Union[str, bytes, int, float]):
            The data to store in Redis.

        Returns:
            str: The randomly generated key
            which is used to store the data.
        """
        # Generate a random UUID key using
        # uuid4 and convert it to a string
        key = str(uuid.uuid4())

        # Ensure data is bytes
        # comment the below to run the main test files
        # assert isinstance(data, bytes), """Expected the value `data`
        # to be of the type `bytes`"""

        # Store the data in Redis using the generated key
        # self._redis.mset({key: data})
        self._redis.set(key, data)
        # Return the generated key
        return key

    def get(self, key: str, fn: Optional[
            Callable] = None) -> Optional[T]:
        """
        Retrieve data from Redis and
        optionally apply a conversion function.

        Args:
            key (str): The key used to retrieve the data from Redis.
            fn (Optional[Callable]): A callable function used to
            convert the data to the desired original format.

        Returns:
            Optional[T]: The retrieved data, possibly converted
            by fn, or None if the key does not exist.
        """
        # Retrieve the data from Redis using the provided key
        data = self._redis.get(key)

        # If the key does not exist, Redis
        # returns None, so return None
        if data is None:
            return None

        # Ensure data is bytes
        # assert isinstance(data, bytes), """Expected the value `data`
        # to be of the type `bytes`"""

        # If a conversion function is
        # provided, apply it to the data
        if fn is not None:
            return fn(data)

        # Return the data as it is if no
        # conversion function is provided
        return cast(T, data)

    def get_str(self, key: str) -> Optional[str]:
        """
        Retrieve data from Redis
        and convert it to a string.

        Args:
            key (str): The key used to
            retrieve the data from Redis.

        Returns:
            Optional[str]: The retrieved data as a
            string, or None if the key does not exist.
        """
        # Use the get method with a `lambda` function
        # to decode `bytes` to a `UTF-8` `string`
        return self.get(key, fn=lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """
        Retrieve data from Redis and
        convert it to an integer.

        Args:
            key (str): The key used to
            retrieve the data from Redis.

        Returns:
            Optional[int]: The retrieved data as an
            integer, or None if the key does not exist.
        """
        # Use the get method with the `int`
        # function to convert `bytes` to an `integer`
        return self.get(key, fn=int)


# @staticmethod
def replay(method: Callable):
    """
    Display the history of calls for/to
    a particular function/method.

    Args:
        method (Callable): The function/method
        whose call history is to be replayed.
    """
    # Construct the keys for inputs and outputs
    # using the method's qualified name
    key_inputs = f"{method.__qualname__}:inputs"
    key_outputs = f"{method.__qualname__}:outputs"

    # Retrieve all inputs and outputs from Redis
    # Access the Redis instance from the method
    redis_instance = method.__self__._redis
    # Get all input entries
    inputs = redis_instance.lrange(key_inputs, 0, -1)
    # Get all output entries
    outputs = redis_instance.lrange(key_outputs, 0, -1)

    # Print the number of times the method was called
    print(f"{method.__qualname__} was called {len(inputs)} times:")

    # Loop over inputs and outputs and
    # print them in the specified format
    for input_data, output_data in zip(inputs, outputs):
        # Decode the byte strings and format the output
        input_str = input_data.decode('utf-8')
        output_str = output_data.decode('utf-8')
        print(f"{method.__qualname__}(*{input_str}) -> {output_str}")
