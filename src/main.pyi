from tkinter import Tk
from typing import ByteString


class App(Tk):
    def __init__(self, *args, **kwargs) -> None: ...

    @staticmethod
    def message(err: ByteString, out: ByteString) -> None: ...
    def chooseItem(self) -> None: ...
    def selectItem(self) -> None: ...

    def btnRefresh_Event(self) -> None: ...
    def btnConnect_Event(self) -> None: ...
    def btnDisconnect_Event(self) -> None: ...
    def btnClose(self) -> None: ...
    def checkBoxPass_Event(self) -> None: ...
    def gui(self) -> None: ...