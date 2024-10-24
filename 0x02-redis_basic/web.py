#!/usr/bin/env python3
"""
This module provides a function to fetch HTML
content from a URL and cache it using Redis.
The caching mechanism includes tracking the number of times a URL
is accessed and setting an expiration time for the cached content.
"""

from functools import wraps
import redis
import requests
from typing import Callable

# Initialize Redis client connection
r = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """
    A decorator to count how many
    times a method is called.

    Args:
        method (Callable): The method to be decorated.

    Returns:
        Callable: The wrapped method
        that increments the call count.
    """
    @wraps(method)
    def wrapper(*args, **kwargs):
        # Increment the count in Redis
        # using the method's qualified name
        r.incr(f"count:{method.__qualname__}")
        # Execute the original method
        # and return its output
        return method(*args, **kwargs)

    return wrapper


@count_calls
async def get_page(url: str) -> str:
    """
    Fetches the HTML content from a given URL
    and caches it in Redis with an expiration time.

    Args:
        url (str): The URL to fetch.

    Returns:
        str: The HTML content of the page.
    """
    # Check if the content is already cached in Redis
    cached_content = r.get(f"cache:{url}")
    if cached_content:
        # If cached, decode and return the content
        return (await cached_content).decode('utf-8')

    # If not cached, fetch the content using requests
    response = requests.get(url)
    html_content = response.text

    # Cache the content in Redis
    # with a 10-second expiration time
    r.setex(f"cache:{url}", 10, html_content)

    return html_content


if __name__ == "__main__":
    # Test the function with a slow response URL
    url = "http://slowwly.robertomurray.co.uk/"
    print(get_page(url))  # Fetch and cache the page
    print(get_page(url))  # Retrieve the cached page


# #!/usr/bin/env python3
# """
# This module provides a function to fetch HTML
# content from a URL and cache it using Redis.
# The caching mechanism includes tracking the number of times a URL
# is accessed and setting an expiration time for the cached content.
# """

# import redis
# import requests
# from functools import wraps
# from typing import Callable

# # Initialize Redis client connection
# r = redis.Redis()


# def count_calls(method: Callable) -> Callable:
#     """
#     A decorator to count how many times a method is called.

#     Args:
#         method (Callable): The method to be decorated.

#     Returns:
#         Callable: The wrapped method that increments the call count.
#     """
#     @wraps(method)
#     def wrapper(url: str) -> str:
#         """Wrapper function that increments
#           call count and manages caching."""
#         # Generate Redis keys for counting and caching
#         key_count = f"count:{url}"
#         key_cache = f"cache:{url}"

#         # Increment the count of how many times the URL has been accessed
#         r.incr(key_count)

#         # Check if the content is already cached in Redis
#         cached_content = r.get(key_cache)
#         if cached_content:
#             # If cached, decode and return the content
#             return cached_content.decode('utf-8')

#         # If not cached, fetch the content using the original method
#         html_content = method(url)

#         # Cache the content in Redis with a 10-second expiration time
#         r.setex(key_cache, 10, html_content)

#         return html_content

#     return wrapper


# @count_calls
# def get_page(url: str) -> str:
#     """
#     Fetches the HTML content from a given URL
#     and caches it in Redis with an expiration time.

#     Args:
#         url (str): The URL to fetch.

#     Returns:
#         str: The HTML content of the page.
#     """
#     # Perform an HTTP GET request to retrieve the content of the URL
#     response = requests.get(url)
#     return response.text


# if __name__ == "__main__":
#     # Test the function with a slow response URL
#     print(get_page('http://slowwly.robertomurray.co.uk/'))
