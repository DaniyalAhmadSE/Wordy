import tkinter as tk
from typing import Any


class TextFieldUtils:
    @staticmethod
    def enable_ctrl_a_select(widget: tk.Entry | tk.Text):
        def callback(event: "tk.Event[Any]"):
            # select text
            event.widget.select_range(0, "end")
            # move cursor to the end
            event.widget.icursor("end")

        widget.bind("<Control-KeyRelease-a>", callback)

    @staticmethod
    def make_read_only(widget: tk.Entry | tk.Text):
        """Makes an Entry or Text widget read-only,
        in the sense that the user cannot modify the text (but it can
        still be set programmatically). The user can still select and copy
        text
        and key bindings for <<Copy>> and <<Select-All>> still work properly.

        Inputs:
        - tkWdg: a Tk widget
        """

        def killEvent(event: "tk.Event[Any]"):
            return "break"

        def doCopy(event: "tk.Event[Any]"):
            event.widget.event_generate("<<Copy>>")

        def doSelectAll(event: "tk.Event[Any]"):
            event.widget.event_generate("<<Select-All>>")

        # kill all events that can change the text,
        # including all typing (even shortcuts for
        # copy and select all)
        widget.bind("<<Cut>>", killEvent)
        widget.bind("<<Paste>>", killEvent)
        widget.bind("<<Paste-Selection>>", killEvent)
        widget.bind("<<Clear>>", killEvent)
        widget.bind("<Key>", killEvent)
        # restore copy and select all
        for evt in widget.event_info("<<Copy>>"):
            widget.bind(evt, doCopy)
        for evt in widget.event_info("<<Select-All>>"):
            widget.bind(evt, doSelectAll)

    @staticmethod
    def add_place_holder(
        widget: tk.Entry | tk.Text,
        place_holder: str,
        is_text: bool = False,
    ):
        def on_focus_in(widget: tk.Entry | tk.Text, init_i: int = 0):
            if widget.cget("state") == "disabled":
                widget.configure(state="normal")
                widget.config(fg="black")
                widget.delete(init_i, "end")

        def on_focus_out(
            widget: tk.Entry | tk.Text,
            placeholder: str,
            is_text: bool = False,
        ):
            is_empty = False
            if is_text:
                is_empty = widget.get(1.0, "end") == "\n"
            else:
                is_empty = widget.get() == ""

            if is_empty:
                widget.insert("end", placeholder)
                if is_text:
                    widget.config(fg="grey")
                widget.configure(state="disabled")

        widget.insert("end", place_holder)
        widget.configure(state="disabled")
        if is_text:
            widget.config(fg="darkgrey")
            widget.bind("<Button-1>", lambda x: on_focus_in(widget, 1.0))
        else:
            widget.configure(disabledbackground="White")
            widget.bind("<Button-1>", lambda x: on_focus_in(widget))

        widget.bind("<FocusOut>", lambda x: on_focus_out(widget, place_holder, is_text))
