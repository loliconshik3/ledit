import tkinter as tk
from tkinter import ttk

class MainInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('version')
        self.window.geometry("1024x768")
        self.create_widgets()

    def create_widgets(self):
        self.window['padx'] = 10
        self.window['pady'] = 10

        main_notebook_controll = ttk.Notebook(self.window, width=1000, height=700)

        a_tab = ttk.Frame(main_notebook_controll)
        b_tab = ttk.Frame(main_notebook_controll)
        c_tab = ttk.Frame(main_notebook_controll)

        main_notebook_controll.add(a_tab, text="Notebook A")
        main_notebook_controll.add(b_tab, text="Notebook B")
        main_notebook_controll.add(c_tab, text="Notebook C")

        main_notebook_controll.grid(row=1, column=1)

        c_tab = ttk.Frame(main_notebook_controll)
        main_notebook_controll.add(c_tab, text="Notebook D")

program = MainInterface()
program.window.mainloop()