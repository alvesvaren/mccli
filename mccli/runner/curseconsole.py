import curses
from typing import TYPE_CHECKING, Any

Window = Any

if TYPE_CHECKING:
    from _curses import _CursesWindow
    Window = _CursesWindow



def main(stdscr: Window):
    curses.cbreak()
    curses.use_default_colors()
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()

    subwin = stdscr.subwin(rows-1, cols, 0, 0)
    subwin.scrollok(True)

    stdscr.keypad(True)
    stdscr.refresh()
    stdscr.nodelay(True)
    
    chars = ""
    while 1:
        old = stdscr.getyx()
        stdscr.move(rows-1, 0)
    
        stdscr.addstr("> ")
        stdscr.move(rows-1, len(chars) + 2)
        char = stdscr.getch()
        if char in range(0x110000) and chr(char).isprintable():
            stdscr.addch(char)
            chars += chr(char)
            subwin.addch(char)
            subwin.refresh()
        
        stdscr.clrtoeol()
        
        if char == 10:
            stdscr.clrtoeol()
            chars = ""
        if char == 127:
            chars = chars[:-1]
        # subwin.refresh()






if __name__ == "__main__":
    curses.wrapper(main)