import subprocess as sp
import tkinter as tk
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("NetworkManager")
        self.geometry("350x360")
        self.resizable(False, False)
        self.gui()
        self.btnRefresh_Event()
        self.select()
        self.bind("<<ListboxSelect>>", lambda event: self.choose())
        self.mainloop()

    def choose(self):
        self.__entryName.delete(0, tk.END)
        self.__entryName.insert(tk.END, self.__lstAll.get(tk.ACTIVE))

    def select(self):
        self.__lstAll.select_set(0)
        self.__lstAll.focus_set()
        self.choose()

    def btnRefresh_Event(self):
        self.__lstAll.delete(0, tk.END)
        processNM = sp.Popen(["nmcli", "-f", "SSID", "device", "wifi"], stdout=sp.PIPE)
        processCut = sp.Popen(["sed", "1d"], stdin=processNM.stdout, stdout=sp.PIPE)
        while True:
            line = processCut.stdout.readline()
            if line != b'':
                self.__lstAll.insert(tk.END, line.rstrip())
            else:
                break
        self.select()

    @staticmethod
    def message(err, out):
        if b"Error" in out or b"Error" in err:
            messagebox.showerror("Error", err + out)
        else:
            messagebox.showinfo("Information", out.decode("ASCII").strip())

    def btnConnect_Event(self):
        name = self.__entryName.get().strip()
        password = self.__entryPassword.get().strip()
        if password == "":
            proc = sp.Popen(["nmcli", "device", "wifi", "connect", name], stdout=sp.PIPE, stderr=sp.PIPE)
        else:
            proc = sp.Popen(["nmcli", "device", "wifi", "connect", name, "password", password], stdout=sp.PIPE, stderr=sp.PIPE)
        res = proc.communicate()
        out = res[0]
        err = res[1]
        self.message(err, out)

    def checkBoxPass_Event(self):
        if self.__var.get() == 0:
            self.__entryPassword.config(show="*")
        else:
            self.__entryPassword.config(show="")

    def btnDisconnect_Event(self):
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
        self.destroy()

    def gui(self):
        self.__lblMain = tk.Label(self, text="NetworkManager", font=("Arial", 25))
        self.__btnRefresh = tk.Button(self, text="Refresh", command=lambda: self.btnRefresh_Event())
        self.__frameLst = tk.Frame(self)
        self.__lstAll = tk.Listbox(self.__frameLst)
        self.__scrollBar = tk.Scrollbar(self.__frameLst)
        self.__lblName = tk.Label(self, text="SSID", font=("Arial", 10))
        self.__entryName = tk.Entry(self)
        self.__lblPassword = tk.Label(self, text="Password", font=("Arial", 10))
        self.__entryPassword = tk.Entry(self, show="*")
        self.__btnConnect = tk.Button(self, text="Connect", command=lambda: self.btnConnect_Event())
        self.__var = tk.IntVar()
        self.__checkBoxPass = tk.Checkbutton(self, text="Show password", variable=self.__var, onvalue=1, offvalue=0, command=lambda: self.checkBoxPass_Event())
        self.__btnDisconnect = tk.Button(self, text="Disconnect", command=lambda: self.btnDisconnect_Event())
        self.__btnExit = tk.Button(self, text="Exit", command=lambda: self.btnClose_Event())

        self.__lblMain.pack(padx=10, pady=10)
        self.__btnRefresh.pack(anchor=tk.W, padx=5, pady=5)
        self.__frameLst.pack(side=tk.LEFT, fill=tk.Y)
        self.__lstAll.pack(pady=5, padx=5, side=tk.LEFT, fill=tk.BOTH)
        self.__scrollBar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        self.__lblName.pack(anchor=tk.W, padx=5)
        self.__entryName.pack(pady=5, padx=5)
        self.__lblPassword.pack(anchor=tk.W, padx=5)
        self.__entryPassword.pack(pady=5, padx=5)
        self.__checkBoxPass.pack(anchor=tk.W)
        self.__btnConnect.pack(pady=5, padx=5)
        self.__btnDisconnect.pack(pady=10, padx=5)
        self.__btnExit.pack(pady=20)

        self.__lstAll.config(yscrollcommand=self.__scrollBar.set)
        self.__scrollBar.config(command=self.__lstAll.yview)


if __name__ == "__main__":
    App(className="NetworkManager")