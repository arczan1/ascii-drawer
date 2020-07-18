class Canvas:
    """
        Representation of ASCII art image
    """

    def __init__(self, width: int, height: int):
        """
        :param width: ASCII image width
        :param height: ASCII image height
        """
        self.width = width
        self.height = height
        self.cursor = {"x": 0, "y": 0}

        # Initialize empty board
        self._board = [[" " for _ in range(width)] for _ in range(height)]

    def set_char(self, char: str):
        """Set sign at cursor position

        :param char: New sign
        """
        self._board[self.cursor["y"]][self.cursor["x"]] = char

    def get_char(self, x: int, y: int) -> str:
        """Return sign at (x, y)

        :param x: From 0 to (width-1)
        :param y: From 0 to (height-1)
        :return: Sign at (x, y)
        """
        if self.is_inside(x, y):
            return self._board[y][x]
        else:
            return " "

    def is_inside(self, x: int, y: int) -> bool:
        """Check if point(x, y) is inside canvas coordinates

        :param x: From 0 to (width-1)
        :param y: From 0 to (height-1)
        :return: If (x, y) is inside image
        """
        if x < 0 or y < 0:
            return False
        if x >= self.width or y >= self.height:
            return False
        return True

    def __iter__(self):
        self.iter_num = -1
        return self

    def __next__(self):
        self.iter_num += 1
        if self.iter_num >= self.height:
            raise StopIteration
        return self._board[self.iter_num][:]

    def move_cursor_to(self, x: int, y: int):
        """Move cursor to (x, y)

        :param x: From 0 to (width-1)
        :param y: From 0 to (height-1)
        """
        if self.is_inside(x, y):
            self.cursor["x"] = x
            self.cursor["y"] = y

    def move_cursor_right(self):
        self.move_cursor_to(self.cursor["x"]+1, self.cursor["y"])

    def move_cursor_left(self):
        self.move_cursor_to(self.cursor["x"]-1, self.cursor["y"])

    def move_cursor_up(self):
        self.move_cursor_to(self.cursor["x"], self.cursor["y"]-1)

    def move_cursor_down(self):
        self.move_cursor_to(self.cursor["x"], self.cursor["y"]+1)
