"""1:1 Antigravity Right Auxiliary Pane (Overview, Review Diffs, Terminal, File/Artifact, Browser, Subagents)."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from nicegui import ui

from .icons import AntigravityIcon
from .state import ArtifactItem, SubagentItem

AuxTabType = Literal[
    "overview",
    "review",
    "terminal",
    "file",
    "browser",
    "agents",
    "new-tab",
]


@dataclass
class DiffLine:
    type: Literal["context", "add", "del", "hunk"]
    text: str
    old_num: int | None = None
    new_num: int | None = None


@dataclass
class ChangedFile:
    name: str
    path: str
    additions: int
    deletions: int
    status: Literal["modified", "added", "deleted"]
    lines: list[DiffLine]


CHANGED_FILES: list[ChangedFile] = [
    ChangedFile(
        name="auxiliary_pane.py",
        path="src/nicegui_ai/antigravity/auxiliary_pane.py",
        additions=184,
        deletions=22,
        status="modified",
        lines=[
            DiffLine(
                type="hunk",
                text="@@ -220,10 +220,28 @@ class AuxiliaryPane(ui.element):",
            ),
            DiffLine(old_num=220, new_num=220, type="context", text="    def _render_overview(self) -> None:"),
            DiffLine(old_num=221, new_num=None, type="del", text='        with ui.column().classes("p-4 gap-4"):'),
            DiffLine(
                old_num=None,
                new_num=221,
                type="add",
                text='        with ui.column().classes("flex-auto w-full min-h-0 gap-0").props(\'data-testid="overview-panel"\'):',
            ),
            DiffLine(
                old_num=None,
                new_num=222,
                type="add",
                text='            with ui.column().classes("shrink-0 gap-px p-1 border-b border-[#222222] w-full"):',
            ),
            DiffLine(
                old_num=None,
                new_num=223,
                type="add",
                text='                self._overview_row("overview-panel-row-review", "review_tab", "Review", "review")',
            ),
            DiffLine(
                old_num=None,
                new_num=224,
                type="add",
                text='                self._overview_row("overview-panel-row-files", "file_doc", "Files", "file")',
            ),
            DiffLine(
                old_num=None,
                new_num=225,
                type="add",
                text='                self._overview_row("overview-panel-row-terminal", "terminal_tab", "Terminal", "terminal")',
            ),
        ],
    ),
    ChangedFile(
        name="chat_view.py",
        path="src/nicegui_ai/antigravity/chat_view.py",
        additions=245,
        deletions=38,
        status="modified",
        lines=[
            DiffLine(
                type="hunk",
                text="@@ -512,8 +512,19 @@ class ChatView(ui.element):",
            ),
            DiffLine(old_num=512, new_num=512, type="context", text="    # Composer Footer (MBb at 5441000)"),
            DiffLine(old_num=513, new_num=None, type="del", text='    with ui.row().classes("items-center gap-1"):' ),
            DiffLine(
                old_num=None,
                new_num=513,
                type="add",
                text='    with ui.row().classes("w-full items-center justify-between gap-1 p-0.5"):',
            ),
            DiffLine(
                old_num=None,
                new_num=514,
                type="add",
                text="        self._render_modes_trigger()",
            ),
            DiffLine(
                old_num=None,
                new_num=515,
                type="add",
                text="        self._render_permissions_selector()",
            ),
        ],
    ),
    ChangedFile(
        name="customizations_view.py",
        path="src/nicegui_ai/antigravity/customizations_view.py",
        additions=312,
        deletions=0,
        status="added",
        lines=[
            DiffLine(type="hunk", text="@@ -0,0 +1,14 @@"),
            DiffLine(
                old_num=None,
                new_num=1,
                type="add",
                text="class WorkspaceCustomizationsView(ui.element):",
            ),
            DiffLine(
                old_num=None,
                new_num=2,
                type="add",
                text='    """1:1 Workspace Customizations View (Skills, Rules, Plugins, Custom Agents)."""',
            ),
        ],
    ),
]


SOURCE_FILES: dict[str, dict[str, object]] = {
    "antigravity_rea_reconstruction.md": {
        "lang": "Markdown Artifact",
        "frontmatter": {
            "title": "Antigravity 1:1 Desktop UI/UX Reconstruction",
            "status": "Verified (0 diffs)",
            "bundle": "nicegui_ai.antigravity",
        },
        "content": (
            "# Antigravity 1:1 Desktop UI/UX Reconstruction\n\n"
            "> **100% 1-to-1 UI/UX Parity Verified**: Reconstructed directly into Python & NiceGUI components in `src/nicegui_ai/antigravity/`.\n\n"
            "## Verified Component Mapping\n\n"
            "- **Overview Panel (`P_b` / `N_b` / `O_b`)**: Modular sections for Subagents, Background Tasks, Goals, Artifacts, Documents, Links, Modified Files, and Uploads.\n"
            "- **Review Changes (`diff-view-mode-trigger`)**: Collapsible unified/split code diffs with inline gutter comments (`comment-box`).\n"
            "- **Composer Controls (`MBb`)**: `/` Fastpick menu, Modes (`Autonomous Mode`, `Best of N`), Permissions Preset (`Awb`), and Side Question panel."
        ),
    },
    "src/nicegui_ai/antigravity/app.py": {
        "lang": "Python NiceGUI",
        "content": (
            "from nicegui import ui\n"
            "from .sidebar import Sidebar\n"
            "from .chat_view import ChatView\n"
            "from .auxiliary_pane import AuxiliaryPane\n"
            "from .settings_modal import SettingsModal\n"
            "from .history_view import ConversationHistoryView, SearchConversationsModal\n"
            "from .automations_view import AutomationsView\n"
            "from .customizations_view import WorkspaceCustomizationsView\n"
        ),
    },
    "src/nicegui_ai/antigravity/chat_view.py": {
        "lang": "Python NiceGUI",
        "content": (
            "# chat_view.py — 1:1 Conversation Stream, Zero-State Home (rYb), Kebab Menu (LMb),\n"
            "# Fastpick Slash Menu (pmb), Modes (HBb), Permissions (Awb), and Lifted Context Menu.\n"
            "class ChatView(ui.element):\n"
            "    pass\n"
        ),
    },
    "AGENTS.md": {
        "lang": "Markdown Rule",
        "frontmatter": {
            "scope": "Workspace",
            "enforcement": "Always On",
        },
        "content": (
            "# AGENTS.md — nicegui-ai Antigravity Suite\n\n"
            "1. Preserve 100% 1:1 DOM, CSS token, and data-testid parity with `main.js`.\n"
            "2. Verify all UI changes via `uv run ruff check .`, `uv run mypy src`, and `uv run pytest`.\n"
            "3. Capture headless Chromium screenshots with `scripts/capture_screenshots.py`."
        ),
    },
}


class AuxiliaryPane(ui.element):
    """1:1 Antigravity Right Auxiliary Pane with 6 tabs, + menu, and full interactive subviews."""

    def __init__(
        self,
        *,
        is_open: bool = True,
        active_artifact: ArtifactItem | None = None,
        subagents: list[SubagentItem] | None = None,
        artifact_width: Literal["compact", "default", "wide", "full"] = "default",
        initial_tab: AuxTabType = "terminal",
        initial_open_plus: bool = False,
        initial_open_overview_customize: bool = False,
        initial_open_diff_comment: bool = False,
        on_close: Callable[[], None] | None = None,
        on_tab_change: Callable[[AuxTabType], None] | None = None,
    ) -> None:
        super().__init__("aside")
        self.is_open = is_open
        self.active_artifact = active_artifact
        self.subagents = subagents or []
        self.artifact_width = artifact_width
        self.active_tab: AuxTabType = initial_tab
        self.plus_dropdown_open = initial_open_plus
        self.customize_overview_open = initial_open_overview_customize
        self.is_maximized = False
        self.on_close = on_close
        self.on_tab_change = on_tab_change

        # Overview state
        self.enabled_overview_sections: dict[str, bool] = {
            "subagents": True,
            "backgroundTasks": True,
            "goals": True,
            "artifacts": True,
            "documents": True,
            "links": True,
            "modifiedFiles": True,
            "uploads": False,
        }
        self.collapsed_overview_sections: dict[str, bool] = {}

        # Review state
        self.diff_mode: Literal["all", "uncommitted", "last-turn"] = "all"
        self.diff_view_style: Literal["unified", "split"] = "unified"
        self.expanded_diff_files: dict[str, bool] = {
            "src/nicegui_ai/antigravity/auxiliary_pane.py": True,
            "src/nicegui_ai/antigravity/chat_view.py": True,
            "src/nicegui_ai/antigravity/customizations_view.py": False,
        }
        self.active_comment_line_key: str | None = (
            "src/nicegui_ai/antigravity/auxiliary_pane.py:add:221"
            if initial_open_diff_comment
            else None
        )

        self.draft_comment = (
            "Verify OverviewPanel customize sections match P_b/O_b in main.js"
            if initial_open_diff_comment
            else ""
        )
        self.submitted_comments: list[dict[str, str]] = [
            {
                "id": "c-1",
                "file": "src/nicegui_ai/antigravity/auxiliary_pane.py",
                "line": "223",
                "author": "Van Luther",
                "text": "Confirmed overview-panel-row-review matches main.js offset 6587500.",
                "timestamp": "4m ago",
            }
        ]

        # Terminal state
        self.terminal_lines: list[dict[str, str]] = [
            {"cmd": "ps aux | grep -i antigravity", "output": "vanluther 3366 /home/vanluther/Downloads/Antigravity/Antigravity-x64/antigravity"},
            {"cmd": "uv run pytest", "output": "======================== 28 passed in 0.84s ========================"},
        ]
        self.terminal_input = ""
        self.active_process_id = "proc-1"

        # File / Artifact viewer state
        self.selected_source_file = "antigravity_rea_reconstruction.md"
        self.file_tree_open = True

        # Browser state
        self.browser_url = "http://127.0.0.1:8080"
        self.browser_reload_count = 0

        # Subagents state
        self.selected_subagent_id = (
            self.subagents[0].id if self.subagents else "ag-self"
        )
        self.subagent_states: dict[str, str] = {}
        self.subagent_prompts: dict[str, list[dict[str, str]]] = {}

        self.props('data-testid="auxiliary-pane"')
        self._apply_root_classes()
        self.render()

    def _apply_root_classes(self) -> None:
        width_cls = (
            "flex-1"
            if self.is_maximized
            else "w-[680px]"
            if self.artifact_width == "wide"
            else "w-[780px]"
            if self.artifact_width == "full"
            else "w-[560px]"
        )
        self._classes.clear()
        if not self.is_open:
            self.classes("hidden")
            return
        self.classes(
            f"{width_cls} bg-[#101010] border-l border-[#222222] flex flex-col h-full shrink-0 select-none relative z-20"
        )

    def set_tab(self, tab: AuxTabType) -> None:
        self.active_tab = tab
        self.plus_dropdown_open = False
        if self.on_tab_change:
            self.on_tab_change(tab)
        self.render()

    def set_open(self, open_state: bool) -> None:
        self.is_open = open_state
        self._apply_root_classes()
        self.render()

    def render(self) -> None:
        self.clear()
        self._apply_root_classes()
        if not self.is_open:
            return

        with self:
            self._render_header_bar()
            if self.active_tab == "overview":
                self._render_overview_tab()
            elif self.active_tab == "review":
                self._render_review_tab()
            elif self.active_tab == "terminal":
                self._render_terminal_tab()
            elif self.active_tab == "file":
                self._render_file_tab()
            elif self.active_tab == "browser":
                self._render_browser_tab()
            elif self.active_tab == "agents":
                self._render_subagents_tab()
            elif self.active_tab == "new-tab":
                self._render_new_tab_view()

    def _render_header_bar(self) -> None:
        with ui.row().classes(
            "h-[40px] px-2 border-b border-[#222222] items-center justify-between shrink-0 bg-[#101010] w-full gap-1 relative"
        ):
            with ui.row().classes("items-center gap-0.5 relative"):
                self._tab_icon_btn("overview", "overview_tab", "Overview", "aux-tab-overview")
                self._tab_icon_btn("review", "review_tab", "Review Changes", "aux-tab-review", badge="3")
                self._tab_icon_btn("terminal", "terminal_tab", "Terminal", "aux-tab-terminal")
                self._tab_icon_btn("file", "file_doc", "Files & Artifacts", "aux-tab-file")
                self._tab_icon_btn("browser", "globe", "Browser Preview", "aux-tab-browser")
                self._tab_icon_btn(
                    "agents",
                    "subagent",
                    "Subagents Inspector",
                    "aux-tab-agents",
                    badge=str(len(self.subagents)),
                )

                # '+' button with dropdown
                with ui.element("div").classes("relative ml-0.5"):
                    plus_btn = (
                        ui.button(on_click=self._toggle_plus_dropdown)
                        .props('flat dense no-caps data-testid="aux-plus-button"')
                        .classes(
                            f"p-1.5 rounded-md transition-colors min-h-0 min-w-0 "
                            f"{'text-[#cccccc] bg-[#272727]' if self.plus_dropdown_open or self.active_tab == 'new-tab' else 'text-[#6e6e6e] hover:text-[#cccccc] hover:bg-[#191919]/60'}"
                        )
                    )
                    with plus_btn:
                        AntigravityIcon("plus", size=14)

                    if self.plus_dropdown_open:
                        with ui.column().props('data-testid="aux-panel-plus-dropdown-menu"').classes(
                            "absolute left-0 top-full mt-1 w-48 bg-[#191919] border border-[#222222] rounded-lg shadow-2xl py-1 z-50 gap-0"
                        ):
                            ui.label("Open Auxiliary Tab").classes(
                                "px-2.5 py-1 text-[10px] font-medium uppercase tracking-wider text-[#6e6e6e]"
                            )
                            plus_items: list[tuple[AuxTabType, str, str, str]] = [
                                ("overview", "overview_tab", "Overview", "Ctrl+Shift+O"),
                                ("review", "review_tab", "Review Changes", "Ctrl+Shift+R"),
                                ("terminal", "terminal_tab", "Terminal", "Ctrl+`"),
                                ("file", "file_doc", "File & Artifact Viewer", "Ctrl+Shift+E"),
                                ("browser", "globe", "Browser Preview", "Ctrl+Shift+B"),
                                ("agents", "subagent", "Subagents Inspector", "Ctrl+Shift+A"),
                            ]
                            for tab_id, icon_name, label, shortcut in plus_items:
                                with (
                                    ui.button(on_click=lambda t=tab_id: self.set_tab(t))
                                    .props(f'flat dense no-caps data-testid="aux-plus-item-{tab_id}"')
                                    .classes(
                                        "w-full px-2.5 py-1.5 text-[12px] text-[#cccccc] hover:bg-[#272727]/70 flex items-center justify-between rounded-none font-normal"
                                    )
                                ):
                                    with ui.row().classes("items-center gap-2"):
                                        AntigravityIcon(icon_name, size=14, classes="text-[#6e6e6e]")
                                        ui.label(label)
                                    ui.label(shortcut).classes("text-[10px] text-[#6e6e6e] font-mono")

            with ui.row().classes("items-center gap-1"):
                max_btn = (
                    ui.button(on_click=self._toggle_maximized)
                    .props('flat dense no-caps data-testid="aux-fullscreen-toggle"')
                    .classes("p-1.5 text-[#6e6e6e] hover:text-[#cccccc] rounded-md hover:bg-[#191919]/60 min-h-0 min-w-0")
                )
                with max_btn:
                    AntigravityIcon("fullscreen", size=14)

                close_btn = (
                    ui.button(on_click=self._handle_close)
                    .props('flat dense no-caps data-testid="aux-close-button"')
                    .classes("p-1.5 text-[#6e6e6e] hover:text-[#cccccc] rounded-md hover:bg-[#191919]/60 min-h-0 min-w-0")
                )
                with close_btn:
                    AntigravityIcon("close", size=14)

    def _tab_icon_btn(
        self,
        tab_id: AuxTabType,
        icon_name: str,
        tooltip: str,
        test_id: str,
        badge: str | None = None,
    ) -> None:
        is_active = self.active_tab == tab_id
        btn = (
            ui.button(on_click=lambda t=tab_id: self.set_tab(t))
            .props(f'flat dense no-caps data-testid="{test_id}" title="{tooltip}"')
            .classes(
                f"p-1.5 rounded-md transition-colors flex items-center gap-1 min-h-0 min-w-0 "
                f"{'text-[#cccccc] bg-[#272727]' if is_active else 'text-[#6e6e6e] hover:text-[#cccccc] hover:bg-[#191919]/60'}"
            )
        )
        with btn:
            AntigravityIcon(icon_name, size=15)
            if badge:
                ui.label(badge).classes(
                    "text-[9px] font-mono px-1 py-0.2 rounded bg-[#101010]/70 text-[#cccccc]"
                )

    def _toggle_plus_dropdown(self) -> None:
        self.plus_dropdown_open = not self.plus_dropdown_open
        self.render()

    def _toggle_maximized(self) -> None:
        self.is_maximized = not self.is_maximized
        self.render()

    def _handle_close(self) -> None:
        if self.on_close:
            self.on_close()
        else:
            self.set_open(False)

    # =========================================================================
    # TAB 1: OVERVIEW PANEL (P_b / N_b / O_b)
    # =========================================================================
    def _render_overview_tab(self) -> None:
        with (
            ui.column()
            .props('data-testid="overview-panel"')
            .classes("flex-auto w-full min-h-0 flex-col overflow-y-auto gap-0")
        ):
            # Top Header + Customize Trigger
            with ui.row().classes(
                "px-3 py-2 border-b border-[#222222] items-center justify-between w-full relative shrink-0"
            ):
                ui.label("Conversation Overview").classes("text-[12px] font-medium text-[#cccccc]")
                with ui.element("div").classes("relative"):
                    cust_btn = (
                        ui.button(on_click=self._toggle_overview_customize)
                        .props('flat dense no-caps data-testid="overview-panel-customize-trigger"')
                        .classes(
                            "px-2 py-1 rounded text-[11px] text-[#6e6e6e] hover:text-[#cccccc] hover:bg-[#191919] flex items-center gap-1 min-h-0"
                        )
                    )
                    with cust_btn:
                        AntigravityIcon("tune", size=13)
                        ui.label("Customize")

                    if self.customize_overview_open:
                        with ui.column().classes(
                            "absolute right-0 top-full mt-1 w-56 bg-[#191919] border border-[#222222] rounded-lg shadow-2xl p-2 z-50 gap-1"
                        ):
                            ui.label("Visible Sections").classes(
                                "px-1.5 py-0.5 text-[10px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                            )
                            section_labels = [
                                ("subagents", "Subagents"),
                                ("backgroundTasks", "Background Tasks"),
                                ("goals", "Goals"),
                                ("artifacts", "Artifacts"),
                                ("documents", "Documents"),
                                ("links", "Links"),
                                ("modifiedFiles", "Modified Files"),
                                ("uploads", "Uploads"),
                            ]
                            for sec_key, sec_label in section_labels:
                                enabled = self.enabled_overview_sections.get(sec_key, True)
                                with (
                                    ui.button(
                                        on_click=lambda k=sec_key: self._toggle_overview_section(k)
                                    )
                                    .props(f'flat dense no-caps data-testid="overview-customize-{sec_key}"')
                                    .classes(
                                        "w-full px-2 py-1 text-[11px] text-[#cccccc] hover:bg-[#272727]/60 rounded flex items-center justify-between font-normal"
                                    )
                                ):
                                    ui.label(sec_label)
                                    if enabled:
                                        AntigravityIcon("check", size=12, classes="text-emerald-400")

            # Quick Navigation Rows (Review, Files, Terminal, Browser, Plugins)
            with ui.column().classes("shrink-0 gap-px p-1.5 border-b border-[#222222] w-full"):
                self._overview_quick_row(
                    "overview-panel-row-review",
                    "review_tab",
                    "Review",
                    "3 modified files (+741 -60)",
                    lambda: self.set_tab("review"),
                )
                self._overview_quick_row(
                    "overview-panel-row-files",
                    "file_doc",
                    "Files",
                    "4 workspace documents",
                    lambda: self.set_tab("file"),
                )
                self._overview_quick_row(
                    "overview-panel-row-terminal",
                    "terminal_tab",
                    "Terminal",
                    "2 active shells",
                    lambda: self.set_tab("terminal"),
                )
                self._overview_quick_row(
                    "overview-panel-row-browser",
                    "globe",
                    "Browser",
                    self.browser_url,
                    lambda: self.set_tab("browser"),
                )
                self._overview_quick_row(
                    "overview-panel-row-plugins",
                    "extension",
                    "Plugins",
                    "3 MCP servers active",
                    lambda: self.set_tab("agents"),
                )

            # Modular Collapsible Sections
            with ui.column().classes("p-3 gap-3 w-full"):
                if self.enabled_overview_sections.get("goals", True):
                    with self._overview_section("goals", "Goals", "3/3 completed"):
                        goals = [
                            "Extract exact DOM, CSS tokens, and SVGs via morluto/rea",
                            "Reconstruct 1:1 Antigravity suite in nicegui_ai.antigravity",
                            "Verify all 26 UI views via pytest and headless Chromium",
                        ]
                        for g in goals:
                            with ui.row().classes("items-center gap-2 text-[11px] text-[#cccccc] py-0.5"):
                                AntigravityIcon("check", size=12, classes="text-emerald-400 shrink-0")
                                ui.label(g)

                if self.enabled_overview_sections.get("subagents", True):
                    with self._overview_section(
                        "subagents", "Subagents", f"{len(self.subagents)} configured"
                    ):
                        for agent in self.subagents:
                            with (
                                ui.button(on_click=lambda a=agent: self._open_subagent(a.id))
                                .props('flat dense no-caps')
                                .classes(
                                    "w-full px-2.5 py-1.5 bg-[#191919] hover:bg-[#272727]/60 border border-[#222222] rounded-md flex items-center justify-between font-normal"
                                )
                            ):
                                with ui.row().classes("items-center gap-2"):
                                    ui.element("span").classes("w-1.5 h-1.5 rounded-full bg-emerald-400")
                                    ui.label(agent.name).classes("text-[12px] text-[#cccccc] font-medium")
                                ui.label(agent.role).classes("text-[10px] text-[#6e6e6e] truncate max-w-[200px]")

                if self.enabled_overview_sections.get("backgroundTasks", True):
                    with self._overview_section("backgroundTasks", "Background Tasks", "2 running"):
                        tasks = [
                            ("task-cdp", "CDP Runtime Inspector (127.0.0.1:46349)", "Running"),
                            ("task-pytest", "uv run pytest -q", "Completed (0.84s)"),
                        ]
                        for _tid, tlabel, tstatus in tasks:
                            with ui.row().classes(
                                "w-full px-2.5 py-1.5 bg-[#191919] border border-[#222222] rounded-md items-center justify-between text-[11px]"
                            ):
                                ui.label(tlabel).classes("text-[#cccccc] font-mono text-[11px]")
                                ui.label(tstatus).classes("text-[10px] text-emerald-400")


                if self.enabled_overview_sections.get("artifacts", True) and self.active_artifact:
                    with self._overview_section("artifacts", "Artifacts", "1 artifact"):
                        with (
                            ui.button(on_click=lambda: self.set_tab("file"))
                            .props('flat dense no-caps')
                            .classes(
                                "w-full px-2.5 py-2 bg-[#191919] hover:bg-[#272727]/60 border border-[#222222] rounded-md flex items-center justify-between font-normal"
                            )
                        ):
                            with ui.row().classes("items-center gap-2"):
                                AntigravityIcon("file_doc", size=14, classes="text-blue-400")
                                ui.label(self.active_artifact.title).classes("text-[12px] text-[#cccccc]")
                            ui.label("Open ▸").classes("text-[10px] text-[#6e6e6e]")

                if self.enabled_overview_sections.get("modifiedFiles", True):
                    with self._overview_section(
                        "modifiedFiles", "Modified Files", f"{len(CHANGED_FILES)} files"
                    ):
                        for cf in CHANGED_FILES:
                            with (
                                ui.button(on_click=lambda: self.set_tab("review"))
                                .props('flat dense no-caps')
                                .classes(
                                    "w-full px-2.5 py-1.5 bg-[#191919] hover:bg-[#272727]/60 border border-[#222222] rounded-md flex items-center justify-between font-normal"
                                )
                            ):
                                ui.label(cf.path).classes("text-[11px] font-mono text-[#cccccc] truncate")
                                with ui.row().classes("items-center gap-1.5 font-mono text-[10px]"):
                                    ui.label(f"+{cf.additions}").classes("text-emerald-400")
                                    ui.label(f"-{cf.deletions}").classes("text-rose-400")

    def _overview_quick_row(
        self,
        test_id: str,
        icon_name: str,
        label: str,
        summary: str,
        on_click: Callable[[], None],
    ) -> None:
        with (
            ui.button(on_click=on_click)
            .props(f'flat dense no-caps data-testid="{test_id}"')
            .classes(
                "w-full px-2.5 py-1.5 rounded-md hover:bg-[#191919] flex items-center justify-between text-left font-normal"
            )
        ):
            with ui.row().classes("items-center gap-2"):
                AntigravityIcon(icon_name, size=14, classes="text-[#6e6e6e]")
                ui.label(label).classes("text-[12px] text-[#cccccc] font-medium")
            ui.label(summary).classes("text-[11px] text-[#6e6e6e]")

    def _overview_section(self, key: str, title: str, badge: str) -> ui.column:
        collapsed = self.collapsed_overview_sections.get(key, False)
        container = ui.column().classes("w-full gap-1.5")
        with container:
            with (
                ui.button(on_click=lambda k=key: self._toggle_collapse_overview_section(k))
                .props("flat dense no-caps")
                .classes("w-full flex items-center justify-between py-0.5 text-left font-normal")
            ):
                with ui.row().classes("items-center gap-1.5"):
                    AntigravityIcon(
                        "chevron_right" if collapsed else "chevron_down",
                        size=11,
                        classes="text-[#6e6e6e]",
                    )
                    ui.label(title).classes(
                        "text-[11px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                    )
                ui.label(badge).classes("text-[10px] text-[#6e6e6e]")
        body = ui.column().classes("w-full gap-1.5")
        if collapsed:
            body.classes("hidden")
        return body

    def _toggle_overview_customize(self) -> None:
        self.customize_overview_open = not self.customize_overview_open
        self.render()

    def _toggle_overview_section(self, key: str) -> None:
        self.enabled_overview_sections[key] = not self.enabled_overview_sections.get(
            key, True
        )
        self.render()

    def _toggle_collapse_overview_section(self, key: str) -> None:
        self.collapsed_overview_sections[key] = not self.collapsed_overview_sections.get(
            key, False
        )
        self.render()

    def _open_subagent(self, agent_id: str) -> None:
        self.selected_subagent_id = agent_id
        self.set_tab("agents")

    # =========================================================================
    # TAB 2: REVIEW DIFFS VIEW (diff-view-mode-trigger, code-gutter-diff)
    # =========================================================================
    def _render_review_tab(self) -> None:
        with (
            ui.column()
            .props('data-testid="review-changes-tab"')
            .classes("flex-1 flex flex-col overflow-hidden w-full gap-0")
        ):
            # Toolbar
            with ui.row().classes(
                "px-3 py-2 border-b border-[#222222] bg-[#151515]/50 items-center justify-between w-full shrink-0"
            ):
                with ui.row().classes("items-center gap-2"):
                    mode_labels = {
                        "all": "All conversation changes",
                        "uncommitted": "Uncommitted changes",
                        "last-turn": "Last agent turn",
                    }
                    mode_btn = (
                        ui.button(on_click=self._cycle_diff_mode)
                        .props('flat dense no-caps data-testid="diff-view-mode-trigger"')
                        .classes(
                            "px-2.5 py-1 bg-[#191919] border border-[#222222] rounded-md text-[11px] text-[#cccccc] flex items-center gap-1.5 min-h-0 font-normal"
                        )
                    )
                    with mode_btn:
                        ui.label(mode_labels[self.diff_mode])
                        AntigravityIcon("chevron_down", size=11, classes="text-[#6e6e6e]")

                    with ui.row().classes("items-center gap-1 text-[11px] font-mono"):
                        ui.label("+741").classes("text-emerald-400")
                        ui.label("-60").classes("text-rose-400")

                with ui.row().classes("items-center gap-1 bg-[#191919] p-0.5 rounded-md border border-[#222222]"):
                    for style in ("unified", "split"):
                        active = self.diff_view_style == style
                        ui.button(
                            style.capitalize(),
                            on_click=lambda s=style: self._set_diff_style(s),
                        ).props("flat dense no-caps").classes(
                            f"px-2 py-0.5 rounded text-[11px] min-h-0 font-normal "
                            f"{'bg-[#272727] text-[#cccccc]' if active else 'text-[#6e6e6e] hover:text-[#cccccc]'}"
                        )

            # File Diffs Accordion List
            with ui.column().classes("flex-1 overflow-y-auto p-3 gap-3 w-full"):
                for cf in CHANGED_FILES:
                    expanded = self.expanded_diff_files.get(cf.path, True)
                    with ui.column().classes(
                        "w-full border border-[#222222] rounded-lg overflow-hidden bg-[#151515]/30 gap-0"
                    ):
                        # File Header
                        with (
                            ui.button(on_click=lambda p=cf.path: self._toggle_diff_file(p))
                            .props('flat dense no-caps data-testid="file-diff-accordion-toggle"')
                            .classes(
                                "w-full px-3 py-2 bg-[#191919] hover:bg-[#272727]/50 flex items-center justify-between font-normal rounded-none"
                            )
                        ):
                            with ui.row().classes("items-center gap-2"):
                                AntigravityIcon(
                                    "chevron_down" if expanded else "chevron_right",
                                    size=11,
                                    classes="text-[#6e6e6e]",
                                )
                                ui.label(cf.path).classes("text-[12px] font-mono text-[#cccccc]")
                            with ui.row().classes("items-center gap-1.5 font-mono text-[11px]"):
                                ui.label(f"+{cf.additions}").classes("text-emerald-400")
                                ui.label(f"-{cf.deletions}").classes("text-rose-400")

                        if expanded:
                            with (
                                ui.column()
                                .props('data-testid="code-gutter-diff"')
                                .classes("w-full font-mono text-[11px] divide-y divide-[#222222]/40 gap-0")
                            ):
                                for idx, dl in enumerate(cf.lines):
                                    line_num = dl.new_num or dl.old_num or idx
                                    line_key = f"{cf.path}:{dl.type}:{line_num}"
                                    bg_cls = (

                                        "bg-emerald-500/10 text-emerald-200"
                                        if dl.type == "add"
                                        else "bg-rose-500/10 text-rose-200"
                                        if dl.type == "del"
                                        else "bg-blue-500/10 text-blue-300"
                                        if dl.type == "hunk"
                                        else "text-[#cccccc]/85"
                                    )
                                    with ui.row().classes(
                                        f"w-full px-2 py-0.5 items-center gap-2 group {bg_cls} no-wrap"
                                    ):
                                        ui.label(str(dl.old_num or "")).classes(
                                            "w-7 text-right text-[10px] text-[#6e6e6e] shrink-0"
                                        )
                                        ui.label(str(dl.new_num or "")).classes(
                                            "w-7 text-right text-[10px] text-[#6e6e6e] shrink-0"
                                        )
                                        comment_btn = (
                                            ui.button(
                                                "+",
                                                on_click=lambda k=line_key: self._open_diff_comment(k),
                                            )
                                            .props('flat dense no-caps data-testid="gutter-comment-button"')
                                            .classes(
                                                "w-4 h-4 rounded bg-blue-600/80 text-white text-[10px] opacity-80 hover:opacity-100 min-h-0 min-w-0 p-0 shrink-0"
                                            )
                                        )
                                        _ = comment_btn
                                        prefix = (
                                            "+"
                                            if dl.type == "add"
                                            else "-"
                                            if dl.type == "del"
                                            else " "
                                        )
                                        ui.label(f"{prefix} {dl.text}").classes(
                                            "truncate flex-1 font-mono text-[11px]"
                                        )

                                    # Inline comment editor if active
                                    if self.active_comment_line_key == line_key:
                                        with (
                                            ui.column()
                                            .props('data-testid="comment-box"')
                                            .classes("w-full p-3 bg-[#191919] border-y border-[#222222] gap-2")
                                        ):
                                            ui.label(f"Add inline review comment on {line_key}").classes(
                                                "text-[11px] text-[#6e6e6e]"
                                            )
                                            comment_input = (
                                                ui.textarea(
                                                    value=self.draft_comment,
                                                    on_change=lambda e: setattr(
                                                        self, "draft_comment", str(e.value)
                                                    ),
                                                )
                                                .props("outlined dense autogrow dark")
                                                .classes("w-full text-[12px] bg-[#101010]")
                                            )
                                            _ = comment_input
                                            with ui.row().classes("justify-end gap-2 w-full"):
                                                ui.button(
                                                    "Cancel",
                                                    on_click=lambda: self._open_diff_comment(None),
                                                ).props("flat dense no-caps").classes(
                                                    "px-2.5 py-1 text-[11px] text-[#6e6e6e] hover:text-[#cccccc]"
                                                )
                                                ui.button(
                                                    "Add Comment",
                                                    on_click=lambda f=cf.path, ln=str(line_num): self._submit_diff_comment(f, ln),
                                                ).props("flat dense no-caps").classes(
                                                    "px-3 py-1 bg-blue-600 text-white rounded text-[11px]"
                                                )

                # Existing Review Comments
                if self.submitted_comments:
                    ui.label("Review Comments").classes(
                        "text-[11px] font-semibold uppercase tracking-wider text-[#6e6e6e] mt-2"
                    )
                    for sc in self.submitted_comments:
                        with (
                            ui.column()
                            .props('data-testid="comment-card"')
                            .classes("w-full p-2.5 bg-[#191919] border border-[#222222] rounded-lg gap-1")
                        ):
                            with ui.row().classes("items-center justify-between w-full"):
                                ui.label(f"{sc['author']} • {sc['file']}:{sc['line']}").classes(
                                    "text-[11px] font-medium text-[#cccccc]"
                                )
                                ui.label(sc["timestamp"]).classes("text-[10px] text-[#6e6e6e]")
                            ui.label(sc["text"]).classes("text-[12px] text-[#cccccc]/90")

    def _cycle_diff_mode(self) -> None:
        order: list[Literal["all", "uncommitted", "last-turn"]] = [
            "all",
            "uncommitted",
            "last-turn",
        ]
        idx = (order.index(self.diff_mode) + 1) % len(order)
        self.diff_mode = order[idx]
        self.render()

    def _set_diff_style(self, style: Literal["unified", "split"]) -> None:
        self.diff_view_style = style
        self.render()

    def _toggle_diff_file(self, path: str) -> None:
        self.expanded_diff_files[path] = not self.expanded_diff_files.get(path, True)
        self.render()

    def _open_diff_comment(self, line_key: str | None) -> None:
        self.active_comment_line_key = line_key
        self.render()

    def _submit_diff_comment(self, file_path: str, line_num: str) -> None:
        if self.draft_comment.strip():
            self.submitted_comments.append(
                {
                    "id": f"c-{len(self.submitted_comments) + 1}",
                    "file": file_path,
                    "line": line_num,
                    "author": "Van Luther",
                    "text": self.draft_comment.strip(),
                    "timestamp": "Just now",
                }
            )
        self.draft_comment = ""
        self.active_comment_line_key = None
        self.render()

    # =========================================================================
    # TAB 3: 2-COLUMN TERMINAL VIEW (~ ❯ █ + Right Process Tree)
    # =========================================================================
    def _render_terminal_tab(self) -> None:
        with (
            ui.row()
            .props('data-testid="terminal-tab-view"')
            .classes("flex-1 w-full h-full overflow-hidden gap-0 no-wrap")
        ):
            # Left Column: Interactive Terminal Output + Prompt
            with ui.column().classes(
                "flex-1 h-full bg-[#101010] p-3 font-mono text-[12px] overflow-y-auto justify-between"
            ):
                with ui.column().classes("w-full gap-2"):
                    for entry in self.terminal_lines:
                        with ui.row().classes("items-center gap-1.5 text-[#cccccc]"):
                            ui.label("~").classes("text-blue-400 font-semibold")
                            ui.label("❯").classes("text-emerald-400")
                            ui.label(entry["cmd"]).classes("text-[#cccccc]")
                        if entry.get("output"):
                            ui.label(entry["output"]).classes(
                                "text-[11px] text-[#6e6e6e] whitespace-pre-wrap pl-3"
                            )

                    with ui.row().classes("items-center gap-1.5 text-[#cccccc] mt-1"):
                        ui.label("~").classes("text-blue-400 font-semibold")
                        ui.label("❯").classes("text-emerald-400")
                        ui.element("span").classes("w-2 h-4 bg-[#cccccc] inline-block animate-pulse")

                # Bottom Command Input Bar
                with ui.row().classes(
                    "w-full pt-2 border-t border-[#222222] items-center gap-2"
                ):
                    cmd_input = (
                        ui.input(
                            placeholder="Run shell command in /mnt/storage/projects/nicegui-ai...",
                            value=self.terminal_input,
                            on_change=lambda e: setattr(self, "terminal_input", str(e.value)),
                        )
                        .props('borderless dense dark data-testid="terminal-command-input"')
                        .classes("flex-1 text-[12px] font-mono text-[#cccccc]")
                    )
                    cmd_input.on("keydown.enter", self._execute_terminal_cmd)
                    ui.button("Run", on_click=self._execute_terminal_cmd).props(
                        "flat dense no-caps"
                    ).classes("px-2.5 py-1 bg-[#191919] hover:bg-[#272727] rounded text-[11px] text-[#cccccc]")

            # Right Column: Conversations Process Tree Sidebar
            with ui.column().classes(
                "w-[190px] h-full bg-[#151515] border-l border-[#222222] p-2 shrink-0 gap-1"
            ):
                ui.label("Conversations").classes(
                    "px-2 py-1 text-[10px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                )
                processes = [
                    ("proc-1", "bash (nicegui-ai)", "Clone Antigravity UI"),
                    ("proc-2", "uv run pytest", "ModelSelector Reasoning"),
                ]
                for pid, plabel, pconv in processes:
                    active = self.active_process_id == pid
                    with (
                        ui.button(on_click=lambda i=pid: self._select_process(i))
                        .props("flat dense no-caps")
                        .classes(
                            f"w-full px-2 py-1.5 rounded-md text-left flex flex-col items-start gap-0.5 font-normal "
                            f"{'bg-[#272727] text-[#cccccc]' if active else 'text-[#6e6e6e] hover:text-[#cccccc] hover:bg-[#191919]'}"
                        )
                    ):
                        with ui.row().classes("items-center gap-1.5 w-full"):
                            AntigravityIcon("terminal_tab", size=12, classes="text-emerald-400")
                            ui.label(plabel).classes("text-[11px] font-mono truncate")
                        ui.label(pconv).classes("text-[10px] text-[#6e6e6e] truncate pl-4")

    def _execute_terminal_cmd(self) -> None:
        cmd = self.terminal_input.strip()
        if not cmd:
            return
        self.terminal_lines.append(
            {
                "cmd": cmd,
                "output": f"[Executed in /mnt/storage/projects/nicegui-ai]: {cmd} (exit code 0)",
            }
        )
        self.terminal_input = ""
        self.render()

    def _select_process(self, proc_id: str) -> None:
        self.active_process_id = proc_id
        self.render()

    # =========================================================================
    # TAB 4: ARTIFACT / FILE VIEWER (artifact-view, markdown-frontmatter)
    # =========================================================================
    def _render_file_tab(self) -> None:
        file_entry = SOURCE_FILES.get(
            self.selected_source_file,
            SOURCE_FILES["antigravity_rea_reconstruction.md"],
        )
        frontmatter = file_entry.get("frontmatter")
        content = str(file_entry.get("content", ""))

        with (
            ui.row()
            .props('data-testid="artifact-view"')
            .classes("flex-1 w-full h-full overflow-hidden gap-0 no-wrap")
        ):
            if self.file_tree_open:
                with (
                    ui.column()
                    .props('data-testid="tab-file-tree-sidebar"')
                    .classes("w-[185px] h-full bg-[#151515] border-r border-[#222222] p-2 shrink-0 gap-1")
                ):
                    ui.label("Workspace Files").classes(
                        "px-2 py-1 text-[10px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                    )
                    for fname in SOURCE_FILES:
                        is_sel = fname == self.selected_source_file
                        with (
                            ui.button(on_click=lambda f=fname: self._select_source_file(f))
                            .props("flat dense no-caps")
                            .classes(
                                f"w-full px-2 py-1.5 rounded text-left text-[11px] flex items-center gap-1.5 font-normal "
                                f"{'bg-[#272727] text-[#cccccc]' if is_sel else 'text-[#6e6e6e] hover:text-[#cccccc] hover:bg-[#191919]'}"
                            )
                        ):
                            AntigravityIcon("file_doc", size=12, classes="shrink-0")
                            ui.label(fname.split("/")[-1]).classes("truncate")

            # Document Content Area
            with ui.column().classes("flex-1 h-full overflow-y-auto p-4 gap-3"):
                with ui.row().classes(
                    "w-full items-center justify-between pb-2 border-b border-[#222222]"
                ):
                    with ui.row().classes("items-center gap-2"):
                        ui.button(
                            on_click=self._toggle_file_tree
                        ).props("flat dense no-caps").classes(
                            "p-1 text-[#6e6e6e] hover:text-[#cccccc] min-h-0 min-w-0"
                        )
                        ui.label(self.selected_source_file).classes(
                            "text-[12px] font-mono text-[#cccccc]"
                        )
                    ui.label(str(file_entry.get("lang", "Markdown"))).classes(
                        "text-[10px] px-2 py-0.5 rounded bg-[#191919] border border-[#222222] text-[#6e6e6e]"
                    )

                if isinstance(frontmatter, dict):
                    with (
                        ui.column()
                        .props('data-testid="markdown-frontmatter"')
                        .classes("w-full bg-[#191919] border border-[#222222] rounded-lg p-2.5 gap-1")
                    ):
                        for k, v in frontmatter.items():
                            with ui.row().classes("items-center justify-between text-[11px] w-full"):
                                ui.label(str(k)).classes("font-mono text-[#6e6e6e]")
                                ui.label(str(v)).classes("font-mono text-[#cccccc]")

                if str(file_entry.get("lang", "")).startswith("Markdown"):
                    ui.markdown(content).classes("text-[12px] text-[#cccccc] leading-relaxed w-full")
                else:
                    ui.code(content, language="python").classes("w-full text-[11px]")

    def _select_source_file(self, filename: str) -> None:
        self.selected_source_file = filename
        self.render()

    def _toggle_file_tree(self) -> None:
        self.file_tree_open = not self.file_tree_open
        self.render()

    # =========================================================================
    # TAB 5: BROWSER PREVIEW (browser-pane)
    # =========================================================================
    def _render_browser_tab(self) -> None:
        with (
            ui.column()
            .props('data-testid="browser-pane"')
            .classes("flex-1 w-full h-full overflow-hidden gap-0")
        ):
            with ui.row().classes(
                "px-3 py-2 border-b border-[#222222] bg-[#151515] items-center gap-2 w-full"
            ):
                AntigravityIcon("globe", size=14, classes="text-[#6e6e6e]")
                url_in = (
                    ui.input(
                        value=self.browser_url,
                        on_change=lambda e: setattr(self, "browser_url", str(e.value)),
                    )
                    .props('borderless dense dark data-testid="browser-url-bar"')
                    .classes(
                        "flex-1 px-2.5 py-0.5 bg-[#101010] border border-[#222222] rounded text-[11px] font-mono text-[#cccccc]"
                    )
                )
                _ = url_in
                ui.button(
                    "Reload",
                    on_click=self._reload_browser,
                ).props("flat dense no-caps").classes(
                    "px-2 py-1 bg-[#191919] hover:bg-[#272727] rounded text-[11px] text-[#cccccc]"
                )

            with ui.column().classes(
                "flex-1 w-full bg-[#101010] p-6 items-center justify-center gap-3 text-center"
            ):
                with ui.column().classes(
                    "max-w-md p-5 bg-[#191919] border border-[#222222] rounded-xl items-center gap-2"
                ):
                    AntigravityIcon("antigravity_logo", size=28, classes="text-[#cccccc]")
                    ui.label("Antigravity Headless Browser Target").classes(
                        "text-[14px] font-medium text-[#cccccc]"
                    )
                    ui.label(f"Connected to {self.browser_url} (CDP Port 46349)").classes(
                        "text-[11px] font-mono text-emerald-400"
                    )
                    ui.label(
                        "Live DOM & CSS Computed Style Inspector ready for agent visual verification."
                    ).classes("text-[12px] text-[#6e6e6e]")

    def _reload_browser(self) -> None:
        self.browser_reload_count += 1
        self.render()

    # =========================================================================
    # TAB 6: SUBAGENTS INSPECTOR (subagent-tab-sidebar, approve/deny/stop)
    # =========================================================================
    def _render_subagents_tab(self) -> None:
        selected = next(
            (a for a in self.subagents if a.id == self.selected_subagent_id),
            self.subagents[0] if self.subagents else None,
        )
        with (
            ui.row()
            .props('data-testid="subagents-inspector-view"')
            .classes("flex-1 w-full h-full overflow-hidden gap-0 no-wrap")
        ):
            # Left Sidebar
            with (
                ui.column()
                .props('data-testid="subagent-tab-sidebar"')
                .classes("w-[180px] h-full bg-[#151515] border-r border-[#222222] p-2 shrink-0 gap-1")
            ):
                ui.label("Subagents").classes(
                    "px-2 py-1 text-[10px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                )
                for agent in self.subagents:
                    is_sel = selected is not None and agent.id == selected.id
                    with (
                        ui.button(on_click=lambda a=agent: self._select_subagent(a.id))
                        .props("flat dense no-caps")
                        .classes(
                            f"w-full px-2 py-1.5 rounded text-left flex flex-col items-start gap-0.5 font-normal "
                            f"{'bg-[#272727] text-[#cccccc]' if is_sel else 'text-[#6e6e6e] hover:text-[#cccccc] hover:bg-[#191919]'}"
                        )
                    ):
                        ui.label(agent.name).classes("text-[11px] font-medium truncate w-full")
                        ui.label(self.subagent_states.get(agent.id, agent.state)).classes(
                            "text-[10px] text-emerald-400 font-mono"
                        )

            # Right Detail Inspector
            with ui.column().classes("flex-1 h-full p-4 overflow-y-auto gap-4"):
                if selected:
                    with ui.row().classes(
                        "w-full items-center justify-between pb-3 border-b border-[#222222]"
                    ):
                        with ui.column().classes("gap-0.5"):
                            ui.label(selected.name).classes("text-[14px] font-medium text-[#cccccc]")
                            ui.label(selected.role).classes("text-[11px] text-[#6e6e6e]")
                        with ui.row().classes("items-center gap-1.5"):
                            ui.button(
                                "Approve",
                                on_click=lambda a=selected: self._set_subagent_state(a.id, "approved"),
                            ).props('flat dense no-caps data-testid="subagent-approve"').classes(
                                "px-2.5 py-1 bg-emerald-600/20 text-emerald-300 border border-emerald-500/30 rounded text-[11px]"
                            )
                            ui.button(
                                "Deny",
                                on_click=lambda a=selected: self._set_subagent_state(a.id, "denied"),
                            ).props('flat dense no-caps data-testid="subagent-deny"').classes(
                                "px-2.5 py-1 bg-amber-600/20 text-amber-300 border border-amber-500/30 rounded text-[11px]"
                            )
                            ui.button(
                                "Stop",
                                on_click=lambda a=selected: self._set_subagent_state(a.id, "stopped"),
                            ).props('flat dense no-caps data-testid="subagent-stop"').classes(
                                "px-2.5 py-1 bg-rose-600/20 text-rose-300 border border-rose-500/30 rounded text-[11px]"
                            )

                    with ui.column().classes(
                        "w-full p-3 bg-[#191919] border border-[#222222] rounded-lg gap-1.5"
                    ):
                        ui.label("Latest Trajectory Step").classes(
                            "text-[10px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                        )
                        ui.label(selected.last_activity).classes("text-[12px] text-[#cccccc]")
                        ui.label(
                            f"Current status: {self.subagent_states.get(selected.id, selected.state)}"
                        ).classes("text-[11px] font-mono text-emerald-400")

    def _select_subagent(self, agent_id: str) -> None:
        self.selected_subagent_id = agent_id
        self.render()

    def _set_subagent_state(self, agent_id: str, new_state: str) -> None:
        self.subagent_states[agent_id] = new_state
        self.render()

    # =========================================================================
    # TAB 7: NEW TAB LAUNCHER (aux-pane-new-tab-view)
    # =========================================================================
    def _render_new_tab_view(self) -> None:
        with (
            ui.column()
            .props('data-testid="aux-pane-new-tab-view"')
            .classes("flex-1 p-6 items-center justify-center gap-4 w-full")
        ):
            ui.label("Open Auxiliary Surface").classes("text-[14px] font-medium text-[#cccccc]")
            cards: list[tuple[AuxTabType, str, str]] = [
                ("overview", "overview_tab", "Conversation Overview"),
                ("review", "review_tab", "Review File Diffs"),
                ("terminal", "terminal_tab", "Interactive Terminal"),
                ("file", "file_doc", "Artifact & File Viewer"),
                ("browser", "globe", "Browser Preview"),
                ("agents", "subagent", "Subagents Inspector"),
            ]
            with ui.grid(columns=2).classes("gap-3 w-full max-w-md"):
                for tab_id, icon_name, label in cards:
                    with (
                        ui.button(on_click=lambda t=tab_id: self.set_tab(t))
                        .props("flat dense no-caps")
                        .classes(
                            "p-3 bg-[#191919] hover:bg-[#272727] border border-[#222222] rounded-lg flex items-center gap-2.5 text-left font-normal"
                        )
                    ):
                        AntigravityIcon(icon_name, size=16, classes="text-[#cccccc]")
                        ui.label(label).classes("text-[12px] text-[#cccccc]")
