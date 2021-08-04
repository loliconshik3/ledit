import tkinter.font as tkfont
import tkinter as tk
import json
import os

class TextLineNumbers():
    def __init__(self, root, config, text_widget, theme):
        self.widget = tk.Canvas(root, width=30)
        self.text_widget = text_widget
        self.config = config
        self.theme = theme

        self.font = tkfont.Font(family=config['font'], size=config['font_size'])
        self.widget.config(highlightbackground=theme['borders_color'], background=theme['num_of_lines_background_color'])

        self.__init_canvas_widget()
        
    def __init_canvas_widget(self):
        self.widget.pack(side="left", fill="y")

    def redraw(self, *args):
        '''redraw line numbers'''
        self.widget.delete("all")

        i = self.text_widget.index("@0,0")
        while True :
            dline= self.text_widget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]

            test = self.widget.create_text(2,y,anchor="nw", font=self.font, text=" "+linenum+" ", fill=self.theme['num_of_lines_text_color'])
            i = self.text_widget.index("%s+1line" % i)

        #Выравнивание ширины канваса под размер текста
        self.widget.configure(width=50)
        index = 1000; count = 1
        while index < 100000000:
            width = (int(self.widget.itemcget(test, 'text')) // index)
            if width >= 1:
                self.widget.configure(width=50+count*10)
                count += 1
            index *= 10