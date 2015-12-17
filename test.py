#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import string
from datetime import datetime, timedelta

from config import config
from mongoengine import connect, Document, PointField, IntField, ImageField, FileField, StringField, DateTimeField as MGDT
from pymongo import MongoClient

class Cinemainfo(Document):
    cid = IntField(required=True, unique=True)
    cityid = IntField()
    location = PointField()
    name = StringField()
    address = StringField()
    city = StringField()
    description = StringField()
    score = IntField()
    showinfo = StringField()


class Movie_info(Document):
    mid = IntField(required=True, unique=True)
    title = StringField()
    type = StringField()
    release_date = StringField()
    length = IntField()
    director = StringField()
    actors = StringField()
    description = StringField()
    poster =  StringField()
    score = IntField()
    status = IntField()
    

class Movie_schedule(Document):
    cid = IntField()
    mid = IntField()
    dt = StringField()
    s = StringField()
    
	
	
class MC():
    def __init__(self, host="120.26.56.94", port=27001):
        self.conn = MongoClient(host=host, port=port)
    def db(self,db):
        self.cur_db = self.conn[db]
        self.cur_db.authenticate('yingyue_user_joy', 'joy_hapslpes23')
        return self.cur_db
    def collection(self, c):
        self.cur_collection = self.cur_db[c]
        return self.cur_collection
        
    def save(self, doc):
        self.cur_collection.save(doc)
    def close(self):
        self.conn.close()

def mequery(): 
    connect("yingyue", host='120.26.56.94',port = 27001, username='yingyue_user_joy',password='joy_hapslpes23')
    cc = Cinemainfo.objects(location__near=[114.0467, 22.60293], location__max_distance=300)
    for c in cc: print c.city.encode("utf-8"), c.name.encode("utf-8"), c.address.encode("utf-8")
    
    #mm = Showtime_movies.objects().limit(2)
    #for m in mm: print m.title.encode("utf-8")
    #mm = Coming_movies.objects().limit(2)
    #for m in mm: print m.title.encode("utf-8")
    #ss = Movie_schedule.objects().limit(1)
    #for s in ss: print s.cid, s.mid, s.dt



if __name__ == "__main__":
    #mc = MC()
    #mc.db("yingyue")
    #mc.db( 
    mequery()


