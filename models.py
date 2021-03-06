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
    
class Movies_info(Document):
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
	
	
connect("yingyue", host='120.26.56.94',port = 27001, username='yingyue_user_joy',password='joy_hapslpes23')


if __name__ == "__main__":
    #pageindex = 2
    #pagesize = 10
    #cn = Cinemainfo.objects(location__near=[114.0467, 22.60293], location__max_distance=2000)
            #.skip( pagesize*(pageindex-1)).limit(pagesize)
    #for  c in cn:
    #     print c
    #import sys
    #sys.exit()

    mc = MC()
    mc.db("yingyue")
    cn = mc.collection("cinemainfo").find({"location":{"$near":{"$geometry":{"type":"Point","coordinates":[112,22]}, "$maxDistance":30000}}}).count()
    print cn
    cn = mc.collection("cinemainfo").find({"location":{"$near":{"$geometry":{"coordinates":[114.0467, 22.60293]}, "$maxDistance":30}}})
    print cn[0]

