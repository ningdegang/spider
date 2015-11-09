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
#doc = requests.get(url, headers=headers, proxies=proxy).content.decode("utf-8", "ignore")
class City():
    def __init__(self, url):
        self.url = url
        self.html = PyQuery(requests.get(url=self.url, proxies=proxy).content.decode('utf-8', 'ignore'))
        self.city = self.html('h2.fl')
        if len(self.city) > 1:
            self.city = self.city[1]
        else:
            self.city = ''
        self.movie_urls = [a.attr.href for a in self.html("a[href^='http'].pic.__r_c_")]
        self.movies = []
        for url in self.movie_urls:
            try:
                print url
                #self.movies.append(Movie(url))
            except Exception as e:
                print(url, ':', e)


class Movie():
    def __init__(self, url):
        self.url = url
        self.html = PyQuery.doc(requests.get(url=self.url, proxies=proxy).content.decode('utf-8', 'ignore'))
        self.info = MovieInfo( self.html("div.filminfo a"))

        # self.cinemas = []
        # for c in json.loads(
        #     re.search(
        #         r'cinemasJson[^\[]+?(\[[^\n]+\]);',
        #         self.html,
        #         re.IGNORECASE,
        #     ).groups()[0]
        # ):
        #     try:
        #         self.cinemas.append(Cinema(**c))
        #     except Exception as e:
        #         print('cinema:', e)

        # self.showtimes = []
        # for ms in json.loads(
        #     re.sub(
        #         r'''new Date\(([^\)]+)\)''',
        #         r'\1',
        #         re.search(
        #             r'showtimesJson[^\[]+?(\[[^\n]+\]);',
        #             self.html,
        #             re.IGNORECASE,
        #         ).groups()[0]
        #     )
        # ):
        #     try:
        #         self.showtimes.append(MovieShowtime(**ms))
        #     except Exception as e:
        #         print('movieshowtime:', e)


class MovieInfo():
    def __init__(self, url):
        #print(url)
        self.url = url
        self.html = requests.get(self.url).content.decode('utf-8', 'ignore')
        self.title = re.search('<h1[^>]*>([^<]+)</h1', self.html).groups()[0]
        self.type = re.findall('v:genre">([^<]+)<', self.html)
        self.release_date = datetime.datetime.strptime(
            re.search('v:initialReleaseDate[^>]+>([^<]+)<', self.html).groups()[0],
            '%Y年%m月%d日',
        )
        self.release_date = datetime.date(self.release_date.year, self.release_date.month, self.release_date.day)

        match = re.search('v:runtime[^>]+>([^<]+)<', self.html)
        if match:
            self.length = match.groups()[0]
        else:
            self.length = ''

        self.director = html.unescape(
            re.search('v:directedBy">([^<]+)<', self.html).groups()[0]
        )
        self.actors = [
            a
            for i,a in enumerate(re.findall('v:starring">([^<]+)<', self.html))
            if i%2 == 0
        ]
        self.distributor = ''
        match = re.search('lh18">([^<]+)<', self.html)
        if match:
            self.description = match.groups()[0]
        else:
            self.description = ''
            
        self.scenarist = ''
        self.poster_url = re.search('src="([^"]+)"[^<]+v:image', self.html).groups()[0]


class Cinema(object):
    _cinema = {}
    def __new__(cls, **kwargs):
        if kwargs['cid'] not in cls._cinema:
            cls._cinema[kwargs['cid']] = object.__new__(cls)
        return cls._cinema[kwargs['cid']]

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

