"""Task tray panel displaying running background tasks matching the reference design."""

import uuid
from typing import Self

from nicegui import ui

from nicegui_ai.icons import LucideIcon
from nicegui_ai.types import RunningTask


class TaskHandle:
    """Handle to a running task in TaskTray allowing dynamic updates and completion."""

    def __init__(self, tray: "TaskTray", task: RunningTask) -> None:
        self._tray = tray
        self._task = task

    @property
    def id(self) -> str:
        return self._task.id

    @property
    def text(self) -> str:
        return self._task.text

    def set_text(self, text: str) -> None:
        """Update the displayed task text."""
        self._task.text = text
        self._tray._render()

    def complete(self) -> None:
        """Mark task as complete and remove from tray."""
        self._tray.remove_task(self._task.id)


class TaskTray(ui.element):
    """Collapsible tray showing active background tasks with spinners and monospace prompts."""

    def __init__(self, classes: str = "") -> None:
        super().__init__("div")
        self.classes(
            f"w-full rounded-2xl border border-gray-800/80 bg-[#141924] p-3 shadow-md flex flex-col gap-2 transition-all {classes}"
        )

        self._tasks: list[RunningTask] = []
        self.is_open: bool = True

        with self:
            # Header
            with ui.row().classes(
                "items-center justify-between w-full cursor-pointer select-none"
            ) as self.header_row:
                self.header_row.on("click", self.toggle)
                with ui.row().classes("items-center gap-2 text-xs"):
                    self.title_label = ui.label("0 tasks running").classes(
                        "font-medium text-gray-300 text-xs"
                    )

                self.chevron = LucideIcon(
                    "chevron-down",
                    size=14,
                    classes="text-gray-400 shrink-0 transition-transform",
                )

            # Task rows list container
            self.list_container = ui.column().classes("w-full gap-2 pt-1")

        self.set_visibility(False)

    @property
    def tasks(self) -> list[RunningTask]:
        return list(self._tasks)

    def __len__(self) -> int:
        return len(self._tasks)

    def toggle(self) -> None:
        """Toggle collapsed/expanded state."""
        self.is_open = not self.is_open
        self.list_container.set_visibility(self.is_open)
        self.chevron.set_icon("chevron-down" if self.is_open else "chevron-up")

    def add_task(self, text: str, task_id: str | None = None) -> TaskHandle:
        """Add a background task and return a handle to control it."""
        tid = task_id or str(uuid.uuid4())[:8]
        task = RunningTask(id=tid, text=text)
        self._tasks.append(task)
        self._render()
        return TaskHandle(self, task)

    def remove_task(self, task_id: str) -> RunningTask | None:
        """Remove a task by its ID."""
        found: RunningTask | None = None
        for i, t in enumerate(self._tasks):
            if t.id == task_id:
                found = self._tasks.pop(i)
                break
        if found:
            self._render()
        return found

    def clear(self) -> Self:
        """Clear all tasks and hide the tray."""
        self._tasks.clear()
        self._render()
        return self

    def _render(self) -> None:
        count = len(self._tasks)
        label_text = f"{count} task running" if count == 1 else f"{count} tasks running"
        self.title_label.text = label_text
        self.set_visibility(count > 0)
        self.list_container.clear()

        if count == 0:
            return

        with self.list_container:
            for task in self._tasks:
                with ui.row().classes(
                    "items-start gap-2.5 w-full py-1.5 px-2.5 rounded-lg bg-[#0e121a]/80 border border-gray-800/60"
                ):
                    LucideIcon(
                        "loader",
                        size=14,
                        classes="text-gray-400 animate-spin shrink-0 mt-0.5",
                    )
                    ui.label(task.text).classes(
                        "font-mono text-[11px] text-gray-300 leading-relaxed break-words flex-1"
                    )
