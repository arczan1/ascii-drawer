class Canvas:
    """
        Representation of ASCII art image
    """

    def __init__(self, width=10, height=10, image=None):
        """
        :param width: ASCII image width(if image is None)
        :param height: ASCII image height(if image is None)
        :param image: 2-dimensional list of chars
        """
        # Place cursor at (0, 0)
        self.cursor = {"x": 0, "y": 0}

        if image:   # Load image
            # set width equal to length of the longest row
            self.width = len(image[0])
            for row in image:
                if self.width < len(row):
                    self.width = len(row)

            self._board = image.copy()
            self.height = len(image)

            # Add SPACES at the end of rows shorter than self.width
            for row in self._board:
                row += [" " for _ in range(self.width - len(row))]
        else:   # Create empty image
            self.width = width
            self.height = height
            # Initialize empty board
            self._board = [[" " for _ in range(width)] for _ in range(height)]

    def set_char(self, char: str):
        """Set sign at cursor position

        :param char: New sign
        """
        if char not in ("\n", "\t", "\r"):
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
        """Return canvas object ready to iterate over rows

        :return: Canvas object(self)
        """
        self.iter_num = -1
        return self

    def __next__(self):
        """Iterate over rows

        :return: row
        """
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
