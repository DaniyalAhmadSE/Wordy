from typing import Protocol

from views.interfaces.i_screen import IView


class IViewsManager(Protocol):
    load_screen: IView
    search_screen: IView
    add_screen: IView
    edit_screen: IView
