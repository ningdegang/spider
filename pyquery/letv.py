#!/usr/bin/env python
import requests
import json
from pyquery import PyQuery as PyQ
import time

proxy = { "http":"http://10.197.1.52:8080" }
url="http://list.letv.com/apin/chandata.json?c=1&d=1&md=&o=4&p=%d&s=1"
def one_page(i):
    one = url % i
    try:
        ret = list()
        data = requests.get(url=one, proxies=proxy).content.decode('utf-8', 'ignore')
        data = json.loads(data)
        data =  data["data_list"]
        for n in data:
            if n["category"] != "1" and n["categoryName"] != u'\u7535\u5f71':continue;
            a = dict()
            try:
                vids = n["vids"].split(",")
                if(len(vids)>1):continue
                a["url"] = "http://www.letv.com/ptv/vplay/%s.html" % (n["vids"])
                a["title"] = n["name"]
                a["language"] = n["lgName"] 
                a["director"] = n["directory"]
                a["img"] = n["images"]["90*120"]
                a["description"] = n["description"]
                a["actors"] = n["starring"]
                a["duration"] = n["duration"]
                a["rating"] = n["rating"]
                a["subCategoryName"] = n["subCategoryName"]
                a["releaseDate"] = int(n["releaseDate"]) / 1000 
                a["ctime"] = int(n["mtime"]) /1000
                a["area"] = n["areaName"]
                a["tag"] = n["tag"]
                a["subname"] = n["subname"]
            except Exception ,r :
                print("something failed, reason:%s" % str(r))
                continue
            ret.append(a)
        return ret
    except Exception ,r :
        print("something failed, reason:%s" % str(r))
        return list() 
def main():
    ret = list()
    begin = time.time()
    for i in xrange(1,2):
        t = one_page(i)
        if len(t) == 0: continue
        ret.extend(t)
    end = time.time()
    print("cost time: %d, ret: %d" % ((end - begin), len(ret)))
if __name__ == "__main__":
    main()
