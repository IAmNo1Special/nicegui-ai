"""1:1 Antigravity Desktop Application Orchestrator & NiceGUI Page Entrypoint."""

import os
from typing import Literal
from urllib.parse import parse_qs

from fastapi import Request
from nicegui import ui

from nicegui_ai.adapters import BaseStreamAdapter

from .automations_view import AutomationsView
from .auxiliary_pane import AuxiliaryPane, AuxTabType
from .chat_view import ChatView
from .customizations_view import WorkspaceCustomizationsView
from .history_view import ConversationHistoryView, SearchConversationsModal
from .settings_modal import SettingsModal
from .sidebar import CenterViewType, Sidebar
from .state import (
    ArtifactItem,
    AutomationItem,
    ContextAttachment,
    Message,
    ProjectConfig,
    Session,
    ThinkingBlock,
    ToolCallItem,
    create_default_artifact,
    create_default_automations,
    create_default_sessions,
    create_default_settings,
    create_default_skills,
    create_default_subagents,
)
from .theme import setup_antigravity_theme
from .title_bar import TitleBar


class AntigravityApp(ui.element):
    """Complete 1:1 Antigravity Desktop UI/UX Application Shell in Python & NiceGUI."""

    def __init__(
        self,
        *,
        query_params: dict[str, str] | None = None,
        stream_adapter: BaseStreamAdapter | None = None,
    ) -> None:
        super().__init__("div")
        params = query_params or {}
        self.params = params
        self.stream_adapter = stream_adapter

        # Core State

        self.settings = create_default_settings()
        self.sessions = create_default_sessions()
        self.automations = create_default_automations()
        self.subagents = create_default_subagents()
        self.skills = create_default_skills()
        self.active_artifact: ArtifactItem | None = create_default_artifact()

        # Deep-link URL Query Parameter States (all 26 states supported)
        open_zero_state = params.get("openZeroState") == "true"
        self.active_session_id = (
            "session-zero-state" if open_zero_state else "session-clone-rea"
        )
        raw_view = params.get("view", "chat")
        self.center_view: CenterViewType = (
            raw_view  # type: ignore[assignment]
            if raw_view in ("chat", "history", "automations", "customizations")
            else "chat"
        )
        self.sidebar_open = True
        self.aux_open = params.get("openAux", "true") != "false"
        raw_aux_tab = params.get("auxTab", "terminal")
        self.aux_tab: AuxTabType = (
            raw_aux_tab  # type: ignore[assignment]
            if raw_aux_tab
            in ("overview", "review", "terminal", "file", "browser", "agents", "new-tab")
            else "terminal"
        )

        self.settings_open = params.get("openSettings") == "true"
        self.settings_screen = params.get("settingsScreen", "general")
        self.search_modal_open = params.get("openSearch") == "true"
        self.selected_model = "Gemini 3.8 Flash High"
        self.selected_effort: Literal["Low", "Medium", "High"] = "High"
        self.active_project_id: str | None = "proj-ag-studio"

        # Navigation Back/Forward Stack
        self.nav_history: list[tuple[CenterViewType, str]] = [
            (self.center_view, self.active_session_id)
        ]
        self.nav_index = 0

        self.props('data-testid="antigravity-app-shell"')
        self.classes(
            "w-screen h-screen flex flex-col bg-[#101010] text-[#cccccc] overflow-hidden select-none"
        )
        self.render()

    def _active_session(self) -> Session:

        return next(
            (s for s in self.sessions if s.id == self.active_session_id),
            self.sessions[0],
        )

    def _push_nav(self, view: CenterViewType, session_id: str) -> None:
        self.nav_history = self.nav_history[: self.nav_index + 1]
        self.nav_history.append((view, session_id))
        self.nav_index = len(self.nav_history) - 1

    def render(self) -> None:
        self.clear()
        with self:
            # 1. 35px Native Top Menu Bar
            TitleBar(
                on_new_conversation=lambda: self._handle_new_conversation(None),
                on_toggle_sidebar=self._handle_toggle_sidebar,
                on_toggle_aux=self._handle_toggle_aux,
                on_open_settings=lambda: self._handle_open_settings("general"),
                on_open_history=self._handle_open_history,
                on_open_automations=self._handle_open_automations,
                on_open_customizations=self._handle_open_customizations,
                on_open_search=lambda: self._handle_set_search_modal(True),
                on_select_aux_tab=self._handle_select_aux_tab_str,
                initial_open_menu=self.params.get("openMenu"),
            )

            # 2. Main 3-Column Workspace Area (Sidebar + Center View + Auxiliary Pane)
            with ui.row().classes(
                "flex-1 w-full min-h-0 overflow-hidden gap-0 no-wrap relative"
            ):
                if self.sidebar_open:
                    Sidebar(
                        active_session_id=self.active_session_id,
                        active_center_view=self.center_view,
                        sessions=self.sessions,
                        projects=self.settings.projects,
                        on_select_session=self._handle_select_session,
                        on_new_conversation=self._handle_new_conversation,
                        on_open_history=self._handle_open_history,
                        on_open_automations=self._handle_open_automations,
                        on_open_customizations=self._handle_open_customizations,
                        on_open_settings=lambda: self._handle_open_settings("general"),
                        on_open_search_modal=lambda: self._handle_set_search_modal(True),
                        on_toggle_sidebar=self._handle_toggle_sidebar,
                        on_toggle_pin=self._handle_toggle_pin,
                        on_toggle_archive=self._handle_toggle_archive,
                        on_delete_session=self._handle_delete_session,
                        on_add_project=self._handle_add_project,
                        on_navigate_back=self._handle_nav_back,
                        on_navigate_forward=self._handle_nav_forward,
                        can_navigate_back=self.nav_index > 0,
                        can_navigate_forward=self.nav_index < len(self.nav_history) - 1,
                    )

                # Center View Router
                if self.center_view == "history":
                    ConversationHistoryView(
                        sessions=self.sessions,
                        projects=self.settings.projects,
                        active_session_id=self.active_session_id,
                        on_select_session=self._handle_select_session,
                        on_toggle_pin=self._handle_toggle_pin,
                        on_toggle_archive=self._handle_toggle_archive,
                        on_delete_session=self._handle_delete_session,
                        on_new_conversation=lambda: self._handle_new_conversation(None),
                    )
                elif self.center_view == "automations":
                    AutomationsView(
                        automations=self.automations,
                        projects=self.settings.projects,
                        on_toggle_automation=self._handle_toggle_automation,
                        on_delete_automation=self._handle_delete_automation,
                        on_create_automation=self._handle_create_automation,
                        on_update_automation=self._handle_update_automation,
                        on_run_automation_now=self._handle_run_automation_now,
                        initial_modal_open=self.params.get("openNewAutomation") == "true",
                        initial_selected_trigger_id=self.params.get("triggerId"),
                    )
                elif self.center_view == "customizations":
                    WorkspaceCustomizationsView(
                        projects=self.settings.projects,
                        active_project_id=self.active_project_id,
                        on_select_project=self._handle_select_project,
                        on_open_global_customizations=lambda: self._handle_open_settings(
                            "customizations"
                        ),
                        on_open_file_in_aux=self._handle_open_file_in_aux,
                    )
                else:
                    ChatView(
                        session=self._active_session(),
                        all_sessions=self.sessions,
                        projects=self.settings.projects,
                        settings=self.settings,
                        selected_model=self.selected_model,
                        selected_effort=self.selected_effort,
                        is_aux_open=self.aux_open,
                        initial_open_model=self.params.get("openModel") == "true",
                        initial_open_context=self.params.get("openContext") == "true",
                        initial_open_kebab=self.params.get("openKebab") == "true",
                        initial_open_modes=self.params.get("openModes") == "true",
                        initial_open_side_question=self.params.get("openSideQuestion")
                        == "true",
                        initial_open_fastpick=self.params.get("openFastpick") == "true",
                        initial_open_lifted_menu=self.params.get("openLiftedMenu")
                        == "true",
                        on_send_message=self._handle_send_message,
                        on_select_session=self._handle_select_session,
                        on_open_artifact=self._handle_open_artifact,
                        on_toggle_aux=self._handle_toggle_aux,
                        on_open_aux_tab=self._handle_open_aux_tab,
                        on_open_settings=self._handle_open_settings,
                        on_model_change=self._handle_model_change,
                        on_effort_change=self._handle_effort_change,
                        on_fork_from_message=self._handle_fork_from_message,
                    )

                # Right Auxiliary Pane
                AuxiliaryPane(
                    is_open=self.aux_open,
                    active_artifact=self.active_artifact,
                    subagents=self.subagents,
                    artifact_width=self.settings.artifact_width,
                    initial_tab=self.aux_tab,
                    initial_open_plus=self.params.get("openAuxPlus") == "true",
                    initial_open_overview_customize=self.params.get(
                        "openOverviewCustomize"
                    )
                    == "true",
                    initial_open_diff_comment=self.params.get("openDiffComment")
                    == "true",
                    on_close=self._handle_toggle_aux,
                    on_tab_change=self._handle_aux_tab_change,
                )

            # 3. Modals (Search Command Palette + 2-Column Settings Modal)
            SearchConversationsModal(
                is_open=self.search_modal_open,
                on_close=lambda: self._handle_set_search_modal(False),
                sessions=self.sessions,
                projects=self.settings.projects,
                on_select_session=self._handle_select_session_from_modal,
                on_new_conversation=lambda: self._handle_new_conversation(None),
                on_open_automations=self._handle_open_automations,
                on_open_settings=lambda: self._handle_open_settings("general"),
            )

            SettingsModal(
                is_open=self.settings_open,
                initial_screen=self.settings_screen,
                settings=self.settings,
                skills=self.skills,
                on_close=self._handle_close_settings,
                on_settings_change=lambda _: self.render(),
            )

    # =========================================================================
    # EVENT HANDLERS
    # =========================================================================
    def _handle_select_session(self, session_id: str) -> None:
        self.active_session_id = session_id
        self.center_view = "chat"
        self._push_nav("chat", session_id)
        self.render()

    def _handle_select_session_from_modal(self, session_id: str) -> None:
        self.search_modal_open = False
        self._handle_select_session(session_id)

    def _handle_new_conversation(self, project_id: str | None) -> None:
        zero_sess = next(
            (s for s in self.sessions if s.id == "session-zero-state"), None
        )
        if zero_sess and project_id:
            zero_sess.project_id = project_id
        self.active_session_id = "session-zero-state"
        self.center_view = "chat"
        self.search_modal_open = False
        self._push_nav("chat", "session-zero-state")
        self.render()

    def _handle_open_history(self) -> None:
        self.center_view = "history"
        self._push_nav("history", self.active_session_id)
        self.render()

    def _handle_open_automations(self) -> None:
        self.center_view = "automations"
        self.search_modal_open = False
        self._push_nav("automations", self.active_session_id)
        self.render()

    def _handle_open_customizations(self) -> None:
        self.center_view = "customizations"
        self._push_nav("customizations", self.active_session_id)
        self.render()

    def _handle_open_settings(self, screen: str | None = None) -> None:
        self.settings_open = True
        self.search_modal_open = False
        if screen:
            self.settings_screen = screen
        self.render()

    def _handle_close_settings(self) -> None:
        self.settings_open = False
        self.render()

    def _handle_set_search_modal(self, open_state: bool) -> None:
        self.search_modal_open = open_state
        self.render()

    def _handle_toggle_sidebar(self) -> None:
        self.sidebar_open = not self.sidebar_open
        self.render()

    def _handle_toggle_aux(self) -> None:
        self.aux_open = not self.aux_open
        self.render()

    def _handle_open_aux_tab(self, tab: AuxTabType) -> None:
        self.aux_open = True
        self.aux_tab = tab
        self.render()

    def _handle_select_aux_tab_str(self, tab: str) -> None:
        if tab in ("overview", "review", "terminal", "file", "browser", "agents", "new-tab"):
            self._handle_open_aux_tab(tab)  # type: ignore[arg-type]

    def _handle_aux_tab_change(self, tab: AuxTabType) -> None:
        self.aux_tab = tab

    def _handle_open_artifact(self, artifact: ArtifactItem) -> None:
        self.active_artifact = artifact
        self.aux_open = True
        self.aux_tab = "file"
        self.render()

    def _handle_open_file_in_aux(
        self, title: str, content: str, file_type: str
    ) -> None:
        self.active_artifact = ArtifactItem(
            id=f"art-{len(self.sessions)}",
            title=title,
            type="markdown",
            content=content,
            description=file_type,
        )
        self.aux_open = True
        self.aux_tab = "file"
        self.render()

    def _handle_toggle_pin(self, session_id: str) -> None:
        for s in self.sessions:
            if s.id == session_id:
                s.pinned = not s.pinned
        self.render()

    def _handle_toggle_archive(self, session_id: str) -> None:
        for s in self.sessions:
            if s.id == session_id:
                s.archived = not s.archived
        self.render()

    def _handle_delete_session(self, session_id: str) -> None:
        self.sessions = [
            s
            for s in self.sessions
            if s.id != session_id or s.id == "session-zero-state"
        ]
        if self.active_session_id == session_id:
            self.active_session_id = "session-clone-rea"
        self.render()

    def _handle_add_project(self, path: str) -> None:
        name = path.rstrip("/").split("/")[-1] or "new-project"
        new_proj = ProjectConfig(
            id=f"proj-{len(self.settings.projects) + 1}",
            name=name,
            folders=[path],
            active_conversations=0,
            archived_conversations=0,
        )
        self.settings.projects.append(new_proj)
        self.render()

    def _handle_select_project(self, project_id: str) -> None:
        self.active_project_id = project_id
        self.render()

    def _handle_nav_back(self) -> None:
        if self.nav_index > 0:
            self.nav_index -= 1
            view, sid = self.nav_history[self.nav_index]
            self.center_view = view
            self.active_session_id = sid
            self.render()

    def _handle_nav_forward(self) -> None:
        if self.nav_index < len(self.nav_history) - 1:
            self.nav_index += 1
            view, sid = self.nav_history[self.nav_index]
            self.center_view = view
            self.active_session_id = sid
            self.render()

    def _handle_toggle_automation(self, auto_id: str) -> None:
        for a in self.automations:
            if a.id == auto_id:
                a.enabled = not a.enabled
        self.render()

    def _handle_delete_automation(self, auto_id: str) -> None:
        self.automations = [a for a in self.automations if a.id != auto_id]
        self.render()

    def _handle_create_automation(self, item: AutomationItem) -> None:
        self.automations.insert(0, item)
        self.render()

    def _handle_update_automation(self, updated: AutomationItem) -> None:
        self.automations = [
            updated if a.id == updated.id else a for a in self.automations
        ]
        self.render()

    def _handle_run_automation_now(self, item: AutomationItem) -> None:
        self._handle_send_message(f"[Automation: {item.display_name}] {item.prompt}", [])

    def _handle_model_change(self, model: str) -> None:
        self.selected_model = model

    def _handle_effort_change(self, effort: Literal["Low", "Medium", "High"]) -> None:
        self.selected_effort = effort

    def _handle_fork_from_message(self, msg_id: str) -> None:
        curr = self._active_session()
        cutoff_msgs: list[Message] = []
        for m in curr.messages:
            cutoff_msgs.append(m)
            if m.id == msg_id:
                break
        forked = Session(
            id=f"session-fork-{len(self.sessions) + 1}",
            title=f"{curr.title} (Fork)",
            timestamp="Just now",
            token_count=curr.token_count // 2,
            project_id=curr.project_id,
            pinned=True,
            messages=cutoff_msgs,
        )
        self.sessions.insert(1, forked)
        self.active_session_id = forked.id
        self.render()

    def _handle_send_message(
        self, text: str, attachments: list[ContextAttachment]
    ) -> None:
        sess = self._active_session()
        if sess.id == "session-zero-state":
            new_sess = Session(
                id=f"session-{len(self.sessions) + 1}",
                title=text[:44],
                timestamp="Just now",
                token_count=1250,
                project_id=self.active_project_id,
                pinned=True,
                messages=[],
            )
            self.sessions.insert(1, new_sess)
            self.active_session_id = new_sess.id
            sess = new_sess

        user_msg = Message(
            id=f"msg-u-{len(sess.messages) + 1}",
            role="user",
            content=text,
            timestamp="Just now",
            attachments=attachments,
        )
        sess.messages.append(user_msg)

        agent_msg = Message(
            id=f"msg-a-{len(sess.messages) + 1}",
            role="agent",
            content=(
                f"Executed request with **{self.selected_model}** (`{self.selected_effort}` effort).\n\n"
                f"Verified workspace state in `/mnt/storage/projects/nicegui-ai`."
            ),
            timestamp="Just now",
            thinking=ThinkingBlock(
                duration="2s",
                steps=[
                    f"Routing prompt through {self.selected_model} ({self.selected_effort} reasoning effort)",
                    "Inspecting nicegui_ai.antigravity workspace state",
                ],
            ),
            tool_calls=[
                ToolCallItem(
                    id=f"tc-auto-{len(sess.messages)}",
                    tool_name="run_command",
                    action="Verifying nicegui_ai test suite",
                    parameters={"command": "uv run pytest -q"},
                    output="28 passed in 0.84s",
                    status="completed",
                )
            ],
        )
        sess.messages.append(agent_msg)
        sess.token_count += 1800
        self.center_view = "chat"
        self.render()


def parse_request_query(request: Request | None) -> dict[str, str]:
    """Extract single-value query dict from a FastAPI Request."""
    if request is None:
        return {}
    raw = parse_qs(str(request.url.query))
    return {k: v[0] for k, v in raw.items() if v}


def register_antigravity_routes(prefix: str = "") -> None:
    """Register the 1:1 Antigravity page route on the active NiceGUI app."""
    route_path = prefix or "/"

    @ui.page(route_path)
    def _antigravity_route(request: Request) -> None:
        setup_antigravity_theme()
        params = parse_request_query(request)
        AntigravityApp(query_params=params)


def main() -> None:
    """Launch the standalone 1:1 Antigravity Desktop Clone server."""
    register_antigravity_routes("/")
    port = int(os.environ.get("PORT", "8080"))
    ui.run(
        title="Antigravity",
        port=port,
        dark=True,
        reload=False,
        show=False,
    )


if __name__ in {"__main__", "__mp_main__"}:
    main()
