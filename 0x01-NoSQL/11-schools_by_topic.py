#!/usr/bin/env python3
"""
11-schools_by_topic.py

This script defines a function to return a list of schools
having a specific topic in a MongoDB collection.

Prototype: def schools_by_topic(mongo_collection, topic):
- mongo_collection will be the pymongo collection object.
- topic (string) will be the topic searched.
"""

# from pymongo.collection import Collection
# from typing import List


# def schools_by_topic(mongo_collection: Collection,
#                       topic: str) -> List[dict]:
def schools_by_topic(mongo_collection, topic):
    """
    Returns a list of schools having a specific topic.

    Parameters:
    mongo_collection (Collection): The pymongo collection
    object containing the school documents.
    topic (str): The topic to search for
    in the school documents.

    Returns:
    List[dict]: A list of dictionaries representing
    the school documents that match the topic.
    """
    # Use the find() method to retrieve all 
    # documents where the 'topics' field
    # contains the specified topic.
    schools = mongo_collection.find({"topics": topic})
    
    # Return the list of matching `school` documents.
    # return list(schools)
    return [school for school in schools]
