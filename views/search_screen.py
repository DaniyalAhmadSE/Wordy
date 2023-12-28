import tkinter as tk
from tkinter import ttk
from constants import paddings
from services.wordy_api import WordyApi

from utils.text_field_utils import TextFieldUtils
from views.interfaces.i_views_manager import IViewsManager


class SearchScreen(ttk.Frame):
    def __init__(self, master: "tk.Misc", api: WordyApi, views_manager: IViewsManager):
        super().__init__(master)
        self.api = api
        self.views_manager = views_manager

    def search(self):
        result = self.api.search(self.entry_word.get())
        print(result)
        self.text_meanings.config(state=tk.NORMAL, fg="black")
        self.text_meanings.delete(1.0, tk.END)
        self.text_meanings.insert(tk.END, result)

    def delete(self):
        result = self.api.delete(self.entry_word.get())
        print(result)
        self.entry_word.delete(0, tk.END)
        self.entry_word.event_generate("<FocusOut>")
        self.text_meanings.config(state=tk.NORMAL, fg="black")
        self.text_meanings.delete(1.0, tk.END)
        self.text_meanings.event_generate("<FocusOut>")

    def go_to_add_screen(self):
        self.pack_forget()
        self.views_manager.add_screen.build()

    def go_to_edit_screen(self):
        self.pack_forget()
        self.views_manager.edit_screen.build()

    def build(self):
        self.entry_word = tk.Entry(self, width=57)
        self.button_search = ttk.Button(self, text="Search", command=self.search)

        self.frame_meanings = ttk.Frame(self)
        self.scrollbar_meanings = ttk.Scrollbar(self.frame_meanings)
        self.text_meanings = tk.Text(
            self.frame_meanings,
            height=17,
            width=65,
            wrap=tk.WORD,
            insertontime=0,
            yscrollcommand=self.scrollbar_meanings.set,
        )
        self.scrollbar_meanings.config(command=self.text_meanings.yview)
        self.scrollbar_meanings.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_meanings.pack(side="left")

        self.scrollbar_meanings = ttk.Scrollbar(self, command=self.text_meanings.yview)
        self.button_delete = ttk.Button(self, text="Delete", command=self.delete)
        self.button_edit = ttk.Button(self, text="Edit", command=self.go_to_edit_screen)
        self.button_add = ttk.Button(
            self, text="Add Word", command=self.go_to_add_screen
        )

        TextFieldUtils.enable_ctrl_a_select(self.entry_word)
        TextFieldUtils.add_place_holder(self.entry_word, "Enter Word")
        TextFieldUtils.add_place_holder(
            self.text_meanings, "Meanings will be displayed here", True
        )
        TextFieldUtils.make_read_only(self.text_meanings)

        self.entry_word.grid(
            row=0, column=0, columnspan=2, ipady=3, pady=paddings.TOP, sticky="e"
        )
        self.button_search.grid(row=0, column=2, pady=paddings.TOP, sticky="e")
        self.frame_meanings.grid(row=1, column=0, columnspan=3, pady=paddings.MID)
        self.button_delete.grid(row=2, column=0, pady=paddings.BOTTOM, sticky="w")
        self.button_edit.grid(row=2, column=1, pady=paddings.BOTTOM, sticky="e")
        self.button_add.grid(row=2, column=2, pady=paddings.BOTTOM, sticky="e")

        self.pack()
