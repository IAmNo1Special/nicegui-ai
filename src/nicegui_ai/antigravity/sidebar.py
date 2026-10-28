"""256px Left Sidebar Navigation (h1b) for Antigravity Desktop Clone."""

from collections.abc import Callable
from typing import Literal

from nicegui import ui

from nicegui_ai.antigravity.icons import AntigravityIcon
from nicegui_ai.antigravity.state import ProjectConfig, Session

CenterViewType = Literal["chat", "history", "automations", "customizations"]


class Sidebar(ui.element):
    """256px persistent left sidebar matching Antigravity's h1b navigation tree."""

    def __init__(
        self,
        active_session_id: str,
        active_center_view: CenterViewType,
        sessions: list[Session],
        projects: list[ProjectConfig],
        on_select_session: Callable[[str], None],
        on_new_conversation: Callable[[str | None], None],
        on_open_history: Callable[[], None],
        on_open_automations: Callable[[], None],
        on_open_customizations: Callable[[], None],
        on_open_settings: Callable[[], None],
        on_open_search_modal: Callable[[], None],
        on_toggle_sidebar: Callable[[], None],
        on_toggle_pin: Callable[[str], None] | None = None,
        on_toggle_archive: Callable[[str], None] | None = None,
        on_delete_session: Callable[[str], None] | None = None,
        on_add_project: Callable[[str], None] | None = None,
        on_navigate_back: Callable[[], None] | None = None,
        on_navigate_forward: Callable[[], None] | None = None,
        can_navigate_back: bool = True,
        can_navigate_forward: bool = False,
    ) -> None:
        super().__init__("div")
        self.active_session_id = active_session_id
        self.active_center_view: CenterViewType = active_center_view
        self.sessions = sessions
        self.projects = projects
        self.on_select_session = on_select_session
        self.on_new_conversation = on_new_conversation
        self.on_open_history = on_open_history
        self.on_open_automations = on_open_automations
        self.on_open_customizations = on_open_customizations
        self.on_open_settings = on_open_settings
        self.on_open_search_modal = on_open_search_modal
        self.on_toggle_sidebar = on_toggle_sidebar
        self.on_toggle_pin = on_toggle_pin
        self.on_toggle_archive = on_toggle_archive
        self.on_delete_session = on_delete_session
        self.on_add_project = on_add_project
        self.on_navigate_back = on_navigate_back
        self.on_navigate_forward = on_navigate_forward
        self.can_navigate_back = can_navigate_back
        self.can_navigate_forward = can_navigate_forward

        self.open_projects: dict[str, bool] = {"proj-mvge": True}
        self.filter_menu_open: bool = False
        self.only_non_empty_projects: bool = False
        self.show_archived_in_sidebar: bool = False
        self.adding_project: bool = False
        self.new_project_name: str = ""

        self.props('role="navigation" aria-label="Sidebar" data-testid="sidebar"')
        self.classes(
            "h-full w-[256px] min-w-[256px] flex flex-col pb-2 bg-sidebar select-none "
            "shrink-0 border-r border-border text-sm"
        )

        self.render_content()

    def update_state(
        self,
        active_session_id: str,
        active_center_view: CenterViewType,
        can_back: bool = True,
        can_forward: bool = False,
    ) -> None:
        self.active_session_id = active_session_id
        self.active_center_view = active_center_view
        self.can_navigate_back = can_back
        self.can_navigate_forward = can_forward
        self.render_content()

    def _toggle_project_folder(self, proj_id: str) -> None:
        self.open_projects[proj_id] = not self.open_projects.get(proj_id, False)
        self.render_content()

    def _create_project(self) -> None:
        trimmed = self.new_project_name.strip()
        if trimmed and self.on_add_project:
            self.on_add_project(trimmed)
            self.new_project_name = ""
            self.adding_project = False
            self.render_content()

    def render_content(self) -> None:
        self.clear()
        visible_sessions = [
            s
            for s in self.sessions
            if self.show_archived_in_sidebar or not s.archived
        ]
        pinned_sessions = [s for s in visible_sessions if s.pinned]
        standalone_sessions = [
            s
            for s in visible_sessions
            if not s.project_id and not s.pinned and len(s.messages) > 0
        ]

        with self:
            # Top Header Icons Strip (Height: 40px)
            with ui.element("div").classes(
                "shrink-0 flex items-center pr-2 mb-2 h-[40px] pl-2 gap-1 border-b border-border/40"
            ):
                with (
                    ui.element("button")
                    .props(
                        'type="button" aria-label="New Conversation" '
                        'data-testid="app-icon-new-conversation-button" title="New Conversation"'
                    )
                    .classes(
                        "shrink-0 pl-1 pr-1.5 mr-0.5 flex items-center text-foreground hover:text-white "
                        "cursor-pointer transition-colors bg-transparent border-none"
                    )
                    .on("click", lambda: self.on_new_conversation(None))
                ):
                    AntigravityIcon("antigravity_logo", size=22)

                with ui.element("div").classes("flex items-center gap-0.5"):
                    with (
                        ui.element("button")
                        .props(
                            'type="button" aria-label="Toggle Sidebar" '
                            'data-testid="sidebar-toggle" title="Toggle Sidebar (Ctrl+B)"'
                        )
                        .classes(
                            "inline-flex items-center justify-center h-7 w-7 rounded-lg "
                            "text-secondary-foreground hover:text-foreground hover:bg-secondary "
                            "cursor-pointer transition-colors bg-transparent border-none"
                        )
                        .on("click", self.on_toggle_sidebar)
                    ):
                        AntigravityIcon("sidebar_toggle", size=18)

                    with (
                        ui.element("button")
                        .props(
                            'type="button" aria-label="Go Back" '
                            'data-testid="sidebar-back-button" title="Back (Alt+Left)"'
                        )
                        .classes(
                            "inline-flex items-center justify-center h-7 w-7 rounded-lg "
                            "text-secondary-foreground hover:text-foreground hover:bg-secondary "
                            "cursor-pointer transition-colors bg-transparent border-none"
                        )
                        .on(
                            "click",
                            self.on_navigate_back or self.on_open_history,
                        )
                    ):
                        AntigravityIcon("arrow_back", size=18)

                    with (
                        ui.element("button")
                        .props(
                            'type="button" aria-label="Go Forward" '
                            'data-testid="sidebar-forward-button" title="Forward (Alt+Right)"'
                        )
                        .classes(
                            "inline-flex items-center justify-center h-7 w-7 rounded-lg "
                            "text-secondary-foreground hover:text-foreground hover:bg-secondary "
                            "cursor-pointer transition-colors bg-transparent border-none "
                            + ("" if self.can_navigate_forward else "opacity-40")
                        )
                        .on(
                            "click",
                            lambda: (
                                self.on_navigate_forward()
                                if self.on_navigate_forward
                                else None
                            ),
                        )
                    ):
                        AntigravityIcon("arrow_forward", size=18)

                ui.element("div").classes("flex-1")

                with (
                    ui.element("button")
                    .props(
                        'type="button" aria-label="Search Conversations" '
                        'data-testid="sidebar-search-button" title="Search Conversations (Ctrl+K)"'
                    )
                    .classes(
                        "inline-flex items-center justify-center h-7 w-7 rounded-lg "
                        "text-secondary-foreground hover:text-foreground hover:bg-secondary "
                        "cursor-pointer transition-colors bg-transparent border-none"
                    )
                    .on("click", self.on_open_search_modal)
                ):
                    AntigravityIcon("search", size=18)

            # Main Action Buttons (h1b)
            with ui.element("div").classes("px-2 space-y-0.5"):
                with (
                    ui.element("button")
                    .props('type="button" data-testid="new-conversation-button"')
                    .classes(
                        "inline-flex items-center font-normal transition-colors select-none outline-none "
                        "cursor-pointer w-full justify-between h-8 gap-1.5 px-2 py-1 rounded-lg "
                        "bg-sidebar-muted hover:bg-sidebar-secondary border border-border text-foreground text-sm shadow-sm"
                    )
                    .on("click", lambda: self.on_new_conversation(None))
                ):
                    with ui.element("div").classes("flex items-center gap-1.5 min-w-0"):
                        AntigravityIcon("plus", size=16)
                        ui.label("New Conversation").classes("truncate")
                    ui.label("Ctrl+N").classes(
                        "text-[10px] text-muted-foreground font-mono bg-secondary px-1 rounded border border-border"
                    )

                with ui.element("div").classes("pt-1 space-y-0.5 flex flex-col"):
                    nav_items: list[tuple[str, str, str, CenterViewType, Callable[[], None]]] = [
                        (
                            "Conversation History",
                            "history",
                            "history-button",
                            "history",
                            self.on_open_history,
                        ),
                        (
                            "Automations",
                            "automations",
                            "automations-button",
                            "automations",
                            self.on_open_automations,
                        ),
                        (
                            "Customizations",
                            "customizations",
                            "customizations-button",
                            "customizations",
                            self.on_open_customizations,
                        ),
                    ]
                    for label_txt, icon_name, test_id, view_key, cb in nav_items:
                        is_active_view = self.active_center_view == view_key
                        btn_classes = (
                            "inline-flex items-center font-normal transition-colors select-none outline-none "
                            "cursor-pointer w-full justify-start h-8 gap-1.5 px-2 py-1 rounded-lg border-none text-sm "
                            + (
                                "bg-sidebar-secondary text-foreground font-medium"
                                if is_active_view
                                else "bg-transparent text-secondary-foreground hover:bg-sidebar-muted hover:text-foreground"
                            )
                        )
                        with (
                            ui.element("button")
                            .props(f'type="button" data-testid="{test_id}"')
                            .classes(btn_classes)
                            .on("click", cb)
                        ):
                            AntigravityIcon(icon_name, size=16)
                            ui.label(label_txt).classes("truncate")

            # Scrollable Tree Section
            with ui.element("div").classes(
                "flex-1 overflow-y-auto px-2 pt-3 space-y-4 flex flex-col"
            ):
                # Pinned Conversations
                with ui.element("div"):
                    ui.label("Pinned Conversations").classes(
                        "text-xs font-semibold text-muted-foreground px-2 py-1 tracking-wider"
                    )
                    with ui.element("div").classes("flex flex-col gap-0.5 mt-1"):
                        for s in pinned_sessions:
                            proj = next(
                                (p for p in self.projects if p.id == s.project_id),
                                None,
                            )
                            is_selected = (
                                self.active_center_view == "chat"
                                and self.active_session_id == s.id
                            )
                            row_cls = (
                                "flex items-center justify-between p-2 rounded-lg cursor-pointer transition-colors group "
                                + (
                                    "bg-sidebar-secondary border border-border text-foreground font-semibold"
                                    if is_selected
                                    else "hover:bg-sidebar-muted text-secondary-foreground hover:text-foreground"
                                )
                            )
                            with (
                                ui.element("div")
                                .classes(row_cls)
                                .on("click", lambda _, sid=s.id: self.on_select_session(sid))
                            ):
                                with ui.element("div").classes("min-w-0 flex-1"):
                                    ui.label(s.title).classes("truncate text-xs")
                                    if proj:
                                        with ui.element("div").classes(
                                            "flex items-center gap-1 text-[11px] text-muted-foreground mt-0.5"
                                        ):
                                            AntigravityIcon("folder", size=12)
                                            ui.label(proj.name).classes("truncate")
                                with ui.element("div").classes(
                                    "flex items-center shrink-0 pl-1"
                                ):
                                    AntigravityIcon(
                                        "popout",
                                        size=13,
                                        classes="text-muted-foreground opacity-60 group-hover:opacity-100",
                                    )

                # Projects Section
                with ui.element("div").classes("relative"):
                    with ui.element("div").classes(
                        "flex items-center justify-between px-2 py-1"
                    ):
                        ui.label("Projects").classes(
                            "text-xs font-semibold text-muted-foreground tracking-wider"
                        )
                        with ui.element("div").classes("flex items-center gap-0.5"):
                            with (
                                ui.element("button")
                                .props(
                                    'type="button" aria-label="Filter Projects" '
                                    'data-testid="sidebar-filter-projects-button"'
                                )
                                .classes(
                                    "inline-flex items-center justify-center h-6 w-6 rounded "
                                    "text-secondary-foreground hover:text-foreground hover:bg-secondary "
                                    "bg-transparent border-none cursor-pointer"
                                )
                                .on(
                                    "click",
                                    lambda: self._toggle_filter_menu(),
                                )
                            ):
                                AntigravityIcon("filter", size=14)
                            with (
                                ui.element("button")
                                .props(
                                    'type="button" aria-label="Add Project" '
                                    'data-testid="sidebar-add-project-button"'
                                )
                                .classes(
                                    "inline-flex items-center justify-center h-6 w-6 rounded "
                                    "text-secondary-foreground hover:text-foreground hover:bg-secondary "
                                    "bg-transparent border-none cursor-pointer"
                                )
                                .on("click", lambda: self._toggle_adding_project())
                            ):
                                AntigravityIcon("plus", size=16)

                    if self.adding_project:
                        with ui.element("div").classes(
                            "mb-2 p-2 rounded-lg bg-card border border-card-border flex flex-col gap-1.5"
                        ):
                            inp = (
                                ui.input(placeholder="Project name...")
                                .props("dense borderless")
                                .classes(
                                    "w-full bg-background border border-card-border rounded px-2 py-1 text-xs text-foreground"
                                )
                            )
                            inp.bind_value(self, "new_project_name")
                            with ui.element("div").classes(
                                "flex items-center justify-end gap-1"
                            ):
                                with (
                                    ui.element("button")
                                    .classes(
                                        "px-2 py-0.5 rounded text-[11px] text-muted-foreground hover:text-foreground bg-transparent border-none cursor-pointer"
                                    )
                                    .on("click", lambda: self._toggle_adding_project())
                                ):
                                    ui.label("Cancel")
                                with (
                                    ui.element("button")
                                    .classes(
                                        "px-2 py-0.5 rounded text-[11px] bg-primary text-primary-foreground border-none cursor-pointer"
                                    )
                                    .on("click", self._create_project)
                                ):
                                    ui.label("Create")

                    with ui.element("div").classes("space-y-0.5 mt-0.5 flex flex-col"):
                        for p in self.projects:
                            proj_sessions = [
                                s
                                for s in visible_sessions
                                if s.project_id == p.id
                                and not s.pinned
                                and len(s.messages) > 0
                            ]
                            if self.only_non_empty_projects and not proj_sessions:
                                continue
                            is_open = self.open_projects.get(p.id, False)
                            with ui.element("div"):
                                with (
                                    ui.element("div")
                                    .classes(
                                        "flex items-center justify-between h-8 px-2 py-1 rounded-lg "
                                        "cursor-pointer hover:bg-sidebar-muted text-secondary-foreground "
                                        "hover:text-foreground group transition-colors"
                                    )
                                    .on(
                                        "click",
                                        lambda _, pid=p.id: self._toggle_project_folder(
                                            pid
                                        ),
                                    )
                                ):
                                    with ui.element("div").classes(
                                        "flex items-center gap-1.5 min-w-0"
                                    ):
                                        AntigravityIcon(
                                            "chevron_down"
                                            if is_open
                                            else "chevron_right",
                                            size=14,
                                            classes="text-muted-foreground",
                                        )
                                        AntigravityIcon("folder", size=14)
                                        ui.label(p.name).classes("truncate text-xs")

                                if is_open and proj_sessions:
                                    with ui.element("div").classes(
                                        "pl-3 ml-3 border-l border-border space-y-0.5 my-0.5 flex flex-col"
                                    ):
                                        for item in proj_sessions:
                                            is_sel = (
                                                self.active_center_view == "chat"
                                                and self.active_session_id == item.id
                                            )
                                            item_cls = (
                                                "flex items-center justify-between h-7 px-2 py-1 rounded-md cursor-pointer transition-colors text-xs "
                                                + (
                                                    "bg-sidebar-secondary text-foreground font-medium"
                                                    if is_sel
                                                    else "hover:bg-sidebar-muted text-secondary-foreground hover:text-foreground"
                                                )
                                            )
                                            with (
                                                ui.element("div")
                                                .classes(item_cls)
                                                .on(
                                                    "click",
                                                    lambda _, sid=item.id: (
                                                        self.on_select_session(sid)
                                                    ),
                                                )
                                            ):
                                                ui.label(item.title).classes(
                                                    "truncate pr-2"
                                                )
                                                ui.label(item.timestamp).classes(
                                                    "text-[11px] text-muted-foreground shrink-0"
                                                )

                # Standalone Conversations Section
                with ui.element("div"):
                    with ui.element("div").classes(
                        "flex items-center justify-between px-2 py-1"
                    ):
                        ui.label("Conversations").classes(
                            "text-xs font-semibold text-muted-foreground tracking-wider"
                        )
                        with (
                            ui.element("button")
                            .props('type="button" aria-label="New Standalone Conversation"')
                            .classes(
                                "inline-flex items-center justify-center h-6 w-6 rounded "
                                "text-secondary-foreground hover:text-foreground hover:bg-secondary "
                                "bg-transparent border-none cursor-pointer"
                            )
                            .on("click", lambda: self.on_new_conversation(None))
                        ):
                            AntigravityIcon("plus", size=16)

                    with ui.element("div").classes("space-y-0.5 mt-0.5 flex flex-col"):
                        for c in standalone_sessions:
                            is_sel = (
                                self.active_center_view == "chat"
                                and self.active_session_id == c.id
                            )
                            c_cls = (
                                "flex items-center justify-between h-7 px-2 py-1 rounded-lg cursor-pointer transition-colors text-xs "
                                + (
                                    "bg-sidebar-secondary text-foreground font-medium"
                                    if is_sel
                                    else "hover:bg-sidebar-muted text-secondary-foreground hover:text-foreground"
                                )
                            )
                            with (
                                ui.element("div")
                                .classes(c_cls)
                                .on(
                                    "click",
                                    lambda _, sid=c.id: self.on_select_session(sid),
                                )
                            ):
                                ui.label(c.title).classes("truncate pr-2")
                                ui.label(c.timestamp).classes(
                                    "text-[11px] text-muted-foreground shrink-0"
                                )

            # Bottom Settings Button
            with ui.element("div").classes(
                "px-2 pt-2 border-t border-border/50 space-y-0.5 shrink-0"
            ):
                with (
                    ui.element("button")
                    .props('type="button" data-testid="settings-button"')
                    .classes(
                        "inline-flex items-center font-normal transition-colors select-none outline-none "
                        "cursor-pointer w-full justify-start h-8 gap-2 px-2 py-1 rounded-lg bg-transparent "
                        "text-secondary-foreground hover:bg-sidebar-muted hover:text-foreground border-none text-sm"
                    )
                    .on("click", self.on_open_settings)
                ):
                    AntigravityIcon("settings", size=16)
                    ui.label("Settings").classes("truncate")

    def _toggle_filter_menu(self) -> None:
        self.filter_menu_open = not self.filter_menu_open
        self.render_content()

    def _toggle_adding_project(self) -> None:
        self.adding_project = not self.adding_project
        self.render_content()
