import subprocess
import tkinter as tk


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("Network Manager GUI")
        self.resizable(False, False)
        self.gui()
        self.mainloop()

    def btnRefresh_Event(self):
        self.__lstAll.delete(0, tk.END)
        process1 = subprocess.Popen(["nmcli" ,"-f", "SSID", "device", "wifi"], stdout=subprocess.PIPE)
        process2 = subprocess.Popen(["sed", "1d"], stdin=process1.stdout, stdout=subprocess.PIPE)
        while True:
            line = process2.stdout.readline()
            if line != b'':
                self.__lstAll.insert(tk.END, line.rstrip())
            else:
                break

    def btnConnect_Event(self):
        name = self.__entryName.get().strip()
        password = self.__entryPassword.get().strip()
        if password == "":
            subprocess.run(["nmcli", "device", "wifi", "connect", name])
        else:
            subprocess.run(["nmcli", "device", "wifi", "connect", name, "password", password])

    def gui(self):
        self.__btnRefresh = tk.Button(self, text="Refresh", command=lambda: self.btnRefresh_Event())
        self.__frameLst = tk.Frame(self)
        self.__lstAll = tk.Listbox(self.__frameLst)
        self.__scrollBar = tk.Scrollbar(self.__frameLst)
        self.__entryName = tk.Entry(self)
        self.__entryPassword = tk.Entry(self, show="*")
        self.__btnConnect = tk.Button(self, text="Connect", command=lambda: self.btnConnect_Event())

        self.__btnRefresh.pack()
        self.__frameLst.pack(side=tk.LEFT, fill=tk.Y)
        self.__lstAll.pack(pady=5, padx=5, side=tk.LEFT, fill=tk.BOTH)
        self.__scrollBar.pack(side=tk.RIGHT, fill=tk.Y)
        self.__entryName.pack(pady=5, padx=5)
        self.__entryPassword.pack(pady=5, padx=5)
        self.__btnConnect.pack(pady=5, padx=5)

        self.__lstAll.config(yscrollcommand=self.__scrollBar.set)
        self.__scrollBar.config(command=self.__lstAll.yview)


if __name__ == "__main__":
    App(className="Network Manager GUI")