#!/usr/bin/env python3
"""Module for implementing an expiring web cache and tracker
"""
import requests
import time
from functools import wraps

# Cache configuration
CACHE_EXPIRATION_TIME = 10  # seconds
CACHE = {}

def cache(fn):
    """Decorator that implements a caching system with expiration and access tracking.

    Args:
        fn (callable): The function to be decorated.

    Returns:
        callable: The wrapped function with caching functionality.
    """
    @wraps(fn)
    def wrapped(*args, **kwargs):
        """Wrapper function that implements the caching logic.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            str: The cached or newly fetched content.
        """
        url = args[0]
        current_time = time.time()

        # Clean up expired entries
        for cached_url in list(CACHE.keys()):
            if CACHE[cached_url]["timestamp"] + CACHE_EXPIRATION_TIME <= current_time:
                del CACHE[cached_url]

        # Check if URL is in cache and not expired
        if url in CACHE:
            cache_data = CACHE[url]
            if cache_data["timestamp"] + CACHE_EXPIRATION_TIME > current_time:
                cache_data["count"] += 1
                return cache_data["content"]

        # Fetch new content if not in cache or expired
        content = fn(*args, **kwargs)
        CACHE[url] = {
            "content": content,
            "timestamp": current_time,
            "count": 1
        }
        return content

    return wrapped

@cache
def get_page(url: str) -> str:
    """Fetches the content of a web page and tracks the access count.

    Args:
        url (str): The URL of the webpage to fetch.

    Returns:
        str: The decoded content of the webpage.
    """
    response = requests.get(url)
    return response.text

def get_access_count(url: str) -> int:
    """Gets the number of times a URL has been accessed.

    Args:
        url (str): The URL to check.

    Returns:
        int: The number of times the URL has been accessed, or 0 if URL is not in cache
            or has expired.
    """
    current_time = time.time()

    # Clean up expired entries before checking count
    for cached_url in list(CACHE.keys()):
        if CACHE[cached_url]["timestamp"] + CACHE_EXPIRATION_TIME <= current_time:
            del CACHE[cached_url]

    # Return count only if URL exists and is not expired
    if url in CACHE:
        cache_data = CACHE[url]
        if cache_data["timestamp"] + CACHE_EXPIRATION_TIME > current_time:
            return cache_data["count"]

    return 0
