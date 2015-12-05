#!/usr/bin/env python
# -*- coding:utf-8 -*-
###===========================###
import json
import datetime
import requests


proxy = { "http":"http://10.197.1.52:8080" }
allcinemabycity = "http://api.m.mtime.cn/OnlineLocationCinema/OnlineCinemasByCity.api?locationId=%d"
cinemabyid="http://api.m.mtime.cn/Showtime/ShowtimeMovieAndDateListByCinema.api?cinemaId=3774"
cinemaschedule="http://api.m.mtime.cn/Showtime/ShowTimesByCinemaMovieDate.api?cinemaId=3774&movieId=194879&date=2015-11-15"
cinemadetail="http://api.m.mtime.cn/Cinema/Detail.api?cinemaId=3774"
showtime = "http://api.m.mtime.cn/Showtime/LocationMovies.api?locationId=%d"
coming = "http://api.m.mtime.cn/Movie/MovieComingNew.api?locationId=%d"
moviecomments="http://api.m.mtime.cn/Movie/HotLongComments.api?movieId=194879"
movie_tickets = "http://piao.mtime.com/onlineticket/3774_147115393/seat/"
movie_tickets = "http://api.m.mtime.cn/Showtime/OnlineSeatsByShowTimeID.api?dId=147130820"
header= {"User-Agent": "Mozilla/5.0  AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"}

id2name = {366:u"\u6df1\u5733"}
def get_feature(feature):
    ret = filter(lambda x: feature.get(x), feature.keys()) or list()
    ret = map(lambda x : x.replace("has", ""), ret)
    return " ".join(ret)

def get_all_cinema_by_city(cid):
    url = allcinemabycity % cid
    data= json.loads(requests.get(url=url, headers=header).content.decode('utf-8', 'ignore'))
    def mtime_cinema_to_local(mtime):
        ret = dict()
        ret["name"] = mtime.get("cinameName")
        ret["address"] = mtime.get("address")
        ret["cid"] = mtime.get("cinemaId")
        ret["city"] = id2name.get(cid)
        ret["description"] = get_feature(mtime.get("feature"))
        ret["score"] = int(mtime.get("ratingFinal")*10)
        ret["longitude"] = mtime.get("longitude")
        ret["latitude"] = mtime.get("latitude")
        return ret
    ret = map(mtime_cinema_to_local, data)
    ret = map(lambda x:json.dumps(x)+"\n", ret)
    return ret
    
def mtime_showtime_movie_to_local(mtime):
    ret = dict()
    ret["title"] = mtime.get("t")
    ret["type"] = mtime.get("movieType")
    ret["release_date"] = mtime.get("rd")
    ret["length"] = mtime.get("d")
    ret["director"] = mtime.get("dN")
    ret["actors"] = mtime.get("aN1") + " " + mtime.get("aN2")
    ret["description"] = mtime.get("commonSpecial")
    ret["poster"] = mtime.get("img")
    ret["score"] = int(mtime.get("r")*10)
    return ret

def mtime_coming_movie_to_local(mtime):
    ret = dict()
    ret["title"] = mtime.get("title")
    ret["type"] = mtime.get("type")
    ret["release_date"] = mtime.get("releaseDate")
    ret["director"] = mtime.get("director")
    ret["actors"] = mtime.get("actor1") + " " + mtime.get("actor2")
    ret["poster"] = mtime.get("image")
    return ret


def get_all_movie_by_city_and_status(url, cid, status, func):
    url = url % cid
    print url
    data= json.loads(requests.get(url=url, headers=header).content.decode('utf-8', 'ignore'))
    if data.has_key("ms"): data = data["ms"]
    elif data.has_key("moviecomings"): data = data["moviecomings"]
    else: raise Exception("wrong data")
    ret = map(func, data)
    for a in ret: a["status"]  = status
    ret = map(lambda x:json.dumps(x)+"\n", ret)
    return ret

if __name__ == '__main__':
    #ret = get_all_cinema_by_city(366)
    #for c in ret: print c
    #ret = get_all_movie_by_city_and_status(coming,366, 1, mtime_showtime_movie_to_local)
    #for c in ret: print c
    ret = get_all_movie_by_city_and_status(coming,366, 2, mtime_coming_movie_to_local)
    for c in ret: print c
