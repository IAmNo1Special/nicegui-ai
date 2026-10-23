"""Collapsible reasoning card for displaying AI model thinking steps."""

from nicegui import ui


class ReasoningCard(ui.expansion):
    """Amber-gilded card displaying model reasoning steps and chain-of-thought."""

    def __init__(
        self,
        thought_text: str = "",
        step_count: int = 1,
        default_open: bool = False,
    ) -> None:
        super().__init__(value=default_open)
        self.thought_text = thought_text
        self.step_count = step_count

        self.classes(
            "w-full rounded-xl border border-amber-500/30 bg-[#161410] "
            "text-xs text-amber-200 overflow-hidden shadow-sm my-2 transition-all"
        )
        self.props("dense header-class='p-2 px-3 bg-[#1d1912] hover:bg-[#231e16]'")

        with self.add_slot("header"):
            with ui.row().classes("items-center justify-between w-full pr-1"):
                with ui.row().classes("items-center gap-2"):
                    ui.icon("psychology").classes("text-amber-400 text-sm")
                    ui.label("Reasoning (Thinking Process)").classes(
                        "font-semibold text-amber-300 text-xs"
                    )
                self.steps_badge = ui.label(f"{self.step_count} steps").classes(
                    "text-[10px] font-mono text-amber-400/80 bg-amber-950/60 "
                    "px-1.5 py-0.5 rounded border border-amber-500/20"
                )

        with (
            self,
            ui.column().classes(
                "p-3 bg-[#100e0b] w-full text-amber-200/90 font-mono text-[11px] "
                "leading-relaxed whitespace-pre-wrap border-t border-amber-500/20"
            ),
        ):
            self.content_label = ui.label(self.thought_text).classes(
                "w-full select-text whitespace-pre-wrap"
            )

    def append_thought(self, chunk: str, step_count: int | None = None) -> None:
        """Stream an additional thought chunk into the reasoning card."""
        self.thought_text += chunk
        self.content_label.set_text(self.thought_text)
        if step_count is not None:
            self.step_count = step_count
            self.steps_badge.set_text(f"{self.step_count} steps")
