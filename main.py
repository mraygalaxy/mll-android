#!/usr/bin/env python
# coding: utf-8
__version__ = "0.9.0"
print "1"
import kivy
print "2"
from kivy.app import App
print "4"
from kivy.uix.widget import Widget
print "5"
from kivy.clock import Clock
print "6"
from kivy.core.window import Window
print "7"
try :
    from jnius import autoclass
    print "8"
    from android.runnable import run_on_ui_thread 
    print "9"
except ImportError, e :
    print "10: " + str(e)
    pass
print "11"
from time import sleep
print "12"
import base64
print "13"
import re
print "14"
import os
print "15"
import urllib2
print "16"
import sys
print "17"
import threading
print "18"
import codecs

print "Starting up."

from params import parameters
print "20"
from mica.mica import go, second_splash
print "21"
from mica.common import pre_init_localization
print "22"
from sys import settrace as sys_settrace
print "23"
                 
tree = []

print "24"
cwd = re.compile(".*\/").search(os.path.realpath(__file__)).group(0)
print "25"

sys.path = [cwd, cwd + "mica/"] + sys.path

print "26"
#WebView = autoclass('android.webkit.WebView')
WebView = autoclass("org.renpy.android.MyWebView")
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.renpy.android.PythonActivity').mActivity
String = autoclass('java.lang.String')
MLog = autoclass("org.renpy.android.MLog")
CouchBase = autoclass("org.renpy.android.Couch")
MobileInternet = autoclass("org.renpy.android.Internet")
print "27"

print("Loading mica services")
print("We are located at: " + cwd)

log = MLog(activity)
mobile_internet = MobileInternet(activity)

def tracefunc(frame, event, arg, indent=[0]):
    if event == "call":
        tree.append(frame.f_code.co_name)
        name = ".".join(tree)
        indent[0] += 1
        log.debug(String("-" * indent[0] + "> call function: " + name))
    elif event == "return":
        name = ".".join(tree)
        indent[0] -= 1
        log.debug(String("<" + "-" * indent[0] + " exit function: " + name))
        del tree[-1]

    return tracefunc

#sys_settrace(tracefunc)
log.debug(String("Loading certificate file for couch"))

fh = codecs.open(parameters["cert"], 'r', "utf-8")
cert = fh.read()
fh.close()

log.debug(String("Starting couchbase"))
#String(parameters["local_username"]), String(parameters["local_password"]), parameters["local_port"], 
couch = CouchBase(String(cert), activity)
scratch = couch.files_go_where()
log.debug(String("Files go here: " + str(scratch) + " " + str(type(scratch))))
parameters["scratch"] = str(scratch) + "/"
pre_init_localization(couch.get_language(), log)
for db in [parameters["local_database"], "sessiondb", "files"] :
    log.debug(String("Trying to start DB: " + db))
    port = couch.start(String(db))

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
        Window.bind(on_key_down=self.on_keyboard_up)

    def disable_back_button_death(self,window,key,*largs) :
        if key == 27 :
            log.debug(String("Sending back request."))
            couch.updateView(String("window.history.back();"))
            log.debug(String("back button death is stupid. not doing it."))
            return True
        log.debug(String("Ignoring other buttons: " + str(key)))

    def on_keyboard_up(self, *args) :
        log.debug(String("Got key: " + str(args)))
    
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
        #self.webview.loadUrl('http://localhost:10000/account')
        couch.updateView(String("$.mobile.navigate('#account');"))

    @run_on_ui_thread
    def create_webview(self, *args):
        log.debug(String("creating webview"))
        self.webview = WebView(activity)
        self.webview.clearCache(True);
        #self.webview.clearFormData();
        #self.webview.clearHistory();
        settings = self.webview.getSettings()
        settings.setDefaultTextEncodingName("utf-8")
        settings.setJavaScriptEnabled(True)
        settings.setBuiltInZoomControls(True)
        settings.setAllowUniversalAccessFromFileURLs(True)
        settings.setAllowFileAccess(True)
        settings.setDomStorageEnabled(True);
        #settings.setCacheMode(settings.LOAD_NO_CACHE);

        log.debug(String("setting webview client"))
        self.webview.setWebViewClient(WebViewClient());
        #WebView.setWebContentsDebuggingEnabled(True);
        log.debug(String("setting content view"))
        activity.setContentView(self.webview)
        self.webview.loadData(String(second_splash()), "text/html; charset=utf-8", "utf-8");
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

    def on_resume(self):
        log.debug(String("MICA is resume. Don't know what to do about that yet."))
        return True

if __name__ == '__main__':
    ReaderApp().run()
