from view import ViewController
from canvas import Canvas
# For input
import tty
import sys
import termios


class Controller:
    """Controls views and user input"""
    def __init__(self):
        self.canvas = Canvas(20, 10)
        self.view_controller = ViewController(self.canvas)

        # Possible values:
        #  NORMAL - You can move cursor(WSAD, Arrows, HJKL)
        #           and change mode to another
        #  INSERT - You can change chars and move using Arrows
        self.mode = "NORMAl"

    def start(self):
        """Initialize necessary stuff and start main program loop"""
        self.main_loop()

    def main_loop(self):
        # Normal mode
        while True:
            self.view_controller.draw()

            sign = Controller.get_input()
            sign.lower()
            if sign == "q":
                return
            elif sign in ("a", "s", "d", "w"):
                if sign == "a":
                    self.canvas.move_cursor_left()
                elif sign == "d":
                    self.canvas.move_cursor_right()
                elif sign == "s":
                    self.canvas.move_cursor_down()
                elif sign == "w":
                    self.canvas.move_cursor_up()
            elif sign == "i":
                self.insert_mode_loop()

    def insert_mode_loop(self):
        while True:
            self.view_controller.draw()

            sign = Controller.get_input()
            if sign == "\x7f":
                return
            elif sign == "\x1b":
                self.get_input()
                sign = self.get_input()
                if sign == "D":
                    self.canvas.move_cursor_left()
                elif sign == "C":
                    self.canvas.move_cursor_right()
                elif sign == "B":
                    self.canvas.move_cursor_down()
                elif sign == "A":
                    self.canvas.move_cursor_up()
            else:
                self.canvas.set_char(sign)

    @staticmethod
    def get_input() -> str:
        file_descriptor = sys.stdin.fileno()
        settings = termios.tcgetattr(file_descriptor)

        tty.setraw(file_descriptor)
        sign = sys.stdin.read(1)
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, settings)

        return sign
