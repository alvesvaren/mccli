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
    def __init__(self, scr: Window, prefix="> "):
        curses.cbreak()
        curses.use_default_colors()

        self.main = scr
        self.prefix = prefix
        self.cursor_index = 0
        self.line = ""
        self.history = [""]
        self.rows, self.cols = scr.getmaxyx()
        self.history_index = len(self.history)
        self.main.keypad(True)
        self.main.nodelay(True)

        self.sub = self.main.subpad(self.rows - 1, self.cols, 0, 0)
        self.sub.scrollok(True)
        self.main.clear()
        self.main.refresh()

    def move_cursor(self, index=None):
        if not index is None:
            self.cursor_index = index
        if self.cursor_index < 0:
            self.cursor_index = 0
        if self.cursor_index > len(self.line):
            self.cursor_index = len(self.line)
        self.main.move(self.rows - 1, self.cursor_index + len(self.prefix))

    def update(self):
        self.rows, self.cols = self.main.getmaxyx()
        self.main.move(self.rows - 1, 0)
        self.main.clrtoeol()
        self.main.addstr("> " + self.line)
        self.move_cursor()

        char = self.main.getch()
        if char in (10, curses.KEY_ENTER):
            self.history_index += 1
            self.sub.addstr(self.line)
            self.sub.refresh()
            self.line = ""
            self.history.append(self.line)
            move_cursor(self.main, self.line)
            self.main.clrtoeol()
        elif char in (127, curses.KEY_BACKSPACE):
            self.line = self.line[:self.cursor_index - 1] + \
                self.line[self.cursor_index:]
            self.cursor_index -= 1
            self.move_cursor()
            self.main.clrtoeol()
        elif char in (330, curses.KEY_DC):
            self.line = self.line[:self.cursor_index] + \
                self.line[self.cursor_index + 1:]
        elif char in (258, curses.KEY_DOWN):
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
                self.line = self.history[self.history_index]
            if self.history == len(self.history) - 1:
                self.line = ""
        elif char in (259, curses.KEY_UP):
            if self.history_index > 0:
                self.history_index -= 1
                self.line = self.history[self.history_index]
        elif char in (260, curses.KEY_LEFT):
            self.cursor_index -= 1
            self.move_cursor()
        elif char in (261, curses.KEY_RIGHT):
            self.cursor_index += 1
            self.move_cursor()
        elif char in (546,):  # CTRL + LEFT
            proposed_index = self.line[::-1].find(
                " ", len(self.line) - self.cursor_index + 1)
            if proposed_index > 0:
                self.cursor_index = len(self.line) - proposed_index
            else:
                self.cursor_index = 0
            self.move_cursor()
        elif char in (561,):  # CTRL + RIGHT
            proposed_index = self.line.find(" ", self.cursor_index + 1)
            if proposed_index > 0:
                self.cursor_index = proposed_index + 1
            else:
                self.cursor_index = len(self.line)
            self.move_cursor()
        elif char in (360, curses.KEY_END):
            self.move_cursor(len(self.line))
        elif char in (262, curses.KEY_HOME):
            self.move_cursor(0)

        else:
            if char < 0:
                return
            curses.ungetch(char)
            try:
                char = self.main.get_wch()
            except Exception:
                pass
            if type(char) == str:
                self.line = self.line[:self.cursor_index] + \
                    char + self.line[self.cursor_index:]
                self.main.addstr(char)
                self.cursor_index += 1
            else:
                self.sub.addstr(str(char) + " ")
                self.sub.refresh()


def main(stdscr: Window):
    screen = CurseState(stdscr)
    while 1:
        screen.update()


if __name__ == "__main__":
    curses.wrapper(main)
