from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()

"""
one to one
one to many -> many to one
many to many
"""


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    title = Column(String, unique=False, nullable=False)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author')


class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, unique=False, nullable=False)
    posts = relationship('Post')


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, autoincrement=True, primary_key=True)
    url = Column(String, nullable=False, unique=True)
    name = Column(String, unique=False, nullable=False)
