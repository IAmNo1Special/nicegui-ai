"""Modern pill AI composer with in-flight queueing, task tray, and dynamic action button."""

from collections.abc import Callable
from typing import Any

from nicegui import ui

from nicegui_ai.icons import LucideIcon
from nicegui_ai.model_selector import ModelOption, ModelSelector
from nicegui_ai.queued_messages import QueuedMessagesTray
from nicegui_ai.schema import QueuedMessage
from nicegui_ai.task_tray import TaskHandle, TaskTray
from nicegui_ai.voice_pill import VoicePill


class AiComposer(ui.element):
    """Pill-style prompt composer matching 1:1 modern AI agent interfaces.

    Features:
    - Queued messages tray with Send Now, Edit, and Delete controls.
    - Active background tasks tray with animated spinners.
    - Auto-growing borderless textarea with Shift+Enter multiline support.
    - Inline model picker with upward popover.
    - Embedded VoicePill streaming indicator.
    - Dynamic 3-state Action Button (Disabled Send, Enabled Send, Stop, Queue).
    """

    def __init__(
        self,
        placeholder: str = "Ask anything, @ to mention, / for actions",
        on_send: Callable[[str], Any] | None = None,
        on_cancel: Callable[[], Any] | None = None,
        on_attach: Callable[[], Any] | None = None,
        on_voice: Callable[[str], Any] | None = None,
        model_name: str = "Gemini 3.8 Flash",
        models: list[str | ModelOption | dict[str, Any]] | None = None,
        reasoning_effort: str | None = "High",
        on_model_change: Callable[[str, str | None], None] | None = None,
        auto_drain_queue: bool = True,
        classes: str = "",
    ) -> None:
        super().__init__("div")
        self.on_send_callback = on_send
        self.on_cancel_callback = on_cancel
        self.on_attach_callback = on_attach
        self.on_voice_callback = on_voice
        self.on_model_change_callback = on_model_change
        self.auto_drain_queue = auto_drain_queue
        self.is_running: bool = False
        self._queue_paused: bool = False

        self.models: list[str | ModelOption | dict[str, Any]] = models or [
            ModelOption(name="Gemini 4 Argon", effort="Medium", badge="New"),
            ModelOption(name="Gemini 3.8 Flash", effort="High"),
            ModelOption(name="Claude Opus 5.5", effort="Medium", badge="New"),
            ModelOption(name="Claude Sonnet 5.5", effort="Medium", badge="New"),
            ModelOption(name="GPT-OSS 120B (Medium)", badge="Notice"),
        ]
        self.current_model = model_name
        self.current_effort = reasoning_effort

        self.classes(
            f"p-3 border-t border-gray-800/80 bg-[#0e121a]/95 backdrop-blur shrink-0 w-full flex flex-col gap-2.5 {classes}"
        )

        with self:
            # 1. Top Queued Messages Tray
            self.queued_tray = QueuedMessagesTray(
                on_send_now=self._handle_send_now_from_queue,
                on_edit=self._handle_edit_from_queue,
            )

            # 2. Middle Task Tray
            self.task_tray = TaskTray()

            # 3. Bottom Input Card
            with ui.element("div").classes(
                "relative flex flex-col bg-[#141924] border border-gray-700/80 "
                "focus-within:border-purple-500/80 rounded-2xl p-3 shadow-lg transition-colors w-full gap-2"
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

                # Keystroke bindings:
                # Shift+Enter inserts newline; Enter submits/queues
                self.input.on(
                    "keydown",
                    js_handler="""(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            emit(e);
                        }
                    }""",
                    handler=lambda _: self.submit(),
                )
                self.input.on("input", lambda _: self._update_action_button())
                self.input.on(
                    "update:model-value", lambda _: self._update_action_button()
                )

                # Bottom toolbar
                with ui.row().classes(
                    "items-center justify-between w-full pt-1.5 border-t border-gray-800/60"
                ):
                    # Left side: Attach (+) and ModelSelector
                    with ui.row().classes("items-center gap-1.5"):
                        with (
                            ui.element("button")
                            .classes(
                                "w-6 h-6 rounded-full flex items-center justify-center text-gray-400 "
                                "hover:text-white hover:bg-gray-800/80 transition-colors cursor-pointer border-none bg-transparent"
                            )
                            .props("type=button")
                            .on("click", self._handle_attach)
                        ) as self.attach_btn:
                            LucideIcon("plus", size=14, classes="text-gray-400")

                        self.model_selector = ModelSelector(
                            models=self.models,
                            current_model=self.current_model,
                            reasoning_effort=self.current_effort,
                            variant="inline",
                            on_change=self._handle_model_change,
                        )

                    # Right side: VoicePill and unified Action Button
                    with ui.row().classes("items-center gap-2"):
                        self.voice_pill = VoicePill(
                            state="idle",
                            on_toggle=self._handle_voice_toggle,
                        )

                        # Unified Action Button (Send / Stop / Queue)
                        with (
                            ui.element("button")
                            .props("type=button")
                            .on("click", self._handle_action_button_click)
                        ) as self.action_btn:
                            self.action_icon = LucideIcon(
                                "arrow-right", size=14, classes="text-inherit"
                            )

        self._update_action_button()

    def submit(self) -> None:
        """Submit the current input text or queue it if already running."""
        text = self.input.value.strip() if self.input.value else ""
        if not text:
            return

        self.input.value = ""
        self._update_action_button()

        if self.is_running:
            self.queued_tray.add_message(text)
        else:
            self._queue_paused = False
            if self.on_send_callback:
                self.on_send_callback(text)

    def cancel(self) -> None:
        """Trigger cancellation of the current run."""
        self._queue_paused = True
        if self.on_cancel_callback:
            self.on_cancel_callback()

    def set_running(self, running: bool) -> None:
        """Update visual state between idle and running."""
        was_running = self.is_running
        self.is_running = running
        self._update_action_button()

        # If completed and queue has messages, auto-drain FIFO
        if (
            was_running
            and not running
            and self.auto_drain_queue
            and not self._queue_paused
        ):
            next_msg = self.queued_tray.pop_next()
            if next_msg and self.on_send_callback:
                self.on_send_callback(next_msg.text)

    def add_task(self, text: str, task_id: str | None = None) -> TaskHandle:
        """Forward task creation to the embedded TaskTray."""
        return self.task_tray.add_task(text, task_id)

    def queue_message(self, text: str) -> QueuedMessage:
        """Programmatically append a prompt to the QueuedMessagesTray."""
        return self.queued_tray.add_message(text)

    def _update_action_button(self) -> None:
        """Update unified action button styling and icon based on state."""
        has_text = bool(self.input.value and self.input.value.strip())

        if not self.is_running:
            if not has_text:
                # Idle + Empty -> Disabled Send
                self.action_btn.classes(
                    replace="w-8 h-8 rounded-full bg-gray-800/80 text-gray-500 border border-gray-700/40 "
                    "flex items-center justify-center opacity-40 cursor-not-allowed transition-all"
                )
                self.action_icon.set_icon(
                    "arrow-right", size=14, classes="text-gray-500"
                )
            else:
                # Idle + Text -> Enabled Send
                self.action_btn.classes(
                    replace="w-8 h-8 rounded-full bg-purple-600 hover:bg-purple-500 text-white "
                    "flex items-center justify-center cursor-pointer shadow-md transition-all border-none"
                )
                self.action_icon.set_icon("arrow-right", size=14, classes="text-white")
        else:
            if not has_text:
                # Running + Empty -> Stop button
                self.action_btn.classes(
                    replace="w-8 h-8 rounded-full bg-gray-200 hover:bg-white text-gray-900 "
                    "flex items-center justify-center cursor-pointer shadow-md transition-all border-none"
                )
                self.action_icon.set_icon("square", size=12, classes="text-gray-900")
            else:
                # Running + Text -> Enabled Queue button
                self.action_btn.classes(
                    replace="w-8 h-8 rounded-full bg-purple-600 hover:bg-purple-500 text-white "
                    "flex items-center justify-center cursor-pointer shadow-md transition-all border-none"
                )
                self.action_icon.set_icon("arrow-right", size=14, classes="text-white")

    def _handle_action_button_click(self) -> None:
        has_text = bool(self.input.value and self.input.value.strip())
        if self.is_running and not has_text:
            self.cancel()
        elif has_text:
            self.submit()

    def _handle_attach(self) -> None:
        if self.on_attach_callback:
            self.on_attach_callback()
        else:
            ui.notify("Attachment menu requested", type="info", timeout=1200)

    def _handle_voice_toggle(self, state: str) -> None:
        if self.on_voice_callback:
            self.on_voice_callback(state)

    def _handle_model_change(self, model: str, effort: str | None) -> None:
        self.current_model = model
        self.current_effort = effort
        if self.on_model_change_callback:
            self.on_model_change_callback(model, effort)

    def _handle_send_now_from_queue(self, msg: QueuedMessage) -> None:
        if self.is_running:
            self.cancel()
        self._queue_paused = False
        if self.on_send_callback:
            self.on_send_callback(msg.text)

    def _handle_edit_from_queue(self, msg: QueuedMessage) -> None:
        self.input.value = msg.text
        self._update_action_button()
