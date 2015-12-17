#!/usr/bin/env python
# -*- coding:utf-8 -*-
###===========================###
import json
import datetime
import requests
import pyquery


proxy = { "http":"http://10.197.1.52:8080" }
allcinemabycity = "http://api.m.mtime.cn/OnlineLocationCinema/OnlineCinemasByCity.api?locationId=%d"
cinemashowinfobyid="http://api.m.mtime.cn/Showtime/ShowtimeMovieAndDateListByCinema.api?cinemaId=%d"
cinemaschedule="http://api.m.mtime.cn/Showtime/ShowTimesByCinemaMovieDate.api?cinemaId=%d&movieId=%d&date=%s"
cinemadetail="http://api.m.mtime.cn/Cinema/Detail.api?cinemaId=3774"
showtime = "http://api.m.mtime.cn/Showtime/LocationMovies.api?locationId=%d"
coming = "http://api.m.mtime.cn/Movie/MovieComingNew.api?locationId=%d"
moviecomments="http://api.m.mtime.cn/Movie/HotLongComments.api?movieId=194879"
movie_tickets = "http://piao.mtime.com/onlineticket/%d_%d/seat/"
#movie_tickets = "http://api.m.mtime.cn/Showtime/OnlineSeatsByShowTimeID.api?dId=147130820"
header= {"User-Agent": "Mozilla/5.0  AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"}

id2name={366:u"深圳", 290:u"北京",292:u"上海",365:u"广州",974:u"杭州"}
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
        ret["cityid"] = cid
        ret["description"] = get_feature(mtime.get("feature"))
        ret["score"] = int(mtime.get("ratingFinal")*10)
        ret["location"] =  { "type" : "Point", "coordinates" : [mtime.get("latitude"),mtime.get("longitude")]}
        url = cinemashowinfobyid % ret["cid"]
        tmp = json.loads(requests.get(url=url, headers=header).content.decode('utf-8', 'ignore'))
        ret["showinfo"] = tmp["movies"]
        return ret
    ret = map(mtime_cinema_to_local, data)
    ret = map(lambda x:json.dumps(x)+"\n", ret)
    return ret
    
def mtime_showtime_movie_to_local(mtime):
    ret = dict()
    ret["title"] = mtime.get("t")
    ret["mid"] = mtime.get("id")
    ret["type"] = mtime.get("movieType")
    ret["release_date"] = mtime.get("rd") and datetime.datetime.strptime(mtime.get("rd"), "%Y%m%d").strftime("%Y-%m-%d") or u"未知"
    ret["length"] = mtime.get("d")
    ret["director"] = mtime.get("dN")
    ret["actors"] = mtime.get("aN1") + " " + mtime.get("aN2")
    #ret["shortdesc"] = mtime.get("commonSpecial")
    doc = pyquery.PyQuery("http://movie.mtime.com/%d/" % ret["mid"])
    p = doc("div#movie_warp dt.__r_c_ p.mt6.lh18")
    p = p and p[0].text or u"暂无详细描述"
    ret["description"] = p
    ret["poster"] = mtime.get("img")
    ret["score"] = int((mtime.get("r") and mtime["r"] >=0 or 6 )*10)
    return ret

def mtime_coming_movie_to_local(mtime):
    ret = dict()
    ret["title"] = mtime.get("title")
    ret["mid"] = mtime.get("id")
    ret["type"] = mtime.get("type")
    ret["release_date"] = mtime.get("releaseDate")
    ret["director"] = mtime.get("director")
    ret["actors"] = mtime.get("actor1") + " " + mtime.get("actor2")
    ret["poster"] = mtime.get("image")
    doc = pyquery.PyQuery("http://movie.mtime.com/%d/" % ret["mid"])
    p = doc("div#movie_warp dt.__r_c_ p.mt6.lh18")
    p = p and p[0].text or u"暂无详细描述"
    ret["description"] = p
    p = doc("div#ratingRegion.grade_tool div.gradebox.__r_c_ b")
    p = p and int(p[0].text) or 6
    ret["score"] = p*10
    p = doc("div.otherbox.__r_c_ span")
    p = p and p[0].text or u"暂无详细"
    ret["length"] = p
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

def get_showtime_movies_by_city(cid):
    return get_all_movie_by_city_and_status(showtime,cid, 1, mtime_showtime_movie_to_local) 

def get_coming_movies_by_city(cid):
    return get_all_movie_by_city_and_status(coming, cid, 2, mtime_coming_movie_to_local)

def get_cinema_movie_schedule(cid, mid, dt):
    url = cinemaschedule % (cid, mid, dt)
    print url
    data= json.loads(requests.get(url=url, headers=header).content.decode('utf-8', 'ignore'))
    data = data["s"]
    def formatdata(it):
        print it
        if it.get("provider"):
            it["ticketurl"] = movie_tickets % (cid, it["provider"][0]["dId"])
        del(it["provider"])
        return it
    data = map(formatdata, data)
    ret = {"cid":cid, "mid":mid, "dt":dt}
    ret["s"] = data
    return json.dumps(ret)
    

if __name__ == '__main__':
    #ret = get_all_cinema_by_city(366)
    #for c in ret: print c
    ret = get_showtime_movies_by_city(366)
    for c in ret: print c; break
    ret = get_coming_movies_by_city(366)
    for c in ret: print c; break
    #print get_cinema_movie_schedule(1900, 219145, "12-05")
    
