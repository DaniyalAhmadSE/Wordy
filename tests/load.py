import time
import threading
import tkinter as tk
from tkinter.ttk import Progressbar


class TkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.progress = Progressbar()
        threading.Thread(target=self.db).start()

    def db(self):
        self.progress.grid(row=1, column=0)
        self.progress.start()
        time.sleep(5)  # do something with DB
        self.progress.stop()
        self.progress.grid_forget()


app = TkApp()
app.mainloop()
