def on_focus_in(wgt, init_i=0):
    if wgt.cget('state') == 'disabled':
        wgt.configure(state='normal')
        wgt.config(fg='black')
        wgt.delete(init_i, 'end')


def on_focus_out(wgt, placeholder, is_text=False):
    is_empty = False
    if is_text:
        is_empty = wgt.get(1.0, 'end') == "\n"
    else:
        is_empty = wgt.get() == ""

    if is_empty:
        wgt.insert('end', placeholder)
        if is_text:
            wgt.config(fg='grey')
        wgt.configure(state='disabled')


def add_place_holder(wgt, plc_hldr, is_text=False):
    wgt.insert('end', plc_hldr)
    wgt.configure(state='disabled')
    if is_text:
        wgt.config(fg='darkgrey')
        wgt.bind('<Button-1>', lambda x: on_focus_in(wgt, 1.0))
    else:
        wgt.configure(disabledbackground='White')
        wgt.bind('<Button-1>', lambda x: on_focus_in(wgt))

    wgt.bind('<FocusOut>', lambda x: on_focus_out(wgt, plc_hldr, is_text))
