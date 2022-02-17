import tkinter as tkn
from tkinter import messagebox
import tkinter.ttk as ttk
from utils.wordy_api import WordyApi
from services import make_read_only as mro
from services import enable_ctrl_a_select as ecas
from services import add_place_holder as aph
from constants import paddings as pd
import mttkinter as mutlithreading_helper  # IGNORE


class WordyGui(tkn.Tk):
    def __init__(self):
        super().__init__()
        self.api = WordyApi()
        self.title('Wordy')
        self.geometry('500x360')
        self.resizable(False, False)
        self.start_app()

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

    def start_app(self):
        self.load_screen()
        self.search_screen()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        # self.add_screen()

    def load_screen(self):
        frm_load = ttk.Frame(self)

        lbl_wordy = ttk.Label(
            frm_load, text='WORDY',
            font=('Rachana', 50, 'bold'),
            foreground='#1A5276',
            justify='center',
        )
        lbl_line = ttk.Label(
            frm_load,
            text='The Dictionary You Need',
            font=('Rachana', 16),
            foreground='#1A5276',
        )
        prg_bar = ttk.Progressbar(
            frm_load, orient=tkn.HORIZONTAL, length=300
        )
        lbl_load = ttk.Label(
            frm_load, text='Loading',
            font=('Rachana', 12),
            foreground='#1A5276',
        )

        lbl_wordy.pack()
        lbl_line.pack()
        prg_bar.pack(pady=10)
        lbl_load.pack()
        frm_load.pack(expand=1)
        self.api.start_thread(prg_bar, lbl_load)

        # Waiting till the Loading Completes
        while prg_bar.cget('value') < 100:
            self.update()
        frm_load.pack_forget()

    def search_screen(self):

        def search():
            result = self.api.search(ent_word.get())
            print(result)
            txt_means.config(state=tkn.NORMAL, fg='black')
            txt_means.delete(1.0, tkn.END)
            txt_means.insert(tkn.END, result)

        def delete():
            result = self.api.delete(ent_word.get())
            print(result)
            ent_word.delete(0, tkn.END)
            ent_word.event_generate('<FocusOut>')
            txt_means.config(state=tkn.NORMAL, fg='black')
            txt_means.delete(1.0, tkn.END)
            txt_means.event_generate('<FocusOut>')

        def search_to_add():
            frm_src.pack_forget()
            self.add_screen(ent_word.get())

        def search_to_edit():
            frm_src.pack_forget()
            self.edit_screen(ent_word.get())

        frm_src = ttk.Frame(self)

        ent_word = tkn.Entry(frm_src, width=57)
        btn_search = ttk.Button(frm_src, text='Search', command=search)

        frm_means = ttk.Frame(frm_src)
        scr_means = ttk.Scrollbar(frm_means)
        txt_means = tkn.Text(
            frm_means, height=17, width=58, wrap=tkn.WORD,
            insertontime=0, yscrollcommand=scr_means.set
        )
        scr_means.config(command=txt_means.yview)
        scr_means.pack(side=tkn.RIGHT, fill=tkn.Y)
        txt_means.pack(side="left")

        scr_means = ttk.Scrollbar(frm_src, command=txt_means.yview)
        btn_del = ttk.Button(frm_src, text='Delete', command=delete)
        btn_edit = ttk.Button(frm_src, text='Edit', command=search_to_edit)
        btn_add = ttk.Button(
            frm_src, text='Add Word', command=search_to_add
        )

        ecas.enable_ctrl_a_select(ent_word)
        aph.add_place_holder(ent_word, 'Enter Word')
        aph.add_place_holder(
            txt_means, 'Meanings will be displayed here', True
        )
        mro.make_read_only(txt_means)

        ent_word.grid(
            row=0, column=0, columnspan=2, ipady=3, pady=pd.TOP, sticky='e'
        )
        btn_search.grid(row=0, column=2, pady=pd.TOP, sticky='e')
        frm_means.grid(row=1, column=0, columnspan=3, pady=pd.MID)
        btn_del.grid(row=2, column=0, pady=pd.BOTTOM, sticky='w')
        btn_edit.grid(row=2, column=1, pady=pd.BOTTOM, sticky='e')
        btn_add.grid(row=2, column=2, pady=pd.BOTTOM, sticky='e')

        frm_src.pack()

    def add_screen(self, word=''):

        def add():
            result = self.api.add(
                ent_word.get(), txt_means.get(1.0, tkn.END), ent_sa.get()
            )
            print(result)

        def add_to_search():
            frm_add.pack_forget()
            self.search_screen()

        frm_add = ttk.Frame(self)

        ent_word = tkn.Entry(frm_add, width=40)
        ent_sa = tkn.Entry(frm_add, width=26)
        frm_means = ttk.Frame(frm_add)
        scr_means = ttk.Scrollbar(frm_means)
        txt_means = tkn.Text(
            frm_means, height=17, width=58,
            wrap=tkn.WORD, yscrollcommand=scr_means.set
        )
        scr_means.config(command=txt_means.yview)
        scr_means.pack(side=tkn.RIGHT, fill=tkn.Y)
        txt_means.pack(side="left")

        btn_bck = ttk.Button(frm_add, text='Back', command=add_to_search)
        btn_add = ttk.Button(frm_add, text='Add', command=add)

        ecas.enable_ctrl_a_select(ent_word)
        aph.add_place_holder(ent_word, 'Enter Word')
        aph.add_place_holder(ent_sa, 'See Also')
        aph.add_place_holder(
            txt_means, 'Enter meanings, separated by blank lines', True
        )

        ent_word.grid(row=0, column=0, ipady=3, pady=pd.TOP, sticky='w')
        ent_sa.grid(
            row=0, column=1, columnspan=6, ipady=3, pady=pd.TOP, sticky='e'
        )
        frm_means.grid(row=1, column=0, columnspan=7, pady=pd.MID)
        btn_bck.grid(row=2, column=5, pady=pd.BOTTOM, sticky='e')
        btn_add.grid(row=2, column=6, pady=pd.BOTTOM, sticky='e')

        frm_add.pack()

    def edit_screen(self, word=''):

        def edit():
            result = self.api.update(
                ent_word.get(), txt_means.get(1.0, tkn.END), ent_sa.get()
            )
            print(result)

        def edit_to_search():
            frm_edt.pack_forget()
            self.search_screen()

        frm_edt = ttk.Frame(self)

        ent_word = tkn.Entry(frm_edt, width=40)
        ent_sa = tkn.Entry(frm_edt, width=26)
        frm_means = ttk.Frame(frm_edt)
        scr_means = ttk.Scrollbar(frm_means)
        txt_means = tkn.Text(
            frm_means, height=17, width=58,
            wrap=tkn.WORD, yscrollcommand=scr_means.set
        )
        scr_means.config(command=txt_means.yview)
        scr_means.pack(side=tkn.RIGHT, fill=tkn.Y)
        txt_means.pack(side="left")

        btn_bck = ttk.Button(frm_edt, text='Back', command=edit_to_search)
        btn_edt = ttk.Button(frm_edt, text='Edit', command=edit)

        ecas.enable_ctrl_a_select(ent_word)
        aph.add_place_holder(ent_word, 'Enter Word')
        aph.add_place_holder(ent_sa, 'See Also')
        aph.add_place_holder(
            txt_means, 'Enter meanings, separated by blank lines', True
        )

        ent_word.grid(row=0, column=0, ipady=3, pady=pd.TOP, sticky='w')
        ent_sa.grid(
            row=0, column=1, columnspan=6, ipady=3, pady=pd.TOP, sticky='e'
        )
        frm_means.grid(row=1, column=0, columnspan=7, pady=pd.MID)
        btn_bck.grid(row=2, column=5, pady=pd.BOTTOM, sticky='e')
        btn_edt.grid(row=2, column=6, pady=pd.BOTTOM, sticky='e')

        frm_edt.pack()


def launch_gui():
    gui = WordyGui()
    gui.mainloop()


if __name__ == "__main__":
    launch_gui()
