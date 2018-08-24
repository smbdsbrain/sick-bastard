from abc import ABC, abstractmethod


class BaseStorage(ABC):
    providers = {}

    @abstractmethod
    def add_corpus(self, corpus):
        pass

    @abstractmethod
    def build_phrase(self, first_word=None):
        pass

    @classmethod
    def __init_subclass__(cls) -> None:
        cls.providers[cls.__module__.split('.')[-1]] = cls

    @classmethod
    def factory(cls, name, config):
        return cls.providers[name](**config)
