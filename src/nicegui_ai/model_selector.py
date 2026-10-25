"""Model and reasoning effort selector primitives with cascading flyout menus."""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

from nicegui import ui

from nicegui_ai.icons import LucideIcon

ReasoningEffort = Literal["low", "medium", "high", "max"]


@dataclass
class ModelOption:
    """Option descriptor for model identity and reasoning effort choices."""

    name: str
    effort: str | None = None
    badge: str | None = None
    effort_options: list[str] = field(default_factory=lambda: ["Low", "Medium", "High"])


class ReasoningEffortSelector(ui.element):
    """Standalone ambient selector for AI reasoning / thinking effort."""

    def __init__(
        self,
        current_effort: str | None = None,
        on_change: Callable[[str | None], None] | None = None,
        variant: Literal["pill", "inline"] = "pill",
        classes: str = "",
    ) -> None:
        super().__init__("div")
        self.classes(f"relative inline-flex items-center {classes}")

        self._current_effort = current_effort
        self._on_change = on_change
        self._variant = variant
        self._effort_checks: dict[str | None, LucideIcon] = {}

        btn_classes = (
            "flex items-center gap-1.5 px-2.5 py-1 rounded-full border border-gray-800 "
            "bg-[#11151f]/80 hover:bg-[#181e2b] hover:border-gray-700 text-xs text-amber-300/90 "
            "hover:text-amber-200 transition-colors cursor-pointer outline-none"
            if variant == "pill"
            else "flex items-center gap-1 py-0.5 px-1 bg-transparent text-xs text-gray-400 "
            "hover:text-gray-200 transition-colors cursor-pointer outline-none border-none font-mono"
        )

        with ui.element("button").classes(btn_classes).props("type=button") as self.btn:
            if variant == "pill":
                LucideIcon("brain", size=13, classes="text-amber-400")

            self.label = ui.label(self._format_label(self._current_effort)).classes(
                "text-xs font-mono"
                if variant == "inline"
                else "text-xs font-mono font-medium"
            )

            LucideIcon(
                "chevron-up" if variant == "inline" else "chevron-down",
                size=12,
                classes="text-gray-400 ml-0.5",
            )

            menu_props = (
                'anchor="top left" self="bottom left"' if variant == "inline" else ""
            )
            with (
                ui.menu()
                .props(menu_props)
                .classes(
                    "p-2 bg-[#0e121a]/95 border border-gray-800 rounded-xl shadow-2xl backdrop-blur min-w-[170px]"
                ) as self.menu
            ):
                ui.label("REASONING EFFORT").classes(
                    "text-[10px] font-mono tracking-wider text-gray-500 px-2 py-1 uppercase"
                )
                efforts: list[tuple[str | None, str]] = [
                    (None, "Off"),
                    ("low", "Low"),
                    ("medium", "Medium"),
                    ("high", "High"),
                    ("max", "Max"),
                ]
                for eff_val, eff_label in efforts:
                    with (
                        ui.menu_item()
                        .classes(
                            "px-2 py-1.5 rounded-lg hover:bg-gray-800/60 cursor-pointer "
                            "text-xs text-gray-300 flex items-center justify-between transition-colors gap-3"
                        )
                        .on(
                            "click",
                            lambda _, v=eff_val: self._handle_select(v),
                        )
                    ):
                        ui.label(eff_label).classes("text-xs")
                        check = LucideIcon(
                            "check",
                            size=12,
                            classes="text-amber-400"
                            if eff_val == self._current_effort
                            else "opacity-0",
                        )
                        self._effort_checks[eff_val] = check

    def _format_label(self, effort: str | None) -> str:
        if effort:
            return effort.capitalize()
        return "Off"

    @property
    def current_effort(self) -> str | None:
        return self._current_effort

    def set_effort(self, effort: str | None, notify: bool = True) -> None:
        self._current_effort = effort
        self.label.text = self._format_label(effort)
        for eff_val, icon in self._effort_checks.items():
            if eff_val == effort:
                icon.classes(remove="opacity-0", add="text-amber-400")
            else:
                icon.classes(remove="text-amber-400", add="opacity-0")
        if notify and self._on_change:
            self._on_change(effort)

    def _handle_select(self, effort: str | None) -> None:
        self.set_effort(effort)
        self.menu.close()


class ModelSelector(ui.element):
    """Ambient glassmorphic dropdown for model identity and cascading reasoning effort selection."""

    def __init__(
        self,
        models: list[str | ModelOption | dict[str, Any]],
        current_model: str,
        reasoning_effort: str | None = None,
        on_change: Callable[[str, str | None], None] | None = None,
        on_view_usage: Callable[[], None] | None = None,
        show_effort_selector: bool = True,
        variant: Literal["pill", "inline"] = "inline",
        classes: str = "",
    ) -> None:
        super().__init__("div")
        self.classes(f"relative inline-flex items-center {classes}")

        ui.add_head_html("""
<style>
.ai-model-menu {
  overflow: visible !important;
}
.ai-model-row {
  position: relative !important;
}
.ai-model-row .ai-model-flyout {
  display: none !important;
}
.ai-model-row:hover > .ai-model-flyout,
.ai-model-row:focus-within > .ai-model-flyout {
  display: flex !important;
}
</style>
""")

        self._model_options: list[ModelOption] = [
            self._normalize_option(m) for m in models
        ]
        self.models: list[str] = [m.name for m in self._model_options]
        self._current_model = current_model
        self._reasoning_effort = reasoning_effort
        self._on_change = on_change
        self._on_view_usage = on_view_usage
        self._show_effort = show_effort_selector
        self._variant = variant

        trigger_classes = (
            "flex items-center gap-1.5 px-2.5 py-1 rounded-full border border-gray-800 "
            "bg-[#11151f]/80 hover:bg-[#181e2b] hover:border-gray-700 text-xs text-gray-300 "
            "hover:text-white transition-colors cursor-pointer outline-none select-none"
            if variant == "pill"
            else "flex items-center gap-1.5 py-0.5 px-1 bg-transparent text-xs text-gray-300 "
            "hover:text-white transition-colors cursor-pointer outline-none border-none font-medium select-none"
        )

        # Trigger button / dock
        with (
            ui.element("button").classes(trigger_classes).props("type=button")
        ) as self.trigger_btn:
            if variant == "pill":
                LucideIcon("sparkles", size=13, classes="text-purple-400")

            self.model_label = ui.label(self._current_model).classes(
                "font-medium text-xs text-gray-200"
            )

            effort_init_text = (
                self._reasoning_effort
                if variant == "inline"
                else (f"• {self._reasoning_effort}" if self._reasoning_effort else "")
            )
            self.effort_badge = ui.label(effort_init_text or "").classes(
                "text-xs text-gray-400 font-normal"
                if variant == "inline"
                else "text-xs text-amber-400 font-mono"
            )
            if not self._reasoning_effort:
                self.effort_badge.set_visibility(False)

            LucideIcon(
                "chevron-up" if variant == "inline" else "chevron-down",
                size=12,
                classes="text-gray-400 ml-0.5",
            )

            # Main Model Menu
            menu_props = (
                'anchor="top left" self="bottom left"' if variant == "inline" else ""
            )
            with (
                ui.menu()
                .props(menu_props)
                .classes(
                    "ai-model-menu p-1.5 bg-[#141822]/98 border border-gray-800/80 rounded-2xl shadow-2xl backdrop-blur-xl min-w-[290px] !overflow-visible"
                ) as self.menu
            ):
                ui.label("Model").classes(
                    "text-xs text-gray-400 font-medium px-3 pt-2 pb-1.5"
                )

                self.model_items: list[ui.element] = []
                for opt in self._model_options:
                    is_active = opt.name == self._current_model

                    with ui.element("div").classes(
                        "ai-model-row relative px-3 py-2 rounded-xl hover:bg-gray-800/60 cursor-pointer "
                        "text-xs text-gray-200 flex items-center justify-between transition-colors gap-3 group"
                    ) as item:
                        # Clicking the row directly chooses this model with default/current effort
                        item.on(
                            "click",
                            lambda _, o=opt: self._handle_model_click(o),
                        )

                        ui.label(opt.name).classes("text-xs font-medium text-gray-200")

                        with ui.row().classes("items-center gap-2"):
                            active_eff = (
                                self._reasoning_effort if is_active else opt.effort
                            )
                            if active_eff:
                                ui.label(active_eff).classes(
                                    "text-xs text-gray-400 font-normal"
                                )

                            if opt.badge:
                                with ui.element("span").classes(
                                    "px-1.5 py-0.5 text-[10px] font-medium rounded-full bg-gray-800/90 text-gray-300 border border-gray-700/50"
                                ):
                                    ui.label(opt.badge)

                            if is_active:
                                LucideIcon("check", size=13, classes="text-gray-200")
                            else:
                                LucideIcon(
                                    "chevron-right",
                                    size=13,
                                    classes="text-gray-500 group-hover:text-gray-300",
                                )

                        # Cascading Flyout Submenu for Reasoning Effort (pure CSS hover driven)
                        if self._show_effort and opt.effort_options:
                            with ui.element("div").classes(
                                "ai-model-flyout flex-col gap-1 absolute left-full -top-1 ml-1.5 "
                                "p-1.5 bg-[#141822]/98 border border-gray-800/80 rounded-xl shadow-2xl backdrop-blur-xl min-w-[120px] z-50 "
                                "before:content-[''] before:absolute before:-left-3 before:top-0 before:w-3 before:h-full"
                            ):
                                for eff in opt.effort_options:
                                    is_eff_active = is_active and (
                                        (self._reasoning_effort or "").lower()
                                        == eff.lower()
                                    )
                                    with (
                                        ui.element("div")
                                        .classes(
                                            "px-3 py-1.5 rounded-lg hover:bg-gray-800/80 cursor-pointer "
                                            "text-xs text-gray-200 flex items-center justify-between transition-colors gap-3 select-none"
                                        )
                                        .on(
                                            "click.stop",
                                            lambda _, m=opt.name, e=eff: (
                                                self.set_model_and_effort(m, e)
                                            ),
                                        )
                                    ):
                                        ui.label(eff).classes("text-xs")
                                        if is_eff_active:
                                            LucideIcon(
                                                "check",
                                                size=13,
                                                classes="text-gray-200",
                                            )

                        self.model_items.append(item)

                # Optional View Usage footer
                if self._on_view_usage is not None:
                    ui.separator().classes("my-1 border-gray-800/80")
                    with (
                        ui.menu_item(auto_close=True)
                        .classes(
                            "px-3 py-2 rounded-xl hover:bg-gray-800/60 cursor-pointer "
                            "text-xs text-gray-400 hover:text-gray-200 flex items-center justify-between transition-colors gap-3 group"
                        )
                        .on("click", self._on_view_usage)
                    ):
                        with ui.row().classes("items-center gap-2"):
                            LucideIcon("gauge", size=14, classes="text-gray-400")
                            ui.label("View Usage").classes("text-xs font-medium")
                        LucideIcon(
                            "chevron-right",
                            size=13,
                            classes="text-gray-500 group-hover:text-gray-300",
                        )

        # Backward compatibility aliases
        self.model_btn = self.trigger_btn
        self.model_menu = self.menu
        self.effort_btn = self.trigger_btn
        self.effort_menu = None
        self.effort_selector = None

    def _normalize_option(
        self, item: str | ModelOption | dict[str, Any]
    ) -> ModelOption:
        if isinstance(item, ModelOption):
            return item
        if isinstance(item, dict):
            return ModelOption(
                name=item["name"],
                effort=item.get("effort"),
                badge=item.get("badge"),
                effort_options=item.get("effort_options", ["Low", "Medium", "High"]),
            )
        # Default string option
        name = str(item)
        effort = (
            "Medium"
            if any(k in name.lower() for k in ["opus", "argon", "sonnet"])
            else ("High" if "flash" in name.lower() else None)
        )
        return ModelOption(
            name=name,
            effort=effort,
            badge="New"
            if any(k in name.lower() for k in ["argon", "opus", "sonnet"])
            else None,
            effort_options=["Low", "Medium", "High"],
        )

    @property
    def current_model(self) -> str:
        return self._current_model

    @property
    def reasoning_effort(self) -> str | None:
        return self._reasoning_effort

    def set_model(self, model: str) -> None:
        self.set_model_and_effort(model, self._reasoning_effort)

    def set_reasoning_effort(self, effort: str | None) -> None:
        self.set_model_and_effort(self._current_model, effort)

    def set_model_and_effort(self, model: str, effort: str | None) -> None:
        self._current_model = model
        self._reasoning_effort = effort
        self.model_label.text = model

        if effort:
            self.effort_badge.text = (
                effort if self._variant == "inline" else f"• {effort}"
            )
            self.effort_badge.set_visibility(True)
        else:
            self.effort_badge.text = ""
            self.effort_badge.set_visibility(False)

        self.menu.close()

        if self._on_change:
            self._on_change(self._current_model, self._reasoning_effort)

    def _handle_model_click(self, opt: ModelOption) -> None:
        target_effort = (
            self._reasoning_effort
            if opt.name == self._current_model
            else (opt.effort or self._reasoning_effort or "Medium")
        )
        self.set_model_and_effort(opt.name, target_effort)
