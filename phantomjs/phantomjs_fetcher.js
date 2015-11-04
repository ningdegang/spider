var webpage = require('webpage');
var wait_before_end = 1000;
console.debug = function(msg){};
phantom.clearCookies();

page_loaded = false,
            start_time = Date.now(),
            end_time = null,
            script_result = null;


var page = webpage.create();
page.viewportSize = {
width:  1024, height:  768*3
}
page.settings.userAgent = "test";

// this may cause memory leak: https://github.com/ariya/phantomjs/issues/12903
page.settings.loadImages =  false;
page.settings.resourceTimeout =  30*1000;

// add callbacks
page.onInitialized = function() {
    //script_result = page.evaluateJavaScript(fetch.js_script);
    console.log("onInitialized");
};
page.onLoadFinished = function(status) {
    page_loaded = true;
    //script_result = page.evaluateJavaScript(fetch.js_script);
    console.debug("waiting "+wait_before_end+"ms before finished.");
    end_time = Date.now() + wait_before_end;
    console.log("onLoadFinished");
};
page.onResourceRequested = function(requestData, request) {
    console.debug("Starting request: #"+requestData.id+" ["+requestData.method+"]"+requestData.url);
    /*
    if ((/http:\/\/.+?\.jpg$/gi).test(requestData['url'])) {
        console.debug('Skipping',requestData['url']);
        request.abort();
        return ;
    }
    if ((/http:\/\/.+?\.png$/gi).test(requestData['url'])) {
        console.debug('Skipping',requestData['url']);
        request.abort();
        return ;
    }
    */
    if ((/http:\/\/eclick\.baidu\.com\/.+?/gi).test(requestData['url'])) {
        console.debug('Skipping',requestData['url']);
        request.abort();
        return;
    }
    if ((/http:\/\/pos\.baidu\.com\/.+?/gi).test(requestData['url'])) {
        console.debug('Skipping',requestData['url']);
        request.abort();
        return;
    }

    end_time = null;
};
page.onResourceReceived = function(response) {
    console.debug("Request finished: #"+response.id+" ["+response.status+"]"+response.url);
    if (page_loaded) {
        console.debug("waiting "+wait_before_end+"ms before finished.");
        end_time = Date.now() + wait_before_end;
        //setTimeout(make_result, wait_before_end+10, page);
    }
}
page.onResourceError = page.onResourceTimeout=function(response) {
    console.info("Request error: #"+response.id+" ["+response.errorCode+"="+response.errorString+"]"+response.url);
    if (page_loaded) {
        console.debug("waiting "+wait_before_end+"ms before finished.");
        end_time = Date.now() + wait_before_end;
        //setTimeout(make_result, wait_before_end+10, page);
    }
}

page.onConsoleMessage = function(msg) {
    if((/Unsafe.+/gi).test(msg)){return;}
    console.log(msg);
};


setTimeout(function(page) {
        console.log("whole page timeout !!!");
        phantom.exit();
        }, page.settings.resourceTimeout + 100, page);

page.open("http://theater.mtime.com/China_Shanxi_Province_Xian/");
