

def get_line_end_index(data="", line=1):
    try:
        lines = data.splitlines()
        need_line = lines[line-1]
        column = len(need_line)
    except:
        pass

    return f"{line}.{column}"

def edit_index(index="", line=0, char=0):

    lines = int(index.split('.')[0]) + line
    chars = int(index.split('.')[1]) + char
    
    index = f"{lines}.{chars}"

    return index