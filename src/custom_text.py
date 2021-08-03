import tkinter.font as tkfont
import tkinter as tk
import linenum
import utils
import json
import os

class CustomText():
    def __init__(self, root, config, theme):
        self.widget = tk.Text(root)
        self.editor = None
        self.theme = theme

        self.widget = tk.Text(root, undo=True, background=theme['background_color'], foreground=theme['text_color'])
        font = tkfont.Font(family=config['font'], size=config['font_size'])
        self.widget.configure(font=font)

        tab_size = font.measure(' ' * config['tab_size'])
        self.widget.config(tabs=tab_size)

        self.widget.config(insertbackground=theme['text_cursor_color'])
        self.widget.config(borderwidth = 0, highlightthickness = 0)
        #self.widget.config(highlightbackground=config['borders_color'])

        self.widget.bind('<Tab>', self.tab)

        # create a proxy for the underlying widget
        self._orig = self.widget._w + "_orig"
        self.widget.tk.call("rename", self.widget._w, self._orig)
        self.widget.tk.createcommand(self.widget._w, self._proxy)

        self.syntax_dir = f"{os.path.dirname(os.path.abspath(__file__))[:-4]}/syntax"
        self.syntax_files = os.listdir(self.syntax_dir)
        self.init_syntax_files()

    def init_syntax_files(self):
        """
        Данный метод отвечает за инициализацию файлов синтаксиса.
        """

        for index in range(len(self.syntax_files)):

            with open(f"{self.syntax_dir}/{self.syntax_files[index]}", "r") as file:
                self.syntax_files[index] = json.loads(file.read())


    def tab(self, event):
        self.widget.insert('insert', ' '*self.editor.config['tab_size'])
        return 'break'

    def complete_indentations(self, event=None):
        """
        Этот метод отвечает за дополнение отступов.
        """

        tab_size = self.editor.config['tab_size']
        current_line = self.widget.index('insert linestart')
        before_line_start = utils.edit_index(current_line, -1, 0)

        before_text = (self.widget.get(before_line_start, f'{before_line_start} lineend'))

        last_char = self.widget.get(f'{before_line_start} lineend-1c')

        tabs = 0; symb = 0; spaces = 0
        for char in before_text:
            if char == ' ': spaces+=1
            else: symb += 1; break
            if spaces == tab_size: spaces=0; tabs+=1

        total_tabs = ' ' * tab_size * tabs
        if last_char == ':' or last_char == '[' or last_char == '(' or last_char == '{':
            total_tabs += ' ' * tab_size

        self.widget.insert('insert', total_tabs)

        brackets_list = [')', '}', ']']
        current_index = self.widget.index('insert')
        if self.widget.get(current_index) in brackets_list:
            self.widget.insert(current_index, '\n'+total_tabs[:-tab_size])
            self.widget.mark_set('insert', current_index)

        return


    def complete_quotes(self, event):
        """
        Этот метод, при написании одной кавычки, добавляет к ней ещё одну,
        после чего перемещает курсор внутрь кавычек.

        Работа метода настраиваеться в config.json
        """

        self.widget.insert(self.widget.index('insert'), event.char)

        insert = self.widget.index("insert")
        index = utils.edit_index(index=insert, line=0, char=-1)

        self.widget.mark_set("insert", index)

    def complete_brackets(self, event):
        """
        Этот метод, при написании одной скобки, добавляет к ней ещё одну,
        после чего перемещает курсор внутрь скобок.

        Работа метода настраиваеться в config.json
        """

        brackets_list = {
            "[" : "]", "(" : ")", "{" : "}"
        }

        for bracket in brackets_list.keys():
            if event.char == bracket:
                self.widget.insert(self.widget.index('insert'), brackets_list[bracket])

        insert = self.widget.index("insert")
        index = utils.edit_index(index=insert, line=0, char=-1)

        self.widget.mark_set("insert", index)



    def syntax_redraw(self):
        index = self.widget.index("@0,0")
        first_line = index
        while True :
            dline= self.widget.dlineinfo(index)
            if dline is None: break

            index = self.widget.index("%s+1line" % index)
        last_line = index

        self.syntax_highlight(first_line=first_line, last_line=last_line)

    def text_highlight(self, color=None, first_line=None, last_line=None):
        """
        Данный метод отвечает за подсветку строк текста.
        """

        quotes_list = {}; count = 0
        quotes = ["'", '"']
        
        self.widget.tag_remove("string", "1.0", 'end')
        for quote in quotes:
            start = first_line
            pos = self.widget.search(quote, start, stopindex=last_line)
            while pos:
                if not count in quotes_list.keys():
                    quotes_list[count] = [pos]
                else:
                    quotes_list[count].append(utils.edit_index(pos, 0, 1))
                    self.widget.tag_add("string", quotes_list[count][0], quotes_list[count][1])
                    count += 1

                start = utils.edit_index(pos, 0, 1)
                pos = self.widget.search(quote, start, stopindex=last_line)

        self.widget.tag_config("string", foreground=color)



    def comments_highlight(self, comment_symbol, color, first_line=None, last_line=None):
        """
        Данный метод отвечает за подсветку комментариев.
        """

        comments_list, start = {}, first_line

        pos = self.widget.search(comment_symbol, start, stopindex=last_line)
        while pos:
            pos_x, pos_y = pos.split('.')
            if not pos_x in comments_list.keys():
                comments_list[pos_x] = pos_y
            
            start = utils.edit_index(pos, 0, len(comment_symbol))
            pos = self.widget.search(comment_symbol, start, stopindex=last_line)

        self.widget.tag_remove("comment", "1.0", 'end')
        for index in comments_list.keys():
            line_end = utils.get_line_end_index(self.widget.get("1.0", "end"), int(index))
            comment_start = f"{index}.{comments_list[index]}"

            for tagname in self.widget.tag_names(None):
                self.widget.tag_remove(tagname, comment_start, line_end)

            self.widget.tag_add("comment", comment_start, line_end)

        self.widget.tag_config("comment", foreground=color)



    def syntax_highlight(self, event=None, first_line=None, last_line=None):
        """
        Данный метод отвечает за подсветку всего синтаксиса.
        """

        extension = self.editor.filename.split(".")[-1]
        syntax_file = None

        self.editor.file_ext = None

        for file in self.syntax_files:
            for file_ext in file['file_extension']:
                if file_ext == extension:
                    syntax_file = file
                    self.editor.file_ext = extension
                    break

        try:
            syntaxis = syntax_file['classes']
        
            #Text
            self.text_highlight(color=syntax_file['string_color'],
                                first_line=first_line, 
                                last_line=last_line)

            #Comments
            self.comments_highlight(syntax_file['comment_symbol'], 
                                    syntax_file['comment_color'],
                                    first_line=first_line,
                                    last_line=last_line)

            #Syntax
            for key in syntaxis.keys():
                syntax = syntaxis[key]['syntax_list']
                color = syntaxis[key]['color']

                for tagname in self.widget.tag_names(None):
                    if tagname == key:
                        self.widget.tag_remove(tagname, "1.0", 'end')

                for text in syntax:
                    start = first_line
                    pos = self.widget.search(text, start, stopindex=last_line)
                    while pos:
                        end = utils.edit_index(pos, 0, len(text))
                        
                        before_index = utils.edit_index(pos, 0, -1); before_char = self.widget.get(before_index, pos)
                        after_index = utils.edit_index(end, 0, 1); after_char = self.widget.get(end, after_index)

                        if (before_char in syntax_file['syntax_accept_chars'] or before_char == "	") and after_char in syntax_file['syntax_accept_chars']:
                            if not "comment" in self.widget.tag_names(pos):
                                if not "string" in self.widget.tag_names(pos):
                                    self.widget.tag_add(key, pos, end)
                        
                        start = end
                        pos = self.widget.search(text, start, stopindex=last_line)

                    self.widget.tag_config(key, foreground=color)
                    
        except:
            pass

    def _proxy(self, *args):
        # let the actual widget perform the requested action
        try:
            cmd = (self._orig,) + args
            result = self.widget.tk.call(cmd)
        except:
            result = None

        # generate an event if something was added or deleted,
        # or the cursor position changed
        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("xview", "scroll") or
            args[0:2] == ("yview", "moveto") or
            args[0:2] == ("yview", "scroll")
        ):
            self.widget.event_generate("<<Change>>", when="tail")

        if (args[0] in ("insert", "replace", "delete") or 
            args[0:3] == ("mark", "set", "insert") or
            args[0:2] == ("xview", "moveto") or
            args[0:2] == ("yview", "moveto")
        ):
            self.widget.event_generate("<<SyntaxChange>>", when="tail")

        # return what the actual widget returned
        return result        
