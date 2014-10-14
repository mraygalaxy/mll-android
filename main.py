#!/usr/bin/env python
# coding: utf-8
__version__ = "0.5.0"
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
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

from params import parameters
from mica.mica import go, second_splash
                 
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
couch = CouchBase(String(parameters["local_username"]), String(parameters["local_password"]), parameters["local_port"], String(cert), activity)
port = couch.start(String(parameters["local_database"]))

if port == -1 :
    log.error(String("AAAHHHHHH. FAILURE."))
    log.debug(String("Trying to start replication"))

parameters["couch"] = couch
parameters["mobileinternet"] = mobile_internet
parameters["duplicate_logger"] = log

class Wv(Widget):
    def __init__(self, **kwargs):
        log.debug(String("Initializing webview widget"))
        super(Wv, self).__init__(**kwargs)
        Clock.schedule_once(self.create_webview, 0)
        log.debug(String("first clock scheduled"))
        self.wu = False
        Window.bind(on_keyboard=self.disable_back_button_death)

    def disable_back_button_death(self,window,key,*largs) :
        if key == 27 :
            log.debug(String("back button death is stupid. not doing it."))
            return True
        log.debug(String("Ignoring other buttons: " + str(key)))
    
    @run_on_ui_thread
    def go(self, *args) :
        #log.debug(String("polling twisted"))
        try:
            urllib2.urlopen('http://localhost:10000/serve/favicon.ico')
            self.webview.loadUrl('http://localhost:10000/')
            log.debug(String("Storing webview for web updates"))
            couch.setWebView(self.webview)
            log.debug(String("webview stored initialized"))
            #self.webview.setInitialScale(180);
            return
        except urllib2.HTTPError, e:
            #log.warn(String(str(e.code)))
            pass
        except urllib2.URLError, e:
            #log.warn(String(str(e.args)))
            pass
        Clock.schedule_once(self.go, 1)

    @run_on_ui_thread
    def account(self) :
        log.debug(String("Loading account settings."))
        self.webview.loadUrl('http://localhost:10000/account')

    @run_on_ui_thread
    def create_webview(self, *args):
        log.debug(String("creating webview"))
        self.webview = WebView(activity)
        self.webview.clearCache(True);
        #self.webview.clearFormData();
        #self.webview.clearHistory();
        settings = self.webview.getSettings()
        settings.setJavaScriptEnabled(True)
        settings.setBuiltInZoomControls(True)
        settings.setAllowUniversalAccessFromFileURLs(True)
        #settings.setCacheMode(settings.LOAD_NO_CACHE);

        log.debug(String("setting webview client"))
        self.webview.setWebViewClient(WebViewClient());
        #WebView.setWebContentsDebuggingEnabled(True);
        log.debug(String("setting content view"))
        activity.setContentView(self.webview)
        self.webview.loadData(String(second_splash()), "text/html", "utf-8");
        Clock.schedule_once(self.go, 5)

def background() :
    log.debug(String("Entering MICA thread"))
    go(parameters)

    while True:
        log.error(String("Uh oh. Problem in MICA. May need to restart application."))
        sleep(1)
        
class ReaderApp(App):
    def open_settings(self):
        log.debug(String("Menu button pressed."))
        self.mwv.account()

    def build(self):
        log.debug(String("Starting MICA thread."))
        self.t = threading.Thread(target = background)
        self.t.daemon = True
        self.t.start()
        log.debug(String("Started. Returning webview object"))
        self.mwv = Wv()
        return self.mwv 

    def on_pause(self):
        log.debug(String("MICA is pausing. Don't know what to do about that yet."))
        return True

if __name__ == '__main__':
    ReaderApp().run()
