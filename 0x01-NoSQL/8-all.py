#!/usr/bin/env python3
"""
8-all.py

Function to list all documents in a collection.

Prototype: def list_all(mongo_collection):
- Return an empty list if no document in the collection
- mongo_collection will be the pymongo collection object

This script defines a function to list
all documents in a MongoDB collection.
The function returns an empty list if
there are no documents in the collection.
"""

# from pymongo.collection import Collection
# from typing import List, Dict


# def list_all(mongo_collection: Collection) -> List[Dict]:
def list_all(mongo_collection):
    """
    List all documents in the given MongoDB collection.

    Parameters:
    mongo_collection (Collection): The pymongo collection object from
                                    which to list/retrieve documents.

    Returns:
    List[Dict]: A list of dictionaries representing all
                the documents in the collection.
                Returns an empty list if the collection is
                empty, has no documents or not provided.
    """
    # Check if the collection is not provided or empty
    if mongo_collection is None or mongo_collection.count_documents({}) == 0:
        return []

    # Fetch/Retrieve all documents from the collection
    documents = mongo_collection.find()

    # Convert the cursor to a list and return it
    # return list(documents)
    return [document for document in documents]
