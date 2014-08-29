#!/usr/bin/env python
# coding: utf-8
__version__ = "0.3.2"
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from jnius import autoclass
from android.runnable import run_on_ui_thread 
from time import sleep
import base64
import re
import os
import urllib2
import sys
import threading
import codecs

print "Starting up."

from params import parameters, app
from mica.mica import go
                 
cwd = re.compile(".*\/").search(os.path.realpath(__file__)).group(0)

sys.path = [cwd, cwd + "mica/"] + sys.path

WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.renpy.android.PythonActivity').mActivity
String = autoclass('java.lang.String')
MLog = autoclass("org.renpy.android.MLog")
CouchBase = autoclass("org.renpy.android.Couch")
MobileInternet = autoclass("org.renpy.android.Internet")

print("Loading mica services")

log = MLog(activity)
mobile_internet = MobileInternet(activity)

log.debug(String("Loading certificate file for couch"))

fh = codecs.open(parameters["cert"], 'r', "utf-8")
cert = fh.read()
fh.close()

log.debug(String("Starting couchbase"))
couch = CouchBase(String(app["local_username"]), String(app["local_password"]), app["local_port"], String(cert), activity)
port = couch.start(String(app["local_database"]))

if port == -1 :
    log.error(String("AAAHHHHHH. FAILURE."))
else :
    log.debug(String("Trying to start replication"))
    user = app["remote_user"] 
    pw = app["remote_password"] 
    url = app["remote_protocol"] + "://" + user + ":" + pw + "@" + app["remote_host"] + ":" + str(app["remote_port"])
    if couch.replicate(String(app["remote_database"]), String(url), False) == -1 :
        log.error(String("Replication failed. Boo. =("))
    else :
        log.debug(String("Replication started. Yay."))

parameters["couch"] = couch
parameters["mobileinternet"] = mobile_internet
parameters["duplicate_logger"] = log

def second_splash() :
    fh = open(cwd + "splash_template.html", 'r') 
    output = fh.read()
    fh.close() 

    fh = open(cwd + "icon.png", 'r')
    contents = fh.read() 
    encoded1 = base64.b64encode(contents)
    fh.close()

    output += "<img src='data:image/jpeg;base64," + str(encoded1) + "' width='100%'/>"
    output += """
</div>
<div class="inner2">
"""
    output += "<p><p><p>"
    fh = open(cwd + "mica/serve/spinner.gif", 'r')
    contents = fh.read() 
    encoded2 = base64.b64encode(contents)
    fh.close()
    output += "<img src='data:image/jpeg;base64," + str(encoded2) + "' width='10%'/>"
    output += "&nbsp;&nbsp;Please wait...</p>"
    output += """
</div>
<div class="inner3">
</div>
</body>
</html>
"""
    return output

class Wv(Widget):
    def __init__(self, **kwargs):
        log.debug(String("Initializing webview widget"))
        super(Wv, self).__init__(**kwargs)
        Clock.schedule_once(self.create_webview, 0)
        log.debug(String("first clock scheduled"))
        self.wu = False
    
    @run_on_ui_thread
    def go(self, *args) :
        log.debug(String("polling twisted"))
        try:
            urllib2.urlopen('http://localhost:10000/serve/favicon.ico')
            self.webview.loadUrl('http://localhost:10000/')
            log.debug(String("Storing webview for web updates"))
            couch.setWebView(self.webview)
            log.debug(String("webview stored initialized"))
            #self.webview.setInitialScale(180);
            return
        except urllib2.HTTPError, e:
            log.warn(String(str(e.code)))
        except urllib2.URLError, e:
            log.warn(String(str(e.args)))
        Clock.schedule_once(self.go, 1)

    @run_on_ui_thread
    def create_webview(self, *args):
        log.debug(String("creating webview"))
        self.webview = WebView(activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setBuiltInZoomControls(True)
        self.webview.getSettings().setAllowUniversalAccessFromFileURLs(True)
        log.debug(String("setting webview client"))
        self.webview.setWebViewClient(WebViewClient());
        #WebView.setWebContentsDebuggingEnabled(True);
        log.debug(String("setting content view"))
        activity.setContentView(self.webview)
        log.debug(String("setting content view"))
        self.webview.loadData(String(second_splash()), "text/html", "utf-8");
        Clock.schedule_once(self.go, 5)

def background() :
    go(parameters)

    while True:
        log.error(String("Uh oh. Problem in MICA. May need to restart application."))
        sleep(1)
        
class ReaderApp(App):
    def build(self):
        log.debug(String("Starting MICA thread."))
        self.t = threading.Thread(target = background)
        self.t.daemon = True
        self.t.start()
        log.debug(String("Started. Returning webview object"))
        return Wv()

    def on_pause(self):
        ''' do something '''
        return True

if __name__ == '__main__':
    ReaderApp().run()
