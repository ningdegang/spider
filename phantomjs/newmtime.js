var fs = require("fs");
function crawl_movie_current_playing(page, url) {
    var all = page.evaluate(function(){
            var movies_head = document.querySelectorAll("div.moviebox.clearfix a.picbox.__r_c_");
            var movies_more = document.querySelectorAll("div#hotplayMoreDiv a.picbox.__r_c_");
            console.log("head: "+ movies_head.toString() + "  more: " + movies_more.toString());
            console.log("head: "+ movies_head.length + "  more: " + movies_more.length);
            var ret = new Array();
            for(m in movies_head) {
                if(movies_head[m].href != null && movies_head[m].href != "javascript:;"){
                    console.log("document head: movie "+ movies_head[m].href);
                    ret.push(movies_head[m].href);
                }
            }
            for(m in movies_more) {
                if(movies_more[m].href != null && movies_more[m].href != "javascript:;"){
                    console.log("document more: movie "+ movies_more[m].href);
                    ret.push(movies_more[m].href);
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
    phantom.exit();
}

function crawl_movie_coming(page, url) {
    var all = page.evaluate(function(){
            var info = document.querySelectorAll("dl#upcomingSlide a.img.__r_c_");
            var ret = new Array();
            for(m in info) {
                if(info[m].href != null && info[m].href != "javascript:;"){
                    console.log("document: movie "+ info[m].href);
                    ret.push(info[m].href);
                }
            }
            return ret;
    });
    console.log("begin to write to file");
    var file = fs.open("mtime.movie_info","a");
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


function read_url_and_crawl(filename, callback){
    var file = fs.open(filename, 'r');
    var urls = file.read().toString();
    //console.log(urls);
    file.close();
    urls = urls.split("\n")
    url= urls[0];
    console.log("url last:  "+ url.toString());
    //console.log("len: " + urls.length);
    for(i in urls) {
            //console.log("url: "+ urls[i]);
            //crawl(urls[i]);
        }
    //crawl(url,crawl_movie);
    crawl("http://theater.mtime.com/China_Beijing/", callback);
}


function movies_current_playing(){
    read_url_and_crawl("mtime.url", crawl_movie_current_playing)
}

function movie_coming_soon() {
    read_url_and_crawl("mtime.coming.url", crawl_movie_coming)
}

function main()
{
    movies_current_playing();
    //movie_coming_soon() ;
}
main()
//phantom.exit()
