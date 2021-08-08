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

        self.first_line = None
        self.last_line = None
        
        self.syntax_file = {}
        self.current_text = None
        self.current_file = None

        self.widget = tk.Text(root, undo=True, background=theme['background_color'], foreground=theme['text_color'])
        self.font = tkfont.Font(family=config['font'], size=config['font_size'])
        self.widget.configure(font=self.font)

        tab_size = self.font.measure(' ' * config['tab_size'])
        self.widget.config(tabs=tab_size)

        self.widget.config(insertbackground=theme['text_cursor_color'])
        self.widget.config(borderwidth = 0, highlightthickness = 0)
        #self.widget.config(highlightbackground=config['borders_color'])

        self.widget.bind('<Tab>', self.tab)
        self.widget.bind('<BackSpace>', self.backspace)
        self.widget.bind(config['keybinds']['insert_copied_text'], self.insert)

        # create a proxy for the underlying widget
        self._orig = self.widget._w + "_orig"
        self.widget.tk.call("rename", self.widget._w, self._orig)
        self.widget.tk.createcommand(self.widget._w, self._proxy)

        try:
            home = os.path.expanduser('~')
            self.syntax_dir = f"{home}/.ledit/syntax"
            self.syntax_files = os.listdir(self.syntax_dir)
        except Exception as e:
            print(e)
            
            self.syntax_dir = f"{os.path.dirname(os.path.abspath(__file__))[:-4]}/syntax"
            self.syntax_files = os.listdir(self.syntax_dir)
        
        self.init_syntax_files()

    #====================Init Functions====================
    def init_syntax_files(self):
        """
        Данный метод отвечает за инициализацию файлов синтаксиса.
        """

        for index in range(len(self.syntax_files)):

            with open(f"{self.syntax_dir}/{self.syntax_files[index]}", "r") as file:
                self.syntax_files[index] = json.loads(file.read())

    def init_syntax_colors(self):
        """
        Init colors of syntax highlight.
        """

        print('SYSTEM | Init syntax colors')

        syntax = self.syntax_file
        self.widget.tag_config("function", foreground=syntax['function_color'])
        self.widget.tag_config("string", foreground=syntax['string_color'])
        self.widget.tag_config("comment", foreground=syntax['comment_color'])

        for _class in syntax['classes'].keys():
            color = syntax['classes'][_class]['color']
            self.widget.tag_config(_class, foreground=color)      

        self.syntax_highlight(first_line='1.0', last_line=self.widget.index('end'), replace=False)      
    #======================================================

    def insert(self, event):
        """
        Ctrl+v call this method.
        """

        insert_index = self.widget.index('insert')
        try:
            sel_first, sel_last = self.widget.index('sel.first'), self.widget.index('sel.last')
            self.widget.delete(sel_first, sel_last)
        except:
            pass
        self.widget.insert(insert_index, self.widget.clipboard_get())

        last_insert = self.widget.index('insert')
        self.syntax_highlight(first_line=insert_index, last_line=last_insert, replace=False)
        
        
        self.widget.see(last_insert)
        return 'break'

    def tab(self, event):
        """
        Tab key call this method.
        """

        if not self.macros():
            self.widget.insert('insert', ' '*self.editor.config['tab_size'])
        return 'break'

    def macros(self):
        """
        Macros method.
        """

        try:
            macros_list = self.syntax_file['macros']

            insert_index = self.widget.index('insert')

            for macros in macros_list.keys():
                macros_start_index = self.widget.index(f'insert-{len(macros)}c')
                macros_before_char = self.widget.get(f"{macros_start_index}-1c", macros_start_index)

                if self.widget.get(macros_start_index, insert_index) == macros:

                    if macros_before_char == "" or macros_before_char == "\n" or macros_before_char == " ":
                        tabs = utils.get_line_tabs(self.widget.get(f"{macros_start_index} linestart", f"{macros_start_index} lineend"),
                        self.editor.config['tab_size'])
                        tab_string = (self.editor.config['tab_size'] * " ") * tabs

                        self.widget.delete(macros_start_index, insert_index)

                        total_text = macros_list[macros].replace('\t\t', "  " * self.editor.config['tab_size'] + tab_string)
                        total_text = total_text.replace('\t', " " * self.editor.config['tab_size'] + tab_string)
                        self.widget.insert('insert', total_text)

                        self.syntax_highlight(first_line=macros_start_index, last_line=self.widget.index('insert'), replace=False)

                        return True
        except:
            pass

        return False

    def backspace(self, event):
        """
        Backspace key call this method.
        """

        sel_first, sel_last = self.widget.index('sel.first'), self.widget.index('sel.last')

        tab_size_index = f"insert-{self.editor.config['tab_size']}c"
        backspace = self.widget.get(tab_size_index, 'insert')

        if backspace == " "*self.editor.config['tab_size']:
            self.widget.delete(tab_size_index, 'insert')
        elif sel_first == 'None':
            self.widget.delete('insert-1c')
        else:
            self.widget.delete(sel_first, sel_last)

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

    def functions_highlight(self, syntax=None, color=None, first_line=None, last_line=None):
        function_syntax = syntax.split('{name}')

        self.widget.tag_remove("function", first_line, last_line)
        start = first_line
        pos = self.widget.search(function_syntax[0], start, stopindex=last_line)
        ff_length = len(function_syntax[0])
        while pos:
            func_start_pos = self.widget.index(f"{pos}+{ff_length}c")
            func_end_pos = self.widget.search(function_syntax[1], func_start_pos, stopindex=f"{func_start_pos} lineend")

            if func_end_pos != "":
                self.widget.tag_add("function", func_start_pos, func_end_pos)

            start = self.widget.index(f"{pos}+1c") #utils.edit_index(pos, 0, 1)
            pos = self.widget.search(function_syntax[0], start, stopindex=last_line)

        #self.widget.tag_config("function", foreground=color)

        #print("Sys | Functions highlight")


    def text_highlight(self, color=None, first_line=None, last_line=None):
        """
        Данный метод отвечает за подсветку строк текста.
        """

        quotes_list = {}; count = 0
        quotes = ["'", '"']
        
        first_line = utils.edit_index(first_line, -10, 0)
        last_line = utils.edit_index(last_line, 10, 0)

        self.widget.tag_remove("string", first_line, last_line)
        for quote in quotes:
            start = first_line
            pos = self.widget.search(quote, start, stopindex=last_line)
            while pos:
                if not count in quotes_list.keys():
                    quotes_list[count] = [pos]
                else:
                    quotes_list[count].append(self.widget.index(f"{pos}+1c"))
                    self.widget.tag_add("string", quotes_list[count][0], quotes_list[count][1])
                    count += 1

                start = self.widget.index(f"{pos}+1c") #utils.edit_index(pos, 0, 1)
                pos = self.widget.search(quote, start, stopindex=last_line)

        #self.widget.tag_config("string", foreground=color)

        #print("Sys | Text highlight")



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
            
            start = self.widget.index(f"{pos}+{len(comment_symbol)}c")#utils.edit_index(pos, 0, len(comment_symbol))
            pos = self.widget.search(comment_symbol, start, stopindex=last_line)

        self.widget.tag_remove("comment", first_line, last_line)
        for index in comments_list.keys():
            line_end = self.widget.index(f"{index}.0 lineend")
            comment_start = f"{index}.{comments_list[index]}"

            if not "string" in self.widget.tag_names(comment_start):
                for tagname in self.widget.tag_names(None):
                    self.widget.tag_remove(tagname, comment_start, line_end)

                self.widget.tag_add("comment", comment_start, line_end)

        #self.widget.tag_config("comment", foreground=color)

        #print("Sys | Comments highlight")

    def syntax_highlighting(self, first_line=None, last_line=None, syntaxis=None, syntax_file=None):
        #for tagname in self.widget.tag_names(None):
        #    if tagname in syntaxis.keys():
        #        self.widget.tag_remove(tagname, "1.0", "end")

        for _class in syntaxis.keys():
            self.widget.tag_remove(_class, first_line, last_line)
            color_everywhere = syntaxis[_class]['color_everywhere']
            syntax = syntaxis[_class]['syntax_list']
            #color = syntaxis[_class]['color']

            test_syntax = {}
            for text in syntax:
                test_syntax[text] = text

            #for text in syntax:
            for text in test_syntax:
                start = first_line
                pos = self.widget.search(text, start, stopindex=last_line)

                while pos:
                    end = self.widget.index(f'{pos}+{len(text)}c')

                    tag_names = self.widget.tag_names(pos)

                    if not "comment" in tag_names and not "string" in tag_names:
                        if not color_everywhere:
                            before_index = utils.edit_index(pos, 0, -1); before_char = self.widget.get(before_index, pos)
                            after_index = utils.edit_index(end, 0, 1); after_char = self.widget.get(end, after_index)
                            if before_char in syntax_file['syntax_accept_chars'] and after_char in syntax_file['syntax_accept_chars']:
                                self.widget.tag_add(_class, pos, end)
                        else:
                            self.widget.tag_add(_class, pos, end)
                    start = end
                    pos = self.widget.search(text, start, stopindex=last_line)

            #self.widget.tag_config(_class, foreground=color)



    def syntax_highlight(self, event=None, first_line=None, last_line=None, replace=True):
        """
        Данный метод отвечает за подсветку всего синтаксиса.
        """
        current_text = self.widget.get(first_line, last_line)

        if first_line != self.first_line or last_line != self.last_line or current_text != self.current_text:
            self.first_line = first_line
            self.last_line = last_line
            self.current_text = current_text

            syntax_file = self.syntax_file

            if replace:
                first_line = self.widget.index('insert linestart')
                last_line = self.widget.index('insert lineend')

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

                #Functions
                try:
                    self.functions_highlight(syntax=syntax_file['function_syntax'],
                                            color=syntax_file['function_color'],
                                            first_line=first_line, 
                                            last_line=last_line)
                except Exception as e:
                    print(e)

                #Syntax
                self.syntax_highlighting(first_line=first_line,
                                        last_line=last_line,
                                        syntaxis=syntaxis,
                                        syntax_file=syntax_file)
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
