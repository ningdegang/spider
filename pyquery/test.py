#!/usr/bin/env python
import requests
from pyquery  import PyQuery
import re
from BeautifulSoup import BeautifulSoup as bs
proxy = { "http":"http://10.197.1.52:8080" }
url="http://kansha.baidu.com/movie/"
def main():
    html = requests.get(url=url, proxies=proxy).content.decode('utf-8', 'ignore')
    #print html
    doc = PyQuery(html, parser='html')
    playing = doc("div.span9 div.movie")
    play = list()
    for a in playing.items(): 
        play.append(a.attr["href"])
    play = list(set(play))
    coming = doc("a.img.__r_c_")
    come = list()
    for a in coming.items():
        come.append(a.attr.href)
    come = list(set(come))
    print len(play), len(come) 
    soup = bs(html)
    #doc = PyQuery(soup.prettify(), parser='html')
    #cinemas = doc("div.main.fl a.htitle")
    cinemas = soup.findAll("a", target="_blank",attrs={"class":re.compile("htitle")})
    print len(cinemas)
    #for a in cinemas.items():
    #    print a.attr.href
    
if __name__ == "__main__":
    main()
