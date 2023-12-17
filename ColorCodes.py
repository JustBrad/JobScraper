class Colors:
    def rgb(r, g, b):
        return f"\u001b[38;2;{r};{g};{b}m"

    def rgbBackground(r, g, b):
        return f"\u001b[48;2;{r};{g};{b}m"

    BLUE = "\033[94m"
    CYAN = "\033[96m"
    GREEN = rgb(17, 255, 61)
    YELLOW = rgb(255, 170, 51)
    RED = "\033[91m"
    PURPLE = "\u001b[35m"
    WHITE = "\u001b[37m"
    LTGRAY = "\033[0;37m"
    DKGRAY = "\033[1;30m"
    REDBG = "\u001b[41m"
    GREENBG = rgbBackground(17, 255, 61)
    YELLOWBG = rgbBackground(255, 170, 51)
    BLUEBG = "\u001b[44m"
    PURPLEBG = "\u001b[45m"
    CYANBG = "\u001b[46m"
    WHITEBG = "\u001b[47m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
