from models.storage.base import BaseStorage


class Chain():

    def __init__(self, **kwargs):
        self.storage = BaseStorage.factory(**kwargs.get('storage'))

    def add_corpus(self, text):
        self.storage.add_corpus(text)

    def build_phrase(self, first_word):
        self.storage.build_phrase(first_word)
