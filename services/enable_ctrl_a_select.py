def callback(event):
    # select text
    event.widget.select_range(0, 'end')
    # move cursor to the end
    event.widget.icursor('end')


def enable_ctrl_a_select(wgt):
    wgt.bind('<Control-KeyRelease-a>', callback)
