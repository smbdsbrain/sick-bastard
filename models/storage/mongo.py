from pymongo import MongoClient
from markovify.splitters import split_into_sentences

from models.storage.base import BaseStorage


class MongoStorage(BaseStorage):

    def __init__(self, host, port, db, **kwargs):
        self.client = client = MongoClient(host, port)
        self.db = client[db]

    def add_corpus(self, corpus):
        sentences = split_into_sentences(corpus)

        vertexes_collection = self.db['vertexes']
        edges_collection = self.db['edges']
        words_collection = self.db['words']

        for sentence in sentences:
            words = sentence.split()

            db_words = vertexes_collection.find({'word': {'$in': words}})
