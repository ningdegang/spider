#!/usr/bin/env python
import requests
import json
from pyquery import PyQuery as PyQ
import time

proxy = { "http":"http://10.197.1.52:8080" }
url="http://c.m.163.com/nc/article/list/T1348648517839/0-5.html"
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
                a["smallimgcontent"] = "".join([hex(ord(n))[2:] for n in requests.get(a["smallimg"]).content])
                doc = PyQ(requests.get(a["contenturl"]).content, parser="html")
                content = doc("div.content").html()
                a["content"] = content
            except Exception ,r :
                print("something failed, reason:%s" % str(r))
                continue
            ret.append(json.dumps(a)+"\n")
        return ret
    except Exception ,r :
        print("something failed, reason:%s" % str(r))
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
