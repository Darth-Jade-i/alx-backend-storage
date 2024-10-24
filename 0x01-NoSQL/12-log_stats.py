#!/usr/bin/env python3
"""
Write a Python script that provides some
stats about Nginx logs stored in MongoDB:

Database: logs
Collection: nginx
Display (same as the example):
first line: x logs where x is the
number of documents in this collection
second line: Methods:
5 lines with the number of documents with the
method = ["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
(see example below - warning: it’s a tabulation before each line)
one line with the number of documents with:
method=GET
path=/status
You can use this dump as data sample: dump.zip
"""

# import pymongo
from pymongo import MongoClient


def log_nginx_stats(mongo_collection):
    """
    Provides some stats about Nginx logs stored in MongoDB.

    Args:
    mongo_collection: The MongoDB collection containing the Nginx logs.

    Displays:
    - The total number of logs.
    - The count of logs for each HTTP method in the
    list ["GET", "POST", "PUT", "PATCH", "DELETE"].
    - The number of logs where method is "GET" and path is "/status".
    """
    # Print the total number of logs
    print(f"{mongo_collection.estimated_document_count()} logs")

    # Print the number of logs for each method
    print("Methods:")
    for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count and print the number of logs
    # where method is "GET" and path is "/status"
    number_of_gets = mongo_collection.count_documents({"method": "GET",
                                                       "path": "/status"})
    print(f"{number_of_gets} status check")


if __name__ == "__main__":
    # Connect to the MongoDB server and access the
    # 'nginx' collection within the 'logs' database
    mongo_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx

    # Call the function to display the Nginx log stats
    log_nginx_stats(mongo_collection)


# #!/usr/bin/env python3
# """
# Write a Python script that provides some
# stats about Nginx logs stored in MongoDB:

# Database: logs
# Collection: nginx
# Display (same as the example):
# first line: x logs where x is the
# number of documents in this collection
# second line: Methods:
# 5 lines with the number of documents with the
# method = ["GET", "POST", "PUT", "PATCH", "DELETE"] in this order
# (see example below - warning: it’s a tabulation before each line)
# one line with the number of documents with:
# method=GET
# path=/status
# You can use this dump as data sample: dump.zip
# """

# import pymongo
# from pymongo import MongoClient

# def log_nginx_stats(mongo_collection, option=None):
#     """
#     Provides some stats about Nginx logs stored in MongoDB.

#     Args:
#     mongo_collection: The MongoDB collection containing the Nginx logs.
#     option: (optional) The specific HTTP method to filter logs by.

#     Displays:
#     - The total number of logs if no option is provided.
#     - The count of logs for each HTTP method in the list
#       ["GET", "POST", "PUT", "PATCH", "DELETE"] if no option is provided.
#     - The count of logs for a specific method if option is provided.
#     - The number of logs where method is "GET"
#       and path is "/status" if no option is provided.
#     """
#     # If an option (specific HTTP method) is provided
#     if option:
#         # Count documents that match the provided method using regex
#         value = mongo_collection.count_documents({"method":
#                                                   {"$regex": option}})
#         # Print the count for the specified method
#         print(f"\tmethod {option}: {value}")
#         return

#     # Print the total number of logs
#     print(f"{mongo_collection.estimated_document_count()} logs")

#     # Print the number of logs for each method
#     print("Methods:")
#     for method in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
#         # Recurse with each method as the option
#         log_nginx_stats(mongo_collection, method)

#     # Count and print the number of logs where
#       method is "GET" and path is "/status"
#     number_of_gets = mongo_collection.count_documents({"method": "GET",
#                                                        "path": "/status"})
#     print(f"{number_of_gets} status check")

# if __name__ == "__main__":
#     # Connect to the MongoDB server and access the
#       'nginx' collection within the 'logs' database
#     mongo_collection = MongoClient('mongodb://127.0.0.1:27017').logs.nginx

#     # Call the function to display the Nginx log stats
#     log_nginx_stats(mongo_collection)


# #!/usr/bin/env python3
# """
# This script connects to a MongoDB database
# and retrieves statistics about Nginx logs.
# The stats include the total number of logs,
# the count of logs by method type, and the
# number of logs with specific path and method.
# """

# from pymongo import MongoClient

# # Connect to the MongoDB server running
# on localhost with the default port 27017
# client = MongoClient('mongodb://127.0.0.1:27017')

# # Access the 'logs' database
# db = client.logs

# # Access the 'nginx' collection within the 'logs' database
# collection = db.nginx

# # Get the total number of documents (logs) in the collection
# total_logs = collection.count_documents({})
# print(f"{total_logs} logs")

# # Print a header for the methods section
# print("Methods:")

# # List of HTTP methods to check
# methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

# # Loop through each method and count
# how many documents have that method
# for method in methods:
#     # Count the documents where the 'method'
#       field matches the current method
#     method_count = collection.count_documents({"method": method})
#     print(f"\tmethod {method}: {method_count}")

# # Count the number of documents where the
# 'method' is 'GET' and the 'path' is '/status'
# status_check_count = collection.count_documents({"method": "GET",
#                                                   "path": "/status"})
# print(f"{status_check_count} status check")
