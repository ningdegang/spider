var fs = require("fs");
function crawl(url){
    phantom.onError = function(msg, trace) {
        var msgStack = ['PHANTOM ERROR: ' + msg];
        if ( trace.length) {
            msgStack.push('TRACE:');
            trace.forEach(function(t) {
                    msgStack.push(' -> ' + (t.file || t.sourceURL) + ': ' + t.line + (t.function ? ' (in function ' + t.function +')' : ''));
            });
        }
        console.error(msgStack.join('\n'));
        phantom.exit(1);
    };

    var page = require('webpage').create();

    //page.onResourceRequested = function (req) { console.log(JSON.parse(JSON.stringify(req, undefined, 4)).url); };
    page.onConsoleMessage = function(msg) {
    if((/Unsafe.+/gi).test(msg)){return;}
    console.log(msg);
    };
    page.settings.loadImages =  false;

    page.onResourceRequested = function(requestData, request) {
    if ((/http:\/\/.+?\.jpg$/gi).test(requestData['url'])) {
    //console.log('Skipping', requestData['url']);
    request.abort();
    return ;
    }   
    if ((/http:\/\/.+?\.png$/gi).test(requestData['url'])) {
        //console.log('Skipping', requestData['url']);
        request.abort();
        return ;
    }   
    if ((/http:\/\/eclick\.baidu\.com\/.+?/gi).test(requestData['url'])) {
        //console.log('Skipping', requestData['url']);
        request.abort();
        return;
    }   
    if ((/http:\/\/pos\.baidu\.com\/.+?/gi).test(requestData['url'])) {
        //console.log('Skipping', requestData['url']);
        request.abort();
        return;
    }   
    //console.log("request: ", requestData['url']);
    };
    
    console.log("begen to crawl");

    page.open(url, function() {
        console.log("crawl: ");
        //page.includeJs("http://cdn.bootcss.com/jquery/2.0.2/jquery.js", function() {
        //var all_link = page.evaluate(function(){
            //$("html div.filmcon div.isthefilm div.isthebox div#hotplayContent div.i_more a#hotplayMoreLink.__r_c_").click();
        //    return document.querySelector("a#hotplayMoreLink.__r_c_");
        //});
        //page.sendEvent("click", all_link.offsetLeft, all_link.offsetTop);
        //console.log("sendEvent   " + all_link.offsetLeft.toString() +" " + all_link.offsetTop.toString());
        var all = page.evaluate(function(){
            var movies = document.querySelectorAll("a.ticket.__r_c_");
            var ret = new Array();
            for(m in movies)
            {
                if(movies[m].href != null){
                    console.log("movie: "+ movies[m].href);
                    ret.push(movies[m].href);
                }
            }
            return ret;
           });
        console.log("begin to write to file");
        var file = fs.open("mtime.movies","a")
        for(i in all)
        {
             console.log("write to file:  " + all[i]);
             file.write(all[i]+"\n");
        }
        file.close();
        //});
    });
    page.close();
};

var file = fs.open("mtime.urls", 'r');
var urls = file.read().toString()
//console.log(urls);
file.close();
urls = urls.split("\n")
urls.pop()
//console.log("len: " + urls.length);
for(i in urls)
{
    //console.log("url: "+ urls[url])
    //crawl(urls[i])
}
crawl("http://theater.mtime.com/China_Guangdong_Province_Shenzen/")
//phantom.exit();
