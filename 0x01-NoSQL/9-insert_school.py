#!/usr/bin/env python3
"""
insert a document
"""


def insert_school(mongo_collection, **kwargs):
    """Inserts a new document into the mongo_collection based on kwargs.
    """
    result = mongo_collection.insert_one(kwargs)
    return str(result.inserted_id)
