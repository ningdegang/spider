#!/usr/bin/env python
import requests
import json
from pyquery import PyQuery as PyQ
import time

#proxy = { "http":"http://10.197.1.52:8080" }
url="http://list.letv.com/apin/chandata.json?c=1&d=1&md=&o=4&p=%d&s=1"
url="http://list.letv.com/apin/chandata.json?c=1&d=1&md=&o=9&p=%d&s=1&ph=1"
def one_page(i):
    one = url % i
    try:
        ret = list()
        #data = requests.get(url=one, proxies=proxy).content.decode('utf-8', 'ignore')
        data = requests.get(url=one).content.decode('utf-8', 'ignore')
        data = json.loads(data)
        data =  data["data_list"]
        for n in data:
            if n["category"] != "1" and n["categoryName"] != '\u7535\u5f71':continue;
            a = dict()
            try:
                vids = n["vids"].split(",")
                if(len(vids)>1):continue
                a["url"] = "http://www.letv.com/ptv/vplay/%s.html" % (n["vids"])
                a["title"] = n["name"]
                a["language"] = n["lgName"] 
                a["director"] = " ".join(json.loads(n["directory"]).values())
                a["img"] = n["images"]["90*120"]
                a["description"] = n["description"]
                a["actors"] = " ".join(n["starring"].values())
                a["duration"] = n["duration"]
                a["rating"] = n["rating"]
                a["subCategoryName"] = n["subCategoryName"]
                a["releaseDate"] = int(n["releaseDate"]) / 1000 
                a["ctime"] = int(n["mtime"]) /1000
                a["area"] = n["areaName"]
                a["tag"] = n["tag"]
                a["subname"] = n["subname"]
            except Exception as r :
                print("something failed, reason:%s" % r.message)
                continue
            ret.append(json.dumps(a)+"\n")
        return ret
    except Exception as r :
        print("something failed, reason:%s" % (r.message))
        return list() 

def get_all():
    ret = list()
    for i in xrange(1,24):
        t = one_page(i)
        if len(t) == 0: continue
        ret.extend(t)
    return ret
    
def main():
    ret = list()
    begin = time.time()
    for i in xrange(1,2):
        t = one_page(i)
        if len(t) == 0: continue
        ret.extend(t)
    end = time.time()
    print("cost time: %d, ret: %d" % ((end - begin), len(ret)))
    with open("letv.txt", "w") as f:
        f.writelines(ret)
        
if __name__ == "__main__":
    main()
