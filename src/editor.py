from tkinter.filedialog import asksaveasfile, askopenfile, askdirectory
from tkinter.messagebox import showerror
from tkinter import messagebox
import tkinter.font as tkfont
import command_line
import custom_text
import main_frame
import tkinter
import json
import os

class Editor:
    """
    Экземпляр редактора.
    """

    def __init__(self):

        #==========Tkinter Init==========
        self.root = tkinter.Tk()
        #================================

        #==========Config Init==========
        with open(f"{os.path.dirname(os.path.abspath(__file__))}/config.json", "r") as file:
            self.config = json.loads(file.read())

        with open(f"{os.path.dirname(os.path.abspath(__file__))[:-4]}/themes/{self.config['color_theme']}.json", "r") as theme_file:
            self.theme = json.loads(theme_file.read())
        #===============================

        #==========MainWindow Init==========
        self.title          = self.config['name']
        self.filename       = self.config['empty_file_name']
        self.window_width   = self.config['window_width']
        self.window_height  = self.config['window_height']

        self.file_ext = None
        
        self.__init_main_window()
        #===================================

        #==========Font Init==========
        self.font = tkfont.Font(family=self.config['command_font'], size=int(self.config['command_font_size']))
        #=============================

        #==========MainFrame Init==========
        self.main_frame = main_frame.MainFrame(config=self.config, theme=self.theme)
        self.main_frame.pack(side="top", fill="both", expand=True)
        #==================================

        #==========Text Init==========
        self.text = self.main_frame.text
        self.text.editor = self
        self.text.widget.focus_set()
        #=============================

        #==========CommandLine Init==========
        self.command_line = self.main_frame.command_line
        self.command_line.editor = self
        self.command_line.redraw()
        #====================================

        #==========DirectoryTree Init==========
        if self.config['directory_tree']:
            self.dir_tree = self.main_frame.dir_tree
            self.dir_tree.editor = self
            self.dir_tree.tree.bind('<Double-1>', self.dir_tree.open_selected_file)
            self.dir_tree.tree.bind('<Return>', self.dir_tree.open_selected_file)
            
            self.main_directory = None
            #self.dir_tree.set_path(path=self.open_directory)
        #======================================

        #==========Cash Init==========
        try:
            self.cash = open(f"{os.path.dirname(os.path.abspath(__file__))}/cash", "r+")
            self.cash_text = self.cash.readlines()
            self.last_dir = self.cash_text[0]
        except Exception as e:
            print("System | Cash load has been failed |", e)
        #=============================

        #==========Keys Init==========
        self.__init_keys()
        #=============================

        #==========Main Loop==========
        self.root.mainloop()
        #=============================

    #====================Init Functions====================
    def __init_keys(self):
        keybinds = self.config['keybinds']

        self.root.bind(keybinds['new_file'], self.new_file)
        self.root.bind(keybinds['save_file'], self.save_file)
        self.root.bind(keybinds['select_text'], self.select_text)
        self.root.bind(keybinds['open_file'], self.open_file)
        self.root.bind_all(keybinds['save_as'], self.save_as)

        if self.config['directory_tree']:
            self.root.bind(keybinds['open_directory'], self.open_directory)

        if self.config['complete_quotes']:
            self.root.bind( '<quotedbl>', self.text.complete_quotes)
            self.root.bind( '<quoteright>', self.text.complete_quotes)

        if self.config['complete_brackets']:
            self.root.bind( '<bracketleft>', self.text.complete_brackets)
            self.root.bind( '<braceleft>', self.text.complete_brackets)
            self.root.bind( '<parenleft>', self.text.complete_brackets)

    def __init_main_window(self):
        """
        Данный метод отвечает за инициализацию основного окна.
        """

        self.root.title(f"{self.title} | {self.filename}")

        if not self.config['adaptive_screen_size']:
            self.root.minsize(width=self.window_width, height=self.window_height)

            if self.config['fixed_screen_size']:
                self.root.maxsize(width=self.window_width, height=self.window_height)
        else:
            screen_width = int(self.root.winfo_screenwidth() * self.config['adaptive_screen_size_percentage'])
            screen_height = int(self.root.winfo_screenheight() * self.config['adaptive_screen_size_percentage'])

            self.root.minsize(width=screen_width, height=screen_height)

            if self.config['fixed_screen_size']:
                self.root.maxsize(width=screen_width, height=screen_height)
        
        self.root.attributes('-fullscreen', self.config['fullscreen_mode'])
    #======================================================

    #====================Update Functions====================
    def update_filename(self, filename=""):
        """
        Данный метод отвечает за обновление имени открытого файла, и, соответственно, заголовка окна.
        """

        self.filename = filename
        self.root.title(f"{self.title} | {self.filename}")

    def update_cash(self):
        self.cash.close()
        self.cash = open(f"{os.path.dirname(os.path.abspath(__file__))}/cash", "w")
        self.cash.writelines(self.cash_text)
        self.cash.close()
        self.cash = open(f"{os.path.dirname(os.path.abspath(__file__))}/cash", "r+")

    def update_lastdir(self, lastdir=""):
        """
        Данный метод отвечает за обновление последней открытой директории.
        """
        self.last_dir = lastdir
        
        try:
            self.cash_text[0] = lastdir
        except:
            self.cash_text = [lastdir]

        print(self.cash_text)

        self.update_cash()
    #========================================================


    def new_file(self, event):
        """
        Этот метод, при использовании заданой, в файле config.json, комбинации клавиш, 
        создаёт новый пустой бланк, в редакторе.
        """

        self.text.widget.delete('1.0', tkinter.END)
        self.update_filename(self.config['empty_file_name'])

    def open_file(self, event=None, path=""):
        """
        Этот метод, при использовании заданой, в файле config.json, комбинации клавиш, 
        открывает окно, для выбора файла, который необходимо открыть в редакторе.
        """

        if path == "":
            try:
                inp = askopenfile(mode='r', initialdir=self.last_dir)
            except:
                inp = askopenfile(mode='r')
            if inp is None: return
        else:
            inp = open(path, 'r')
        
        self.update_lastdir(os.path.dirname(inp.name))
        self.update_filename(inp.name)

        data = inp.read()

        self.text.widget.delete('1.0', tkinter.END)
        self.text.widget.insert('1.0', data)

    def save_file(self, event):
        """
        Этот метод, при использовании заданой, в файле config.json, комбинации клавиш, 
        открывает окно, для сохранения файла с нужным именем, если редактируется новый файл, 
        и, в ином случае, просто перезаписывает файл.
        """

        try:
            data = self.text.widget.get('1.0', tkinter.END)

            if self.filename == self.config['empty_file_name']:
                try:
                    out = asksaveasfile(mode='w', initialdir=self.last_dir)
                except:
                    out = asksaveasfile(mode='w')
                if out is None: return

                #out = asksaveasfile(mode="w")
                self.update_filename(out.name)

                try:
                    out.write(data.rstrip())
                except:
                    showerror(title="Error", message="Saving file error")
                print(f"System | Save {self.filename} file.")
            else:
                out = open(f'{self.filename}', 'w')

                out.write(data)
                out.close()
                print(f"System | Save {self.filename} file.")
        except:
            pass

    def save_as(self, event):
        """
        Этот метод, при использовании заданой, в файле config.json, комбинации клавиш, 
        открывает окно, для сохранения файла с нужным именем.
        """

        try:
            try:
                out = asksaveasfile(mode='w', initialdir=self.last_dir)
            except:
                out = asksaveasfile(mode='w')
            if out is None: return
            #out = asksaveasfile(mode="w")
            
            data = self.text.widget.get('1.0', tkinter.END)
            self.update_filename(out.name)

            try:
                out.write(data.rstrip())
            except:
                showerror(title="Error", message="Saving file error")
        except:
            pass

    def open_directory(self, event):
        try:
            directory = askdirectory(initialdir=self.last_dir)
        except:
            directory = askdirectory()

        if directory != None and directory != () and directory != '':
            self.dir_tree.set_path(path=directory, clear=True)
            self.main_directory = directory
            print(self.main_directory)



    def select_text(self, event):
        """
        Этот метод, при использовании заданой, в файле config.json, комбинации клавиш, 
        выбирает весь текст в поле ввода.
        """

        if self.root.focus_get() == self.text.widget:
            self.text.widget.tag_add('sel', "1.0", 'end')
        elif self.root.focus_get() == self.command_line.widget:
            self.command_line.widget.select_range("0", 'end')