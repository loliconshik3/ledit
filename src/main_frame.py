import tkinter.font as tkfont
import tkinter as tk
import directory_tree
import command_line
import custom_text
import linenum
import json
import os


class MainFrame(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        #=====Init Config=====
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/config.json", "r") as file:
            config = json.loads(file.read())
        self.config = config
        #=====================

        #=====Init Text=====
        self.text = custom_text.CustomText(self, config)
        #===================

        #=====Directory tree=====
        if config['directory_tree']:
            self.dir_tree = directory_tree.DirectoryTree(self, config)
            self.dir_tree.tree.pack(side="left", fill='y')
        #========================

        #=====Scroll bar=====
        if config['scrollbar']:
            self.vsb = tk.Scrollbar(self, orient="vertical", command=self.text.widget.yview)
            self.text.widget.configure(yscrollcommand=self.vsb.set)
            self.vsb.pack(side="right", fill="y")
        #====================

        #=====Command line=====
        if config['command_line']:
            self.command_line = command_line.CommandLine(self, config, self.text)
        #======================

        #=====Line numbers=====
        if config['num_of_lines']:
            self.linenumbers = linenum.TextLineNumbers(self, config, self.text.widget)
        #======================

        #=====Pack and bind=====
        self.text.widget.pack(side="right", fill="both", expand=True)
        
        self.text.widget.bind_all("<<Change>>", self._on_change)
        self.text.widget.bind("<Configure>", self._on_change)
        self.text.widget.bind_all("<<SyntaxChange>>", self._on_syntax_change)
        self.text.widget.bind_all("<Return>", self.text.complete_indentations)
        #=======================

    def _on_change(self, event=None):
        if self.config['num_of_lines']:
            self.linenumbers.redraw()

    def _on_syntax_change(self, event=None):
        self.text.syntax_redraw()
        self.command_line.redraw()
