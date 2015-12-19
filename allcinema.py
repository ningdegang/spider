#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import models
import time
from query import mtime

def factory_get(db, collection):
    def deco(func):
        def _deco():
            mc = models.MC()
            mc.db(db)
            c = mc.collection(collection)
            ret = func()
            print "processing: " + func.func_name
            for it in ret: 
                try:
                    it = json.loads(it)
                    if collection == "movie_schedule" and c.find({"cid":it["cid"],
                            "mid":it["mid"],"dt":it["dt"]}).count() == 0:
                        mc.save(it)
                        continue
                    mc.save(it)
                except Exception as e:
                    continue
            mc.close()
            return ret
        return _deco
    return deco

@factory_get("yingyue", "cinemainfo")
def get_all_cinema():
    ret = list()
    for key in mtime.id2name.keys():
        print key
        try:
            ret.extend(mtime.get_all_cinema_by_city(key))
        except:
            continue
    return ret

@factory_get("yingyue", "movie_info")
def get_all_showtime_movie():
    #for key in mtime.id2name.keys():
    ret = mtime.get_showtime_movies_by_city(366)
    return ret

@factory_get("yingyue", "movie_info")
def get_all_coming_movie():
    #for key in mtime.id2name.keys():
    ret = mtime.get_coming_movies_by_city(366)
    return ret

def get_all_movie_schedule():
    ret = list()
    mc = models.MC()  
    mc.db("yingyue")
    cl = mc.collection("cinemainfo")
    cinemas = cl.find()
    mc.collection("movie_schedule")
    for c in cinemas:
        for m in c["showinfo"]:
            for d in m["showDates"]:
                cid, mid , d = c["cid"],m["movieId"], d
                try:
                    a = mtime.get_cinema_movie_schedule(cid, mid, d)
                    a = json.loads(a)
                    mc.save(a)
                except:
                    continue
    
    mc.close()

def drop_cinema_movie_info():
    mc = models.MC()  
    mc.db("yingyue")
    ci = mc.collection("cinemainfo")
    ci.drop()
    ci.ensure_index([("location", "2dsphere")]) 
    mi = mc.collection("movie_info")
    mi.drop() 
    mc.close()
    
if __name__ == "__main__":
    print time.ctime()
    drop_cinema_movie_info()
    get_all_cinema()
    get_all_showtime_movie()
    get_all_coming_movie()
    get_all_movie_schedule()
