"""Amber-gilded collapsible reasoning card for AI agent thinking steps."""

from typing import Self

from nicegui import ui

from nicegui_ai.icons import LucideIcon


class ReasoningCard(ui.element):
    """Amber-gilded collapsible card displaying model reasoning steps and chain-of-thought."""

    def __init__(
        self,
        thought_text: str = "",
        step_count: int = 1,
        title: str = "Reasoning (Thinking Process)",
        steps: list[str] | None = None,
        duration_ms: int | None = None,
        default_open: bool = False,
    ) -> None:
        super().__init__("div")
        self.is_open = default_open
        self.title = title
        self.duration_ms = duration_ms

        if steps and not thought_text:
            thought_text = "\n".join(f"• {s}" for s in steps)
            step_count = len(steps)

        self.thought_text = thought_text
        self.step_count = step_count

        self.classes(
            "w-full rounded-lg border border-amber-500/30 bg-[#161410] "
            "overflow-hidden text-xs shadow-sm mb-3 transition-all"
        )

        with self:
            with ui.element("button").classes(
                "w-full flex items-center justify-between p-2 px-3 "
                "bg-[#1d1912] hover:bg-[#231e16] transition-colors text-left cursor-pointer border-none outline-none"
            ) as self.header_btn:
                self.header_btn.on("click", self.toggle)
                with ui.row().classes("items-center gap-2"):
                    LucideIcon(
                        "brain-circuit", size=14, classes="text-amber-400 shrink-0"
                    )
                    self.title_label = ui.label(self.title).classes(
                        "font-semibold text-amber-300 text-xs"
                    )
                    duration_str = f" ({duration_ms}ms)" if duration_ms else ""
                    self.steps_badge = ui.label(
                        f"{self.step_count} steps{duration_str}"
                    ).classes("text-[10px] text-amber-400/80 font-mono")

                self.chevron = LucideIcon(
                    "chevron-down" if default_open else "chevron-right",
                    size=14,
                    classes="text-amber-400 shrink-0",
                )

            # Collapsible body
            self.body = ui.element("div").classes(
                "p-3 bg-[#12100d] text-amber-200/90 font-mono text-[11px] "
                "leading-relaxed whitespace-pre-wrap border-t border-amber-500/20 select-text"
            )
            self.body.set_visibility(default_open)
            with self.body:
                self.content_label = ui.label(self.thought_text).classes(
                    "w-full select-text whitespace-pre-wrap text-inherit font-mono"
                )

    def toggle(self) -> None:
        """Toggle collapsed/expanded state."""
        self.is_open = not self.is_open
        self.body.set_visibility(self.is_open)
        self.chevron.set_icon("chevron-down" if self.is_open else "chevron-right")

    def open(self) -> Self:
        """Expand reasoning body."""
        self.is_open = True
        self.body.set_visibility(True)
        self.chevron.set_icon("chevron-down")
        return self

    def close(self) -> Self:
        """Collapse reasoning body."""
        self.is_open = False
        self.body.set_visibility(False)
        self.chevron.set_icon("chevron-right")
        return self

    def append_thought(self, chunk: str, step_count: int | None = None) -> None:
        """Stream an additional thought chunk into the reasoning card."""
        self.thought_text += chunk
        self.content_label.set_text(self.thought_text)
        if step_count is not None:
            self.step_count = step_count
            self.steps_badge.set_text(f"{self.step_count} steps")
