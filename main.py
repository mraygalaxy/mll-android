#!/usr/bin/env python
# coding: utf-8
__version__ = "0.3.2"
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.widget import Widget
from kivy.clock import Clock
from jnius import autoclass
from android.runnable import run_on_ui_thread 
import base64
import re
import os
import urllib2
                 
cwd = re.compile(".*\/").search(os.path.realpath(__file__)).group(0)
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.renpy.android.PythonActivity').mActivity
String = autoclass('java.lang.String')

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
    fh = open(cwd + "service/mica/serve/spinner.gif", 'r')
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
        super(Wv, self).__init__(**kwargs)
        Clock.schedule_once(self.create_webview, 0)
    
    @run_on_ui_thread
    def go(self, *args) :
        try:
            urllib2.urlopen('http://localhost:10000/serve/favicon.ico')
            self.webview.loadUrl('http://localhost:10000/')
            #self.webview.setInitialScale(180);
            return
        except urllib2.HTTPError, e:
            print(e.code)
        except urllib2.URLError, e:
            print(e.args)
        Clock.schedule_once(self.go, 1)

    @run_on_ui_thread
    def create_webview(self, *args):
        self.webview = WebView(activity)
        self.webview.getSettings().setJavaScriptEnabled(True)
        self.webview.getSettings().setBuiltInZoomControls(True)
        self.webview.getSettings().setAllowUniversalAccessFromFileURLs(True)
        wvc = WebViewClient();
        self.webview.setWebViewClient(wvc);
        #WebView.setWebContentsDebuggingEnabled(True);
        activity.setContentView(self.webview)
        self.webview.loadData(String(second_splash()), "text/html", "utf-8");
        Clock.schedule_once(self.go, 5)

class ReaderApp(App):
    def build(self):
        if platform == "android" :
            from android import AndroidService
            service = AndroidService('mica', 'synchronized')
            service.start('service started')
            self.service = service
        return Wv()

    def on_pause(self):
        return True

if __name__ == '__main__':
    ReaderApp().run()
