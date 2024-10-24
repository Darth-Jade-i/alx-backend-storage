#!/usr/bin/env python3
"""
101-students.py

This script defines a function to return all students
sorted by their average score in a MongoDB collection.

Prototype: def top_students(mongo_collection):
- mongo_collection will be the pymongo collection object.
- The average score must be part of each
item returned with the key 'averageScore'.
"""

# from pymongo.collection import Collection
# from typing import List


# def top_students(mongo_collection: Collection) -> List[dict]:
def top_students(mongo_collection):
    """
    Returns all students sorted by their average score.

    Parameters:
    mongo_collection (Collection): The pymongo collection
    object containing the student documents.

    Returns:
    List[dict]: A list of dictionaries representing the
    student documents sorted by their average score.
    Each dictionary will include an additional key
    'averageScore' representing the average score.
    """
    # Use the aggregate method to calculate the average
    # score for each student and sort the results
    # 1. Use `$project` to calculate the average score of each student.
    #    - `name`: Pass through the 'name' field
    #       from the original document.
    #    - `averageScore`: Calculate the average of
    #       the 'score' field within the 'topics' array.
    # 2. Use `$sort` to sort the documents by the
    #   calculated `averageScore` in descending order.
    students = mongo_collection.aggregate([
        {
            "$project": {
                # Include the 'name' field in the output.
                "name": 1,
                # Calculate and include 'averageScore'.
                "averageScore": {"$avg": "$topics.score"}
            }
        },
        {
            # Sort the documents by 'averageScore' in descending order.
            "$sort": {"averageScore": -1}
        }
    ])

    # Convert the cursor returned by aggregate() to a list and return it.
    # return list(students)
    return [student for student in students]


# #!/usr/bin/env python3
# """
# This script defines a Python function
# `top_students` that returns all students sorted
# by their average score from a MongoDB collection.
# """


# def top_students(mongo_collection):
#     """
#     Returns all students sorted by their average score.

#     Args:
#     mongo_collection: The pymongo collection
#     object containing the student data.

#     Returns:
#     A list of students, each student document includes
#     an additional key `averageScore` which represents
#     the student's average score across all topics.
#     The list is sorted in descending order based on the `averageScore`.
#     """

#     # The aggregation pipeline is used to process
#     and transform the documents in the collection.
#     # This pipeline is composed of several stages,
#     each modifying the documents in some way.

#     # Step 1: Add a new field `averageScore` to each document.
#     # The `$project` stage is used to include or exclude specific fields.
#     # Here, we are creating a new field `averageScore` by calculating
#     the average of the `score` values in the `topics` array.
#     pipeline = [
#         {
#             "$project": {
#                 # Include the original fields `name`
#                   and `topics` in the output documents.
#                 "name": 1,
#                 "topics": 1,
#                 # Create the `averageScore` field by averaging
#                   the `score` field within the `topics` array.
#                 "averageScore": {
#                     "$avg": "$topics.score"
#                 }
#             }
#         },
#         # Step 2: Sort the documents by the
#           `averageScore` field in descending order.
#         # This ensures that the students with the
#           highest average scores appear first in the results.
#         {
#             "$sort": {
#                 # Sort by `averageScore` in descending order
#                 "averageScore": -1
#             }
#         }
#     ]

#     # Execute the aggregation pipeline on the MongoDB collection
#     return list(mongo_collection.aggregate(pipeline))
