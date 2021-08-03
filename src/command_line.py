import tkinter.font as tkfont
import tkinter
import utils

class CommandLine():

    def __init__(self, root, config, text):
        self.bottom_frame = tkinter.Frame(root)
        self.bottom_frame.pack(side="bottom", fill='x')
        self.config = config
        self.editor = None
        self.text = text

        self.font = tkfont.Font(family=config['command_font'], size=int(config['command_font_size']))

        self.widget = tkinter.Entry(self.bottom_frame, background=config['command_line_background_color'], 
                                                                font=self.font)

        self.info_widget = tkinter.Canvas(self.bottom_frame, height=15, background=config['info_panel_background_color'])
        self.__init_widget()

    def __init_widget(self):
        """
        Данный метод отвечает за инициализацию виджета для ввода комманд.
        """

        self.widget.config(insertbackground=self.config['text_cursor_color'])
        self.widget.config(borderwidth = 0, highlightthickness = 0)
        self.widget.config(highlightbackground=self.config['borders_color'])
        self.widget.config(foreground=self.config['command_line_text_color'])

        self.info_widget.config(highlightbackground=self.config['borders_color'])

        self.widget.pack(side='bottom', fill='x', expand=True)
        self.info_widget.pack(side='bottom', fill='x', expand=True)

        info_text = f"{self.config['name']} v{self.config['version']} | by loliconshik3"
        self.info_widget.create_text(2, 2, anchor='nw', text=info_text, font=self.font, fill=self.config['text_color'])

        self.widget.bind("<Return>", self.use_command)


    def use_command(self, event):
        """
        Этот метод отвечает за исполнение введённых команд.
        Имена и аргументы комманд настраиваются в файле config.json
        """

        commands = self.config['commands']
        command = self.widget.get().split(' ')
        self.widget.delete("0", tkinter.END)
        
        if command[0] == commands['move']:
            try:
                self.text.widget.focus_set() 
                self.text.widget.see(command[1])
                self.text.widget.mark_set("insert", command[1])
            except: pass

        elif command[0] == commands['replace']['name']:

            separator_index = command[2:].index(commands['replace']['separator'])
            replaced_data = " ".join(command[2:separator_index+2])
            replacing_data = " ".join(command[separator_index+3:])

            if command[1] == commands['replace']['all_key']:
                data = self.text.widget.get("1.0", tkinter.END).replace(replaced_data, replacing_data)
            elif command[1] == commands['replace']['one_key']:
                data = self.text.widget.get("1.0", tkinter.END).replace(replaced_data, replacing_data, 1)

            self.text.widget.delete("1.0", tkinter.END)
            self.text.widget.insert("1.0", data)

        elif command[0] == commands['open']['name']:
			
            self.editor.open_file(path = command[1])

    def redraw(self):
        try:
            self.info_widget.delete("all")

            info_text = f"{self.editor.filename.split('/')[-1]} ({self.editor.text.widget.index('insert')}) | {self.editor.file_ext} | utf-8 | {self.config['name']} v{self.config['version']} | by loliconshik3"

            self.info_widget.create_text(2, 2, anchor='nw', text=info_text, font=self.font, fill=self.config['text_color'])
        except Exception as e:
            print(e)

