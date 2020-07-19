from view import ViewController
from state_controller import StateController
from canvas import Canvas
# For input
import tty
import sys
import termios


class Controller:
    """Controls views and user input"""
    def __init__(self, path_to_file: str):
        image = self.load_image(path_to_file)
        self.path_to_file = path_to_file
        self.canvas = Canvas(10, 10, image)
        self.view_controller = ViewController(self.canvas)

    def start(self):
        """Initialize necessary stuff and start main program loop"""
        self.main_loop()

    def main_loop(self):
        # COMMAND mode
        while True:
            self.view_controller.draw()

            sign = Controller.get_input()
            sign.lower()
            if sign == "q":
                return
            elif sign == "\x1b":  # Arrow
                self.get_input()  # Skip "["
                sign = self.get_input()
                if sign == "D":
                    self.canvas.move_cursor_left()
                elif sign == "C":
                    self.canvas.move_cursor_right()
                elif sign == "B":
                    self.canvas.move_cursor_down()
                elif sign == "A":
                    self.canvas.move_cursor_up()
            elif sign == "i":
                self.insert_mode_loop()
            elif sign == "s":
                self.save_image()

    def insert_mode_loop(self):
        StateController.set_mode("INSERT")

        while True:
            self.view_controller.draw()

            sign = Controller.get_input()
            if sign == "\x7f":  # Backspace
                StateController.set_mode("COMMAND")
                return  # Return to COMMAND mode
            elif sign == "\x1b":  # Arrow
                self.get_input()  # Skip "["
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
        """Read one char from user input

        :return: Single sign from input
        """
        # Read terminal settings
        file_descriptor = sys.stdin.fileno()
        settings = termios.tcgetattr(file_descriptor)

        # Set terminal mode
        tty.setraw(file_descriptor)

        # Read char
        sign = sys.stdin.read(1)

        # Restore old settings
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, settings)

        return sign

    def load_image(self, path: str) -> list:
        """Read content of file and returns it as 2-dimensional list

        :param path: Path to file(relative or absolute)
        :return: Content of file as 2-dimensional list
        """
        content = ""
        with open(path, "r") as file:
            content = file.read()

        # Split file content to separated rows
        lines = content.split("\n")

        # Convert string lines to lists
        image = [list(line) for line in lines]
        # Remove empty rows
        image = list(filter(None, image))

        return image

    def save_image(self):
        """Saves current image to file provided when running program

        TODO:
            Add Exceptions handling(e.g. Permission denied)
        """
        with open(self.path_to_file, "w") as file:
            for line in self.canvas:
                file.write("".join(line))
                file.write("\n")
