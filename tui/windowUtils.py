import shutil

# Always get window size after a clear()
def get_window_size():
    columns, lines = shutil.get_terminal_size()
    return columns, lines

# clear window, ready for updated view
def clear():
    print(f"\033[2J\033[H", end="")