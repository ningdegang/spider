#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import models
from query import mtime

def get_all_cinema():
     with open("citys.txt") as f:
     lines = f.readlines()
     for line in lines:
         line = json.loads(line)
         cinema = Cinema()
         if session.query(Cinema).filter_by(address=line["address"]).count() >= 1:
             continue
         cinema.city = line["city"]
         cinema.description = line["description"]
         cinema.score = line["score"]
         cinema.cid = line['cid']
         cinema.address = line["address"]
         cinema.name = line["name"]
         session.add(cinema)
         session.commit()
         CinemaGPS(
             cinema_id=cinema.id,
             point=[line['longitude'], line['latitude']],
         ).save()
                                                                                             
if __name__ == "__main__":
    get_all_cinema():
