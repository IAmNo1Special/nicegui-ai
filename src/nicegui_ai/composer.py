"""Rounded pill AI composer with steering, cancellation, and mention support."""

from collections.abc import Callable
from typing import Any

from nicegui import ui


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
            "w-full bg-[#141924] border border-gray-700/80 focus-within:border-purple-500/80 "
            "rounded-xl p-2.5 shadow-lg transition-colors flex flex-col gap-2"
        )

        with self:
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
                    self.submit() if not getattr(e.args, "shiftKey", False) else None
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
                        self.status_text = ui.label("Ready")
                    ui.label("•").classes("text-gray-600")
                    self.model_badge = ui.label(model_name).classes("text-purple-300")

                with ui.row().classes("items-center gap-1.5"):
                    # Cancel / Stop button
                    self.cancel_btn = (
                        ui.button(on_click=self.cancel)
                        .props("flat dense round size=sm")
                        .classes(
                            "bg-red-950/60 hover:bg-red-900 border border-red-500/40 "
                            "text-red-300 transition-colors p-1"
                        )
                    )
                    with self.cancel_btn:
                        ui.icon("stop").classes("text-xs")
                    self.cancel_btn.set_visibility(False)

                    # Send / Steer button
                    self.send_btn = (
                        ui.button(on_click=self.submit)
                        .props("flat dense round size=sm")
                        .classes(
                            "bg-purple-600 hover:bg-purple-500 text-white transition-colors shadow-sm p-1"
                        )
                    )
                    with self.send_btn:
                        ui.icon("arrow_upward").classes("text-xs")

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
        """Toggle running/idle state, updating buttons and status dot."""
        self.is_running = running
        self.cancel_btn.set_visibility(running)
        if running:
            self.status_dot.classes(
                remove="bg-emerald-400", add="bg-cyan-400 animate-pulse"
            )
            self.status_text.set_text("Generating...")
        else:
            self.status_dot.classes(
                remove="bg-cyan-400 animate-pulse", add="bg-emerald-400"
            )
            self.status_text.set_text("Ready")
