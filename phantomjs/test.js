var page = require("webpage").create();
var page_loaded = false;
var script_executed = false;
var script_result = null;
var wait_before_end  =10;
var count_request = 0;

page.onInitialized = function() { console.log('running document-start script.'); }
page.settings.loadImages = false;
page.settings.diskCache = true;
page.onLoadFinished = function(page) {
  page_loaded = true;
  console.log('running document-end script.');
  page.evaluate("console.log(window.document.querySelect('a'))");
};
page.onError =  function () { //console.log("page error"); 
}

page.onConsoleMessage = function(msg) {
  console.log("page console msg: " + msg); 
}
function print_content(page) {
    var count = 0;
    if(count_request % 2 != 0 && count< 10){
        //console.log("page.content: " + page.content);
        count++;
        setTimeout(print_content, wait_before_end+10, page);
    }
    console.log("page load over ,exiting"); 
    phantom.exit();
}
page.onResourceRequested = function(request) {
  //console.debug("Starting request: #"+request.id+" ["+request.method+"]"+request.url);
  count_request++;  
  if (page_loaded) {
    console.debug("page loaded success, ajax requet");
    console.debug("Starting request: #"+request.id+" ["+request.method+"]"+request.url);
  }
};
page.onResourceReceived = function(response) {
  count_request++;  
  //console.debug("Request finished: #"+response.id+" ["+response.status+"]"+response.url);
  if (page_loaded) {
    console.debug("Request finished: #"+response.id+" ["+response.status+"]"+response.url);
    console.debug("waiting: "+wait_before_end+"ms before finished.");
    setTimeout(print_content, wait_before_end+10, page);
  }
}
page.onResourceError = page.onResourceTimeout=function(response) {
  console.info("Request error: #"+response.id+" ["+response.errorCode+"="+response.errorString+"]"+response.url);
  if (page_loaded) {
    //console.debug("waiting "+wait_before_end+"ms before finished.");
    //end_time = Date.now() + wait_before_end;
    //setTimeout(make_result, wait_before_end+10, page);
  }
}
page.urlChanged = function(url) { console.log("url changed: "+ url) }
page.open("http://www.qq.com");
