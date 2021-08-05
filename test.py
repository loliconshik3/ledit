import tkinter
from pygments import lex
from pygments.lexers.markup import MarkdownLexer
from pygments.token import Generic
from pygments.lexer import bygroups
from pygments.styles import get_style_by_name


# add markup for bold-italic
class Lexer(MarkdownLexer):
    tokens = {key: val.copy() for key, val in MarkdownLexer.tokens.items()}
    # # bold-italic fenced by '***'
    tokens['inline'].insert(2, (r'(\*\*\*[^* \n][^*\n]*\*\*\*)',
                                bygroups(Generic.StrongEmph)))
    # # bold-italic fenced by '___'
    tokens['inline'].insert(2, (r'(\_\_\_[^_ \n][^_\n]*\_\_\_)',
                                bygroups(Generic.StrongEmph)))
    
def load_style(stylename):
    style = get_style_by_name(stylename)
    syntax_highlighting_tags = []
    for token, opts in style.list_styles():
        kwargs = {}
        fg = opts['color']
        bg = opts['bgcolor']
        if fg:
            kwargs['foreground'] = '#' + fg
        if bg:
            kwargs['background'] = '#' + bg
        font = ('Monospace', 10) + tuple(key for key in ('bold', 'italic') if opts[key])
        kwargs['font'] = font
        kwargs['underline'] = opts['underline']
        editor.tag_configure(str(token), **kwargs)
        syntax_highlighting_tags.append(str(token))
    editor.configure(bg=style.background_color,
                     fg=editor.tag_cget("Token.Text", "foreground"),
                     selectbackground=style.highlight_color)
    editor.tag_configure(str(Generic.StrongEmph), font=('Monospace', 10, 'bold', 'italic'))
    syntax_highlighting_tags.append(str(Generic.StrongEmph))
    return syntax_highlighting_tags    

def check_markdown(start='insert linestart', end='insert lineend'):
    data = editor.get(start, end)
    while data and data[0] == '\n':
        start = editor.index('%s+1c' % start)
        data = data[1:]
    editor.mark_set('range_start', start)

