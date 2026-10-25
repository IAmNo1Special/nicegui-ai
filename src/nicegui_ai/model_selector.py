"""Model and reasoning effort selector primitive."""

from collections.abc import Callable
from typing import Literal

from nicegui import ui

from nicegui_ai.icons import LucideIcon

ReasoningEffort = Literal["low", "medium", "high", "max"]


class ModelSelector(ui.element):
    """Ambient glassmorphic pill dropdown for model identity and reasoning effort control."""

    def __init__(
        self,
        models: list[str],
        current_model: str,
        reasoning_effort: str | None = None,
        on_change: Callable[[str, str | None], None] | None = None,
        show_effort_selector: bool = True,
        variant: Literal["pill", "inline"] = "pill",
        classes: str = "",
    ) -> None:
        super().__init__("div")
        self.classes(f"relative inline-flex items-center {classes}")

        self.models = models
        self._current_model = current_model
        self._reasoning_effort = reasoning_effort
        self._on_change = on_change
        self._show_effort = show_effort_selector
        self._variant = variant

        btn_classes = (
            "flex items-center gap-1.5 px-2.5 py-1 rounded-full border border-gray-800 "
            "bg-[#11151f]/80 hover:bg-[#181e2b] hover:border-gray-700 text-xs text-gray-300 "
            "hover:text-white transition-colors cursor-pointer outline-none"
            if variant == "pill"
            else "flex items-center gap-1.5 py-0.5 px-1 bg-transparent text-xs text-gray-400 "
            "hover:text-gray-200 transition-colors cursor-pointer outline-none border-none"
        )

        # Trigger button
        with (
            ui.element("button").classes(btn_classes).props("type=button")
        ) as self.trigger_btn:
            if variant == "pill":
                LucideIcon("sparkles", size=13, classes="text-purple-400")

            self.model_label = ui.label(self._current_model).classes(
                "font-medium text-xs text-gray-200"
            )

            effort_display = (
                f"{self._reasoning_effort.capitalize()}"
                if variant == "inline" and self._reasoning_effort
                else f"• {self._reasoning_effort}"
                if self._reasoning_effort
                else ""
            )
            self.effort_badge = ui.label(effort_display).classes(
                "text-[10px] text-gray-400 font-mono"
                if variant == "inline"
                else "text-[10px] text-amber-400 font-mono"
            )
            if not self._reasoning_effort:
                self.effort_badge.set_visibility(False)

            LucideIcon(
                "chevron-up" if variant == "inline" else "chevron-down",
                size=12,
                classes="text-gray-400 ml-0.5",
            )

            # Dropdown menu
            menu_props = (
                'anchor="top left" self="bottom left"' if variant == "inline" else ""
            )
            with (
                ui.menu()
                .props(menu_props)
                .classes(
                    "p-2 bg-[#0e121a]/95 border border-gray-800 rounded-xl shadow-2xl backdrop-blur min-w-[200px]"
                ) as self.menu
            ):
                ui.label("MODEL").classes(
                    "text-[10px] font-mono tracking-wider text-gray-500 px-2 py-1 uppercase"
                )
                self.model_items: list[ui.element] = []
                for m in self.models:
                    with (
                        ui.menu_item()
                        .classes(
                            "px-2 py-1.5 rounded-lg hover:bg-gray-800/60 cursor-pointer "
                            "text-xs text-gray-300 flex items-center justify-between transition-colors"
                        )
                        .on(
                            "click",
                            lambda _, selected=m: self._handle_model_select(selected),
                        )
                    ) as item:
                        ui.label(selected_model_name := m).classes("text-xs")
                        check = LucideIcon(
                            "check",
                            size=12,
                            classes="text-purple-400"
                            if selected_model_name == self._current_model
                            else "opacity-0",
                        )
                        item._check_icon = check  # type: ignore[attr-defined]
                        self.model_items.append(item)

                if self._show_effort:
                    ui.separator().classes("my-1.5 border-gray-800")
                    ui.label("REASONING EFFORT").classes(
                        "text-[10px] font-mono tracking-wider text-gray-500 px-2 py-1 uppercase"
                    )
                    efforts: list[str | None] = [None, "low", "medium", "high", "max"]
                    for eff in efforts:
                        label_text = eff.capitalize() if eff else "Off"
                        with (
                            ui.menu_item()
                            .classes(
                                "px-2 py-1 rounded-lg hover:bg-gray-800/60 cursor-pointer "
                                "text-xs text-gray-300 flex items-center justify-between transition-colors"
                            )
                            .on(
                                "click",
                                lambda _, selected_eff=eff: self._handle_effort_select(
                                    selected_eff
                                ),
                            )
                        ):
                            ui.label(label_text).classes("text-xs")
                            if eff == self._reasoning_effort:
                                LucideIcon("check", size=12, classes="text-amber-400")

    @property
    def current_model(self) -> str:
        return self._current_model

    @property
    def reasoning_effort(self) -> str | None:
        return self._reasoning_effort

    def set_model(self, model: str) -> None:
        self._current_model = model
        self.model_label.text = model
        if self._on_change:
            self._on_change(self._current_model, self._reasoning_effort)

    def set_reasoning_effort(self, effort: str | None) -> None:
        self._reasoning_effort = effort
        if effort:
            self.effort_badge.text = (
                effort.capitalize() if self._variant == "inline" else f"• {effort}"
            )
            self.effort_badge.set_visibility(True)
        else:
            self.effort_badge.text = ""
            self.effort_badge.set_visibility(False)

        if self._on_change:
            self._on_change(self._current_model, self._reasoning_effort)

    def _handle_model_select(self, model: str) -> None:
        self.set_model(model)
        self.menu.close()

    def _handle_effort_select(self, effort: str | None) -> None:
        self.set_reasoning_effort(effort)
        self.menu.close()
