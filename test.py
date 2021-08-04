import tkinter as tk


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Colorful text")
        self.geometry("256x64")
        self.resizable(width=False, height=False)

        self.text = tk.Text(self)
        self.text.pack()
        self.text.insert("end", "First Line\nSecond Line")

        self.apply_color()

    def apply_color(self):
        from itertools import cycle

        colors = ["Red", "Green", "Blue"]
        color_iterator = cycle(colors)

        # Get the string from the tk.Text widget.
        text_str = self.text.get("1.0", "end-1c")

        lines = text_str.splitlines(True)

        for line_index, line in enumerate(lines, start=1):
            for char_index, char in enumerate(line):
                if char.isspace():
                    # Ignore whitespace
                    continue
                color = next(color_iterator)
                self.text.tag_add(color, f"{line_index}.{char_index}")
        for color in colors:
            self.text.tag_config(color, foreground=color)


def main():

    application = Application()
    application.mainloop()

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())