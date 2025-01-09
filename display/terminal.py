# from localconfig.path import CODING_DIR
from blessed import Terminal

APP_TITLE = "Epi-Project[ing]"

term = Terminal()


class Display:
    def __init__(self):
        self.titlebar_text = ""
        self.statusbar_text = ""
        self._display_border()
        self._wait_for_input()

    def _send_update(self, update):
        pass

    def _display_border(self):
        """Display and update titlebar"""
        width = term.width
        title = " " + APP_TITLE + " "
        title_start = (width - len(title)) // 2  # Center position
        title_end = title_start + len(title)
        line = '╔' + '═' * (title_start - 1) + title + '═' * (width - title_end - 1) + '╗'

        with term.location(y=0), term.hidden_cursor():
            print(term.home + term.on_bright_blue + term.clear, end='')
            print(line)
            for y in range(1, term.height-1):
                print(term.move_xy(0, y) + "║" + term.move_x(term.width-1) + "║")

        with term.location(y=term.height-1):
            line = term.on_bright_blue
            line += "╚" + "═"*(term.width-2) + "╝"
            print(line, end="")

    def _wait_for_input(self):
        with term.cbreak(), term.hidden_cursor():
            val = ''
            while val.lower() != 'q':
                val = term.inkey(timeout=3)
                self._handle_key_name(val)

    def _handle_key_name(self, key):
        with term.location(y=1, x=2):
            if not key.name:
                return
            if key.name == 'KEY_UP':
                print("UP")


class DisplayCategory:
    def __init__(self, category):

        pass


class DisplayProject:
    def __init__(self, project):
        pass


# add to IDEAS2.md: sort order (O)
Display()
