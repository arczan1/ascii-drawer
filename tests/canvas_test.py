import unittest
from canvas import Canvas


class TestCanvas(unittest.TestCase):
    def setUp(self):
        self.canvas = Canvas(10, 10)

    def test_is_inside(self):
        self.assertEqual(self.canvas.is_inside(2, 3), True)
        self.assertEqual(self.canvas.is_inside(0, 0), True)
        self.assertEqual(self.canvas.is_inside(9, 9), True)
        self.assertEqual(self.canvas.is_inside(2, 11), False)
        self.assertEqual(self.canvas.is_inside(12, 2), False)
        self.assertEqual(self.canvas.is_inside(-1, 3), False)

    def test_set_char(self):
        pass
        # self.canvas.set_char(3, 9, "p")
        # self.assertEqual(self.canvas.get_char(3, 9), "p", "")
        # self.canvas.set_char(5, 3, "3")
        # self.assertEqual(self.canvas.get_char(5, 3), "3", "")

    def test_move_cursor_to(self):
        pass


if __name__ == "__main__":
    unittest.main()
