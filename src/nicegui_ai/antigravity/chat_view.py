"""1:1 Antigravity ChatView (Zero-State Home, Active Conversation Stream, Kebab Menu, Lifted Context Menu, and Composer Controls)."""

from collections.abc import Callable
from typing import Literal

from nicegui import ui

from .auxiliary_pane import AuxTabType
from .icons import AntigravityIcon
from .model_selector import AntigravityModelSelector
from .state import (
    AppSettings,
    ArtifactItem,
    ContextAttachment,
    Message,
    ProjectConfig,
    Session,
)

SLASH_COMMANDS: list[dict[str, str]] = [
    {"cmd": "/goal", "desc": "Run a thorough autonomous goal loop until completion"},
    {"cmd": "/plan", "desc": "Draft a structured step-by-step implementation plan"},
    {
        "cmd": "/grill-me",
        "desc": "Stress-test design decisions with interactive questions",
    },
    {"cmd": "/boost", "desc": "Enable multi-perspective reasoning & verification"},
    {"cmd": "/compact", "desc": "Compact conversation history to free context window"},
    {
        "cmd": "/schedule",
        "desc": "Create a recurring cron or one-shot timer automation",
    },
    {
        "cmd": "/browser",
        "desc": "Launch headless browser inspector for web verification",
    },
    {"cmd": "/learn", "desc": "Persist reusable workflow or rule into .agents/skills"},
]

CONTEXT_PICKER_ITEMS: dict[str, list[tuple[str, str, str]]] = {
    "Media": [
        ("att-img", "Upload Image / Screenshot", "PNG, JPG, WebP"),
        ("att-pdf", "Attach PDF Document", "Spec or paper"),
    ],
    "Mentions": [
        ("att-file-app", "@src/nicegui_ai/antigravity/app.py", "File"),
        ("att-file-chat", "@src/nicegui_ai/antigravity/chat_view.py", "File"),
        ("att-skill-ng", "@skill:nicegui", "Skill"),
        ("att-skill-rea", "@skill:clean-room-reverse-engineering", "Skill"),
    ],
    "Actions": [
        ("att-diff", "Git Uncommitted Diff", "+741 -60"),
        ("att-term", "Active Terminal Output", "proc-1"),
    ],
    "Browser": [
        ("att-browser", "Capture Browser Tab DOM", "http://127.0.0.1:8080"),
    ],
}


class ChatView(ui.element):
    """1:1 Antigravity Main Conversation View & Zero-State Home Screen."""

    def __init__(
        self,
        *,
        session: Session,
        all_sessions: list[Session],
        projects: list[ProjectConfig],
        settings: AppSettings,
        selected_model: str = "Gemini 3.8 Flash High",
        selected_effort: Literal["Low", "Medium", "High"] = "High",
        is_streaming: bool = False,
        is_aux_open: bool = True,
        initial_open_model: bool = False,
        initial_open_context: bool = False,
        initial_open_kebab: bool = False,
        initial_open_modes: bool = False,
        initial_open_side_question: bool = False,
        initial_open_fastpick: bool = False,
        initial_open_lifted_menu: bool = False,
        on_send_message: Callable[[str, list[ContextAttachment]], None] | None = None,
        on_select_session: Callable[[str], None] | None = None,
        on_open_artifact: Callable[[ArtifactItem], None] | None = None,
        on_toggle_aux: Callable[[], None] | None = None,
        on_open_aux_tab: Callable[[AuxTabType], None] | None = None,
        on_open_settings: Callable[[str | None], None] | None = None,
        on_model_change: Callable[[str], None] | None = None,
        on_effort_change: Callable[[Literal["Low", "Medium", "High"]], None]
        | None = None,
        on_fork_from_message: Callable[[str], None] | None = None,
    ) -> None:
        super().__init__("main")
        self.session = session
        self.all_sessions = all_sessions
        self.projects = projects
        self.settings = settings
        self.selected_model = selected_model
        self.selected_effort: Literal["Low", "Medium", "High"] = selected_effort
        self.is_streaming = is_streaming
        self.is_aux_open = is_aux_open

        # Interactive popover states
        self.model_open = initial_open_model
        self.context_menu_open = initial_open_context
        self.kebab_menu_open = initial_open_kebab
        self.modes_open = initial_open_modes
        self.side_question_open = initial_open_side_question
        self.fastpick_open = initial_open_fastpick
        self.lifted_menu_msg_id: str | None = (
            session.messages[0].id
            if initial_open_lifted_menu and session.messages
            else None
        )
        self.permissions_menu_open = False

        # Composer & conversation states
        self.input_text = "/" if initial_open_fastpick else ""
        self.attachments: list[ContextAttachment] = []
        self.environment_mode: Literal["Local", "Worktree"] = "Local"
        self.selected_workspace_id = session.project_id or (
            projects[0].id if projects else "proj-ag-studio"
        )
        self.autonomous_mode = settings.lab_autonomous_mode
        self.best_of_n_mode = False
        self.permission_preset: Literal["Strict", "Default", "Auto", "Turbo"] = "Auto"
        self.telemetry_enabled = settings.enable_telemetry
        self.is_unread = False
        self.side_question_input = ""
        self.side_question_answer: str | None = None
        self.zero_state_search = ""

        # Trajectory expansion state
        self.expanded_thoughts: dict[str, bool] = {"m4": True}
        self.expanded_tool_outputs: dict[str, bool] = {"tc-2": True}
        self.selected_ask_option = "Reconstruct 1:1 in nicegui_ai.antigravity"
        self.ask_writein = ""

        # Callbacks
        self.on_send_message = on_send_message
        self.on_select_session = on_select_session
        self.on_open_artifact = on_open_artifact
        self.on_toggle_aux = on_toggle_aux
        self.on_open_aux_tab = on_open_aux_tab
        self.on_open_settings = on_open_settings
        self.on_model_change = on_model_change
        self.on_effort_change = on_effort_change
        self.on_fork_from_message = on_fork_from_message

        self.props('data-testid="chat-view"')
        self.classes(
            "flex-1 flex flex-col h-full bg-[#101010] overflow-hidden relative select-none"
        )
        self.render()

    def set_session(self, session: Session) -> None:
        self.session = session
        self.kebab_menu_open = False
        self.lifted_menu_msg_id = None
        self.render()

    def render(self) -> None:
        self.clear()
        with self:
            if not self.session.messages:
                self._render_zero_state_home()
            else:
                self._render_top_header()
                self._render_message_stream()
                self._render_bottom_composer_area()

    # =========================================================================
    # ZERO-STATE NEW CONVERSATION HOME VIEW (rYb & Q1b)
    # =========================================================================
    def _render_zero_state_home(self) -> None:
        current_proj = next(
            (p for p in self.projects if p.id == self.selected_workspace_id),
            self.projects[0] if self.projects else None,
        )
        proj_name = current_proj.name if current_proj else "antigravity-studio"

        with (
            ui.column()
            .props('data-testid="zero-state-home-view"')
            .classes(
                "flex-1 w-full h-full overflow-y-auto items-center justify-between p-6"
            )
        ):
            # Top Bar with Auxiliary Sidebar Toggle
            with ui.row().classes("w-full items-center justify-end"):
                aux_btn = (
                    ui.button(on_click=self._handle_toggle_aux)
                    .props('flat dense no-caps data-testid="toggle-aux-sidebar"')
                    .classes(
                        "p-1.5 text-[#6e6e6e] hover:text-[#cccccc] rounded-md hover:bg-[#191919] min-h-0 min-w-0"
                    )
                )
                with aux_btn:
                    AntigravityIcon("aux_sidebar_toggle", size=16)

            # Centered Hero + Workspace Pill + Composer Card
            with ui.column().classes("w-full max-w-[680px] items-center gap-5 my-auto"):
                with ui.row().classes("items-center gap-2"):
                    ui.label("New Conversation in").classes(
                        "text-[20px] font-medium text-[#cccccc]"
                    )
                    ws_btn = (
                        ui.button(on_click=self._cycle_workspace)
                        .props(
                            'flat dense no-caps data-testid="zero-state-workspace-selector"'
                        )
                        .classes(
                            "px-3 py-1 bg-[#191919] hover:bg-[#272727] border border-[#222222] rounded-lg text-[16px] font-medium text-[#cccccc] flex items-center gap-2"
                        )
                    )
                    with ws_btn:
                        AntigravityIcon("folder", size=16, classes="text-[#6e6e6e]")
                        ui.label(proj_name)
                        AntigravityIcon(
                            "chevron_down", size=12, classes="text-[#6e6e6e]"
                        )

                # Composer Card inside Zero-State
                self._render_composer_box(is_zero_state=True)

            # Bottom Recent Conversation History Search Strip (Q1b)
            with ui.column().classes(
                "w-full max-w-[680px] gap-2 pt-4 border-t border-[#222222]/60"
            ):
                with ui.row().classes("w-full items-center justify-between"):
                    ui.label("Recent Conversations").classes(
                        "text-[11px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                    )
                    search_in = (
                        ui.input(
                            placeholder="Filter recent conversations...",
                            value=self.zero_state_search,
                            on_change=lambda e: self._set_zero_state_search(
                                str(e.value)
                            ),
                        )
                        .props(
                            'borderless dense dark data-testid="zero-state-history-search"'
                        )
                        .classes(
                            "w-56 px-2.5 py-0.5 bg-[#191919] border border-[#222222] rounded-md text-[11px] text-[#cccccc]"
                        )
                    )
                    _ = search_in

                filtered = [
                    s
                    for s in self.all_sessions
                    if s.messages
                    and (
                        not self.zero_state_search
                        or self.zero_state_search.lower() in s.title.lower()
                    )
                ][:4]
                with ui.column().classes("w-full gap-1"):
                    for s in filtered:
                        with (
                            ui.button(
                                on_click=lambda sid=s.id: (
                                    self.on_select_session(sid)
                                    if self.on_select_session
                                    else None
                                )
                            )
                            .props(
                                f'flat dense no-caps data-testid="zero-state-session-{s.id}"'
                            )
                            .classes(
                                "w-full px-3 py-1.5 rounded-md hover:bg-[#191919] flex items-center justify-between font-normal"
                            )
                        ):
                            ui.label(s.title).classes(
                                "text-[12px] text-[#cccccc] truncate"
                            )
                            ui.label(s.timestamp).classes("text-[11px] text-[#6e6e6e]")

    def _cycle_workspace(self) -> None:
        if not self.projects:
            return
        ids = [p.id for p in self.projects]
        idx = (
            (ids.index(self.selected_workspace_id) + 1) % len(ids)
            if self.selected_workspace_id in ids
            else 0
        )
        self.selected_workspace_id = ids[idx]
        self.render()

    def _set_zero_state_search(self, val: str) -> None:
        self.zero_state_search = val
        self.render()

    # =========================================================================
    # ACTIVE CONVERSATION TOP HEADER (40px, Kebab Menu LMb, Aux Toggle)
    # =========================================================================
    def _render_top_header(self) -> None:
        proj = next(
            (p for p in self.projects if p.id == self.session.project_id),
            None,
        )
        proj_name = proj.name if proj else "antigravity-studio"

        with ui.row().classes(
            "h-[40px] px-4 border-b border-[#222222] items-center justify-between shrink-0 bg-[#101010] w-full relative z-30"
        ):
            # Breadcrumb Title + Unread Dot
            with ui.row().classes("items-center gap-2 min-w-0"):
                ui.label(proj_name).classes("text-[12px] text-[#6e6e6e] truncate")
                ui.label("/").classes("text-[12px] text-[#6e6e6e]")
                ui.label(self.session.title).classes(
                    "text-[12px] font-medium text-[#cccccc] truncate"
                )
                if self.is_unread:
                    ui.element("span").props('data-testid="status-unread-dot"').classes(
                        "w-2 h-2 rounded-full bg-blue-400"
                    )

            # Right Actions: Kebab Menu + Aux Sidebar Toggle
            with ui.row().classes("items-center gap-1 relative"):
                with ui.element("div").classes("relative"):
                    kebab_btn = (
                        ui.button(on_click=self._toggle_kebab_menu)
                        .props('flat dense no-caps data-testid="conversation-kebab"')
                        .classes(
                            f"p-1.5 rounded-md transition-colors min-h-0 min-w-0 "
                            f"{'bg-[#272727] text-[#cccccc]' if self.kebab_menu_open else 'text-[#6e6e6e] hover:text-[#cccccc] hover:bg-[#191919]'}"
                        )
                    )
                    with kebab_btn:
                        AntigravityIcon("more_horiz", size=15)

                    if self.kebab_menu_open:
                        with (
                            ui.column()
                            .props('data-testid="conversation-kebab-menu"')
                            .classes(
                                "absolute right-0 top-full mt-1 w-56 bg-[#191919] border border-[#222222] rounded-lg shadow-2xl py-1 z-50 gap-0"
                            )
                        ):
                            kebab_actions = [
                                ("Rename Conversation", "Ctrl+R"),
                                ("Mark Unread", "Alt+U"),
                                ("View Debug Trajectory", "Ctrl+Shift+D"),
                                ("Copy Conversation ▸", ""),
                                ("Fork Conversation ▸", ""),
                                ("Split Pane ▸", ""),
                                ("Share Transcript", ""),
                                ("Archive", ""),
                                ("Delete", ""),
                            ]
                            for act_label, shortcut in kebab_actions:
                                with (
                                    ui.button(
                                        on_click=lambda a=act_label: (
                                            self._handle_kebab_action(a)
                                        )
                                    )
                                    .props("flat dense no-caps")
                                    .classes(
                                        "w-full px-3 py-1.5 text-[12px] text-[#cccccc] hover:bg-[#272727]/70 flex items-center justify-between rounded-none font-normal"
                                    )
                                ):
                                    ui.label(act_label)
                                    if shortcut:
                                        ui.label(shortcut).classes(
                                            "text-[10px] text-[#6e6e6e] font-mono"
                                        )

                            ui.element("div").classes(
                                "my-1 border-t border-[#222222] w-full"
                            )
                            with (
                                ui.button(on_click=self._toggle_telemetry)
                                .props(
                                    'flat dense no-caps data-testid="conversation-telemetry-switch"'
                                )
                                .classes(
                                    "w-full px-3 py-1.5 text-[12px] text-[#cccccc] hover:bg-[#272727]/70 flex items-center justify-between rounded-none font-normal"
                                )
                            ):
                                ui.label("Conversation Telemetry")
                                ui.label(
                                    "ON" if self.telemetry_enabled else "OFF"
                                ).classes(
                                    f"text-[10px] font-mono px-1.5 py-0.5 rounded "
                                    f"{'bg-emerald-500/20 text-emerald-400' if self.telemetry_enabled else 'bg-[#272727] text-[#6e6e6e]'}"
                                )

                aux_btn = (
                    ui.button(on_click=self._handle_toggle_aux)
                    .props('flat dense no-caps data-testid="toggle-aux-sidebar"')
                    .classes(
                        f"p-1.5 rounded-md transition-colors min-h-0 min-w-0 "
                        f"{'text-[#cccccc] bg-[#272727]' if self.is_aux_open else 'text-[#6e6e6e] hover:text-[#cccccc] hover:bg-[#191919]'}"
                    )
                )
                with aux_btn:
                    AntigravityIcon("aux_sidebar_toggle", size=15)

    def _toggle_kebab_menu(self) -> None:
        self.kebab_menu_open = not self.kebab_menu_open
        self.render()

    def _handle_kebab_action(self, action: str) -> None:
        if action == "Mark Unread":
            self.is_unread = not self.is_unread
        self.kebab_menu_open = False
        self.render()

    def _toggle_telemetry(self) -> None:
        self.telemetry_enabled = not self.telemetry_enabled
        self.settings.enable_telemetry = self.telemetry_enabled
        self.render()

    def _handle_toggle_aux(self) -> None:
        self.is_aux_open = not self.is_aux_open
        if self.on_toggle_aux:
            self.on_toggle_aux()

    # =========================================================================
    # MESSAGE STREAM (User LiftedContextMenu, Agent Thought & Tool Steps, Ask Question)
    # =========================================================================
    def _render_message_stream(self) -> None:
        max_w_cls = (
            "max-w-[640px]"
            if self.settings.conversation_width == "compact"
            else "max-w-[960px]"
            if self.settings.conversation_width == "wide"
            else "max-w-full"
            if self.settings.conversation_width == "full"
            else "max-w-[780px]"
        )
        with ui.column().classes(
            "flex-1 w-full overflow-y-auto px-6 py-5 items-center"
        ):
            with ui.column().classes(f"w-full {max_w_cls} gap-5"):
                for msg in self.session.messages:
                    if msg.role == "user":
                        self._render_user_message(msg)
                    else:
                        self._render_agent_message(msg)

                # Interactive Ask Question Card (on Clone Antigravity UI session)
                if self.session.id == "session-clone-rea":
                    self._render_ask_question_card()

    def _render_user_message(self, msg: Message) -> None:
        is_lifted = self.lifted_menu_msg_id == msg.id
        with ui.column().classes("w-full items-end gap-1 relative"):
            with (
                ui.column()
                .props(f'data-testid="lifted-context-menu-trigger-{msg.id}"')
                .classes(
                    "max-w-[85%] px-4 py-2.5 bg-[#191919] border border-[#222222] rounded-2xl text-[13px] text-[#cccccc] leading-relaxed gap-2 relative group"
                )
            ):
                ui.label(msg.content).classes("whitespace-pre-wrap")
                with ui.row().classes(
                    "items-center justify-end gap-2 text-[10px] text-[#6e6e6e] pt-1"
                ):
                    ui.label(msg.timestamp)
                    ui.button(
                        "Menu",
                        on_click=lambda m=msg.id: self._toggle_lifted_menu(m),
                    ).props(
                        f'flat dense no-caps data-testid="open-lifted-menu-{msg.id}"'
                    ).classes(
                        "px-1.5 py-0.5 rounded bg-[#272727]/60 text-[10px] text-[#cccccc] min-h-0"
                    )

            if is_lifted:
                with (
                    ui.column()
                    .props('data-testid="lifted-context-menu-root"')
                    .classes(
                        "w-56 bg-[#191919]/95 backdrop-blur-md border border-[#222222] rounded-xl shadow-2xl py-1.5 z-50 gap-0.5 mt-1"
                    )
                ):
                    lifted_items = [
                        ("Copy Message", "Ctrl+C"),
                        ("Edit & Resubmit", "E"),
                        ("Fork Conversation From Here", "Ctrl+Shift+F"),
                        ("Undo Turn to Here", "Ctrl+Z"),
                    ]
                    for label, shortcut in lifted_items:
                        with (
                            ui.button(
                                on_click=lambda lbl=label, mid=msg.id: (
                                    self._handle_lifted_action(lbl, mid)
                                )
                            )
                            .props("flat dense no-caps")
                            .classes(
                                "w-full px-3 py-1.5 text-[12px] text-[#cccccc] hover:bg-[#272727] flex items-center justify-between rounded-none font-normal"
                            )
                        ):
                            ui.label(label)
                            ui.label(shortcut).classes(
                                "text-[10px] text-[#6e6e6e] font-mono"
                            )

    def _toggle_lifted_menu(self, msg_id: str) -> None:
        self.lifted_menu_msg_id = None if self.lifted_menu_msg_id == msg_id else msg_id
        self.render()

    def _handle_lifted_action(self, action: str, msg_id: str) -> None:
        if action == "Fork Conversation From Here" and self.on_fork_from_message:
            self.on_fork_from_message(msg_id)
        self.lifted_menu_msg_id = None
        self.render()

    def _render_agent_message(self, msg: Message) -> None:
        thought_open = self.expanded_thoughts.get(msg.id, False)
        with ui.column().classes("w-full items-start gap-2.5"):
            # Collapsible Thought & Tool Trajectory Header
            if msg.thinking or msg.tool_calls:
                duration_label = (
                    f"Worked for {msg.thinking.duration}"
                    if msg.thinking
                    else "Executed tool calls"
                )
                with ui.column().classes(
                    "w-full bg-[#151515] border border-[#222222] rounded-xl overflow-hidden gap-0"
                ):
                    with (
                        ui.button(on_click=lambda m=msg.id: self._toggle_thought(m))
                        .props(
                            f'flat dense no-caps data-testid="trajectory-toggle-{msg.id}"'
                        )
                        .classes(
                            "w-full px-3 py-2 flex items-center justify-between text-left hover:bg-[#191919] font-normal rounded-none"
                        )
                    ):
                        with ui.row().classes("items-center gap-2"):
                            AntigravityIcon(
                                "chevron_down" if thought_open else "chevron_right",
                                size=12,
                                classes="text-[#6e6e6e]",
                            )
                            ui.label("Exploring files, running commands").classes(
                                "text-[12px] font-medium text-[#cccccc]"
                            )
                            ui.label(f"• {duration_label}").classes(
                                "text-[11px] text-[#6e6e6e]"
                            )
                        ui.label(f"{len(msg.tool_calls)} steps").classes(
                            "text-[11px] font-mono text-[#6e6e6e]"
                        )

                    if thought_open:
                        with ui.column().classes(
                            "w-full px-3 pb-3 pt-1 border-t border-[#222222]/60 gap-2"
                        ):
                            if msg.thinking:
                                for step in msg.thinking.steps:
                                    with ui.row().classes(
                                        "items-center gap-2 text-[11px] text-[#6e6e6e]"
                                    ):
                                        AntigravityIcon(
                                            "sparkle", size=11, classes="text-[#6e6e6e]"
                                        )
                                        ui.label(step)

                            for tc in msg.tool_calls:
                                step_testid = (
                                    "run-command-step"
                                    if tc.tool_name == "run_command"
                                    else "view-file-step"
                                )
                                tc_open = self.expanded_tool_outputs.get(tc.id, False)
                                with (
                                    ui.column()
                                    .props(f'data-testid="{step_testid}"')
                                    .classes(
                                        "w-full bg-[#191919] border border-[#222222] rounded-lg overflow-hidden gap-0"
                                    )
                                ):
                                    with (
                                        ui.button(
                                            on_click=lambda tid=tc.id: (
                                                self._toggle_tool_output(tid)
                                            )
                                        )
                                        .props("flat dense no-caps")
                                        .classes(
                                            "w-full px-2.5 py-1.5 flex items-center justify-between font-normal rounded-none"
                                        )
                                    ):
                                        with ui.row().classes("items-center gap-2"):
                                            AntigravityIcon(
                                                "terminal_tab"
                                                if tc.tool_name == "run_command"
                                                else "file_doc",
                                                size=12,
                                                classes="text-[#6e6e6e]",
                                            )
                                            ui.label(tc.action).classes(
                                                "text-[11px] text-[#cccccc] font-medium"
                                            )
                                        ui.label(tc.tool_name).classes(
                                            "text-[10px] font-mono text-[#6e6e6e]"
                                        )

                                    if tc_open and tc.output:
                                        ui.label(tc.output).classes(
                                            "w-full px-3 py-2 bg-[#101010] border-t border-[#222222] font-mono text-[11px] text-[#cccccc]/80 whitespace-pre-wrap"
                                        )

                                    for art in tc.artifacts:
                                        with (
                                            ui.button(
                                                on_click=lambda a=art: (
                                                    self._handle_open_artifact(a)
                                                )
                                            )
                                            .props(
                                                'flat dense no-caps data-testid="agent-embed"'
                                            )
                                            .classes(
                                                "w-full px-3 py-2 bg-[#151515] hover:bg-[#272727]/50 border-t border-[#222222] flex items-center justify-between font-normal rounded-none"
                                            )
                                        ):
                                            with ui.row().classes("items-center gap-2"):
                                                AntigravityIcon(
                                                    "file_doc",
                                                    size=14,
                                                    classes="text-blue-400",
                                                )
                                                ui.label(art.title).classes(
                                                    "text-[12px] font-medium text-[#cccccc]"
                                                )
                                            ui.label("Open Artifact ▸").classes(
                                                "text-[11px] text-blue-400"
                                            )

            # Main Agent Markdown Body
            ui.markdown(msg.content).classes(
                "text-[13px] text-[#cccccc] leading-relaxed w-full"
            )

    def _toggle_thought(self, msg_id: str) -> None:
        self.expanded_thoughts[msg_id] = not self.expanded_thoughts.get(msg_id, False)
        self.render()

    def _toggle_tool_output(self, tool_id: str) -> None:
        self.expanded_tool_outputs[tool_id] = not self.expanded_tool_outputs.get(
            tool_id, False
        )
        self.render()

    def _handle_open_artifact(self, artifact: ArtifactItem) -> None:
        if self.on_open_artifact:
            self.on_open_artifact(artifact)
        elif self.on_open_aux_tab:
            self.on_open_aux_tab("file")

    def _render_ask_question_card(self) -> None:
        with (
            ui.column()
            .props('data-testid="ask-question-card"')
            .classes(
                "w-full p-3.5 bg-[#191919] border border-[#222222] rounded-xl gap-2.5"
            )
        ):
            with ui.row().classes("items-center justify-between w-full"):
                ui.label("Clarification Question").classes(
                    "text-[11px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                )
                ui.label("ask_question").classes("text-[10px] font-mono text-[#6e6e6e]")
            ui.label(
                "How should nicegui-ai package the 1:1 Antigravity desktop component suite?"
            ).classes("text-[12px] font-medium text-[#cccccc]")

            options = [
                "Reconstruct 1:1 in nicegui_ai.antigravity",
                "Keep assistant-ui primitives at root & add CLI entrypoints",
            ]
            for opt in options:
                selected = self.selected_ask_option == opt
                with (
                    ui.button(on_click=lambda o=opt: self._select_ask_option(o))
                    .props('flat dense no-caps data-testid="ask-question-option"')
                    .classes(
                        f"w-full px-3 py-1.5 rounded-lg border text-left flex items-center justify-between font-normal text-[12px] "
                        f"{'bg-[#272727] border-[#cccccc]/40 text-[#cccccc]' if selected else 'bg-[#151515] border-[#222222] text-[#6e6e6e] hover:text-[#cccccc]'}"
                    )
                ):
                    ui.label(opt)
                    if selected:
                        AntigravityIcon("check", size=12, classes="text-emerald-400")

            writein = (
                ui.input(
                    placeholder="Or type a custom write-in response...",
                    value=self.ask_writein,
                    on_change=lambda e: setattr(self, "ask_writein", str(e.value)),
                )
                .props('borderless dense dark data-testid="ask-question-writein"')
                .classes(
                    "w-full px-2.5 py-1 bg-[#101010] border border-[#222222] rounded-md text-[11px] text-[#cccccc]"
                )
            )
            _ = writein

    def _select_ask_option(self, opt: str) -> None:
        self.selected_ask_option = opt
        self.render()

    # =========================================================================
    # FLOATING COMPOSER & FOOTER CONTROLS (MBb: +, @, /, Modes, Side Question, Permissions, Model)
    # =========================================================================
    def _render_bottom_composer_area(self) -> None:
        with ui.column().classes(
            "w-full px-6 pb-4 pt-1 items-center shrink-0 relative z-30"
        ):
            self._render_composer_box(is_zero_state=False)

    def _render_composer_box(self, *, is_zero_state: bool) -> None:
        with ui.column().classes(
            "w-full max-w-[780px] bg-[#191919] border border-[#222222] rounded-2xl p-3 gap-2.5 shadow-xl relative"
        ):
            # Side Question Panel (above input when open)
            if self.side_question_open:
                with (
                    ui.column()
                    .props('data-testid="side-question-panel"')
                    .classes(
                        "w-full p-2.5 bg-[#151515] border border-[#222222] rounded-xl gap-2 mb-1"
                    )
                ):
                    with ui.row().classes("items-center justify-between w-full"):
                        ui.label(
                            "Side Question (Ask without interrupting conversation)"
                        ).classes("text-[11px] font-medium text-[#cccccc]")
                        ui.button(
                            "Close",
                            on_click=self._toggle_side_question,
                        ).props("flat dense no-caps").classes(
                            "text-[10px] text-[#6e6e6e] hover:text-[#cccccc] min-h-0"
                        )
                    with ui.row().classes("w-full items-center gap-2"):
                        sq_in = (
                            ui.input(
                                placeholder="Ask a quick side question about this workspace...",
                                value=self.side_question_input,
                                on_change=lambda e: setattr(
                                    self, "side_question_input", str(e.value)
                                ),
                            )
                            .props(
                                'borderless dense dark data-testid="side-question-input"'
                            )
                            .classes(
                                "flex-1 px-2.5 py-1 bg-[#101010] border border-[#222222] rounded text-[11px] text-[#cccccc]"
                            )
                        )
                        _ = sq_in
                        ui.button("Ask", on_click=self._submit_side_question).props(
                            "flat dense no-caps"
                        ).classes(
                            "px-2.5 py-1 bg-[#272727] text-[#cccccc] rounded text-[11px]"
                        )
                    if self.side_question_answer:
                        ui.label(self.side_question_answer).classes(
                            "text-[11px] text-emerald-400 font-mono"
                        )

            # Slash Command Fastpick Menu (pmb)
            if self.fastpick_open:
                with (
                    ui.column()
                    .props('data-testid="fastpick"')
                    .classes(
                        "w-full bg-[#151515] border border-[#222222] rounded-xl py-1.5 px-1 gap-0.5 mb-1 max-h-52 overflow-y-auto"
                    )
                ):
                    ui.label("Slash Commands & Workflows").classes(
                        "px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                    )
                    for sc in SLASH_COMMANDS:
                        with (
                            ui.button(
                                on_click=lambda c=sc["cmd"]: self._select_slash_command(
                                    c
                                )
                            )
                            .props(
                                f'flat dense no-caps data-testid="fastpick-item-{sc["cmd"][1:]}"'
                            )
                            .classes(
                                "w-full px-2.5 py-1.5 rounded-lg hover:bg-[#272727] flex items-center justify-between font-normal text-left"
                            )
                        ):
                            ui.label(sc["cmd"]).classes(
                                "text-[12px] font-mono font-medium text-[#cccccc]"
                            )
                            ui.label(sc["desc"]).classes(
                                "text-[11px] text-[#6e6e6e] truncate"
                            )

            # Attachment Chips Row
            if self.attachments:
                with ui.row().classes("items-center gap-1.5 flex-wrap w-full"):
                    for att in self.attachments:
                        with ui.row().classes(
                            "px-2 py-0.5 bg-[#272727] border border-[#222222] rounded-md items-center gap-1.5 text-[11px] text-[#cccccc]"
                        ):
                            ui.label(att.label)
                            ui.button(
                                "×",
                                on_click=lambda aid=att.id: self._remove_attachment(
                                    aid
                                ),
                            ).props("flat dense no-caps").classes(
                                "text-[#6e6e6e] hover:text-[#cccccc] min-h-0 min-w-0 p-0 text-[11px]"
                            )

            # Prompt Textarea
            prompt_input = (
                ui.textarea(
                    placeholder="Ask Antigravity anything, @ to mention files/skills, / for workflows...",
                    value=self.input_text,
                    on_change=lambda e: self._on_prompt_change(str(e.value)),
                )
                .props('borderless dense autogrow dark data-testid="composer-input"')
                .classes("w-full text-[13px] text-[#cccccc] leading-relaxed")
            )
            _ = prompt_input

            # Footer Toolbar (MBb)
            with ui.row().classes(
                "w-full items-center justify-between gap-2 pt-1 relative"
            ):
                # Left Controls: + Context Picker, Modes, Side Question, Permissions, Model Selector
                with ui.row().classes("items-center gap-1.5 flex-wrap relative"):
                    # '+' Add Context Button & Popover (vBb)
                    with ui.element("div").classes("relative"):
                        ctx_btn = (
                            ui.button(on_click=self._toggle_context_menu)
                            .props(
                                'flat dense no-caps data-testid="composer-plus-context"'
                            )
                            .classes(
                                f"p-1.5 rounded-lg border transition-colors min-h-0 min-w-0 "
                                f"{'bg-[#272727] border-[#cccccc]/30 text-[#cccccc]' if self.context_menu_open else 'bg-[#151515] border-[#222222] text-[#6e6e6e] hover:text-[#cccccc]'}"
                            )
                        )
                        with ctx_btn:
                            AntigravityIcon("plus", size=14)

                        if self.context_menu_open:
                            with (
                                ui.column()
                                .props('data-testid="context-picker-popover"')
                                .classes(
                                    "absolute left-0 bottom-full mb-2 w-72 bg-[#191919] border border-[#222222] rounded-xl shadow-2xl p-2 z-50 gap-2"
                                )
                            ):
                                for cat_name, items in CONTEXT_PICKER_ITEMS.items():
                                    ui.label(cat_name).classes(
                                        "px-2 text-[10px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                                    )
                                    for aid, alabel, adetail in items:
                                        with (
                                            ui.button(
                                                on_click=lambda i=aid, lbl=alabel: (
                                                    self._add_context_attachment(i, lbl)
                                                )
                                            )
                                            .props(
                                                f'flat dense no-caps data-testid="context-item-{aid}"'
                                            )
                                            .classes(
                                                "w-full px-2 py-1 rounded hover:bg-[#272727] flex items-center justify-between text-left font-normal"
                                            )
                                        ):
                                            ui.label(alabel).classes(
                                                "text-[11px] text-[#cccccc] truncate"
                                            )
                                            ui.label(adetail).classes(
                                                "text-[10px] text-[#6e6e6e] font-mono"
                                            )

                    # Zero-state Environment selector pill (Local / Worktree)
                    if is_zero_state:
                        env_btn = (
                            ui.button(on_click=self._toggle_environment_mode)
                            .props(
                                'flat dense no-caps data-testid="environment-selector"'
                            )
                            .classes(
                                "px-2.5 py-1 bg-[#151515] hover:bg-[#272727] border border-[#222222] rounded-lg text-[11px] text-[#cccccc] flex items-center gap-1.5 min-h-0 font-normal"
                            )
                        )
                        with env_btn:
                            AntigravityIcon("branch", size=12, classes="text-[#6e6e6e]")
                            ui.label(self.environment_mode)

                    # Modes Trigger & Popover (HBb: Autonomous Mode & Best of N)
                    with ui.element("div").classes("relative"):
                        modes_btn = (
                            ui.button(on_click=self._toggle_modes_popover)
                            .props(
                                'flat dense no-caps data-testid="internal-modes-trigger"'
                            )
                            .classes(
                                f"px-2.5 py-1 rounded-lg border text-[11px] flex items-center gap-1.5 min-h-0 font-normal "
                                f"{'bg-[#272727] border-[#cccccc]/30 text-[#cccccc]' if self.modes_open else 'bg-[#151515] border-[#222222] text-[#6e6e6e] hover:text-[#cccccc]'}"
                            )
                        )
                        with modes_btn:
                            AntigravityIcon("tune", size=13)
                            ui.label("Modes")

                        if self.modes_open:
                            with (
                                ui.column()
                                .props('data-testid="modes-popover"')
                                .classes(
                                    "absolute left-0 bottom-full mb-2 w-64 bg-[#191919] border border-[#222222] rounded-xl shadow-2xl p-2.5 z-50 gap-2"
                                )
                            ):
                                ui.label("Execution Modes").classes(
                                    "text-[10px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                                )
                                with (
                                    ui.button(on_click=self._toggle_autonomous_mode)
                                    .props(
                                        'flat dense no-caps data-testid="autonomous-mode-row"'
                                    )
                                    .classes(
                                        "w-full px-2 py-1.5 rounded hover:bg-[#272727] flex items-center justify-between text-left font-normal"
                                    )
                                ):
                                    ui.label("Autonomous Mode").classes(
                                        "text-[12px] text-[#cccccc]"
                                    )
                                    ui.label(
                                        "ON" if self.autonomous_mode else "OFF"
                                    ).classes(
                                        f"text-[10px] font-mono px-1.5 py-0.5 rounded "
                                        f"{'bg-emerald-500/20 text-emerald-400' if self.autonomous_mode else 'bg-[#272727] text-[#6e6e6e]'}"
                                    )
                                with (
                                    ui.button(on_click=self._toggle_best_of_n)
                                    .props(
                                        'flat dense no-caps data-testid="best-of-n-toggle"'
                                    )
                                    .classes(
                                        "w-full px-2 py-1.5 rounded hover:bg-[#272727] flex items-center justify-between text-left font-normal"
                                    )
                                ):
                                    ui.label("Best of N (Battle Mode)").classes(
                                        "text-[12px] text-[#cccccc]"
                                    )
                                    ui.label(
                                        "ON" if self.best_of_n_mode else "OFF"
                                    ).classes(
                                        f"text-[10px] font-mono px-1.5 py-0.5 rounded "
                                        f"{'bg-blue-500/20 text-blue-400' if self.best_of_n_mode else 'bg-[#272727] text-[#6e6e6e]'}"
                                    )

                    # Side Question Trigger
                    sq_btn = (
                        ui.button(
                            "Side Question",
                            on_click=self._toggle_side_question,
                        )
                        .props('flat dense no-caps data-testid="side-question-trigger"')
                        .classes(
                            f"px-2.5 py-1 rounded-lg border text-[11px] min-h-0 font-normal "
                            f"{'bg-[#272727] border-[#cccccc]/30 text-[#cccccc]' if self.side_question_open else 'bg-[#151515] border-[#222222] text-[#6e6e6e] hover:text-[#cccccc]'}"
                        )
                    )
                    _ = sq_btn

                    # Permissions Preset Selector (Awb)
                    perm_btn = (
                        ui.button(on_click=self._cycle_permission_preset)
                        .props(
                            'flat dense no-caps data-testid="permissions-selector-trigger"'
                        )
                        .classes(
                            "px-2.5 py-1 bg-[#151515] hover:bg-[#272727] border border-[#222222] rounded-lg text-[11px] text-[#cccccc] flex items-center gap-1.5 min-h-0 font-normal"
                        )
                    )
                    with perm_btn:
                        AntigravityIcon("shield", size=12, classes="text-emerald-400")
                        ui.label(f"Permissions: {self.permission_preset}")

                    # 1:1 Antigravity Model Selector
                    AntigravityModelSelector(
                        selected_model=self.selected_model,
                        on_select_model=self._handle_model_change,
                        on_open_models_settings=lambda: (
                            self.on_open_settings("models")
                            if self.on_open_settings
                            else None
                        ),
                        initial_open=self.model_open,
                    )

                # Right Controls: Send Prompt Button
                send_btn = (
                    ui.button(on_click=self._handle_send)
                    .props('flat dense no-caps data-testid="composer-send-button"')
                    .classes(
                        "p-2 rounded-full bg-[#cccccc] hover:bg-white text-[#101010] transition-colors min-h-0 min-w-0"
                    )
                )
                with send_btn:
                    AntigravityIcon("send_arrow", size=14)

    def _on_prompt_change(self, val: str) -> None:
        self.input_text = val
        if val.startswith("/") and not self.fastpick_open:
            self.fastpick_open = True
            self.render()
        elif not val.startswith("/") and self.fastpick_open:
            self.fastpick_open = False
            self.render()

    def _select_slash_command(self, cmd: str) -> None:
        self.input_text = f"{cmd} "
        self.fastpick_open = False
        self.render()

    def _toggle_context_menu(self) -> None:
        self.context_menu_open = not self.context_menu_open
        self.render()

    def _add_context_attachment(self, att_id: str, label: str) -> None:
        if not any(a.id == att_id for a in self.attachments):
            self.attachments.append(
                ContextAttachment(id=att_id, label=label, category="file")
            )
        self.context_menu_open = False
        self.render()

    def _remove_attachment(self, att_id: str) -> None:
        self.attachments = [a for a in self.attachments if a.id != att_id]
        self.render()

    def _toggle_environment_mode(self) -> None:
        self.environment_mode = (
            "Worktree" if self.environment_mode == "Local" else "Local"
        )
        self.render()

    def _toggle_modes_popover(self) -> None:
        self.modes_open = not self.modes_open
        self.render()

    def _toggle_autonomous_mode(self) -> None:
        self.autonomous_mode = not self.autonomous_mode
        self.settings.lab_autonomous_mode = self.autonomous_mode
        self.render()

    def _toggle_best_of_n(self) -> None:
        self.best_of_n_mode = not self.best_of_n_mode
        self.render()

    def _toggle_side_question(self) -> None:
        self.side_question_open = not self.side_question_open
        self.render()

    def _submit_side_question(self) -> None:
        if self.side_question_input.strip():
            self.side_question_answer = f"Answer: '{self.side_question_input.strip()}' verified against nicegui_ai.antigravity state."
            self.render()

    def _cycle_permission_preset(self) -> None:
        presets: list[Literal["Strict", "Default", "Auto", "Turbo"]] = [
            "Strict",
            "Default",
            "Auto",
            "Turbo",
        ]
        idx = (presets.index(self.permission_preset) + 1) % len(presets)
        self.permission_preset = presets[idx]
        self.render()

    def _handle_model_change(self, model: str) -> None:
        self.selected_model = model
        self.model_open = False
        if self.on_model_change:
            self.on_model_change(model)
        self.render()

    def _handle_effort_change(self, effort: Literal["Low", "Medium", "High"]) -> None:
        self.selected_effort = effort
        if self.on_effort_change:
            self.on_effort_change(effort)
        self.render()

    def _handle_send(self) -> None:
        text = self.input_text.strip()
        if not text:
            return
        atts = list(self.attachments)
        self.input_text = ""
        self.attachments = []
        self.fastpick_open = False
        if self.on_send_message:
            self.on_send_message(text, atts)
        self.render()
