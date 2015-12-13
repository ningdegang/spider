#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import models
from query import mtime

def factory_get(db, collection):
    def deco(func):
        def _deco():
            mc = models.MC()
            mc.db(db)
            c = mc.collection(collection)
            c.drop()
            ret = func()
            for it in ret: 
                it = json.loads(it)
                mc.save(it)
            if collection == "cinema": c.create_index({"location":'2dsphere'})
            mc.close()
            return ret
        return _deco
    return deco

@factory_get("test", "cinema")
def get_all_cinema():
    for key in mtime.id2name.keys():
        ret = mtime.get_all_cinema_by_city(key)
    return ret

@factory_get("test", "showtime_movies")
def get_all_showtime_movie():
    for key in mtime.id2name.keys():
        ret = mtime.get_showtime_movies_by_city(key)
    return ret

@factory_get("test", "coming_movies")
def get_all_coming_movie():
    for key in mtime.id2name.keys():
        ret = mtime.get_coming_movies_by_city(key)
    return ret

@factory_get("test", "movie_schedule")
def get_all_movie_schedule():
    ret = list()
    mc = models.MC()  
    mc.db("test")
    cl = mc.collection("cinema")
    cinemas = cl.find()
    for c in cinemas:
        for m in c["showinfo"]:
            for d in m["showDates"]:
                cid, mid , d = c["cid"],m["movieId"], d
                print cid, mid, d
                a = mtime.get_cinema_movie_schedule(cid, mid, d)
                ret.append(a)
                return ret
    return ret
    
    
if __name__ == "__main__":
    get_all_cinema()
    #get_all_showtime_movie()
    #get_all_coming_movie()
    #print get_all_movie_schedule()
