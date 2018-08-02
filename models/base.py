from sqlalchemy import (Boolean, Column, Date, DateTime,
                        ForeignKey, Index, Integer, Numeric,
                        Sequence, String, UniqueConstraint, func)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()



class Vertex(Base):
    __tablename__ = 'vertexes'
    id = Column(Integer, primary_key=True)
    word = Column(String, nullable=False)

class Edge(Base):
    __tablename__ = 'edges'
    id = Column(Integer, primary_key=True)
    from_vertex = ForeignKey('vertexes.id', nullable=False)
    to_vertex = ForeignKey('vertexes.id', nullable=False)

class Begin(Base):
    __tablename__ = 'begins'
    id = Column(Integer, primary_key=True)
    vertex_id = ForeignKey('vertexes.id', nullable=False)

class End(Base):
    __tablename__ = 'ends'
    id = Column(Integer, primary_key=True)
    vertex_id = ForeignKey('vertexes.id', nullable=False)
