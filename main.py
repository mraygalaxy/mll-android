#!/usr/bin/env python
# coding: utf-8
__version__ = "0.3.0"
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.utils import platform
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image


class ServiceApp(App):
    def build(self):
        if platform == "android" :
            from android import AndroidService
            service = AndroidService('mica', 'synchronized')
            service.start('service started')
            self.service = service

        layout = BoxLayout(orientation='vertical')
        btn1 = Button(text='Hello')
        btn2 = Button(text='World')
        txt1 = TextInput(text='Hello again')
        img = Image(source = 'icon.png')
        layout.add_widget(btn1)
        layout.add_widget(btn2)
        layout.add_widget(txt1)
        layout.add_widget(img)
        return layout

if __name__ == '__main__':
    ServiceApp().run()
