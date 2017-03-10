#!/usr/bin/env python3
import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


class ButtonsGrid(GridLayout):
    def forward(self, btn):
        self.parent.ids.status_bar.text = "Pulsado " + btn.text

    def right(self, btn):
        self.parent.ids.status_bar.text = "Pulsado " + btn.text

    def back(self, btn):
        self.parent.ids.status_bar.text = "Pulsado " + btn.text

    def left(self, btn):
        self.parent.ids.status_bar.text = "Pulsado " + btn.text


class ContainerBox(BoxLayout):
    def video_loaded(self):
        self.parent.ids.status_bar.text = 'Video Loaded'


class Paso4App(App):  # por defecto se busca un paso4.kv
    def build(self):
        return ContainerBox()


if __name__ == '__main__':
    Paso4App().run()
