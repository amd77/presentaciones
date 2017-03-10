#!/usr/bin/env python

import kivy
kivy.require('1.9.1')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class ButtonsGrid(App):
    def build(self):
        layout = GridLayout(cols=3, rows=3)
        for i in range(3):
            for j in range(3):
                text = '{},{}'.format(i, j)
                layout.add_widget(Button(text=text, on_press=self.clicked))
        return layout

    def clicked(self, btn):
        print(btn.text)

if __name__ == '__main__':
    ButtonsGrid().run()
