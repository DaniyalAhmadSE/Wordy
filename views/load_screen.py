import tkinter as tk
from tkinter import ttk

from services.wordy_api import WordyApi
from views.interfaces.i_views_manager import IViewsManager
from views.interfaces.i_screen import IView


class LoadScreen(ttk.Frame, IView):
    def __init__(
        self,
        master: tk.Tk,
        api: WordyApi,
        views_manager: IViewsManager,
    ) -> None:
        super().__init__(master)
        self.api = api
        self.views_manager = views_manager

    def load_with_animation(self):
        self.api.start_thread(self.progress_bar, self.label_load)
        # Waiting till the Loading Completes
        while self.progress_bar.cget("value") < 100:
            self.update()

    def go_to_search_screen(self):
        self.x = self.master
        self.pack_forget()
        self.views_manager.search_screen.build()

    def build(self):
        self.label_wordy = ttk.Label(
            self,
            text="WORDY",
            font=("Rachana", 50, "bold"),
            foreground="#1A5276",
            justify="center",
        )
        self.label_line = ttk.Label(
            self,
            text="The Dictionary You Need",
            font=("Rachana", 16),
            foreground="#1A5276",
        )
        self.progress_bar = ttk.Progressbar(self, orient=tk.HORIZONTAL, length=300)
        self.label_load = ttk.Label(
            self,
            text="Loading",
            font=("Rachana", 12),
            foreground="#1A5276",
        )

        self.label_wordy.pack()
        self.label_line.pack()
        self.progress_bar.pack(pady=10)
        self.label_load.pack()

        self.pack(expand=1)

        self.load_with_animation()
        self.go_to_search_screen()
