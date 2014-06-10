#!/usr/bin/env python
# coding: utf-8
__version__ = "0.3.0"
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
                 
cwd = re.compile(".*\/").search(os.path.realpath(__file__)).group(0)
WebView = autoclass('android.webkit.WebView')
WebViewClient = autoclass('android.webkit.WebViewClient')
activity = autoclass('org.renpy.android.PythonActivity').mActivity
String = autoclass('java.lang.String')

def second_splash() :
    fh = open(cwd + "icon.png", 'r')
    contents = fh.read() 
    encoded1 = base64.b64encode(contents)
    fh.close()
    fh = open(cwd + "service/mica/serve/spinner.gif", 'r')
    contents = fh.read() 
    encoded2 = base64.b64encode(contents)
    fh.close()
    fh = open(cwd + "splash_template.html", 'r') 
    output = fh.read()
    fh.close() 
    output += "<img src='data:image/jpeg;base64," + str(encoded1) + "' width='100%'/>"
    output += """
</div>
<div class="inner2">
"""
    output += "<p><p><p>"
    output += "<img src='data:image/jpeg;base64," + str(encoded2) + "' width='15%'/>"
    output += "&nbsp;&nbsp;Please wait...</p>"
    output += """
</div>
<div class="inner3">
                (We're pulling in a lot of dependencies.)
</div>
</div>
</div>
<img style="visibility:hidden" id='check_pic' src="/serve/favicon.ico" onabort="alert('interrupted')" onload="check_success('http://127.0.0.1:10000/')" onerror="check_available('127.0.0.1:10000')"/>
    </body>
</html>
"""
    return output
class Wv(Widget):
    def __init__(self, **kwargs):
        super(Wv, self).__init__(**kwargs)
        Clock.schedule_once(self.create_webview, 0)
    
    @run_on_ui_thread
    def create_webview(self, *args):
        webview = WebView(activity)
        webview.getSettings().setJavaScriptEnabled(True)
        webview.getSettings().setBuiltInZoomControls(True)
        wvc = WebViewClient();
        webview.setWebViewClient(wvc);
        activity.setContentView(webview)
        #webview.loadUrl('http://localhost:10000')
        webview.loadData(String(second_splash()), "text/html", "utf-8");

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
