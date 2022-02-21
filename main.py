# MIT License
#
# Copyright (c) 2022 Egor Bronnikov
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import tkinter as tk
from tkinter import messagebox
import subprocess as sp


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        """ Class that creates the `root` window

            :param args: all `args` options that has `tkinter.Tk`
            :param kwargs: all `kwargs` options that has `tkinter.Tk`

            :return: `side effect`: creates a window
            :rtype: None
        """
        super().__init__(*args, **kwargs)

        self.title("NetworkManager")
        self.geometry("350x360")
        self.resizable(False, False)
        self.gui()
        self.btnRefresh_Event()
        self.selectItem()
        self.bind("<<ListboxSelect>>", lambda event: self.chooseItem())
        self.mainloop()

    @staticmethod
    def message(err, out):
        """ Informs the user about connection status

            :param err: message `stderr` after run subprocess
            :type err: ByteString
            :param out: message `stdout` after run subprocess
            :type out: ByteString

            :return: `side effect`: creates messagebox with output information
            :rtype: None
        """
        if b"Error" in out or b"Error" in err:
            messagebox.showerror("Error", err + out)
        else:
            messagebox.showinfo("Information", out.decode("ASCII").strip())

    def chooseItem(self):
        """ Insert the SSID of the selected item in the list in entry

            :return: `side effect`: insert SSID in entry
            :rtype: None
        """
        self._entryName.delete(0, tk.END)
        self._entryName.insert(tk.END, self._lstAll.get(tk.ACTIVE))

    def selectItem(self):
        """ Event for a bind to change a list item

            :return: `side effect`: change selected item
            :rtype: None
        """
        self._lstAll.select_set(0)
        self._lstAll.focus_set()
        self.chooseItem()

    def btnRefresh_Event(self):
        """ Button event for `btnRefresh`

            :return: `side effect`: button event
            :rtype: None
        """
        self._lstAll.delete(0, tk.END)
        processNM = sp.Popen(["nmcli", "-f", "SSID", "device", "wifi"], stdout=sp.PIPE)
        processCut = sp.Popen(["sed", "1d"], stdin=processNM.stdout, stdout=sp.PIPE)
        while True:
            line = processCut.stdout.readline()
            if line != b'':
                self._lstAll.insert(tk.END, line.rstrip())
            else:
                break
        self.selectItem()

    def btnConnect_Event(self):
        """ Button event for `btnConnect`

            :return: `side effect`: button event
            :rtype: None
        """
        name = self._entryName.get().strip()
        password = self._entryPassword.get().strip()
        if password == "":
            proc = sp.Popen(["nmcli", "device", "wifi", "connect", name], stdout=sp.PIPE, stderr=sp.PIPE)
        else:
            proc = sp.Popen(["nmcli", "device", "wifi", "connect", name, "password", password], stdout=sp.PIPE, stderr=sp.PIPE)
        res = proc.communicate()
        out = res[0]
        err = res[1]
        self.message(err, out)

    def btnDisconnect_Event(self):
        """ Button event for `btnDisconnect`

            :return: `side effect`: button event
            :rtype: None
        """
        procIW = sp.Popen(["iw", "dev"], stdout=sp.PIPE)
        procGrep = sp.Popen(["grep", "Interface"], stdin=procIW.stdout, stdout=sp.PIPE)
        procInterface = sp.Popen(["cut", "-d", " ", "-f", "2"], stdin=procGrep.stdout, stdout=sp.PIPE)
        interface = procInterface.communicate()[0]
        procDisconnect = sp.Popen(["nmcli", "device", "disconnect", interface.decode("ASCII").strip()], stdout=sp.PIPE, stderr=sp.PIPE)
        res = procDisconnect.communicate()
        out = res[0]
        err = res[1]
        self.message(err, out)

    def btnClose_Event(self):
        """ Button event for `btnClose`

            :return: `side effect`: button event
            :rtype: None
        """
        self.destroy()

    def checkBoxPass_Event(self):
        """ Checkbox event for `chackBoxPass`

            :return: `side effect`: checkbox event
            :rtype: None
        """
        if self.__var.get() == 0:
            self._entryPassword.config(show="*")
        else:
            self._entryPassword.config(show="")

    def gui(self):
        """ Renders graphics primitives

            :return: `side effect`: render GUI
            :rtype: None
        """
        # Creation
        self._lblMain = tk.Label(self, text="NetworkManager", font=("Arial", 25))
        self._btnRefresh = tk.Button(self, text="Refresh", command=lambda: self.btnRefresh_Event())
        self._frameLst = tk.Frame(self)
        self._lstAll = tk.Listbox(self._frameLst)
        self._scrollBar = tk.Scrollbar(self._frameLst)
        self._lblName = tk.Label(self, text="SSID", font=("Arial", 10))
        self._entryName = tk.Entry(self)
        self._lblPassword = tk.Label(self, text="Password", font=("Arial", 10))
        self._entryPassword = tk.Entry(self, show="*")
        self._btnConnect = tk.Button(self, text="Connect", command=lambda: self.btnConnect_Event())
        self._var = tk.IntVar()
        self._checkBoxPass = tk.Checkbutton(self, text="Show password", variable=self._var, onvalue=1, offvalue=0, command=lambda: self.checkBoxPass_Event())
        self._btnDisconnect = tk.Button(self, text="Disconnect", command=lambda: self.btnDisconnect_Event())
        self._btnExit = tk.Button(self, text="Exit", command=lambda: self.btnClose_Event())

        # Packing
        self._lblMain.pack(padx=10, pady=10)
        self._btnRefresh.pack(anchor=tk.W, padx=5, pady=5)
        self._frameLst.pack(side=tk.LEFT, fill=tk.Y)
        self._lstAll.pack(pady=5, padx=5, side=tk.LEFT, fill=tk.BOTH)
        self._scrollBar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self._lblName.pack(anchor=tk.W, padx=5)
        self._entryName.pack(pady=5, padx=5)
        self._lblPassword.pack(anchor=tk.W, padx=5)
        self._entryPassword.pack(pady=5, padx=5)
        self._checkBoxPass.pack(anchor=tk.W)
        self._btnConnect.pack(pady=5, padx=5)
        self._btnDisconnect.pack(pady=10, padx=5)
        self._btnExit.pack(pady=20)

        self._lstAll.config(yscrollcommand=self._scrollBar.set)
        self._scrollBar.config(command=self._lstAll.yview)


if __name__ == "__main__":
    App(className="NetworkManager")
