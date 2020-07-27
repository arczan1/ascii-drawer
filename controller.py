from getkey import getkey, keys

from view import ViewController
from state_controller import StateController
from canvas import Canvas


class Controller:
    """Controls views and user input"""
    def __init__(self, width=10, height=10, path_to_file=None):
        if path_to_file is not None:
            # Create canvas with loaded image
            image = self.load_image(path_to_file)
            self.canvas = Canvas(image=image)
        else:
            # Create empty canvas
            self.canvas = Canvas(width, height)
        self.path_to_file = path_to_file
        self.view_controller = ViewController(self.canvas)

    def start(self):
        """Initialize necessary stuff and start main program loop"""
        self.main_loop()

    def main_loop(self):
        # COMMAND mode
        while True:
            self.view_controller.draw()

            # sign = Controller.get_input()
            # sign.lower()
            key = getkey()
            if key == keys.ESC:
                return
            elif key in (keys.UP, keys.DOWN, keys.RIGHT, keys.LEFT):  # Arrow
                if key == keys.LEFT:
                    self.canvas.move_cursor_left()
                elif key == keys.RIGHT:
                    self.canvas.move_cursor_right()
                elif key == keys.DOWN:
                    self.canvas.move_cursor_down()
                elif key == keys.UP:
                    self.canvas.move_cursor_up()
            elif key == "i":
                self.insert_mode_loop()
            elif key == "s":
                self.save_image()

    def insert_mode_loop(self):
        StateController.set_mode("INSERT")

        while True:
            self.view_controller.draw()

            key = getkey()
            if key == keys.ESC:
                StateController.set_mode("COMMAND")
                return  # Return to COMMAND mode
            elif key in (keys.UP, keys.DOWN, keys.RIGHT, keys.LEFT):  # Arrow
                if key == keys.LEFT:
                    self.canvas.move_cursor_left()
                elif key == keys.RIGHT:
                    self.canvas.move_cursor_right()
                elif key == keys.DOWN:
                    self.canvas.move_cursor_down()
                elif key == keys.UP:
                    self.canvas.move_cursor_up()
            else:
                self.canvas.set_char(key)

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
