import curses
from typing import TYPE_CHECKING, Any

Window = Any

if TYPE_CHECKING:
    from _curses import _CursesWindow
    Window = _CursesWindow

def move_cursor(stdscr, chars):
    rows, cols = stdscr.getmaxyx()
    stdscr.move(rows-1, len(chars) + 2)


class CurseState:
    def __init__(self, scr: _CursesWindow, prefix = "> "):
        self.scr = scr
        self.prefix = prefix
        self.cursor_index = 0
        self.line = ""
        self.history = []
        self.rows, self.cols = scr.getmaxyx()
        self.history_index = len(self.history)
    
    def move_cursor(self, index = None):
        if not index is None:
            self.cursor_index = index
        self.scr.move(self.rows - 1, self.cursor_index + len(self.prefix))
    
    def update(self):
        self.rows, self.cols = self.scr.getmaxyx()
        self.scr.move(self.rows - 1, 0)
        self.scr.addstr("> ")
        self.move_cursor()

        char = self.scr.getch()
        if char in (10, curses.KEY_ENTER):
            self.history.append(self.line)
            # run command
            self.line = ""
            move_cursor(self.scr, self.line)
            self.scr.clrtoeol()
        elif char in (127, curses.KEY_BACKSPACE):
            self.line = self.line[:-1]
            move_cursor(self.scr, self.line)
            self.scr.clrtoeol()
        elif char in (258, curses.KEY_DOWN):
            pass
        elif char in (259, curses.KEY_UP):
            pass
        elif char in (260, curses.KEY_LEFT):
            self.scr.move(self.rows-1, 0)
            self.scr.refresh()
        else:
            if char < 0:
                return
            curses.ungetch(char)
            try:
                char = self.scr.get_wch()
            except Exception:
                pass
        


def main(stdscr: Window):
    curses.cbreak()
    curses.use_default_colors()
    stdscr.clear()
    rows, cols = stdscr.getmaxyx()
    
    subpad = stdscr.subpad(rows-1, cols, 0, 0)
    subpad.scrollok(True)

    stdscr.keypad(True)
    stdscr.refresh()
    stdscr.nodelay(True)
    history = []
    chars = ""
    while 1:
        rows, cols = stdscr.getmaxyx()
        stdscr.move(rows-1, 0)
        
        stdscr.addstr("> ")
        move_cursor(stdscr, chars)
        
        char = stdscr.getch()
        if char in (10, curses.KEY_ENTER):
            history.append(chars)
            # run command
            chars = ""
            move_cursor(stdscr, chars)
            stdscr.clrtoeol()
        elif char in (127, curses.KEY_BACKSPACE):
            chars = chars[:-1]
            move_cursor(stdscr, chars)
            stdscr.clrtoeol()
        elif char in (258, curses.KEY_DOWN):
            pass
        elif char in (259, curses.KEY_UP):
            pass
        elif char in (260, curses.KEY_LEFT):
            stdscr.move(rows-1, 0)
            stdscr.refresh()
        else:
            if char < 0:
                continue
            curses.ungetch(char)
            try:
                char = stdscr.get_wch()
            except Exception:
                pass

        if type(char) == str and char.isprintable() and char:
            stdscr.addstr(char)
            chars += char
            subpad.addstr(char.encode("utf-8").hex() + " ")
            # subwin.addstr(char)
            subpad.refresh()
            
        elif type(char) == int and char > 0:
            subpad.addstr(str(char) + " ")
        
        # stdscr.clrtoeol()
        
        # if char == 10:
        #     stdscr.clrtoeol()
        #     chars = ""
        # if char == 127:
        #     chars = chars[:-1]
        # subwin.refresh()






if __name__ == "__main__":
    curses.wrapper(main)