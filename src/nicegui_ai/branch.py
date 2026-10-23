"""Branch navigation picker for multi-turn forks and alternative completions."""

from collections.abc import Callable

from nicegui import ui


class BranchPicker(ui.row):
    """Inline < 1 / 3 > branch picker to inspect alternate conversation turns."""

    def __init__(
        self,
        current_index: int = 1,
        total_branches: int = 1,
        on_change: Callable[[int], None] | None = None,
    ) -> None:
        super().__init__()
        self.current_index = current_index
        self.total_branches = total_branches
        self.on_change = on_change

        self.classes(
            "items-center gap-1 bg-[#161c26]/80 border border-gray-700/60 "
            "rounded-full px-2 py-0.5 text-[10px] font-mono text-gray-300 shadow-sm"
        )

        with self:
            self.prev_btn = (
                ui.button(on_click=self.previous)
                .props("flat dense round size=xs")
                .classes("text-gray-400 hover:text-white p-0.5")
            )
            with self.prev_btn:
                ui.icon("chevron_left").classes("text-xs")

            self.label = ui.label(f"{self.current_index} / {self.total_branches}")

            self.next_btn = (
                ui.button(on_click=self.next)
                .props("flat dense round size=xs")
                .classes("text-gray-400 hover:text-white p-0.5")
            )
            with self.next_btn:
                ui.icon("chevron_right").classes("text-xs")

        self._update_state()

    def _update_state(self) -> None:
        self.label.set_text(f"{self.current_index} / {self.total_branches}")
        self.prev_btn.set_visibility(self.total_branches > 1)
        self.next_btn.set_visibility(self.total_branches > 1)

    def previous(self) -> None:
        if self.current_index > 1:
            self.current_index -= 1
        else:
            self.current_index = self.total_branches
        self._update_state()
        if self.on_change:
            self.on_change(self.current_index)

    def next(self) -> None:
        if self.current_index < self.total_branches:
            self.current_index += 1
        else:
            self.current_index = 1
        self._update_state()
        if self.on_change:
            self.on_change(self.current_index)
