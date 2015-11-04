var fs = require("fs");
function crawl_movie(page, url) {
    console.log("+++++crawl: "+url);
    var all = page.evaluate(function(){
            var movies_head = document.querySelectorAll("div.moviebox.clearfix a.picbox.__r_c_");
            var movies_more = document.querySelectorAll("div#hotplayMoreDiv.moviemore.clearfix a.picbox.__r_c_");
            var movies = movies_head.concat(movies_more);
            var ret = new Array();
            for(m in movies) {
                if(movies[m].href != null && movies[m].href != "javascript:;"){
                    console.log("document: movie "+ movies[m].href);
                    ret.push(movies[m].href);
                }
            }
            return ret;
            });
    console.log("begin to write to file");
    var file = fs.open("mtime.movies","a")
        for(i in all) {
            console.log("write to file:  " + all[i]);
            file.write(all[i]+"\n");
        }
    file.close();
}

function crawl_movie(page, url) {
    var all = page.evaluate(function(){
            var info = document.querySelectorAll("a.ticket.__r_c_");
            var ret = new Array();
            for(m in movies) {
                if(movies[m].href != null && movies[m].href != "javascript:;"){
                    console.log("document: movie "+ movies[m].href);
                    ret.push(movies[m].href);
                }
            }
            return ret;
    });
    console.log("begin to write to file");
    var file = fs.open("mtime.movie_info","a")
        for(i in all) {
            console.log("write to file:  " + all[i]);
            file.write(all[i]+"\n");
        }
    file.close();
}

function crawl(url, callback){
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
    
    console.log("begen to crawl :  " + url);
    page.open(url, function(){
        callback(page, url); 
    });
    //page.close();
};


function movies(){
    var file = fs.open("mtime.urls", 'r');
    var urls = file.read().toString()
        //console.log(urls);
        file.close();
    urls = urls.split("\n")
        urls.pop()
        //console.log("len: " + urls.length);
        for(i in urls) {
            //console.log("url: "+ urls[i])
            //crawl(urls[i])
        }
    crawl("http://theater.mtime.com/China_Guangdong_Province_Shenzen/",crawl_movie)
}

function movie_info()
{
    var file = fs.open("mtime.movies", 'r');
    var urls = file.read().toString()
    //console.log(urls);
    file.close();
    urls = urls.split("\n");
    url = urls.pop();
    //console.log("len: " + urls.length);
    for(i in urls) {
        //console.log("url: "+ urls[i])
        //crawl(urls[i])
    }
    crawl(url, crawl_movie_info)
}

function main()
{
    movies();
    //movie_info();
}
main()
//phantom.exit()
