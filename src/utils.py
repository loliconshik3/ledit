#from pynotifier import Notification

#def notify(title="", description="", iconPath="", duration=5, urgency="normal"):
#    Notification(title, description, duration, urgency, iconPath).send()


def get_line_end_index(data="", line=1):
    try:
        lines       = data.splitlines()
        need_line   = lines[line-1]
        column      = len(need_line)
    except:
        pass

    return f"{line}.{column}"

def edit_index(index="", line=0, char=0):
    """
    This method edit geted index. (Non Effective!)
    """

    index = index.split('.')
    lines = int(index[0]) + line
    chars = int(index[1]) + char
    
    index = f"{lines}.{chars}"

    return index

def get_line_tabs(data, tab_size):
    tabs = 0; symb = 0; spaces = 0
    for char in data:
        if char == ' ': spaces+=1
        else: symb += 1; break
        if spaces == tab_size: spaces=0; tabs+=1

    return tabs
