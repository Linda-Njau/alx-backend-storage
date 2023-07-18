#!/usr/bin/env python3
"""update_topics function"""

def update_topics(mongo_collection, name, topics):
    """ changes all topics of a document based on the name"""
    updated_topics = mongo_collection.update_many(
            {'name' : name },
            {'$set': {'topics' : topics}}
    )
    return updated_topics
