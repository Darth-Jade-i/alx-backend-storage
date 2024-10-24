#!/usr/bin/env python3
"""
10-update_topics.py

This script defines a function to update all topics of a school
document based on the school's name in a MongoDB collection.

Prototype: def update_topics(mongo_collection, name, topics):
- mongo_collection will be the pymongo collection object.
- name (string) will be the school name to update.
- topics (list of strings) will be the list
of topics approached in the school.
"""

# from pymongo.collection import Collection
# from typing import List


# def update_topics(mongo_collection: Collection,
#                   name: str, topics: List[str]):
def update_topics(mongo_collection, name, topics):
    """
    Updates the list of topics for a school document
    in the collection based on the school's name.

    Parameters:
    mongo_collection (Collection): The pymongo collection
    object containing the school documents.
    name (str): The name of the school whose
    topics are to be updated.
    topics (List[str]): The new list of topics to
    set for the school document.

    Returns:
    None
    """
    # Perform the update operation to set the 'topics' field
    # for the document with the matching 'name' field.
    # The update is done using the `$set` operator.
    mongo_collection.update_many(
        # Filter: Match documents with the specified school name.
        {"name": name},
        # Update: Set the 'topics' field to the provided list.
        {"$set": {"topics": topics}}
    )
