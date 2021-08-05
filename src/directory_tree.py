import tkinter.ttk as ttk
import tkinter as tk
import os

class DirectoryTree:

    def __init__(self, root, config, theme):
        self.root   = root
        self.config = config
        self.theme  = theme

        self.frame = tk.Frame(root)
        self.frame.pack(side='left', fill='both')

        self.tree = ttk.Treeview(self.frame, show='tree')

        self.style = ttk.Style(self.tree)
        self.style.theme_use('clam')
        self.style.configure('Treeview', background=theme['directory_tree_background_color'], 
                                         fieldbackground=theme['directory_tree_background_color'], 
                                         foreground = theme['directory_tree_text_color'],
                                         bordercolor=theme['directory_tree_background_color'],
                                         lightcolor=theme['directory_tree_background_color']
        )

        self.editor = None

    def set_path(self, parent=None, path="", clear=False):
        """
        This method set path to directory tree.
        After this method tree has been update, and show new directory.
        """

        if clear:
            for child in self.tree.get_children():
                self.tree.delete(child)

        if parent == None:
            parent_path = path.split('/')[-1].upper()
            parent = self.tree.insert('', 'end', text = parent_path, open = False)

        for directory in os.listdir(path):

            full_path = os.path.join(path, directory)
            isdir = os.path.isdir(full_path)

            id = self.tree.insert(parent, 'end', text = directory, open = False)

            if isdir:
                self.set_path(id, full_path)

    def open_selected_file(self, event):
        """
        This method open selected (in directory tree) file.
        """

        curItem = self.tree.focus()
        childs  = self.tree.get_children(curItem)
        
        item_path = []

        witem   = curItem
        parent  = self.tree.parent(witem)
        while parent != "":
            item_path.append(self.tree.item(witem)['text'])
            witem   = parent
            parent  = self.tree.parent(witem)

        item_path.reverse()
        item_path = "/".join(item_path)
        #print(item_path)

        if childs == ():
            self.editor.open_file(path=f"{self.editor.main_directory}/{item_path}")
            #print(item)