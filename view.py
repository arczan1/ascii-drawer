from canvas import Canvas
from state_controller import StateController


class Frame:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        # Fill frame with " "
        self._screen = [[" " for _ in range(width)] for _ in range(height)]

    def is_inside(self, x: int, y: int) -> bool:
        """Check if point(x, y) is inside frame coordinates

        :param x: From 0 to (width-1)
        :param y: From 0 to (height-1)
        :return: If (x, y) is inside frame
        """
        if x < 0 or y < 0:
            return False
        if x >= self.width or y >= self.height:
            return False
        return True

    def add_line_at(self, x: int, y: int, line: list):
        if self.is_inside(x, y) and self.is_inside(x+len(line), y):
            self._screen[y][x:x+len(line)] = line[:]

    def add_char_at(self, x: int, y: int, char: str):
        if self.is_inside(x, y):
            self._screen[y][x] = char

    def display(self):
        """Display frame on the screen"""
        # Move cursor to top left corner
        print("\033[1;1H", end="")
        for row in self._screen:
            print("".join(row))


class View:
    """Base class for all View Class"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def draw(self, frame: Frame):
        """Should be overwrite"""
        pass


class CanvasView(View):
    """Draw canvas on the frame"""

    def __init__(self, canvas: Canvas, x: int, y: int):
        super().__init__(x, y)
        self.canvas = canvas

    def draw(self, frame: Frame):
        for i, row in enumerate(self.canvas):
            frame.add_line_at(self.x, self.y+i, row)


class ControlView(View):
    """Draw controls on the frame"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def draw(self, frame: Frame):
        frame.add_line_at(self.x, self.y, list("Controls:"))
        if StateController.get_mode() == "COMMAND":
            frame.add_line_at(self.x, self.y+1, list("q: EXIT"))
            frame.add_line_at(self.x, self.y+2, list("i: INSERT mode"))
            frame.add_line_at(self.x, self.y+3, list("s: SAVE"))
            frame.add_line_at(self.x, self.y+4, list("S: SAVE AS"))
        elif StateController.get_mode() == "INSERT":
            frame.add_line_at(self.x, self.y+1, list("Backspace: "))
            frame.add_line_at(self.x, self.y+2, list(" COMMAND mode"))
            frame.add_line_at(self.x, self.y+3, list("OTHER: insert char"))


class TextBoxView(View):
    """Draw text on the frame"""
    def __init__(self, x: int, y: int, width: int, height: int):
        super().__init__(x, y)
        self.width = width
        self.height = height

    def draw(self, text: str):
        pass


class ModeView(View):
    """Draw current mode on the frame"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def draw(self, frame: Frame):
        frame.add_line_at(self.x, self.y, list("MODE:"))
        frame.add_line_at(self.x, self.y+1, list(StateController.get_mode()))


class ViewController:
    """Controls other views and draw border"""
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.canvas_view = CanvasView(canvas, 1, 1)
        self.control_view = ControlView(canvas.width+2, 1)
        mode_y = canvas.height
        if mode_y < 10:
            mode_y = 8
        self.mode_view = ModeView(canvas.width+2, mode_y-1)

    def draw(self):
        """Draw canvas and borders on a frame and displays it"""
        # Create new frame
        frame_height = self.canvas.height+2
        # Min frame height is 10
        if frame_height < 10:
            frame_height = 10
        frame = Frame(self.canvas.width+2+20, frame_height)

        # Border
        self.draw_border(frame)
        # Canvas
        self.canvas_view.draw(frame)
        # Control
        self.control_view.draw(frame)
        # Mode
        self.mode_view.draw(frame)

        # Cursor
        cursor_icon = "\033[47m\033[30m{}\033[37m\033[40m".format(
            self.canvas.get_char(**self.canvas.cursor))
        frame.add_char_at(self.canvas.cursor["x"]+1, self.canvas.cursor["y"]+1,
                          cursor_icon)

        # Display final frame
        frame.display()

    def draw_border(self, frame: Frame):
        """Draw borders on frame

        :param frame: Frame object to draw on

        TODO:
            Simplify code
        """
        # Top and bottom
        frame.add_line_at(1, 0, ["-" for _ in range(self.canvas.width)])
        frame.add_line_at(1, self.canvas.height+1,
                          ["-" for _ in range(self.canvas.width)])

        frame.add_line_at(self.canvas.width+1, 0, ["-" for _ in range(20)])
        frame.add_line_at(self.canvas.width+1, frame.height-4,
                          ["-" for _ in range(20)])
        frame.add_line_at(self.canvas.width+2, frame.height-1,
                          ["-" for _ in range(19)])

        # Left and right
        for y in range(1, self.canvas.height+1):
            frame.add_char_at(0, y, "|")

        for y in range(1, frame.height-1):
            frame.add_char_at(self.canvas.width+1, y, "|")
            frame.add_char_at(frame.width-1, y, "|")

        # Corners
        frame.add_char_at(0, 0, "+")
        frame.add_char_at(0, self.canvas.height+1, "+")
        frame.add_char_at(self.canvas.width+1, 0, "+")
        frame.add_char_at(self.canvas.width+1, self.canvas.height+1, "+")
        frame.add_char_at(frame.width-1, 0, "+")
        frame.add_char_at(frame.width-1, frame.height-1, "+")
        frame.add_char_at(self.canvas.width+1, frame.height-1, "+")
