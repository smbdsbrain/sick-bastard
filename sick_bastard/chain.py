from models.base import Vertex, Edge, Begin, End
from markovify.splitters import split_into_sentences
import sqlalchemy as sa


def add_corpus(config, corpus):
    sentences = split_into_sentences(corpus)

    for sentence in sentences:
        words = sentence.split()
        begin = words[0]
        end = words[-1]


        q = sa.select(Vertex).where(Vertex.word.in_(words))
        alchemy_words = config.connection.execute(q)

        for i, word in enumerate(words):
            if i < len(words) - 1:

                try:
                    alchemy_word = next(i for i in alchemy_words if i.word == word)
                except StopIteration:
                    q = sa.insert(Vertex).values(word=)


    pass
