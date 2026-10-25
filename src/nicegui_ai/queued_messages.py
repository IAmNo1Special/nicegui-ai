"""Queued messages panel matching 1:1 the reference design."""

import uuid
from collections.abc import Callable
from typing import Self

from nicegui import ui

from nicegui_ai.icons import LucideIcon
from nicegui_ai.types import QueuedMessage


class QueuedMessagesTray(ui.element):
    """Collapsible tray showing user messages queued while the agent is busy.

    Matches 1:1 the layout, typography, and controls from the reference design.
    """

    def __init__(
        self,
        on_send_now: Callable[[QueuedMessage], None] | None = None,
        on_edit: Callable[[QueuedMessage], None] | None = None,
        on_delete: Callable[[QueuedMessage], None] | None = None,
        classes: str = "",
    ) -> None:
        super().__init__("div")
        self.classes(
            f"w-full rounded-2xl border border-gray-800/80 bg-[#141924] p-3 shadow-md flex flex-col gap-2 transition-all {classes}"
        )

        self._messages: list[QueuedMessage] = []
        self._on_send_now = on_send_now
        self._on_edit = on_edit
        self._on_delete = on_delete
        self.is_open: bool = True

        with self:
            # Header
            with ui.row().classes(
                "items-center justify-between w-full cursor-pointer select-none"
            ) as self.header_row:
                self.header_row.on("click", self.toggle)
                with ui.row().classes("items-center gap-2 text-xs"):
                    ui.label("Queued Messages").classes(
                        "font-medium text-gray-200 text-xs"
                    )
                    self.count_badge = ui.label("0").classes(
                        "bg-gray-700/80 text-[10px] text-gray-300 font-mono px-1.5 py-0.2 rounded-full"
                    )
                    ui.label("Sends after agent finishes working").classes(
                        "text-[11px] text-gray-400"
                    )

                self.chevron = LucideIcon(
                    "chevron-down",
                    size=14,
                    classes="text-gray-400 shrink-0 transition-transform",
                )

            # Messages container
            self.list_container = ui.column().classes("w-full gap-2 pt-1")

        self.set_visibility(False)

    @property
    def messages(self) -> list[QueuedMessage]:
        """Return the current list of queued messages."""
        return list(self._messages)

    def __len__(self) -> int:
        return len(self._messages)

    def toggle(self) -> None:
        """Toggle collapsed/expanded view of queued messages."""
        self.is_open = not self.is_open
        self.list_container.set_visibility(self.is_open)
        self.chevron.set_icon("chevron-down" if self.is_open else "chevron-up")

    def add_message(self, text: str) -> QueuedMessage:
        """Add a prompt to the queue and refresh the UI."""
        msg = QueuedMessage(id=str(uuid.uuid4())[:8], text=text)
        self._messages.append(msg)
        self._render()
        return msg

    def remove_message(self, msg_id: str) -> QueuedMessage | None:
        """Remove a message by ID from the queue."""
        found: QueuedMessage | None = None
        for i, m in enumerate(self._messages):
            if m.id == msg_id:
                found = self._messages.pop(i)
                break
        if found:
            self._render()
        return found

    def pop_next(self) -> QueuedMessage | None:
        """Pop the next queued message (FIFO order) for execution."""
        if not self._messages:
            return None
        msg = self._messages.pop(0)
        self._render()
        return msg

    def clear(self) -> Self:
        """Clear all messages from the queue and hide the tray."""
        self._messages.clear()
        self._render()
        return self

    def _render(self) -> None:
        count = len(self._messages)
        self.count_badge.text = str(count)
        self.set_visibility(count > 0)
        self.list_container.clear()

        if count == 0:
            return

        with self.list_container:
            for msg in self._messages:
                with ui.row().classes(
                    "items-center justify-between w-full py-1.5 px-2.5 rounded-lg bg-[#0e121a]/80 "
                    "border border-gray-800/60 hover:border-gray-700/80 transition-colors"
                ):
                    ui.label(msg.text).classes(
                        "text-xs text-gray-200 font-sans break-words max-w-[80%]"
                    )
                    with ui.row().classes("items-center gap-2 shrink-0"):
                        # Send now button
                        with (
                            ui.element("button")
                            .classes(
                                "p-1 rounded text-gray-400 hover:text-white hover:bg-gray-800/80 "
                                "transition-colors cursor-pointer border-none bg-transparent"
                            )
                            .on("click", lambda _e, m=msg: self._handle_send_now(m))
                        ):
                            LucideIcon("arrow-right", size=13, classes="text-gray-400")

                        # Edit button
                        with (
                            ui.element("button")
                            .classes(
                                "p-1 rounded text-gray-400 hover:text-white hover:bg-gray-800/80 "
                                "transition-colors cursor-pointer border-none bg-transparent"
                            )
                            .on("click", lambda _e, m=msg: self._handle_edit(m))
                        ):
                            LucideIcon("pencil", size=13, classes="text-gray-400")

                        # Delete button
                        with (
                            ui.element("button")
                            .classes(
                                "p-1 rounded text-gray-400 hover:text-red-400 hover:bg-gray-800/80 "
                                "transition-colors cursor-pointer border-none bg-transparent"
                            )
                            .on("click", lambda _e, m=msg: self._on_msg_delete(m))
                        ):
                            LucideIcon("trash", size=13, classes="text-gray-400")

    def _handle_send_now(self, msg: QueuedMessage) -> None:
        self.remove_message(msg.id)
        if self._on_send_now:
            self._on_send_now(msg)

    def _handle_edit(self, msg: QueuedMessage) -> None:
        self.remove_message(msg.id)
        if self._on_edit:
            self._on_edit(msg)

    def _on_msg_delete(self, msg: QueuedMessage) -> None:
        self.remove_message(msg.id)
        if self._on_delete:
            self._on_delete(msg)
