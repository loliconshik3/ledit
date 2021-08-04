import tkinter as tk
from pygments.lexers import PythonLexer
from pygments.token import Token

lexer = PythonLexer()

root = tk.Tk()

text = tk.Text(root)
text.pack()

# Создаем теги с разными свойствами, которые будем присваивать соответствующим типам токенов
text.tag_config("keyword", foreground='blue')
text.tag_config("string_literal", foreground='red')

# Прописываем соответствие типа токена тегу подсветки
token_type_to_tag = {
    Token.Keyword: "keyword",
    Token.Operator.Word: "keyword",
    Token.Name.Builtin: "keyword",
    Token.Literal.String.Single: "string_literal",
    Token.Literal.String.Double: "string_literal",
}


def get_text_coord(s: str, i: int):
    """
    Из индекса символа получить "координату" в виде "номер_строки_текста.номер_символа_в_строке"
    """
    for row_number, line in enumerate(s.splitlines(keepends=True), 1):
        if i < len(line):
            return f'{row_number}.{i}'
        
        i -= len(line)


def on_edit(event):
    # Удалить все имеющиеся теги из текста
    for tag in text.tag_names():
        text.tag_remove(tag, 1.0, tk.END)
    
    # Разобрать текст на токены
    s = text.get(1.0, tk.END)
    tokens = lexer.get_tokens_unprocessed(s)
    
    for i, token_type, token in tokens:
        print(i, token_type, repr(token))  # Отладочный вывод - тут видно какие типы токенов выдаются
        j = i + len(token)
        if token_type in token_type_to_tag:
            text.tag_add(token_type_to_tag[token_type], get_text_coord(s, i), get_text_coord(s, j))

    # Сбросить флаг редактирования текста
    text.edit_modified(0)


text.bind('<<Modified>>', on_edit)


root.mainloop()