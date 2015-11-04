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
page.open('http://theater.mtime.com/China_Shanxi_Province_Xian/', function() {
  page.includeJs("http://cdn.bootcss.com/jquery/2.0.2/jquery.js", function() {
    var all = page.evaluate(function() {
        $("div.midbox div.cityselect div#changeCityDiv a.citylink.__r_c_").click();
        var as = $("div.showfilm.userbar div.city_list2.clearfix a[value]");
        console.log("=======================:::", as);
        var ret = new Array();
        if(as != null)
        {
            for(var i = 0; i<as.length; i++)
            {
                ret.push(as[i].text);
            }
        }
        return ret.join("&&");
    });
    var tt = all.split("&&");
    for(i=0; i<3; i++)
    {
        console.log("aaaaa++++++++++++++" + tt[i]);
        var url = page.evaluate(function(i) {
            var as = $("div.showfilm.userbar div.city_list2.clearfix a[value]");
            console.log("before as length", as.length);
            if(as.length == 0)
            {
                $("div.midbox div.cityselect div#changeCityDiv a.citylink.__r_c_").click();
                as = $("div.showfilm.userbar div.city_list2.clearfix a[value]");
            }
            console.log("i in page ", i.toString());
            console.log("after as length", as.length);
            console.log("as: ", as.toString());
            console.log("as text", as.text());
            a = as[i];
            for(x in a){
                console.log("x: " +x );
                console.log("value:  " + a[x]);
            }

            return as[i].textContent
            var tt = window.location.href;
            history.back(); 
            return tt;
            
        }, i);
        console.log("url:  ", url);
    };
    
    phantom.exit()
  });
});
