class StateController:
    """Static class that holds important informantions like current mode"""

    # Possible values:
    #  NORMAL - You can move cursor(Arrows)
    #           and change mode to another
    #  INSERT - You can change chars and move using Arrows
    _mode = "COMMAND"
    # LINUX/WINDOWS?
    _system = ""

    @classmethod
    def set_mode(cls, mode: str):
        cls._mode = mode

    @classmethod
    def get_mode(cls) -> str:
        return cls._mode

    @classmethod
    def set_system(cls, system: str):
        cls._system = system

    @classmethod
    def get_system(cls) -> str:
        return cls._system
