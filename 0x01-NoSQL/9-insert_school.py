#!/usr/bin/env python3
""" insert_school function"""

def insert_school(mongo_collection, **kwargs):
    """inserts a new document in a collection"""
    new_school = mongo_collection.insert_many([kwargs])
    return new_school
