#!/usr/bin/env python3
"""
Provide some stats about Nginx logs stored in MongoDB
Database: logs, Collection: nginx
Display (same as example):
- First line: x logs, x being the number of documents in this collection
- Second line: Methods
- 5 lines with method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
- One line with method=GET, path=/status
- Top 10 most present IPs in the collection
"""

from pymongo import MongoClient

# Define the list of HTTP methods to check
METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE"]


def log_stats(mongo_collection):
    """
    Provide some stats about Nginx logs stored in MongoDB

    Parameters:
    mongo_collection (Collection): The pymongo collection object (MongoDB
    collection) containing the Nginx logs from which to retrieve stats.

    Displays:
    - The total number of logs.
    - The count of logs for each HTTP method in the
    list ["GET", "POST", "PUT", "PATCH", "DELETE"].
    - The number of logs where method is "GET" and path is "/status".
    - The top 10 most present IPs in the collection, sorted by frequency.
    """
    # Count the total number of documents in the
    # collection and print the total number of logs
    total_logs = mongo_collection.count_documents({})
    # print(f"{mongo_collection.estimated_document_count()} logs")
    print(f"{total_logs} logs")

    # Print/display the number of logs per/for each method
    print("Methods:")
    for method in METHODS:
        # Count the number of documents for each HTTP method
        count = mongo_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    # Count and print the number of logs/documents
    # where method is "GET" and path is "/status"
    status_check_count = mongo_collection.count_documents({"method": "GET",
                                                           "path": "/status"})
    print(f"{status_check_count} status check")

    # Aggregate pipeline to get the top 10
    # most present IPs, sorted by frequency
    print("IPs:")
    pipeline = [
        # Group by IP and count occurrences
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        # Sort by count in descending order
        {"$sort": {"count": -1}},
        # Limit to top 10 IPs
        {"$limit": 10}
    ]
    top_ips = mongo_collection.aggregate(pipeline)

    # Print/display the top 10 IPs with their counts
    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    # Connect to MongoDB server and access the
    # 'nginx' collection within the 'logs' database
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    # Call the 'log_stats' function to display the Nginx log stats
    log_stats(nginx_collection)
