import sqlalchemy as sa
from markovify.splitters import split_into_sentences
from sqlalchemy import Column, Integer, String, and_, func
from sqlalchemy.ext.declarative import declarative_base

from models.storage.base import BaseStorage

Base = declarative_base()


class Vertex(Base):
    __tablename__ = 'vertexes'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)


class Edge(Base):
    __tablename__ = 'edges'
    id = Column(Integer, primary_key=True)
    from_vertex = Column(Integer, nullable=False)
    to_vertex = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False, default=0)


class Begin(Base):
    __tablename__ = 'begins'
    id = Column(Integer, primary_key=True)
    vertex_id = Column(Integer,  nullable=False)


class End(Base):
    __tablename__ = 'ends'
    id = Column(Integer, primary_key=True)
    vertex_id = Column(Integer,  nullable=False)


class PostgresStorage(BaseStorage):

    def __init__(self, config):
        self.config = config

    def add_corpus(self, corpus):
        sentences = split_into_sentences(corpus)

        for sentence in sentences:
            words = sentence.split()
            if not words or len(words) == 1:
                continue

            # selecting words from db
            q = sa.select(Vertex.__table__.c).where(Vertex.word.in_(words))
            alchemy_words = [row for row in self.config.connection.execute(q)]

            # get id of words in db in right order
            db_words_ids = {}
            for i, word in enumerate(words):
                try:
                    alchemy_word = next(j for j in alchemy_words if j['word'] == word)
                    id = alchemy_word['id']
                except StopIteration:
                    q = sa.insert(Vertex).values(word=word)
                    result = self.config.connection.execute(q)
                    id = result.inserted_primary_key[0]

                db_words_ids[i] = id

            edges = []
            # building edges
            for i, word in enumerate(words):
                if i == len(words) - 1:
                    break
                edges.append((db_words_ids[i], db_words_ids[i + 1]))

            # get existing edges
            q = sa.select(Edge.__table__.c).where(
                and_(
                    Edge.from_vertex.in_([edge[0] for edge in edges]),
                    Edge.to_vertex.in_([edge[1] for edge in edges]),
                )
            )
            alchemy_edges = [row for row in self.config.connection.execute(q)]

            edges_id_to_increment = []
            for edge in edges:
                try:
                    edge_id = next(
                        j['id'] for j in alchemy_edges
                        if j['from_vertex'] == edge[0] and j['to_vertex'] == edge[1]
                    )
                    pass
                except StopIteration:
                    q = sa.insert(Edge).values(
                        from_vertex=edge[0],
                        to_vertex=edge[1]
                    )
                    result = self.config.connection.execute(q)
                    edge_id = result.inserted_primary_key[0]
                    pass

                edges_id_to_increment.append(edge_id)

            if edges_id_to_increment:
                q = sa.update(Edge.__table__).where(Edge.count.in_(edges_id_to_increment)).values(
                    {'count': Edge.count + 1})
                self.config.connection.execute(q)

            q = sa.select(Begin.__table__.c).where(Begin.vertex_id == db_words_ids[0])
            result = self.config.connection.execute(q).first()
            if not result:
                q = sa.insert(Begin).values(vertex_id=db_words_ids[0])
                self.config.connection.execute(q)

            q = sa.select(End.__table__.c).where(End.vertex_id == db_words_ids[len(words) - 1])
            result = self.config.connection.execute(q).first()
            if not result:
                q = sa.insert(End).values(vertex_id=db_words_ids[len(words) - 1])
                self.config.connection.execute(q)

    def build_phrase(self, first_word=None):

        global current_id
        if first_word:
            q = sa.select(Begin.__table__.c).where(Vertex.word == first_word)
            word = self.config.connection.execute(q).first()
            if word:
                current_id = word['vertex_id']
        else:
            q = sa.select(Begin.__table__.c).order_by(func.random())
            current_id = self.config.connection.execute(q).first()['vertex_id']

        counter = 0
        result = []
        while True:
            counter += 1

            if counter >= 100:
                break

            q = sa.select(Vertex.__table__.c).where(Vertex.id == current_id)
            word = self.config.connection.execute(q).first()
            result.append(word['word'])

            q = sa.select(End.__table__.c).where(End.vertex_id == current_id)
            if self.config.connection.execute(q).first():
                break

            q = sa.select(Edge.__table__.c).order_by(Edge.count).where(
                Edge.from_vertex == current_id
            )
            r = self.config.connection.execute(q).first()
            current_id = r['to_vertex']

        print(' '.join(result))
