"""Rounded pill AI composer with steering, cancellation, and Lucide controls."""

from collections.abc import Callable
from typing import Any

from nicegui import ui

from nicegui_ai.icons import LucideIcon


class AiComposer(ui.element):
    """Pill-style prompt composer with in-flight steering controls."""

    def __init__(
        self,
        placeholder: str = "Message AI agent... (type / for commands, @ for files)",
        on_send: Callable[[str], Any] | None = None,
        on_cancel: Callable[[], Any] | None = None,
        model_name: str = "Model Ready",
    ) -> None:
        super().__init__("div")
        self.on_send_callback = on_send
        self.on_cancel_callback = on_cancel
        self.is_running = False

        self.classes(
            "p-3 border-t border-gray-800/80 bg-[#0e121a]/95 backdrop-blur shrink-0 w-full"
        )

        with self:
            with ui.element("div").classes(
                "relative flex flex-col bg-[#141924] border border-gray-700/80 "
                "focus-within:border-purple-500/80 rounded-xl p-2.5 shadow-lg transition-colors w-full gap-1.5"
            ):
                # Textarea input
                self.input = (
                    ui.textarea(placeholder=placeholder)
                    .props("autogrow borderless dense rows=1")
                    .classes(
                        "w-full bg-transparent text-xs text-gray-100 placeholder-gray-500 "
                        "resize-none outline-none font-sans min-h-[36px] max-h-36"
                    )
                )

                # Keyboard shortcut: Enter to submit (Shift+Enter for newline)
                self.input.on(
                    "keydown.enter.prevent",
                    lambda e: (
                        self.submit()
                        if not getattr(e.args, "shiftKey", False)
                        else None
                    ),
                )

                # Bottom toolbar: model status & action buttons
                with ui.row().classes(
                    "items-center justify-between w-full pt-1.5 border-t border-gray-800/60"
                ):
                    with ui.row().classes(
                        "items-center gap-2 text-[10px] text-gray-400 font-mono"
                    ):
                        with ui.row().classes("items-center gap-1"):
                            self.status_dot = ui.element("span").classes(
                                "w-1.5 h-1.5 rounded-full bg-emerald-400"
                            )
                            self.status_text = ui.label("Steering: Ready")
                        ui.label("•").classes("text-gray-600")
                        self.model_badge = ui.label(model_name).classes(
                            "text-purple-300"
                        )

                    with ui.row().classes("items-center gap-1.5"):
                        # Cancel / Stop button
                        with (
                            ui.element("button")
                            .classes(
                                "p-1.5 rounded-lg bg-red-950/60 hover:bg-red-900 border border-red-500/40 "
                                "text-red-300 transition-colors cursor-pointer leading-none"
                            )
                            .on("click", self.cancel)
                        ) as self.cancel_btn:
                            LucideIcon("square", size=14, classes="text-red-300")

                        # Send / Steer button
                        with (
                            ui.element("button")
                            .classes(
                                "p-1.5 rounded-lg bg-purple-600 hover:bg-purple-500 text-white "
                                "transition-colors shadow-sm cursor-pointer leading-none"
                            )
                            .on("click", self.submit)
                        ) as self.send_btn:
                            LucideIcon("arrow-up", size=14, classes="text-white")

    def submit(self) -> None:
        """Submit the current input text."""
        text = self.input.value.strip() if self.input.value else ""
        if not text:
            return

        self.input.value = ""
        if self.on_send_callback:
            self.on_send_callback(text)

    def cancel(self) -> None:
        """Trigger cancellation of the current run."""
        if self.on_cancel_callback:
            self.on_cancel_callback()

    def set_running(self, running: bool) -> None:
        """Update visual state between idle and running."""
        self.is_running = running
        if running:
            self.status_dot.classes(
                replace="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"
            )
            self.status_text.set_text("Steering: Active")
        else:
            self.status_dot.classes(replace="w-1.5 h-1.5 rounded-full bg-emerald-400")
            self.status_text.set_text("Steering: Ready")
