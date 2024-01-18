import mttkinter as ignorable_import  # IGNORE

import tkinter as tk
from tkinter import messagebox
from services.wordy_api import WordyApi

from constants import paddings as paddings
from views.add_screen import AddScreen
from views.edit_screen import EditScreen
from views.interfaces.i_views_manager import IViewsManager
from views.load_screen import LoadScreen
from views.search_screen import SearchScreen


class WordyGui(tk.Tk, IViewsManager):
    def __init__(self):
        super().__init__()
        self.api = WordyApi()
        self.title("Wordy")
        self.geometry("555x380")
        self.resizable(False, False)

        self.load_screen = LoadScreen(
            master=self,
            api=self.api,
            views_manager=self,
        )
        self.search_screen = SearchScreen(
            master=self,
            api=self.api,
            views_manager=self,
        )
        self.add_screen = AddScreen(
            master=self,
            api=self.api,
            views_manager=self,
        )
        self.edit_screen = EditScreen(
            master=self,
            api=self.api,
            views_manager=self,
        )

    def build(self):
        self.load_screen.build()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.mainloop()

    def on_closing(self):
        if self.api.are_unsaved_changes:
            save_changes = messagebox.askyesnocancel(
                "Save Changes", "Do you want to save the changes?"
            )
            if save_changes is None:
                return
            if save_changes:
                self.api.save_changes()
        self.destroy()
