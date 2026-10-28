"""1:1 Antigravity Model Selector with side-by-side Reasoning Effort flyout."""

from collections.abc import Callable
from dataclasses import dataclass, field

from nicegui import ui

from nicegui_ai.antigravity.icons import AntigravityIcon


@dataclass
class AntigravityModelDef:
    id: str
    name: str
    short_name: str
    badge: str | None = None
    efforts: list[str] = field(default_factory=lambda: ["Low", "Medium", "High", "Max"])
    default_effort: str | None = "High"


ANTIGRAVITY_MODELS: list[AntigravityModelDef] = [
    AntigravityModelDef(
        id="gemini-3.8-flash",
        name="Gemini 3.8 Flash",
        short_name="Gemini 3.8 Flash",
        badge="Fast",
        efforts=["Low", "Medium", "High", "Max"],
        default_effort="High",
    ),
    AntigravityModelDef(
        id="gemini-3.1-pro",
        name="Gemini 3.1 Pro",
        short_name="Gemini 3.1 Pro",
        badge="Hybrid",
        efforts=["Low", "Medium", "High", "Max"],
        default_effort="High",
    ),
    AntigravityModelDef(
        id="gemini-omni-1.1-flash",
        name="Gemini Omni 1.1 Flash",
        short_name="Gemini Omni 1.1 Flash",
        badge="Multimodal",
        efforts=["Low", "Medium", "High"],
        default_effort="Medium",
    ),
    AntigravityModelDef(
        id="claude-3.7-sonnet",
        name="Claude 3.7 Sonnet",
        short_name="Claude 3.7 Sonnet",
        efforts=["Low", "Medium", "High"],
        default_effort="High",
    ),
    AntigravityModelDef(
        id="gpt-oss-120b",
        name="GPT-OSS 120B",
        short_name="GPT-OSS 120B",
        efforts=["Medium", "High"],
        default_effort="Medium",
    ),
]


class AntigravityModelSelector(ui.element):
    """Upward model picker popover with side-by-side reasoning effort flyout."""

    def __init__(
        self,
        selected_model: str = "Gemini 3.8 Flash High",
        on_select_model: Callable[[str], None] | None = None,
        on_open_models_settings: Callable[[], None] | None = None,
        initial_open: bool = False,
    ) -> None:
        super().__init__("div")
        self.selected_model = selected_model
        self.on_select_model = on_select_model
        self.on_open_models_settings = on_open_models_settings
        self.is_open: bool = initial_open
        self.hovered_model_id: str = "gemini-3.8-flash"

        self.classes("relative inline-flex items-center")
        self.render_selector()

    def _parse_selected(self) -> tuple[AntigravityModelDef, str | None]:
        for m in ANTIGRAVITY_MODELS:
            if self.selected_model.startswith(m.short_name):
                rest = self.selected_model.removeprefix(m.short_name).strip()
                return m, (rest if rest else m.default_effort)
        return ANTIGRAVITY_MODELS[0], "High"

    def _choose_model(self, model_def: AntigravityModelDef, effort: str | None) -> None:
        eff = effort or model_def.default_effort
        full = f"{model_def.short_name} {eff}".strip() if eff else model_def.short_name
        self.selected_model = full
        self.is_open = False
        self.render_selector()
        if self.on_select_model:
            self.on_select_model(full)

    def _toggle_open(self) -> None:
        self.is_open = not self.is_open
        self.render_selector()

    def render_selector(self) -> None:
        self.clear()
        active_def, active_effort = self._parse_selected()
        hovered_def = next(
            (m for m in ANTIGRAVITY_MODELS if m.id == self.hovered_model_id),
            active_def,
        )

        with self:
            # Trigger Button
            with (
                ui.element("button")
                .props('type="button" data-testid="model-selector-trigger"')
                .classes(
                    "inline-flex items-center gap-1 h-7 px-2 py-1 rounded-lg bg-transparent "
                    "hover:bg-[#272727] text-[#888888] hover:text-[#cccccc] "
                    "text-xs border-none cursor-pointer transition-colors select-none"
                )
                .on("click", self._toggle_open)
            ):
                ui.label(active_def.short_name).classes(
                    "font-medium text-[#cccccc] truncate"
                )
                if active_effort:
                    ui.label(active_effort).classes("text-[#888888]")
                AntigravityIcon(
                    "model_arrow",
                    size=14,
                    classes="text-[#888888] ml-0.5 "
                    + ("" if self.is_open else "rotate-180"),
                )

            # Upward Two-Column Popover
            if self.is_open:
                with (
                    ui.element("div")
                    .props('data-testid="model-selector-popover"')
                    .classes(
                        "absolute bottom-full right-0 mb-2 flex flex-row flex-nowrap items-start gap-1.5 z-50 select-none"
                    )
                    .style(
                        "display: flex !important; flex-direction: row !important; flex-wrap: nowrap !important;"
                    )
                ):
                    # Left Column: Model List
                    with ui.element("div").classes(
                        "w-64 bg-[#191919] border border-[#272727] rounded-xl shadow-2xl p-1.5 flex flex-col gap-0.5 shrink-0"
                    ):
                        with ui.element("div").classes(
                            "px-2.5 py-1 text-[11px] font-medium text-[#888888] flex items-center justify-between"
                        ):
                            ui.label("Select Model")
                            ui.label("Effort ▸").classes(
                                "text-[10px] font-mono text-[#6e6e6e]"
                            )

                        for m in ANTIGRAVITY_MODELS:
                            is_curr = m.id == active_def.id
                            is_hov = m.id == hovered_def.id
                            row_cls = (
                                "w-full text-left px-2.5 py-1.5 rounded-lg flex items-center justify-between "
                                "text-xs cursor-pointer transition-colors border-none "
                                + (
                                    "bg-[#272727] text-[#cccccc] font-medium"
                                    if is_curr or is_hov
                                    else "bg-transparent text-[#888888] hover:bg-[#272727] hover:text-[#cccccc]"
                                )
                            )
                            with (
                                ui.element("button")
                                .props(
                                    f'type="button" data-testid="model-option-{m.id}"'
                                )
                                .classes(row_cls)
                                .on(
                                    "mouseenter",
                                    lambda _, mid=m.id: self._set_hovered(mid),
                                )
                                .on(
                                    "click",
                                    lambda _, mod=m: self._choose_model(
                                        mod, mod.default_effort
                                    ),
                                )
                            ):
                                with ui.element("div").classes(
                                    "flex items-center gap-1.5 truncate"
                                ):
                                    ui.label(m.name).classes("truncate")
                                    if m.badge:
                                        ui.label(m.badge).classes(
                                            "text-[10px] px-1.5 py-0.2 rounded bg-[#101010] text-[#888888] border border-[#272727]"
                                        )
                                with ui.element("div").classes(
                                    "flex items-center gap-1 shrink-0"
                                ):
                                    eff_txt = (
                                        active_effort if is_curr else m.default_effort
                                    )
                                    if eff_txt:
                                        ui.label(eff_txt).classes(
                                            "text-[11px] text-[#888888]"
                                        )
                                    AntigravityIcon(
                                        "check" if is_curr else "chevron_right",
                                        size=13,
                                        classes="text-[#cccccc]"
                                        if is_curr
                                        else "text-[#6e6e6e]",
                                    )

                        ui.element("div").classes("my-1 border-t border-[#272727]")

                        with (
                            ui.element("button")
                            .props(
                                'type="button" data-testid="model-view-usage-button"'
                            )
                            .classes(
                                "w-full text-left px-2.5 py-1.5 rounded-lg hover:bg-[#272727] "
                                "text-xs text-[#888888] hover:text-[#cccccc] flex items-center "
                                "justify-between border-none bg-transparent cursor-pointer"
                            )
                            .on("click", self._handle_open_usage)
                        ):
                            ui.label("View Usage & Quotas")
                            AntigravityIcon(
                                "chevron_right", size=13, classes="text-[#6e6e6e]"
                            )

                    # Right Side-by-Side Flyout: Reasoning Effort
                    if hovered_def.efforts:
                        with (
                            ui.element("div")
                            .props('data-testid="model-effort-flyout"')
                            .classes(
                                "w-44 bg-[#191919] border border-[#272727] rounded-xl shadow-2xl p-1.5 flex flex-col gap-0.5 shrink-0"
                            )
                        ):
                            ui.label(f"{hovered_def.short_name} Effort").classes(
                                "px-2.5 py-1 text-[11px] font-medium text-[#888888] truncate"
                            )
                            for eff in hovered_def.efforts:
                                is_eff_sel = (
                                    hovered_def.id == active_def.id
                                    and active_effort == eff
                                )
                                eff_cls = (
                                    "w-full text-left px-2.5 py-1.5 rounded-lg flex items-center justify-between "
                                    "text-xs cursor-pointer transition-colors border-none "
                                    + (
                                        "bg-[#272727] text-[#cccccc] font-medium"
                                        if is_eff_sel
                                        else "bg-transparent text-[#888888] hover:bg-[#272727] hover:text-[#cccccc]"
                                    )
                                )
                                with (
                                    ui.element("button")
                                    .props(
                                        f'type="button" data-testid="effort-option-{eff.lower()}"'
                                    )
                                    .classes(eff_cls)
                                    .on(
                                        "click",
                                        lambda _, mod=hovered_def, e=eff: (
                                            self._choose_model(mod, e)
                                        ),
                                    )
                                ):
                                    ui.label(eff)
                                    if is_eff_sel:
                                        AntigravityIcon(
                                            "check", size=13, classes="text-[#cccccc]"
                                        )

    def _set_hovered(self, model_id: str) -> None:
        if self.hovered_model_id != model_id:
            self.hovered_model_id = model_id
            self.render_selector()

    def _handle_open_usage(self) -> None:
        self.is_open = False
        self.render_selector()
        if self.on_open_models_settings:
            self.on_open_models_settings()
