import unittest
from state_controller import StateController


class TestStateController(unittest.TestCase):
    def test_get_mode(self):
        self.assertEqual(StateController.get_mode(), StateController._mode,
                         "get_mode() returned wrong value")

    def test_set_mode(self):
        StateController.set_mode("INSERT")
        self.assertEqual("INSERT", StateController._mode,
                         "set_mode() set wrong value")

    def test_get_system(self):
        self.assertEqual(StateController.get_system(), StateController._system,
                         "get_system() returned wrong value")

    def test_set_system(self):
        StateController.set_system("WINDOWS")
        self.assertEqual("WINDOWS", StateController._system,
                         "set_system() set wrong value")
