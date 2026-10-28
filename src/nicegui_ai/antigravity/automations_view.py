"""1:1 Antigravity Automations View (K1b), New Automation Modal (I1b), & Detail Schedule Editor (B1b / A1b)."""

from collections.abc import Callable
from typing import Literal

from nicegui import ui

from nicegui_ai.antigravity.icons import AntigravityIcon
from nicegui_ai.antigravity.state import AutomationItem, ProjectConfig


class AutomationsView(ui.element):
    """Full Automations view supporting list, New Automation modal, and Schedule Detail editor."""

    def __init__(
        self,
        automations: list[AutomationItem],
        projects: list[ProjectConfig],
        on_toggle_automation: Callable[[str], None],
        on_delete_automation: Callable[[str], None],
        on_create_automation: Callable[[AutomationItem], None],
        on_update_automation: Callable[[AutomationItem], None],
        on_run_automation_now: Callable[[AutomationItem], None],
        initial_modal_open: bool = False,
        initial_selected_trigger_id: str | None = None,
    ) -> None:
        super().__init__("div")
        self.automations = automations
        self.projects = projects
        self.on_toggle_automation = on_toggle_automation
        self.on_delete_automation = on_delete_automation
        self.on_create_automation = on_create_automation
        self.on_update_automation = on_update_automation
        self.on_run_automation_now = on_run_automation_now

        self.modal_open: bool = initial_modal_open
        self.selected_trigger_id: str | None = initial_selected_trigger_id
        self.trigger_category: Literal["time", "event"] = "time"
        self.editing_title: bool = False

        # New automation draft fields
        self.draft_name: str = ""
        self.draft_prompt: str = ""
        self.draft_project_id: str = (
            projects[3].id
            if len(projects) > 3
            else (projects[0].id if projects else "")
        )
        self.draft_frequency: Literal["daily", "weekly", "hourly", "weekdays"] = "daily"
        self.draft_hour: str = "9:00 AM"

        self.props('data-testid="cloud-triggers-view"')
        self.classes(
            "flex-1 flex flex-col h-full bg-background text-foreground overflow-y-auto relative"
        )
        self.render_view()

    def render_view(self) -> None:
        self.clear()
        selected_item = next(
            (a for a in self.automations if a.id == self.selected_trigger_id), None
        )

        with self:
            if selected_item is not None:
                self._render_detail_editor(selected_item)
            else:
                self._render_list_view()

            if self.modal_open:
                self._render_new_modal()

    def _render_list_view(self) -> None:
        with ui.element("div").classes(
            "w-full max-w-3xl mx-auto p-8 space-y-6 pb-20 flex flex-col"
        ):
            # Header
            with ui.element("div").classes("flex items-center justify-between gap-4"):
                with ui.element("div").classes("flex flex-col gap-1"):
                    ui.label("Automations").classes(
                        "text-lg font-medium text-foreground select-none"
                    )
                    ui.label(
                        "Schedule recurring background agent tasks and repository event triggers."
                    ).classes("text-xs text-muted-foreground")

                with ui.element("div").classes("flex items-center gap-2"):
                    with (
                        ui.element("button")
                        .props('type="button" data-testid="sidecar-create-with-prompt"')
                        .classes(
                            "inline-flex items-center gap-1.5 h-8 px-3 rounded-lg bg-card "
                            "hover:bg-secondary text-secondary-foreground hover:text-foreground "
                            "text-xs border border-card-border cursor-pointer transition-colors"
                        )
                        .on("click", self._open_modal)
                    ):
                        AntigravityIcon("sparkles", size=14, classes="text-primary")
                        ui.label("Create with Prompt")

                    with (
                        ui.element("button")
                        .props('type="button" data-testid="cloud-trigger-new-button"')
                        .classes(
                            "inline-flex items-center gap-1.5 h-8 px-3 rounded-lg bg-secondary "
                            "hover:bg-secondary/80 text-foreground text-xs font-medium "
                            "border border-card-border cursor-pointer transition-colors"
                        )
                        .on("click", self._open_modal)
                    ):
                        AntigravityIcon("plus", size=14)
                        ui.label("New Automation")

            # Triggers List Card
            with ui.element("div").classes(
                "border border-card-border rounded-xl overflow-hidden bg-card divide-y divide-border flex flex-col"
            ):
                for item in self.automations:
                    proj = next(
                        (p for p in self.projects if p.id == item.project_id), None
                    )
                    with (
                        ui.element("div")
                        .props('data-testid="cloud-trigger-row"')
                        .classes(
                            "flex items-center justify-between gap-4 px-4 py-3.5 hover:bg-secondary/40 "
                            "cursor-pointer transition-colors"
                        )
                        .on(
                            "click",
                            lambda _, aid=item.id: self._select_trigger(aid),
                        )
                    ):
                        with ui.element("div").classes(
                            "flex flex-col gap-1 min-w-0 flex-1"
                        ):
                            with ui.element("div").classes("flex items-center gap-2"):
                                AntigravityIcon(
                                    "automations",
                                    size=15,
                                    classes="text-primary"
                                    if item.enabled
                                    else "text-muted-foreground",
                                )
                                ui.label(item.display_name).classes(
                                    "text-sm font-medium text-foreground truncate"
                                )
                                if proj:
                                    ui.label(proj.name).classes(
                                        "text-[10px] px-1.5 py-0.2 rounded bg-secondary text-secondary-foreground border border-card-border"
                                    )
                            ui.label(item.prompt).classes(
                                "text-xs text-muted-foreground truncate"
                            )
                            with ui.element("div").classes(
                                "flex items-center gap-2 text-[11px] text-muted-foreground/80 font-mono"
                            ):
                                ui.label(item.schedule_summary)
                                if item.last_run:
                                    ui.label(f"• Last run: {item.last_run}")

                        with ui.element("div").classes(
                            "flex items-center gap-2 shrink-0"
                        ):
                            with (
                                ui.element("button")
                                .props('type="button"')
                                .classes(
                                    "px-2.5 py-1 rounded-md bg-secondary/80 hover:bg-secondary "
                                    "text-xs text-foreground border border-card-border cursor-pointer"
                                )
                                .on(
                                    "click.stop",
                                    lambda _, it=item: self.on_run_automation_now(it),
                                )
                            ):
                                ui.label("Run Now")

                            with (
                                ui.element("button")
                                .props(
                                    'type="button" role="switch" '
                                    f'aria-checked="{str(item.enabled).lower()}" '
                                    'data-testid="cloud-trigger-enable-toggle"'
                                )
                                .classes(
                                    "relative inline-flex h-4 w-7 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors "
                                    + ("bg-primary" if item.enabled else "bg-secondary")
                                )
                                .on(
                                    "click.stop",
                                    lambda _, aid=item.id: self._toggle_and_refresh(
                                        aid
                                    ),
                                )
                            ):
                                ui.element("span").classes(
                                    "pointer-events-none inline-block h-3 w-3 transform rounded-full bg-white shadow transition "
                                    + (
                                        "translate-x-3"
                                        if item.enabled
                                        else "translate-x-0"
                                    )
                                )

    def _render_detail_editor(self, item: AutomationItem) -> None:
        proj = next(
            (p for p in self.projects if p.id == item.project_id),
            self.projects[0] if self.projects else None,
        )
        with (
            ui.element("div")
            .props('data-testid="cloud-trigger-detail"')
            .classes("w-full max-w-2xl mx-auto p-8 space-y-6 pb-20 flex flex-col")
        ):
            # Top Title Bar
            with ui.element("div").classes("flex items-center justify-between gap-4"):
                with ui.element("div").classes("flex items-center gap-2 min-w-0"):
                    ui.label(item.display_name).classes(
                        "text-lg font-medium text-foreground truncate"
                    )
                    ui.label("✎").classes(
                        "text-xs text-muted-foreground cursor-pointer hover:text-foreground"
                    )

                with ui.element("div").classes("flex items-center gap-2"):
                    with (
                        ui.element("button")
                        .props('type="button"')
                        .classes(
                            "h-8 px-3 rounded-lg bg-secondary hover:bg-secondary/80 "
                            "text-xs text-foreground border border-card-border cursor-pointer"
                        )
                        .on("click", lambda: self.on_run_automation_now(item))
                    ):
                        ui.label("Run Now")
                    with (
                        ui.element("button")
                        .props('type="button" aria-label="Close detail"')
                        .classes(
                            "h-8 w-8 rounded-lg hover:bg-secondary text-muted-foreground "
                            "hover:text-foreground bg-transparent border-none cursor-pointer flex items-center justify-center"
                        )
                        .on("click", lambda: self._select_trigger(None))
                    ):
                        AntigravityIcon("close", size=14)

            # Editor Panel (A1b)
            with (
                ui.element("div")
                .props('data-testid="cloud-trigger-editor-panel"')
                .classes("space-y-5 flex flex-col")
            ):
                # Prompt Section
                with ui.element("div").classes("space-y-1.5 flex flex-col"):
                    with ui.element("div").classes(
                        "flex items-center justify-between text-xs"
                    ):
                        ui.label("Prompt").classes("text-muted-foreground font-medium")
                        ui.label("Runs as Gemini 3.8 Flash").classes(
                            "text-[11px] font-mono text-muted-foreground"
                        )
                    with ui.element("div").classes(
                        "p-3.5 rounded-xl border border-card-border bg-card text-xs text-foreground leading-relaxed min-h-[96px]"
                    ):
                        ui.label(item.prompt)

                # Workspace Selector
                with ui.element("div").classes("space-y-1.5 flex flex-col"):
                    ui.label("Workspace").classes(
                        "text-xs text-muted-foreground font-medium"
                    )
                    with ui.element("div").classes(
                        "flex items-center justify-between h-9 px-3 rounded-xl border border-card-border bg-card text-xs text-foreground"
                    ):
                        with ui.element("div").classes("flex items-center gap-2"):
                            AntigravityIcon(
                                "folder", size=14, classes="text-muted-foreground"
                            )
                            folder_str = (
                                f" ({proj.folders[0]})" if proj and proj.folders else ""
                            )
                            ui.label(
                                f"{proj.name if proj else 'Workspace'}{folder_str}"
                            )
                        AntigravityIcon(
                            "chevron_down",
                            size=14,
                            classes="text-muted-foreground",
                        )

                # Trigger Schedule vs Event
                with ui.element("div").classes("space-y-2 flex flex-col"):
                    with ui.element("div").classes("flex items-center justify-between"):
                        ui.label("Trigger").classes(
                            "text-xs text-muted-foreground font-medium"
                        )
                        with ui.element("div").classes(
                            "flex items-center rounded-lg border border-card-border bg-card p-0.5 text-xs"
                        ):
                            with (
                                ui.element("button")
                                .props(
                                    'type="button" data-testid="trigger-category-time"'
                                )
                                .classes(
                                    "px-2.5 py-1 rounded-md text-xs border-none cursor-pointer "
                                    + (
                                        "bg-secondary text-foreground font-medium"
                                        if self.trigger_category == "time"
                                        else "bg-transparent text-muted-foreground"
                                    )
                                )
                                .on(
                                    "click",
                                    lambda: self._set_trigger_category("time"),
                                )
                            ):
                                ui.label("Schedule")
                            with (
                                ui.element("button")
                                .props(
                                    'type="button" data-testid="trigger-category-event"'
                                )
                                .classes(
                                    "px-2.5 py-1 rounded-md text-xs border-none cursor-pointer "
                                    + (
                                        "bg-secondary text-foreground font-medium"
                                        if self.trigger_category == "event"
                                        else "bg-transparent text-muted-foreground"
                                    )
                                )
                                .on(
                                    "click",
                                    lambda: self._set_trigger_category("event"),
                                )
                            ):
                                ui.label("Event")

                    with (
                        ui.element("div")
                        .props('data-testid="schedule-editor-panel"')
                        .classes(
                            "p-4 rounded-xl border border-card-border bg-card space-y-3 flex flex-col"
                        )
                    ):
                        with ui.element("div").classes(
                            "flex items-center gap-2 text-xs text-foreground"
                        ):
                            with ui.element("div").classes(
                                "px-3 py-1.5 rounded-lg border border-card-border bg-background flex items-center gap-2"
                            ):
                                ui.label(
                                    "Every day"
                                    if item.frequency == "daily"
                                    else f"Every {item.day_of_week or 'Monday'}"
                                )
                                AntigravityIcon("chevron_down", size=12)
                            ui.label("at").classes("text-muted-foreground")
                            with ui.element("div").classes(
                                "px-3 py-1.5 rounded-lg border border-card-border bg-background flex items-center gap-2"
                            ):
                                ui.label(item.hour)
                                AntigravityIcon("chevron_down", size=12)

                        with (
                            ui.element("div")
                            .props('data-testid="schedule-timezone"')
                            .classes(
                                "flex items-center justify-between text-xs pt-1 border-t border-card-border/60"
                            )
                        ):
                            ui.label("Timezone").classes("text-muted-foreground")
                            ui.label("America/New_York (EDT, UTC-4)").classes(
                                "font-mono text-secondary-foreground"
                            )

                # Save / Reset Footer
                with ui.element("div").classes("flex justify-end gap-2"):
                    with ui.element("button").classes(
                        "h-8 px-3 rounded-lg bg-card text-muted-foreground text-xs border border-card-border cursor-pointer"
                    ):
                        ui.label("Reset")
                    with ui.element("button").classes(
                        "h-8 px-3 rounded-lg bg-secondary text-foreground text-xs border border-card-border cursor-pointer"
                    ):
                        ui.label("Save Changes")

                # Recent Runs Section
                with ui.element("div").classes(
                    "pt-4 border-t border-card-border space-y-2.5 flex flex-col"
                ):
                    ui.label("Recent Runs").classes(
                        "text-xs text-muted-foreground font-medium"
                    )
                    with ui.element("div").classes(
                        "border border-card-border rounded-xl bg-card divide-y divide-border overflow-hidden flex flex-col"
                    ):
                        runs = [
                            (
                                "run-482",
                                "14.2s",
                                "2h ago",
                                "Verified 315 data-testids and 26 Chromium screenshots with 0 diffs.",
                            ),
                            (
                                "run-481",
                                "18.7s",
                                "1d ago",
                                "Completed typecheck and bundle parity check on main.",
                            ),
                        ]
                        for run_id, dur, ago, desc in runs:
                            with ui.element("div").classes(
                                "flex items-center justify-between px-4 py-3 text-xs"
                            ):
                                with ui.element("div").classes("flex flex-col gap-0.5"):
                                    with ui.element("div").classes(
                                        "flex items-center gap-2"
                                    ):
                                        ui.element("span").classes(
                                            "w-2 h-2 rounded-full bg-emerald-400"
                                        )
                                        ui.label("Succeeded").classes(
                                            "text-foreground font-medium"
                                        )
                                        ui.label(f"{run_id} • {dur}").classes(
                                            "font-mono text-[11px] text-muted-foreground"
                                        )
                                    ui.label(desc).classes("text-muted-foreground")
                                ui.label(ago).classes(
                                    "text-[11px] text-muted-foreground shrink-0"
                                )

    def _render_new_modal(self) -> None:
        with (
            ui.element("div")
            .props('data-testid="new-cloud-trigger-modal"')
            .classes(
                "fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-xs p-4"
            )
        ):
            with ui.element("div").classes(
                "w-[640px] max-w-full rounded-xl border border-card-border bg-card shadow-2xl p-6 space-y-5 flex flex-col"
            ):
                with ui.element("div").classes("flex items-center justify-between"):
                    ui.label("New Automation").classes(
                        "text-base font-medium text-foreground"
                    )
                    with (
                        ui.element("button")
                        .props('type="button"')
                        .classes(
                            "h-7 w-7 rounded-lg hover:bg-secondary text-muted-foreground hover:text-foreground bg-transparent border-none cursor-pointer flex items-center justify-center"
                        )
                        .on("click", self._close_modal)
                    ):
                        AntigravityIcon("close", size=14)

                with ui.element("div").classes("space-y-4 flex flex-col"):
                    with ui.element("div").classes("space-y-1 flex flex-col"):
                        ui.label("Automation Name").classes(
                            "text-xs text-muted-foreground"
                        )
                        name_inp = (
                            ui.input(placeholder="e.g., Daily REA Bundle Parity Audit")
                            .props("dense borderless")
                            .classes(
                                "w-full h-9 px-3 rounded-lg border border-card-border bg-background text-xs text-foreground"
                            )
                        )
                        name_inp.bind_value(self, "draft_name")

                    with ui.element("div").classes("space-y-1 flex flex-col"):
                        ui.label("Agent Prompt").classes(
                            "text-xs text-muted-foreground"
                        )
                        prompt_inp = (
                            ui.textarea(
                                placeholder="Describe what the background agent should inspect, test, or report..."
                            )
                            .props("dense borderless rows=3")
                            .classes(
                                "w-full p-3 rounded-lg border border-card-border bg-background text-xs text-foreground"
                            )
                        )
                        prompt_inp.bind_value(self, "draft_prompt")

                    with ui.element("div").classes("grid grid-cols-2 gap-3"):
                        with ui.element("div").classes(
                            "p-3 rounded-lg border border-card-border bg-background text-xs flex items-center justify-between"
                        ):
                            ui.label("Frequency: Every day")
                            AntigravityIcon("chevron_down", size=12)
                        with ui.element("div").classes(
                            "p-3 rounded-lg border border-card-border bg-background text-xs flex items-center justify-between"
                        ):
                            ui.label("Time: 9:00 AM")
                            AntigravityIcon("chevron_down", size=12)

                with ui.element("div").classes(
                    "flex items-center justify-end gap-2 pt-2 border-t border-card-border"
                ):
                    with (
                        ui.element("button")
                        .props('type="button"')
                        .classes(
                            "h-8 px-3 rounded-lg bg-transparent hover:bg-secondary text-xs text-muted-foreground hover:text-foreground border-none cursor-pointer"
                        )
                        .on("click", self._close_modal)
                    ):
                        ui.label("Cancel")
                    with (
                        ui.element("button")
                        .props('type="button" data-testid="create-automation-submit"')
                        .classes(
                            "h-8 px-4 rounded-lg bg-primary text-primary-foreground text-xs font-medium border-none cursor-pointer"
                        )
                        .on("click", self._submit_new_automation)
                    ):
                        ui.label("Create Automation")

    def _open_modal(self) -> None:
        self.modal_open = True
        self.render_view()

    def _close_modal(self) -> None:
        self.modal_open = False
        self.render_view()

    def _select_trigger(self, trigger_id: str | None) -> None:
        self.selected_trigger_id = trigger_id
        self.render_view()

    def _set_trigger_category(self, cat: Literal["time", "event"]) -> None:
        self.trigger_category = cat
        self.render_view()

    def _toggle_and_refresh(self, aid: str) -> None:
        self.on_toggle_automation(aid)
        self.render_view()

    def _submit_new_automation(self) -> None:
        name = self.draft_name.strip() or "Scheduled Workspace Check"
        prompt = self.draft_prompt.strip() or "Run tests and report any regressions."
        new_item = AutomationItem(
            id=f"auto-{len(self.automations) + 1}",
            display_name=name,
            project_id=self.draft_project_id,
            prompt=prompt,
            schedule_summary=f"Every day at {self.draft_hour} • antigravity-studio",
            frequency=self.draft_frequency,
            hour=self.draft_hour,
            enabled=True,
            last_run="Just created",
        )
        self.on_create_automation(new_item)
        self.draft_name = ""
        self.draft_prompt = ""
        self.modal_open = False
        self.render_view()
