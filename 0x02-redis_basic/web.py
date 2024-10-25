#!/usr/bin/env python3
"""Module for implementing an expiring web cache and tracker with improved error handling
and thread safety.
"""
import requests
import time
import threading
from functools import wraps
from typing import Dict, Any, Optional
from datetime import datetime

class WebCache:
    """Class to manage web page caching and access tracking."""

    def __init__(self, expiration_time: int = 10):
        """Initialize the cache with configurable expiration time.

        Args:
            expiration_time (int): Cache expiration time in seconds
        """
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._lock = threading.Lock()
        self.expiration_time = expiration_time

    def get_cache_entry(self, url: str) -> Optional[Dict[str, Any]]:
        """Get a cache entry if it exists and is not expired.

        Args:
            url (str): The URL to check in cache

        Returns:
            Optional[Dict[str, Any]]: Cache entry if valid, None otherwise
        """
        with self._lock:
            if url not in self._cache:
                return None

            entry = self._cache[url]
            if time.time() - entry["timestamp"] > self.expiration_time:
                del self._cache[url]
                return None

            entry["count"] += 1
            return entry

    def set_cache_entry(self, url: str, content: str) -> None:
        """Set a new cache entry for a URL.

        Args:
            url (str): The URL to cache
            content (str): The content to cache
        """
        with self._lock:
            self._cache[url] = {
                "content": content,
                "timestamp": time.time(),
                "count": 1
            }

    def get_access_count(self, url: str) -> int:
        """Get the number of times a URL has been accessed.

        Args:
            url (str): The URL to check

        Returns:
            int: Number of times the URL was accessed
        """
        with self._lock:
            return self._cache.get(url, {}).get("count", 0)

# Create a global cache instance
cache_manager = WebCache()

def cache(func):
    """Decorator that implements a caching system with expiration and access tracking.

    Args:
        func: The function to be decorated

    Returns:
        callable: The wrapped function with caching functionality
    """
    @wraps(func)
    def wrapper(url: str, *args, **kwargs) -> str:
        """Wrapper function that implements the caching logic.

        Args:
            url (str): The URL to fetch
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            str: The cached or newly fetched content

        Raises:
            requests.RequestException: If the URL fetch fails
        """
        # Try to get from cache first
        cached = cache_manager.get_cache_entry(url)
        if cached:
            return cached["content"]

        # Fetch new content if not in cache or expired
        content = func(url, *args, **kwargs)
        cache_manager.set_cache_entry(url, content)
        return content

    return wrapper

@cache
def get_page(url: str) -> str:
    """Fetches the content of a web page and tracks the access count.

    Args:
        url (str): The URL of the webpage to fetch

    Returns:
        str: The decoded content of the webpage

    Raises:
        requests.RequestException: If the URL fetch fails
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch {url}: {str(e)}")

def get_access_count(url: str) -> int:
    """Gets the number of times a URL has been accessed.

    Args:
        url (str): The URL to check

    Returns:
        int: The number of times the URL has been accessed
    """
    return cache_manager.get_access_count(url)
