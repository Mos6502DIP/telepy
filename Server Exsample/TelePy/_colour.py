colors = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "light_black": "\033[1;30m",
    "light_red": "\033[1;31m",
    "light_green": "\033[1;32m",
    "light_yellow": "\033[1;33m",
    "light_blue": "\033[1;34m",
    "light_magenta": "\033[1;35m",
    "light_cyan": "\033[1;36m",
    "light_white": "\033[1;37m",
    "reset": "\033[0m"
}
backgrounds = {
    "black": "\033[40m",
    "red": "\033[41m",
    "green": "\033[42m",
    "yellow": "\033[43m",
    "blue": "\033[44m",
    "magenta": "\033[45m",
    "cyan": "\033[46m",
    "white": "\033[47m",
    "light_black": "\033[1;40m",
    "light_red": "\033[1;41m",
    "light_green": "\033[1;42m",
    "light_yellow": "\033[1;43m",
    "light_blue": "\033[1;44m",
    "light_magenta": "\033[45m",
    "light_cyan": "\033[1;46m",
    "light_white": "\033[1;47m",
}

def colour(text, color, background=None):
    color_code = colors.get(color, colors['reset'])
    background_code = backgrounds.get(background, '')
    return f"{background_code}{color_code}{text}{colors['reset']}"
