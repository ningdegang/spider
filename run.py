#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import models
from query import letv 
from query import netease


def update_letv():
    models.init_db()
    session = models.Session()
    movies = session.query(models.OnLineMovies)
    ret = letv.one_page(1)
    for one in ret:
        one = json.loads(one)
        movie = movies.filter_by(title=one["title"]).first()
        if not movie: 
            movie = models.OnLineMovies()
            movie.title = one["title"]
            movie.url = one["url"]
            movie.language = one["language"] 
            movie.director = one["director"]
            movie.img = one["img"]
            movie.description = one["description"]
            movie.actors = one["actors"]
            movie.duration = one["duration"]
            movie.rating = int(float(one["rating"]))*10
            movie.subCategoryName = one["subCategoryName"]
            movie.releaseDate = one["releaseDate"]
            movie.ctime = one["ctime"]
            movie.area = one["area"]
            movie.tag = one["tag"]
            movie.subname = one["subname"]
            session.add(movie)
            session.commit()

if __name__ == "__main__":
    update_letv()
    #main()
