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

    def start(self):
        """Initialize necessary stuff and start main program loop"""
        self.view_controller.draw()
        self.main_loop()

    def main_loop(self):
        while True:
            sign = Controller.get_input()
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
            self.view_controller.draw()

    @staticmethod
    def get_input() -> str:
        file_descriptor = sys.stdin.fileno()
        settings = termios.tcgetattr(file_descriptor)

        tty.setraw(file_descriptor)
        sign = sys.stdin.read(1)
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, settings)

        return sign
