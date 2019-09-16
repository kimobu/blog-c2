import sys,datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))
    
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(User, backref="posts")
    subject = Column(Text())
    body = Column(Text())
    date = Column(DateTime, default=datetime.datetime.now)

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    body = Column(Text())
    date = Column(DateTime, default=datetime.datetime.now)
    post_id = Column(Integer, ForeignKey('posts.id'))
    posts = relationship(Post, backref="comments")

engine = create_engine('sqlite:///blog.db')

Base.metadata.create_all(engine)

