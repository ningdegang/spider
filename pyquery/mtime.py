#!/usr/bin/env python
# -*- coding:utf-8 -*-
###===========================###
import json
import datetime
import requests
from pyquery  import PyQuery 


proxy = { "http":"http://10.197.1.52:8080" }
allcinemabycity = "http://api.m.mtime.cn/OnlineLocationCinema/OnlineCinemasByCity.api?locationId=366"
cinemabyid="http://api.m.mtime.cn/Showtime/ShowtimeMovieAndDateListByCinema.api?cinemaId=3774"
cinemaschedule="http://api.m.mtime.cn/Showtime/ShowTimesByCinemaMovieDate.api?cinemaId=3774&movieId=194879&date=2015-11-15"
cinemadetail="http://api.m.mtime.cn/Cinema/Detail.api?cinemaId=3774"
showtime = "http://api.m.mtime.cn/Showtime/LocationMovies.api?locationId=366"
coming = "http://api.m.mtime.cn/Movie/MovieComingNew.api?locationId=366"
moviecomments="http://api.m.mtime.cn/Movie/HotLongComments.api?movieId=194879"
movie_tickets = "http://piao.mtime.com/onlineticket/3774_147115393/seat/"
movie_tickets = "http://api.m.mtime.cn/Showtime/OnlineSeatsByShowTimeID.api?dId=147130820"
headers={"X-Mtime-Mobile-PushToken": "3916021343709077051.658892915382386192"}
#doc = requests.get(url, headers=headers, proxies=proxy).content.decode("utf-8", "ignore")
class City(object):
    def __init__(self,id):
        self.id= id
        self. data= requests.get(url=self.url, proxies=proxy).content.decode('utf-8', 'ignore')
        self.movie_urls = [a.attr.href for a in self.html("a[href^='http'].pic.__r_c_")]
        self.playing_movies = []
        self.coming_movies = []
        self.cinemas = []


class Movie(object):
    def __init__(self,id):
        self. id= id
        self.data= requests.get(url=self.url, proxies=proxy).content.decode('utf-8', 'ignore')
        self.title = ""
        self.release_data = ""
        self.director = ""
        self.actors = ""
        self.detributor = ""
        self.description = ""
        self.scenarist = ""
        self.poster_url = ""


class Cinema(object):

    def __init__(self, **kwargs):
        self.name = kwargs['cname']
        self.district = kwargs['dsname']
        self.location = kwargs['address']
        #self.city = '' #在json中取不到,需要从City实例中取 

        #temp = json.loads(
            #re.sub(r'(,|\{)([^:]+):', r'\1"\2":', kwargs['feature']),
        #)
        #self.description = '\n'.join([
            #temp['FeatureFoodCinemaContent'],
            #temp['FeatureGameContent'],
            #temp['FeatureFoodContent'],
        #])
        temp = json.loads(
            requests.get('http://api.map.baidu.com/geocoder/v2/?ak=eKeDnKN1sZHFHW908pyBAowt&output=json&address='+self.location).text
        )
        if temp['status'] != 0:
            raise Exception(json.dumps(temp))
        else:
            self.lng = temp['result']['location']['lng']
            self.lat = temp['result']['location']['lat']


class MovieShowtime():
    def __init__(self, **kwargs):
        self.starttime = datetime.datetime.strptime(kwargs['realtime'], '%B, %d %Y %H:%M:%S')
        self.endtime = self.starttime + datetime.timedelta(hours=2)
        self.d2d3 = kwargs['version']
        self.language = kwargs['language']
        self.cinema = Cinema._cinema[kwargs['cinemaId']]


if __name__ == '__main__':
    #from multiprocessing.pool import ThreadPool
    #tp = ThreadPool(25)
    #url_list = open('mtime.urls').read().replace(' ', '').replace('\r', '').split('\n')
    # citys = tp.map(lambda url: City(url), filter(None, url_list))
    # for c in citys:
        # save_in_database(c)
    city = City('http://theater.mtime.com/China_Guangdong_Province_Shenzen/')

