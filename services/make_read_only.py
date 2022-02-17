def make_read_only(tkWdg):
    """Makes a Tk widget (typically an Entry or Text) read-only,
    in the sense that the user cannot modify the text (but it can
    still be set programmatically). The user can still select and copy
    text
    and key bindings for <<Copy>> and <<Select-All>> still work properly.

    Inputs:
    - tkWdg: a Tk widget
    """

    def killEvent(evt):
        return "break"

    def doCopy(evt):
        tkWdg.event_generate("<<Copy>>")

    def doSelectAll(evt):
        tkWdg.event_generate("<<Select-All>>")

    # kill all events that can change the text,
    # including all typing (even shortcuts for
    # copy and select all)
    tkWdg.bind("<<Cut>>", killEvent)
    tkWdg.bind("<<Paste>>", killEvent)
    tkWdg.bind("<<Paste-Selection>>", killEvent)
    tkWdg.bind("<<Clear>>", killEvent)
    tkWdg.bind("<Key>", killEvent)
    # restore copy and select all
    for evt in tkWdg.event_info("<<Copy>>"):
        tkWdg.bind(evt, doCopy)
    for evt in tkWdg.event_info("<<Select-All>>"):
        tkWdg.bind(evt, doSelectAll)
