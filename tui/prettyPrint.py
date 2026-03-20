# Non-comprehensive list of colors ANSI colors.
from .windowUtils import get_window_size

COLORS = {
    "reset"     : "\033[0m",
    "black"     : "\033[30m",
    "red"       : "\033[31m",
    "green"     : "\033[32m",
    "yellow"    : "\033[33m",
    "blue"      : "\033[34m",
    "magenta"   : "\033[35m",
    "cyan"      : "\033[36m",
    "white"     : "\033[37m",
    "gray"      : "\033[90m",
    "b_red"     : "\033[91m",  # b_ for bright
    "b_greeb"   : "\033[92m",
    "b_yellow"  : "\033[93m",
    "b_blue"    : "\033[94m",
    "b_magenta" : "\033[95m",
    "b_cyan"    : "\033[96m",
    "b_white"   : "\033[97m"
}

def start_color(color):
    return f"{COLORS[color]}"

def end_color():
    return f"{COLORS["reset"]}"

def print_color(data_to_print, color_to_print):
    return f"{COLORS[color_to_print]}{data_to_print} {COLORS["reset"]}"

def print_info(info_string):
    return f"{COLORS['cyan']}[INFO]: {info_string} {COLORS["reset"]}"

def print_success(success_string):
    return f"{COLORS['green']}[INFO]: {success_string} {COLORS["reset"]}"

def print_error(error_string):
    return f"{COLORS['b_red']}[ERROR]: {error_string} {COLORS["reset"]}"

def print_welcome():
    welcome_large = r"""
Welcome to
__/\\\\____________/\\\\_____________________________________/\\\________/\\\_____________________        
 _\/\\\\\\________/\\\\\\____________________________________\/\\\_______\/\\\_____________________       
  _\/\\\//\\\____/\\\//\\\____________________________________\//\\\______/\\\___/\\\_______________      
   _\/\\\\///\\\/\\\/_\/\\\_____/\\\\\\\\_____/\\\\\__/\\\\\____\//\\\____/\\\___\///___/\\\\\\\\\\\_     
    _\/\\\__\///\\\/___\/\\\___/\\\/////\\\__/\\\///\\\\\///\\\___\//\\\__/\\\_____/\\\_\///////\\\/__    
     _\/\\\____\///_____\/\\\__/\\\\\\\\\\\__\/\\\_\//\\\__\/\\\____\//\\\/\\\_____\/\\\______/\\\/____   
      _\/\\\_____________\/\\\_\//\\///////___\/\\\__\/\\\__\/\\\_____\//\\\\\______\/\\\____/\\\/______  
       _\/\\\_____________\/\\\__\//\\\\\\\\\\_\/\\\__\/\\\__\/\\\______\//\\\_______\/\\\__/\\\\\\\\\\\_ 
        _\///______________\///____\//////////__\///___\///___\///________\///________\///__\///////////__

Author: Alexander Koefoed
----------------------------------------------------------------------------------------------------------
    """
    welcome_small = r"""
Welcome to

MM   MM MMMMMMM MM   MM M         M MM MMMMMMM
M M M M M       M M M M  M       M          M
M  M  M MMMMMMM M  M  M   M     M   MM     M
M     M M       M     M    M   M    MM    M
M     M M       M     M     M M     MM   M
M     M MMMMMMM M     M      M      MM MMMMMMM

Author: Alexander Koefoed
-----------------------------------------------
"""
    if get_window_size()[0] < 106:
        print(f"{COLORS['b_magenta']} \n {welcome_small} \n {COLORS['reset']}")
        return 0
    print(f"{COLORS['b_magenta']} \n {welcome_large} \n {COLORS['reset']}")
    return 0