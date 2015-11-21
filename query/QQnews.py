#!/usr/bin/env python
import requests
import json
from pyquery import PyQuery as PyQ
import time

proxy = { "http":"http://10.197.1.52:8080" }
url="http://r.inews.qq.com/getQQNewsIndexAndItems"
def news():
    try:
        ret = list()
        data = requests.get(url=url, proxies=proxy).content.decode('utf-8', 'ignore')
        data = json.loads(data)["T1348648517839"]
        for n in data:
            a = dict()
            try:
                a["contenturl"] = n["url"]
                a["title"] = n["title"]
                a["digest"] = n["digest"]
                a["smallimg"] = n["imgsrc"]
                a["id"] = n["docid"]
                a["time"] = n["ptime"]
                a["smallimgcontent"] = requests.get(a["smallimg"]).content
                doc =  PyQ(requests.get(a["contenturl"]).content, parser="html")
                content = doc("div.content").html()
                a["content"] = content
            except Exception ,r :
                print("something failed, reason:%s" % str(r))
                continue
            ret.append(a)
        return ret
    except Exception ,r :
        print("something failed, reason:%s" % str(r))
        return list()
def main():
    begin = time.time()
    ret = news()
    end = time.time()
    print("cost time: %d, ret: %d" % ((end - begin), len(ret)))
if __name__ == "__main__":
    main()
