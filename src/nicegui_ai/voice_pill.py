"""Voice status and push-to-talk audio indicator primitive."""

from collections.abc import Callable
from typing import Literal

from nicegui import ui

from nicegui_ai.icons import LucideIcon

VoiceState = Literal["idle", "listening", "thinking", "speaking"]


class VoicePill(ui.element):
    """Pill indicator and control for voice and audio streaming agents."""

    def __init__(
        self,
        state: VoiceState = "idle",
        on_toggle: Callable[[str], None] | None = None,
        classes: str = "",
    ) -> None:
        super().__init__("div")
        self.classes(f"relative inline-flex items-center {classes}")

        self._state: VoiceState = state
        self._on_toggle = on_toggle

        with (
            ui.element("button")
            .classes(
                "flex items-center gap-2 px-3 py-1.5 rounded-full border border-gray-800 "
                "bg-[#11151f]/80 hover:bg-[#181e2b] transition-all cursor-pointer outline-none"
            )
            .props("type=button")
            .on("click", self._handle_click)
        ) as self.pill_btn:
            self.icon_slot = ui.element("div").classes("flex items-center")
            self.label = ui.label("").classes("text-xs font-medium")
            self.wave_container = ui.element("div").classes(
                "flex items-center gap-0.5 ml-1"
            )
            with self.wave_container:
                self.bars = [
                    ui.element("span").classes(
                        "w-0.5 h-3 bg-current rounded-full animate-pulse"
                    ),
                    ui.element("span").classes(
                        "w-0.5 h-4 bg-current rounded-full animate-pulse delay-75"
                    ),
                    ui.element("span").classes(
                        "w-0.5 h-2 bg-current rounded-full animate-pulse delay-150"
                    ),
                ]

        self._render_state()

    @property
    def state(self) -> VoiceState:
        return self._state

    @property
    def is_active(self) -> bool:
        return self._state != "idle"

    def set_state(self, state: VoiceState) -> None:
        self._state = state
        self._render_state()

    def toggle(self) -> None:
        new_state: VoiceState = "listening" if self._state == "idle" else "idle"
        self.set_state(new_state)
        if self._on_toggle:
            self._on_toggle(self._state)

    def _handle_click(self) -> None:
        self.toggle()

    def _render_state(self) -> None:
        self.icon_slot.clear()
        with self.icon_slot:
            if self._state == "idle":
                LucideIcon("mic", size=14, classes="text-gray-400")
                self.label.text = "Voice"
                self.label.classes(replace="text-xs font-medium text-gray-400")
                self.wave_container.set_visibility(False)
                self.pill_btn.classes(
                    replace="flex items-center gap-2 px-3 py-1.5 rounded-full border border-gray-800 "
                    "bg-[#11151f]/80 hover:bg-[#181e2b] text-gray-400 transition-all cursor-pointer outline-none"
                )
            elif self._state == "listening":
                LucideIcon("mic", size=14, classes="text-emerald-400")
                self.label.text = "Listening"
                self.label.classes(replace="text-xs font-medium text-emerald-300")
                self.wave_container.set_visibility(True)
                self.pill_btn.classes(
                    replace="flex items-center gap-2 px-3 py-1.5 rounded-full border border-emerald-500/40 "
                    "bg-emerald-950/30 text-emerald-400 shadow-[0_0_12px_rgba(16,185,129,0.2)] transition-all cursor-pointer outline-none"
                )
            elif self._state == "thinking":
                LucideIcon("sparkles", size=14, classes="text-amber-400 animate-spin")
                self.label.text = "Thinking..."
                self.label.classes(replace="text-xs font-medium text-amber-300")
                self.wave_container.set_visibility(False)
                self.pill_btn.classes(
                    replace="flex items-center gap-2 px-3 py-1.5 rounded-full border border-amber-500/40 "
                    "bg-amber-950/30 text-amber-400 shadow-[0_0_12px_rgba(245,158,11,0.2)] transition-all cursor-pointer outline-none"
                )
            elif self._state == "speaking":
                LucideIcon("volume-2", size=14, classes="text-purple-400")
                self.label.text = "Speaking"
                self.label.classes(replace="text-xs font-medium text-purple-300")
                self.wave_container.set_visibility(True)
                self.pill_btn.classes(
                    replace="flex items-center gap-2 px-3 py-1.5 rounded-full border border-purple-500/40 "
                    "bg-purple-950/30 text-purple-400 shadow-[0_0_12px_rgba(168,85,247,0.2)] transition-all cursor-pointer outline-none"
                )
