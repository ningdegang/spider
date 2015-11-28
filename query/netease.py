#!/usr/bin/env python
import requests
import json
from pyquery import PyQuery as PyQ
import time

proxy = { "http":"http://10.197.1.52:8080" }
ent_url="http://c.m.163.com/nc/article/list/T1348648517839/0-5.html"
movie_url="http://c.m.163.com/nc/article/list/T1348648650048/0-2.html"
doc_url = "http://c.m.163.com/nc/article/%s/full.html" 
headers = {"User-Agent":"NTES Android"}
def news():
    try:
        ret = list()
        #data = requests.get(url=movie_url,headers=headers, proxies=proxy).content.decode('utf-8', 'ignore')
        data = requests.get(url=movie_url,headers=headers).content.decode('utf-8', 'ignore')
        data = json.loads(data)["T1348648650048"]
        for n in data:
            a = dict()
            try:
                a["title"] = n["title"]
                a["digest"] = n["digest"]
                a["smallimg"] = n["imgsrc"]
                a["id"] = n["docid"]
                a["time"] = n["ptime"]
                doc =  PyQ(requests.get(n["url"]).content, parser="html")
                a["content"] = doc("div.content").html()
                #a["smallimgcontent"] = "".join([hex(ord(n))[2:] for n in requests.get(a["smallimg"]).content])
                #real_url = doc_url % a["id"]
                #doc = json.loads(requests.get(real_url).content)[a["id"]]
                #a["content"] = doc["body"]
                #a["contentimgs"] = [{"src":t["src"], "title":t["alt"]} for t in doc["img"]]
            except Exception as e :
                print n
                print("something failed, reason: %s" % (e.message))
                continue
            ret.append(json.dumps(a)+"\n")
        return ret
    except Exception as e :
        print("something failed, reason:%s" % (e.message))
        return list()
def main():
    begin = time.time()
    ret = news()
    end = time.time()
    print("cost time: %d, ret: %d" % ((end - begin), len(ret)))
    with open("netease.txt", "w") as f:
        f.writelines(ret)
if __name__ == "__main__":
    main()
