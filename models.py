#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import string
from datetime import datetime, timedelta
from contextlib import contextmanager

from sqlalchemy import create_engine, Table, Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import String, Integer, DateTime, TIMESTAMP, BigInteger, Float

from config import config

class Query():
    def __get__(self, instance, owner):
        return Session().query(owner)

class Base(object):
    id = Column(Integer, primary_key=True)
    modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    created = Column(DateTime, default=datetime.now)
    query =  Query()

Base = declarative_base(cls=Base)
Session = None

class User(Base):
    __tablename__ = 'user'
    username = Column(String(50), unique=True, nullable=False)
    password = Column('password', String(255), nullable=False)
    token = Column(String(50))
    level = Column(Integer, default=1)


class Cinema(Base):
    __tablename__ = 'cinema'
    name = Column(String(50))
    address = Column(String(200))
    city = Column(String(50))
    description = Column(String(255))
    score = Column(Integer, default=100)




class Movie(Base):
    __tablename__ = 'movie'
    title = Column(String(50))
    type = Column(String(10))
    release_date = Column(DateTime)
    length = Column(String(10))
    director = Column(String(50))
    actors = Column(String(50))
    distributor = Column(String(50))
    description = Column(String(255))
    scenarist = Column(String(50))
    product_manager = Column(String(50))
    poster = Column(String(32))
    score = Column(Integer, default=100)
    status = Column(Integer, default=1)

class OnLineMovies(Base):
    __tablename__ = "onlinemovies"
    url = Column(String(50))
    title = Column(String(20))
    language =  Column(String(10)) 
    director = Column(String(20))
    img = Column(String(100))
    description = Column(String(500)) 
    actors = Column(String(50))
    rating = Column(Integer, default=80)
    subCategoryName = Column(String(20))
    releaseDate = Column(Integer, default=0)    
    ctime = Column(Integer, default=0) 
    area = Column(String(10))
    tag = Column(String(50))
    subname = Column(String(20))
         


class EntertainmentNews(Base):
    '娱乐八卦'
    __tablename__ = 'entertainmentnews'
    title = Column(String(100), nullable=False)
    content = Column(String(255), nullable=False)
    photo = Column(String(33*9))
    digest = Column(String(100), nullable=False)
    time = Column(String(20), nullable=False)

def init_db():
    engine = create_engine(
        config['sqlalchemy']['url'],
        encoding='utf-8',
        pool_size =config['sqlalchemy']['pool_size'],
        max_overflow = config['sqlalchemy']['max_overflow'],
        pool_recycle = config['sqlalchemy']['pool_recycle'],
        echo = config['sqlalchemy']['echo']
    )
    global Base, Session
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    return engine

if __name__ == "__main__":
    engine = init_db()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
