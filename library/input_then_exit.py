import os


def input_then_exit(txt: str = "input enter to exit.") -> None:
    input(txt)
    os._exit(0)
