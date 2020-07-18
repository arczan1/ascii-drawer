from canvas import Canvas


class Frame:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self._screen = [[" " for _ in range(width)]
                        for _ in range(height)]

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
        frame.add_line_at(self.x, self.y+1, list("q - EXIT"))
        frame.add_line_at(self.x, self.y+2, list("i - INSERT mode"))
        frame.add_line_at(self.x, self.y+3, list("Backspace -"))
        frame.add_line_at(self.x, self.y+4, list("  Normal mode"))


class ModeView(View):
    """Draw current mode on the frame"""
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def draw(self, frame: Frame):
        frame.add_line_at(self.x, self.y, list("MODE:"))
        frame.add_line_at(self.x, self.y+1, list(""))


class ViewController:
    """Controls other views and draw border"""
    def __init__(self, canvas: Canvas):
        self.canvas = canvas
        self.canvas_view = CanvasView(canvas, 1, 1)
        self.control_view = ControlView(canvas.width+2, 1)
        self.mode_view = ModeView(canvas.width+2, canvas.height-1)

    def draw(self):
        """Draw canvas and borders on a frame and displays it"""
        # Create new frame
        frame = Frame(self.canvas.width+2+20, self.canvas.height+2)

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
        # Top and bottom
        frame.add_line_at(1, 0, ["-" for _ in range(self.canvas.width)])
        frame.add_line_at(1, self.canvas.height+1,
                          ["-" for _ in range(self.canvas.width)])

        frame.add_line_at(self.canvas.width+1, 0, ["-" for _ in range(20)])
        frame.add_line_at(self.canvas.width+1, self.canvas.height+1,
                          ["-" for _ in range(20)])
        frame.add_line_at(self.canvas.width+1, self.canvas.height-2,
                          ["-" for _ in range(20)])

        # Corners
        frame.add_char_at(0, 0, "+")
        frame.add_char_at(0, self.canvas.height+1, "+")
        frame.add_char_at(self.canvas.width+1, 0, "+")
        frame.add_char_at(self.canvas.width+1, self.canvas.height+1, "+")
        frame.add_char_at(frame.width-1, 0, "+")
        frame.add_char_at(frame.width-1, frame.height-1, "+")

        # Left and right
        for y in range(1, self.canvas.height+1):
            frame.add_char_at(0, y, "|")
            frame.add_char_at(self.canvas.width+1, y, "|")
            frame.add_char_at(frame.width-1, y, "|")
