#!/usr/bin/env python3
import kivy
# kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

import requests


def get(key, value):
    url = "http://robocop.local:8000/{}/{}".format(key, value)
    requests.get(url)


def servo(value):  # value entre 0 y 1
    minimo, maximo = 0.04, 0.13
    return value * (maximo-minimo) + minimo


def motor(value):  # value entre -1 y 1
    return value


class ButtonsGrid(GridLayout):
    def brazo_drcha(self, value):
        self.parent.ids.status_bar.text = "Brazo derecha a " + str(value)
        get("brazo_drcha", servo(value))

    def brazo_izqda(self, value):
        self.parent.ids.status_bar.text = "Brazo izquierda a " + str(value)
        get("brazo_izqda", servo(value))

    def rueda_drcha(self, value):
        self.parent.ids.status_bar.text = "rueda derecha a " + str(value)
        get("rueda_drcha", servo(value))

    def rueda_izqda(self, value):
        self.parent.ids.status_bar.text = "rueda izquierda a " + str(value)
        get("rueda_izqda", motor(value))

    def rueda(self, value):
        self.parent.ids.status_bar.text = "ambas ruedas a " + str(value)
        get("rueda_drcha", motor(value))
        get("rueda_izqda", motor(value))

    def rueda_izqda(self, value):
        self.parent.ids.status_bar.text = "rueda izquierda a " + str(value)
        get("rueda_izqda", motor(value))


class ContainerBox(BoxLayout):
    def video_loaded(self):
        self.ids.status_bar.text = 'Video Loaded'


class Paso5App(App):  # por defecto se busca un paso4.kv
    def build(self):
        return ContainerBox()


if __name__ == '__main__':
    Paso5App().run()
