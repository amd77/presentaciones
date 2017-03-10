#!/usr/bin/env python3
import kivy
kivy.require('1.9.1')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.gridlayout import GridLayout


class ButtonsGrid(GridLayout):  # Su maquetado y callbacks están definidos en el .kv
    def clicked(self, btn):
        print("Pulsado " + btn.text)


class Paso3App(App):  # Al elegir este nombre, se busca un paso3.kv
    def build(self):
        return ButtonsGrid()


if __name__ == '__main__':
    Paso3App().run()
