from typing import Protocol


class IView(Protocol):
    def build(self) -> None:
        ...
