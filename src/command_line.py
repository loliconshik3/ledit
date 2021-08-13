import tkinter.font as tkfont
import subprocess
import tkinter
import utils
import sys
import os

class CommandLine():

    def __init__(self, root, config, text, theme):
        self.bottom_frame = tkinter.Frame(root)
        self.bottom_frame.pack(side="bottom", fill='x')

        self.config     = config
        self.editor     = None
        self.theme      = theme
        self.text       = text

        self.font   = tkfont.Font(family=config['command_font'], size=int(config['command_font_size']))

        self.widget = tkinter.Entry(self.bottom_frame, background=theme['command_line_background_color'], 
                                                                font=self.font)

        self.info_widget = tkinter.Canvas(self.bottom_frame, height=15, background=theme['info_panel_background_color'])
        self.__init_widget()

        try:
            home = os.path.expanduser("~")
            self.history = open(f"{home}/.ledit/commands_history", "r+")
        except:
            self.history = open(f"{os.path.dirname(os.path.abspath(__file__))}/commands_history", "r+")
        
        self.history_text = self.history.readlines()
        self.history_index = len(self.history_text) - 1

    def __init_widget(self):
        """
        Данный метод отвечает за инициализацию виджета для ввода комманд.
        """

        self.widget.config(insertbackground=self.theme['text_cursor_color'])
        self.widget.config(borderwidth = 0, highlightthickness = 0)
        self.widget.config(highlightbackground=self.theme['borders_color'])
        self.widget.config(foreground=self.theme['command_line_text_color'])

        self.info_widget.config(highlightbackground=self.theme['borders_color'])

        self.widget.pack(side='bottom', fill='x', expand=True)
        self.info_widget.pack(side='bottom', fill='x', expand=True)

        self.redraw()
        #info_text = f"{self.config['name']} v{self.config['version']} | by loliconshik3"
        #self.info_widget.create_text(2, 2, anchor='nw', text=info_text, font=self.font, fill=self.theme['text_color'])

        self.widget.bind("<Return>", self.use_command)
        self.widget.bind("<Up>", self.previous_command)
        self.widget.bind("<Down>", self.next_command)


    def previous_command(self, event):
        print(self.history_index)

        if self.history_index >= 0:
            self.widget.delete('0', 'end')
            self.widget.insert('0', self.history_text[self.history_index].replace("\n", ""))
            if self.history_index > 0: self.history_index -= 1
        else:
            self.history_index = len(self.history_text) - 1
            self.widget.delete('0', 'end')

    def next_command(self, event):
        print(self.history_index)

        if self.history_index <= len(self.history_text) - 1:
            if self.history_index < len(self.history_text) - 1: self.history_index += 1
            self.widget.delete('0', 'end')
            self.widget.insert('0', self.history_text[self.history_index].replace("\n", ""))
        else:
            self.history_index = len(self.history_text) - 1
            self.widget.delete('0', 'end')

    def update_history(self, text):
        """
        This method update ledit commands history.
        """

        self.history_text.append(text)

        self.history.close()

        try:
            home = os.path.expanduser("~")
            self.history = open(f"{home}/.ledit/commands_history", "w")
        except:
            self.history = open(f"{os.path.dirname(os.path.abspath(__file__))}/commands_history", "w")

        self.history.writelines("\n".join(self.history_text))
        self.history.close()

        try:
            home = os.path.expanduser("~")
            self.history = open(f"{home}/.ledit/commands_history", "r+")
        except:
            self.history = open(f"{os.path.dirname(os.path.abspath(__file__))}/commands_history", "r+")

        self.history_index = len(self.history_text) - 1

    def use_command(self, event):
        """
        Этот метод отвечает за исполнение введённых команд.
        Имена и аргументы комманд настраиваются в файле config.json
        """

        commands        = self.config['commands']
        command_text    = self.widget.get()
        command         = command_text.split(' ')
        self.widget.delete("0", tkinter.END)

        if command_text != "":
            try:
                if command_text != self.history_text[-1]:
                    self.update_history(command_text)
            except:
                self.update_history(command_text)

        if command[0] == commands['move']:
            self.move(command)

        elif command[0] == commands['replace']['name']:
            self.replace_text(command, commands)

        elif command[0] == commands['open']['name']:
            self.editor.open_file(path = command[1])

        elif command[0] == commands['open_directory']['name']:
            self.editor.open_directory(path = command[1])

        elif command[0] == commands['open_config']['name']:
            self.editor.open_file(path=self.editor.config_path)

        elif command[0] == commands['select']['name']:
            self.select_text(start=command[1], end=command[2])

        elif command[0] == commands['find']['name']:
            self.find_text(command, commands)

        #elif command[0] == "run":
        #    if sys.platform == "win32":
        #        new_window_command = "cmd.exe /c start".split()
        #    else:  
        #        new_window_command = "terminal -e".split()
        #
        #    subprocess.check_call(new_window_command + ['python', f'{self.editor.filename}'])

        #elif command[0] == 'theme':
        #    self.editor.theme = self.editor.theme_files[command[1]]

        #elif command[0] == commands['update_config']['name']:
        #    self.editor.update_config(command[1])

    def select_text(self, start, end):
        self.text.widget.focus_set()
        self.text.widget.mark_set('insert', end)
        self.text.widget.see(end)
        self.text.widget.tag_add('sel', start, end)

    def move(self, command):
        """
        Move command method. 

        Move text cursor in input coordinates.
        After that focused screen on this coordinates.
        """

        try:
            self.text.widget.focus_set() 
            self.text.widget.see(command[1])
            self.text.widget.mark_set("insert", command[1])
        except: pass

    def find_text(self, command, commands):
        """
        Replace command method. 
        
        Replace all (or not all) text.
        """
        
        try:
            finded_data   = " ".join(command[1:])

            searched_first_index = self.text.widget.search(finded_data, 'insert', stopindex=f"end")
            searched_last_index = self.text.widget.index(f"{searched_first_index}+{len(finded_data)}c")

            self.text.widget.focus_set()
            self.text.widget.see(searched_first_index)
            self.text.widget.mark_set('insert', searched_last_index)
            self.text.widget.tag_add('sel', searched_first_index, searched_last_index)
        except Exception as e:
            print(e)

    def replace_text(self, command, commands):
        """
        Replace command method. 
        
        Replace all (or not all) text.
        """

        separator_index = command[2:].index(commands['replace']['separator'])
        replaced_data   = " ".join(command[2:separator_index+2])
        replacing_data  = " ".join(command[separator_index+3:])

        if command[1] == commands['replace']['all_key']:
            data = self.text.widget.get("1.0", tkinter.END).replace(replaced_data, replacing_data)
        elif command[1] == commands['replace']['one_key']:
            data = self.text.widget.get("1.0", tkinter.END).replace(replaced_data, replacing_data, 1)

        self.text.widget.delete("1.0", tkinter.END)
        self.text.widget.insert("1.0", data)


    def redraw(self):
        """
        Redraw info panel.
        Use, when need update information on panel.
        """

        try:
            self.info_widget.delete("all")

            filename        = self.editor.filename.split('/')[-1]
            insert_index    = self.editor.text.widget.index('insert')
            file_ext        = self.editor.file_ext
            name            = self.editor.maincfg['title'] #self.config['name']
            version         = self.editor.maincfg['version'] #self.config['version']
            text_scale      = self.editor.text_percentage_size
            theme           = self.config['color_theme']
            system          = sys.platform

            if self.editor.current_file_text != self.text.widget.get('1.0', 'end'):
                filename += '*'

            info_text = f"{filename} ({insert_index}) | ft: {file_ext} | utf-8 | scale: {text_scale} | {system} | {name} v{version} | theme: {theme} | by loliconshik3"

            self.info_widget.create_text(2, 2, anchor='nw', text=info_text, font=self.font, fill=self.theme['info_panel_text_color'])
        except Exception as e:
            print(e)

