"""1:1 Antigravity Conversation History View (IRb) & Ctrl+K Search Conversations Modal (oMb)."""

from collections.abc import Callable
from typing import Literal

from nicegui import ui

from nicegui_ai.antigravity.icons import AntigravityIcon
from nicegui_ai.antigravity.state import ProjectConfig, Session


class ConversationHistoryView(ui.element):
    """Dedicated center view for searching, grouping, and managing all conversations."""

    def __init__(
        self,
        sessions: list[Session],
        projects: list[ProjectConfig],
        active_session_id: str,
        on_select_session: Callable[[str], None],
        on_toggle_pin: Callable[[str], None],
        on_toggle_archive: Callable[[str], None],
        on_delete_session: Callable[[str], None],
        on_new_conversation: Callable[[], None],
    ) -> None:
        super().__init__("div")
        self.sessions = sessions
        self.projects = projects
        self.active_session_id = active_session_id
        self.on_select_session = on_select_session
        self.on_toggle_pin = on_toggle_pin
        self.on_toggle_archive = on_toggle_archive
        self.on_delete_session = on_delete_session
        self.on_new_conversation = on_new_conversation

        self.search_query: str = ""
        self.group_by: Literal["project", "none"] = "project"
        self.sort_by: Literal["recent", "tokens"] = "recent"
        self.show_pinned_only: bool = False
        self.include_archived: bool = False
        self.display_menu_open: bool = False
        self.banner_dismissed: bool = False
        self.collapsed_groups: dict[str, bool] = {}

        self.props('data-testid="conversation-history-view"')
        self.classes(
            "flex-1 flex flex-col h-full bg-background text-foreground overflow-y-auto"
        )
        self.render_view()

    def _filtered_sessions(self) -> list[Session]:
        q = self.search_query.strip().lower()
        items = [
            s
            for s in self.sessions
            if s.id != "session-zero-state"
            and (self.include_archived or not s.archived)
            and (not self.show_pinned_only or s.pinned)
            and (not q or q in s.title.lower())
        ]
        if self.sort_by == "tokens":
            items.sort(key=lambda x: x.token_count, reverse=True)
        return items

    def render_view(self) -> None:
        self.clear()
        filtered = self._filtered_sessions()

        with self:
            with ui.element("div").classes(
                "w-full max-w-3xl mx-auto p-8 space-y-6 pb-20 flex flex-col"
            ):
                # Top Sticky Header
                with ui.element("div").classes(
                    "flex items-center justify-between gap-4"
                ):
                    with ui.element("div").classes("flex flex-col gap-0.5"):
                        ui.label("Conversation History").classes(
                            "text-lg font-medium text-foreground select-none"
                        )
                        ui.label(
                            f"{len(filtered)} conversations across {len(self.projects)} workspaces"
                        ).classes("text-xs text-muted-foreground")

                    with (
                        ui.element("button")
                        .props(
                            'type="button" data-testid="history-new-conversation-button"'
                        )
                        .classes(
                            "inline-flex items-center gap-1.5 h-8 px-3 rounded-lg bg-secondary "
                            "hover:bg-secondary/80 text-foreground text-xs font-medium "
                            "border border-card-border cursor-pointer transition-colors"
                        )
                        .on("click", self.on_new_conversation)
                    ):
                        AntigravityIcon("plus", size=14)
                        ui.label("New Conversation")

                # Shortcut Callout Banner
                if not self.banner_dismissed:
                    with ui.element("div").classes(
                        "flex items-center justify-between px-3.5 py-2.5 rounded-xl "
                        "border border-card-border bg-card text-xs text-secondary-foreground"
                    ):
                        with ui.element("div").classes("flex items-center gap-2"):
                            AntigravityIcon(
                                "search", size=14, classes="text-muted-foreground"
                            )
                            ui.label(
                                "Tip: Press Ctrl+K from anywhere to search conversations and jump between workspaces."
                            )
                        with (
                            ui.element("button")
                            .props('type="button"')
                            .classes(
                                "text-muted-foreground hover:text-foreground bg-transparent border-none cursor-pointer text-xs"
                            )
                            .on("click", self._dismiss_banner)
                        ):
                            ui.label("Dismiss")

                # Search & Display Options Bar
                with ui.element("div").classes("flex items-center gap-2 relative"):
                    with ui.element("div").classes(
                        "relative flex-1 flex items-center bg-card border border-card-border rounded-lg px-3 h-9"
                    ):
                        AntigravityIcon(
                            "search", size=15, classes="text-muted-foreground mr-2"
                        )
                        inp = (
                            ui.input(
                                placeholder="Search conversations by title or workspace...",
                                on_change=lambda e: self._on_search_change(e.value),
                            )
                            .props(
                                'dense borderless data-testid="history-search-input"'
                            )
                            .classes("flex-1 text-xs text-foreground bg-transparent")
                        )
                        inp.value = self.search_query

                    with ui.element("div").classes("relative"):
                        with (
                            ui.element("button")
                            .props(
                                'type="button" data-testid="history-display-options-button"'
                            )
                            .classes(
                                "inline-flex items-center gap-1.5 h-9 px-3 rounded-lg border border-card-border "
                                "bg-card hover:bg-secondary text-xs text-secondary-foreground hover:text-foreground cursor-pointer"
                            )
                            .on("click", self._toggle_display_menu)
                        ):
                            AntigravityIcon("tune", size=14)
                            ui.label("Display")

                        if self.display_menu_open:
                            with (
                                ui.element("div")
                                .props('data-testid="history-display-popover"')
                                .classes(
                                    "absolute right-0 top-full mt-1 w-64 rounded-xl border border-card-border "
                                    "bg-card shadow-2xl p-3 z-40 space-y-3 text-xs flex flex-col"
                                )
                            ):
                                with ui.element("div").classes(
                                    "flex items-center justify-between"
                                ):
                                    ui.label("Group By").classes(
                                        "text-muted-foreground"
                                    )
                                    with ui.element("div").classes(
                                        "flex items-center rounded-lg bg-background border border-card-border p-0.5"
                                    ):
                                        for g_val, g_lbl in [
                                            ("project", "Project"),
                                            ("none", "None"),
                                        ]:
                                            with (
                                                ui.element("button")
                                                .classes(
                                                    "px-2 py-0.5 rounded text-[11px] border-none cursor-pointer "
                                                    + (
                                                        "bg-secondary text-foreground font-medium"
                                                        if self.group_by == g_val
                                                        else "bg-transparent text-muted-foreground"
                                                    )
                                                )
                                                .on(
                                                    "click",
                                                    lambda _, gv=g_val: (
                                                        self._set_group_by(gv)
                                                    ),
                                                )
                                            ):
                                                ui.label(g_lbl)

                                with ui.element("div").classes(
                                    "flex items-center justify-between"
                                ):
                                    ui.label("Sort By").classes("text-muted-foreground")
                                    with ui.element("div").classes(
                                        "flex items-center rounded-lg bg-background border border-card-border p-0.5"
                                    ):
                                        for s_val, s_lbl in [
                                            ("recent", "Recent"),
                                            ("tokens", "Tokens"),
                                        ]:
                                            with (
                                                ui.element("button")
                                                .classes(
                                                    "px-2 py-0.5 rounded text-[11px] border-none cursor-pointer "
                                                    + (
                                                        "bg-secondary text-foreground font-medium"
                                                        if self.sort_by == s_val
                                                        else "bg-transparent text-muted-foreground"
                                                    )
                                                )
                                                .on(
                                                    "click",
                                                    lambda _, sv=s_val: (
                                                        self._set_sort_by(sv)
                                                    ),
                                                )
                                            ):
                                                ui.label(s_lbl)

                # Grouped or Flat Conversation List
                if self.group_by == "project":
                    for proj in self.projects:
                        p_sessions = [s for s in filtered if s.project_id == proj.id]
                        if not p_sessions:
                            continue
                        is_collapsed = self.collapsed_groups.get(proj.id, False)
                        with ui.element("div").classes("space-y-1.5 flex flex-col"):
                            with (
                                ui.element("button")
                                .props('type="button"')
                                .classes(
                                    "flex items-center justify-between w-full px-1 py-1 text-left "
                                    "bg-transparent border-none cursor-pointer"
                                )
                                .on(
                                    "click",
                                    lambda _, pid=proj.id: self._toggle_group(pid),
                                )
                            ):
                                with ui.element("div").classes(
                                    "flex items-center gap-2"
                                ):
                                    AntigravityIcon(
                                        "chevron_right"
                                        if is_collapsed
                                        else "chevron_down",
                                        size=14,
                                        classes="text-muted-foreground",
                                    )
                                    AntigravityIcon(
                                        "folder",
                                        size=14,
                                        classes="text-secondary-foreground",
                                    )
                                    ui.label(proj.name).classes(
                                        "text-xs font-semibold text-foreground"
                                    )
                                    ui.label(str(len(p_sessions))).classes(
                                        "text-[11px] px-1.5 py-0.2 rounded-full bg-secondary text-muted-foreground"
                                    )
                                ui.label(
                                    proj.folders[0] if proj.folders else ""
                                ).classes("text-[11px] font-mono text-muted-foreground")

                            if not is_collapsed:
                                with ui.element("div").classes(
                                    "border border-card-border rounded-xl overflow-hidden bg-card divide-y divide-border flex flex-col"
                                ):
                                    for s in p_sessions:
                                        self._render_session_row(s, proj.name)

                    standalone = [s for s in filtered if not s.project_id]
                    if standalone:
                        with ui.element("div").classes("space-y-1.5 flex flex-col"):
                            ui.label("Standalone Conversations").classes(
                                "text-xs font-semibold text-muted-foreground px-1"
                            )
                            with ui.element("div").classes(
                                "border border-card-border rounded-xl overflow-hidden bg-card divide-y divide-border flex flex-col"
                            ):
                                for s in standalone:
                                    self._render_session_row(s, None)
                else:
                    with ui.element("div").classes(
                        "border border-card-border rounded-xl overflow-hidden bg-card divide-y divide-border flex flex-col"
                    ):
                        for s in filtered:
                            proj_obj = next(
                                (p for p in self.projects if p.id == s.project_id),
                                None,
                            )
                            self._render_session_row(
                                s, proj_obj.name if proj_obj else None
                            )

    def _render_session_row(self, s: Session, proj_name: str | None) -> None:
        with (
            ui.element("div")
            .props('data-testid="history-conversation-row"')
            .classes(
                "flex items-center justify-between gap-3 px-4 py-3 hover:bg-secondary/50 "
                "cursor-pointer transition-colors group"
            )
            .on("click", lambda _, sid=s.id: self.on_select_session(sid))
        ):
            with ui.element("div").classes("flex flex-col gap-0.5 min-w-0 flex-1"):
                with ui.element("div").classes("flex items-center gap-2"):
                    ui.label(s.title).classes(
                        "text-sm font-medium text-foreground truncate"
                    )
                    if s.pinned:
                        ui.label("Pinned").classes(
                            "text-[10px] px-1.5 py-0.2 rounded bg-secondary text-secondary-foreground border border-card-border"
                        )
                with ui.element("div").classes(
                    "flex items-center gap-2 text-xs text-muted-foreground"
                ):
                    if proj_name:
                        ui.label(proj_name)
                        ui.label("•")
                    ui.label(f"{s.token_count:,} tokens")
                    ui.label("•")
                    ui.label(s.timestamp)

            with ui.element("div").classes("flex items-center gap-1.5 shrink-0"):
                with (
                    ui.element("button")
                    .props('type="button"')
                    .classes(
                        "px-2 py-1 rounded text-[11px] bg-secondary/70 hover:bg-secondary "
                        "text-secondary-foreground hover:text-foreground border border-card-border cursor-pointer"
                    )
                    .on(
                        "click.stop",
                        lambda _, sid=s.id: self._pin_and_refresh(sid),
                    )
                ):
                    ui.label("Unpin" if s.pinned else "Pin")
                with (
                    ui.element("button")
                    .props('type="button"')
                    .classes(
                        "px-2 py-1 rounded text-[11px] bg-transparent hover:bg-red-500/20 "
                        "text-muted-foreground hover:text-red-400 border-none cursor-pointer"
                    )
                    .on(
                        "click.stop",
                        lambda _, sid=s.id: self._delete_and_refresh(sid),
                    )
                ):
                    ui.label("Delete")

    def _dismiss_banner(self) -> None:
        self.banner_dismissed = True
        self.render_view()

    def _on_search_change(self, val: str) -> None:
        self.search_query = val
        self.render_view()

    def _toggle_display_menu(self) -> None:
        self.display_menu_open = not self.display_menu_open
        self.render_view()

    def _set_group_by(self, val: str) -> None:
        self.group_by = "project" if val == "project" else "none"
        self.render_view()

    def _set_sort_by(self, val: str) -> None:
        self.sort_by = "tokens" if val == "tokens" else "recent"
        self.render_view()

    def _toggle_group(self, pid: str) -> None:
        self.collapsed_groups[pid] = not self.collapsed_groups.get(pid, False)
        self.render_view()

    def _pin_and_refresh(self, sid: str) -> None:
        self.on_toggle_pin(sid)
        self.render_view()

    def _delete_and_refresh(self, sid: str) -> None:
        self.on_delete_session(sid)
        self.render_view()


class SearchConversationsModal(ui.element):
    """Ctrl+K Command Palette / Conversation Picker Modal (oMb)."""

    def __init__(
        self,
        is_open: bool,
        on_close: Callable[[], None],
        sessions: list[Session],
        projects: list[ProjectConfig],
        on_select_session: Callable[[str], None],
        on_new_conversation: Callable[[], None],
        on_open_automations: Callable[[], None],
        on_open_settings: Callable[[], None],
    ) -> None:
        super().__init__("div")
        self.is_open = is_open
        self.on_close = on_close
        self.sessions = sessions
        self.projects = projects
        self.on_select_session = on_select_session
        self.on_new_conversation = on_new_conversation
        self.on_open_automations = on_open_automations
        self.on_open_settings = on_open_settings
        self.query: str = ""

        self.render_modal()

    def set_open(self, open_state: bool) -> None:
        self.is_open = open_state
        self.render_modal()

    def render_modal(self) -> None:
        self.clear()
        if not self.is_open:
            self.classes(replace="hidden")
            return

        self.props('data-testid="conversation-picker-modal"')
        self.classes(
            replace="fixed inset-0 z-50 flex items-start justify-center pt-20 bg-black/60 backdrop-blur-xs"
        )

        q = self.query.strip().lower()
        matches = [
            s
            for s in self.sessions
            if s.id != "session-zero-state" and (not q or q in s.title.lower())
        ]

        with self:
            with ui.element("div").classes(
                "w-full max-w-xl rounded-2xl border border-card-border bg-card shadow-2xl overflow-hidden flex flex-col"
            ):
                # Top Search Input Bar
                with ui.element("div").classes(
                    "flex items-center gap-2.5 px-4 py-3 border-b border-card-border"
                ):
                    AntigravityIcon("search", size=16, classes="text-muted-foreground")
                    inp = (
                        ui.input(
                            placeholder="Search conversations, workspaces, or commands...",
                            on_change=lambda e: self._update_query(e.value),
                        )
                        .props(
                            'dense borderless autofocus data-testid="conversation-picker-input"'
                        )
                        .classes("flex-1 text-sm text-foreground bg-transparent")
                    )
                    inp.value = self.query
                    with (
                        ui.element("button")
                        .props('type="button"')
                        .classes(
                            "text-[10px] font-mono px-1.5 py-0.5 rounded bg-secondary text-muted-foreground border border-card-border cursor-pointer"
                        )
                        .on("click", self.on_close)
                    ):
                        ui.label("ESC")

                # Results List
                with ui.element("div").classes(
                    "max-h-96 overflow-y-auto p-2 space-y-2 flex flex-col"
                ):
                    # Quick Actions
                    ui.label("Quick Actions").classes(
                        "px-2.5 py-1 text-[11px] font-semibold text-muted-foreground uppercase tracking-wider"
                    )
                    actions = [
                        ("New Conversation", "Ctrl+N", self._act_new),
                        ("Open Automations", "Cloud Triggers", self._act_auto),
                        ("Open Settings", "Ctrl+,", self._act_settings),
                    ]
                    for act_lbl, act_hint, act_fn in actions:
                        with (
                            ui.element("button")
                            .props('type="button"')
                            .classes(
                                "w-full flex items-center justify-between px-3 py-2 rounded-lg "
                                "hover:bg-secondary text-xs text-foreground bg-transparent border-none cursor-pointer"
                            )
                            .on("click", act_fn)
                        ):
                            ui.label(act_lbl)
                            ui.label(act_hint).classes(
                                "text-[10px] font-mono text-muted-foreground"
                            )

                    ui.label("Recent Conversations").classes(
                        "px-2.5 pt-2 py-1 text-[11px] font-semibold text-muted-foreground uppercase tracking-wider"
                    )
                    for s in matches[:8]:
                        proj = next(
                            (p for p in self.projects if p.id == s.project_id), None
                        )
                        with (
                            ui.element("button")
                            .props(f'type="button" data-testid="picker-session-{s.id}"')
                            .classes(
                                "w-full flex items-center justify-between px-3 py-2 rounded-lg "
                                "hover:bg-secondary text-left bg-transparent border-none cursor-pointer"
                            )
                            .on(
                                "click",
                                lambda _, sid=s.id: self._pick_session(sid),
                            )
                        ):
                            with ui.element("div").classes(
                                "flex items-center gap-2 min-w-0"
                            ):
                                AntigravityIcon(
                                    "history",
                                    size=14,
                                    classes="text-muted-foreground",
                                )
                                ui.label(s.title).classes(
                                    "text-xs text-foreground truncate"
                                )
                                if proj:
                                    ui.label(proj.name).classes(
                                        "text-[10px] px-1.5 py-0.2 rounded bg-background text-muted-foreground border border-card-border"
                                    )
                            ui.label(s.timestamp).classes(
                                "text-[11px] text-muted-foreground shrink-0"
                            )

    def _update_query(self, val: str) -> None:
        self.query = val
        self.render_modal()

    def _pick_session(self, sid: str) -> None:
        self.on_close()
        self.on_select_session(sid)

    def _act_new(self) -> None:
        self.on_close()
        self.on_new_conversation()

    def _act_auto(self) -> None:
        self.on_close()
        self.on_open_automations()

    def _act_settings(self) -> None:
        self.on_close()
        self.on_open_settings()
