import tkinter as tk
from tkinter import ttk
from constants import paddings

from services.wordy_api import WordyApi
from utils.text_field_utils import TextFieldUtils
from views.interfaces.i_screen import IView
from views.interfaces.i_views_manager import IViewsManager


class EditScreen(ttk.Frame, IView):
    def __init__(
        self, master: tk.Misc, api: WordyApi, views_manager: IViewsManager
    ) -> None:
        super().__init__(master)
        self.api = api
        self.views_manager = views_manager

    def edit(self):
        result = self.api.update(
            self.entry_word.get(),
            self.text_meanings.get(1.0, tk.END),
            self.entry_see_also.get(),
        )
        print(result)

    def go_to_search_screen(self):
        self.pack_forget()
        self.views_manager.search_screen.build()

    def build(self):
        self.entry_word = tk.Entry(self, width=40)
        self.entry_see_also = tk.Entry(self, width=26)
        self.frame_meanings = ttk.Frame(self)
        self.scollbar_meanings = ttk.Scrollbar(self.frame_meanings)
        self.text_meanings = tk.Text(
            self.frame_meanings,
            height=17,
            width=58,
            wrap=tk.WORD,
            yscrollcommand=self.scollbar_meanings.set,
        )
        self.scollbar_meanings.config(command=self.text_meanings.yview)
        self.scollbar_meanings.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_meanings.pack(side="left")

        self.button_back = ttk.Button(
            self, text="Back", command=self.go_to_search_screen
        )
        self.button_edit = ttk.Button(self, text="Edit", command=self.edit)

        TextFieldUtils.enable_ctrl_a_select(self.entry_word)
        TextFieldUtils.add_place_holder(self.entry_word, "Enter Word")
        TextFieldUtils.add_place_holder(self.entry_see_also, "See Also")
        TextFieldUtils.add_place_holder(
            self.text_meanings, "Enter meanings, separated by blank lines", True
        )

        self.entry_word.grid(row=0, column=0, ipady=3, pady=paddings.TOP, sticky="w")
        self.entry_see_also.grid(
            row=0, column=1, columnspan=6, ipady=3, pady=paddings.TOP, sticky="e"
        )
        self.frame_meanings.grid(row=1, column=0, columnspan=7, pady=paddings.MID)
        self.button_back.grid(row=2, column=5, pady=paddings.BOTTOM, sticky="e")
        self.button_edit.grid(row=2, column=6, pady=paddings.BOTTOM, sticky="e")

        self.pack()
