#!/usr/bin/env python3
"""def list_all function definition"""

def list_all(mongo_collection):
    """lists all documents in a collection"""
    doc_list = []
    for doc in mongo_collection.find():
        doc_list.append(doc)
    return doc_list

