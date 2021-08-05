import tkinter.font as tkfont
import tkinter as tk
import json
import os

class TextLineNumbers():
    def __init__(self, root, config, text_widget, theme):
        self.widget         = tk.Canvas(root, width=30)
        self.text_widget    = text_widget
        self.config         = config
        self.theme          = theme

        self.font = tkfont.Font(family=config['font'], size=config['font_size'])
        self.widget.config(highlightbackground=theme['borders_color'], background=theme['num_of_lines_background_color'])

        self.__init_canvas_widget()
        
    def __init_canvas_widget(self):
        self.widget.pack(side="left", fill="y")

    def redraw(self, *args):
        '''redraw line numbers'''
        self.widget.delete("all")

        index = self.text_widget.index("@0,0")
        while True:
            dline = self.text_widget.dlineinfo(index)
            linenum = str(index).split(".")[0]
            #dline = self.text_widget.tk.call(self.text_widget, 'dlineinfo', f'{linenum}.0')

            if dline is None: break
            #if type(dline) is str: break
            y = dline[1]

            self.widget.create_text(2,y,anchor="nw", font=self.font, text=" "+linenum+" ", fill=self.theme['num_of_lines_text_color'])
            index = self.text_widget.index(f"{index}+1line")

        linenum = int(linenum) - 1

        #Выравнивание ширины канваса под размер текста
        self.widget.configure(width=50)
        index = 1000; count = 1; widget_width=50

        while index < 100000000:
            width = (linenum // index)

            if width >= 1:
                widget_width = 50 + count * 10
                count += 1
                
            index *= 10

        self.widget.configure(width=widget_width)