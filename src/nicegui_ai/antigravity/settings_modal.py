"""1:1 Antigravity 2-Column Settings Modal (13 Core Screens, Per-Project Settings, and 11 Drill-Down Subviews)."""

from collections.abc import Callable
from typing import Literal

from nicegui import ui

from .icons import AntigravityIcon
from .state import AppSettings, ProjectConfig, SkillItem
from .theme import apply_antigravity_theme_mode

SettingsScreenId = str


class SettingsModal(ui.element):
    """1:1 Antigravity 2-Column Settings Modal (`max-w-5xl max-h-[80vh]`)."""

    def __init__(
        self,
        *,
        is_open: bool = False,
        initial_screen: str = "general",
        settings: AppSettings,
        skills: list[SkillItem] | None = None,
        on_close: Callable[[], None] | None = None,
        on_settings_change: Callable[[AppSettings], None] | None = None,
    ) -> None:
        super().__init__("div")
        self.is_open = is_open

        self.active_screen = self._normalize_screen(initial_screen)
        self.active_subview: str | None = None
        self.settings = settings
        self.skills = skills or []
        self.on_close = on_close
        self.on_settings_change = on_settings_change

        # Draft inputs for subviews
        self.new_rule_value = ""
        self.new_url_value = ""
        self.new_mcp_name = ""
        self.new_mcp_cmd = ""
        self.feedback_text = ""

        self._apply_root_classes()
        self.render()

    @staticmethod
    def _normalize_screen(screen: str | None) -> str:
        if not screen:
            return "general"
        if screen.startswith("project:"):
            return screen
        return screen.lower()


    def _apply_root_classes(self) -> None:
        self._classes.clear()
        if not self.is_open:
            self.classes("hidden")
            return
        self.classes(
            "fixed inset-0 z-50 flex items-center justify-center bg-black/75 backdrop-blur-xs p-6 select-none"
        )

    def open(self, screen: str | None = None) -> None:
        self.is_open = True
        if screen:
            self.active_screen = self._normalize_screen(screen)
            self.active_subview = None
        self._apply_root_classes()
        self.render()

    def close(self) -> None:
        self.is_open = False
        self._apply_root_classes()
        if self.on_close:
            self.on_close()
        self.render()

    def set_screen(self, screen: str) -> None:
        self.active_screen = self._normalize_screen(screen)
        self.active_subview = None
        self.render()


    def set_subview(self, subview: str | None) -> None:
        self.active_subview = subview
        self.render()

    def render(self) -> None:
        self.clear()
        self._apply_root_classes()
        if not self.is_open:
            return

        with self:
            with (
                ui.row()
                .props('data-testid="settings-modal"')
                .classes(
                    "w-full max-w-5xl h-[680px] max-h-[82vh] bg-[#101010] border border-[#222222] rounded-2xl shadow-2xl overflow-hidden gap-0 no-wrap"
                )
            ):
                self._render_left_sidebar()
                self._render_right_content()

    def _render_left_sidebar(self) -> None:
        with ui.column().classes(
            "w-[210px] h-full bg-[#151515] border-r border-[#222222] flex flex-col justify-between shrink-0 gap-0"
        ):
            with ui.column().classes("flex-1 w-full overflow-y-auto p-2 gap-3"):
                # Agent Section
                with ui.column().classes("w-full gap-0.5"):
                    ui.label("Agent").classes(
                        "px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                    )
                    agent_items = [
                        ("general", "General"),
                        ("browser", "Browser"),
                        ("notifications", "Notifications"),
                        ("terminal", "Terminal"),
                        ("workspaces", "Workspaces"),
                        ("labs", "Labs"),
                    ]
                    for sid, label in agent_items:
                        self._nav_item(sid, label)

                # App Section
                with ui.column().classes("w-full gap-0.5"):
                    ui.label("App").classes(
                        "px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                    )
                    app_items = [
                        ("appearance", "Appearance"),
                        ("editor", "Editor"),
                        ("billing", "Billing"),
                        ("models", "Models"),
                        ("customizations", "Customizations"),
                        ("advanced", "Advanced"),
                        ("about", "About"),
                    ]
                    for sid, label in app_items:
                        self._nav_item(sid, label)

                # Projects Section
                with ui.column().classes("w-full gap-0.5"):
                    ui.label("Projects").classes(
                        "px-2.5 py-1 text-[10px] font-semibold uppercase tracking-wider text-[#6e6e6e]"
                    )
                    for proj in self.settings.projects:
                        self._nav_item(f"project:{proj.id}", proj.name)
                    self._nav_item("not-in-project", "Not in Project")

                # Misc Section
                with ui.column().classes("w-full gap-0.5 pt-1 border-t border-[#222222]"):
                    self._nav_item("shortcuts", "Shortcuts")
                    self._nav_item("feedback", "Provide Feedback")

            # Bottom Account Footer
            with ui.column().classes("p-2 border-t border-[#222222] w-full shrink-0"):
                self._nav_item(
                    "account",
                    f"{self.settings.account_name} ({self.settings.plan_name})",
                )

    def _nav_item(self, screen_id: str, label: str) -> None:
        is_active = self.active_screen == screen_id
        with (
            ui.button(on_click=lambda s=screen_id: self.set_screen(s))
            .props(f'flat dense no-caps data-testid="settings-nav-{screen_id}"')
            .classes(
                f"w-full px-2.5 py-1.5 rounded-md text-left text-[12px] flex items-center justify-between font-normal "
                f"{'bg-[#272727] text-[#cccccc] font-medium' if is_active else 'text-[#6e6e6e] hover:text-[#cccccc] hover:bg-[#191919]'}"
            )
        ):
            ui.label(label).classes("truncate")

    def _render_right_content(self) -> None:
        with ui.column().classes("flex-1 h-full flex flex-col overflow-hidden bg-[#101010]"):
            # Top Header Bar
            with ui.row().classes(
                "h-[48px] px-6 border-b border-[#222222] items-center justify-between w-full shrink-0"
            ):
                with ui.row().classes("items-center gap-2"):
                    if self.active_subview:
                        ui.button(
                            "← Back",
                            on_click=lambda: self.set_subview(None),
                        ).props('flat dense no-caps data-testid="settings-subview-back"').classes(
                            "px-2 py-1 rounded bg-[#191919] text-[11px] text-[#cccccc] min-h-0"
                        )
                    ui.label(self._screen_title()).classes(
                        "text-[15px] font-medium text-[#cccccc]"
                    )
                close_btn = (
                    ui.button(on_click=self.close)
                    .props('flat dense no-caps data-testid="settings-close-button"')
                    .classes("p-1.5 text-[#6e6e6e] hover:text-[#cccccc] rounded-md hover:bg-[#191919] min-h-0 min-w-0")
                )
                with close_btn:
                    AntigravityIcon("close", size=15)

            # Scrollable Screen Content
            with ui.column().classes("flex-1 w-full overflow-y-auto p-6 gap-5"):
                if self.active_subview:
                    self._render_subview_content(self.active_subview)
                elif self.active_screen == "general":
                    self._render_general_screen()
                elif self.active_screen == "browser":
                    self._render_browser_screen()
                elif self.active_screen == "notifications":
                    self._render_notifications_screen()
                elif self.active_screen == "terminal":
                    self._render_terminal_screen()
                elif self.active_screen == "workspaces":
                    self._render_workspaces_screen()
                elif self.active_screen == "labs":
                    self._render_labs_screen()
                elif self.active_screen == "appearance":
                    self._render_appearance_screen()
                elif self.active_screen == "editor":
                    self._render_editor_screen()
                elif self.active_screen == "billing":
                    self._render_billing_screen()
                elif self.active_screen == "models":
                    self._render_models_screen()
                elif self.active_screen == "customizations":
                    self._render_customizations_screen()
                elif self.active_screen == "advanced":
                    self._render_advanced_screen()
                elif self.active_screen == "about":
                    self._render_about_screen()
                elif self.active_screen.startswith("project:"):
                    proj_id = self.active_screen.split(":", 1)[1]
                    self._render_project_screen(proj_id)
                elif self.active_screen == "not-in-project":
                    self._render_not_in_project_screen()
                elif self.active_screen == "shortcuts":
                    self._render_shortcuts_screen()
                elif self.active_screen == "feedback":
                    self._render_feedback_screen()
                elif self.active_screen == "account":
                    self._render_account_screen()

    def _screen_title(self) -> str:
        if self.active_subview:
            return f"Settings / {self.active_subview.replace('-', ' ').title()}"
        if self.active_screen.startswith("project:"):
            pid = self.active_screen.split(":", 1)[1]
            proj = next((p for p in self.settings.projects if p.id == pid), None)
            return f"Project Settings — {proj.name if proj else pid}"
        return self.active_screen.replace("-", " ").title()

    # =========================================================================
    # INDIVIDUAL SETTINGS SCREENS
    # =========================================================================
    def _render_general_screen(self) -> None:
        self._setting_select_row(
            "Queued Message Strategy",
            "How messages sent while the agent is streaming are handled",
            self.settings.queued_message_strategy,
            ["queue", "send"],
            lambda v: self._update_setting("queued_message_strategy", v),
        )
        self._setting_select_row(
            "Security & Permissions Preset",
            "Global security policy for file, network, and terminal execution",
            self.settings.security_preset,
            ["strict", "default", "auto", "turbo", "custom"],
            lambda v: self._update_setting("security_preset", v),
        )
        self._setting_select_row(
            "Artifact Review Mode",
            "When the agent pauses for user approval on implementation plans",
            self.settings.artifact_review_mode,
            ["always", "review", "auto"],
            lambda v: self._update_setting("artifact_review_mode", v),
        )
        self._setting_toggle_row(
            "Enable Terminal Sandbox",
            "Run shell commands inside isolated Linux namespace sandbox by default",
            self.settings.sandbox_enabled,
            lambda v: self._update_setting("sandbox_enabled", v),
        )
        self._setting_drilldown_row(
            "File Access & Network Security Rules",
            f"{len(self.settings.file_read_rules) + len(self.settings.file_write_rules)} active rules",
            lambda: self.set_subview("file-access-rules"),
        )
        self._setting_drilldown_row(
            "Terminal Command Allow / Deny Rules",
            f"{len(self.settings.terminal_command_rules)} command rules",
            lambda: self.set_subview("terminal-execution-rules"),
        )

    def _render_browser_screen(self) -> None:
        self._setting_toggle_row(
            "Enable Agent Browser Tools",
            "Allow the agent to inspect and interact with headless Chromium pages",
            self.settings.enable_browser_tools,
            lambda v: self._update_setting("enable_browser_tools", v),
        )
        self._setting_select_row(
            "JavaScript Execution Policy",
            "Control whether the agent can evaluate scripts inside browser pages",
            self.settings.browser_js_execution_policy,
            ["disabled", "review", "always"],
            lambda v: self._update_setting("browser_js_execution_policy", v),
        )
        self._setting_drilldown_row(
            "Browser Allowed & Denied URLs",
            f"{len(self.settings.browser_allowed_urls)} allowed, {len(self.settings.browser_denied_urls)} denied",
            lambda: self.set_subview("browser-urls"),
        )

    def _render_notifications_screen(self) -> None:
        self._setting_toggle_row(
            "Desktop Agent Notifications",
            "Notify when background tasks, timers, or long turns complete",
            self.settings.enable_agent_notifications,
            lambda v: self._update_setting("enable_agent_notifications", v),
        )
        self._setting_toggle_row(
            "Completion Sound Effects",
            "Play subtle audio cue when an agent turn finishes",
            self.settings.enable_agent_sounds,
            lambda v: self._update_setting("enable_agent_sounds", v),
        )

    def _render_terminal_screen(self) -> None:
        ui.label("Non-Interactive Shell Setup Script").classes(
            "text-[12px] font-medium text-[#cccccc]"
        )
        ui.textarea(
            value=self.settings.terminal_setup_script,
            on_change=lambda e: self._update_setting(
                "terminal_setup_script", str(e.value), rerender=False
            ),
        ).props("outlined dense autogrow dark").classes(
            "w-full font-mono text-[12px] bg-[#191919]"
        )

    def _render_workspaces_screen(self) -> None:
        self._setting_select_row(
            "Default Version Control System",
            "Preferred VCS for branching subagent worktrees",
            self.settings.default_workspace_vcs,
            ["git", "jj"],
            lambda v: self._update_setting("default_workspace_vcs", v),
        )
        self._setting_toggle_row(
            "Sync Jujutsu (jj) Worktrees",
            "Automatically colocate jj and git repositories in subagent branches",
            self.settings.sync_jj_worktrees,
            lambda v: self._update_setting("sync_jj_worktrees", v),
        )

    def _render_labs_screen(self) -> None:
        self._setting_toggle_row(
            "Inline Diff Actions",
            "Enable gutter comment and one-click apply inside Review tab",
            self.settings.lab_inline_actions,
            lambda v: self._update_setting("lab_inline_actions", v),
        )
        self._setting_toggle_row(
            "Autonomous Goal Loop (/goal)",
            "Allow multi-turn self-verification until all acceptance criteria pass",
            self.settings.lab_autonomous_mode,
            lambda v: self._update_setting("lab_autonomous_mode", v),
        )
        self._setting_toggle_row(
            "Demo Presentation Mode",
            "Hide sensitive paths and email addresses during screen recordings",
            self.settings.lab_demo_mode,
            lambda v: self._update_setting("lab_demo_mode", v),
        )

    def _render_appearance_screen(self) -> None:
        self._setting_select_row(
            "Color Theme Mode",
            "Switch between Antigravity Dark (#101010), Light, and OLED (#000000)",
            self.settings.theme_mode,
            ["dark", "light", "oled"],
            self._change_theme_mode,
        )
        self._setting_select_row(
            "Conversation Stream Width",
            "Maximum width of the central message column",
            self.settings.conversation_width,
            ["compact", "default", "wide", "full"],
            lambda v: self._update_setting("conversation_width", v),
        )
        self._setting_select_row(
            "Auxiliary Pane Width",
            "Default width of the right Auxiliary / Artifact pane",
            self.settings.artifact_width,
            ["compact", "default", "wide", "full"],
            lambda v: self._update_setting("artifact_width", v),
        )
        self._setting_toggle_row(
            "Verbose Agent Trajectory Chat",
            "Show detailed tool parameters and durations inline",
            self.settings.verbose_agent_chat,
            lambda v: self._update_setting("verbose_agent_chat", v),
        )

    def _change_theme_mode(self, mode: str) -> None:
        valid_mode: Literal["dark", "light", "oled"] = (
            "light" if mode == "light" else "oled" if mode == "oled" else "dark"
        )
        self.settings.theme_mode = valid_mode
        apply_antigravity_theme_mode(valid_mode)
        if self.on_settings_change:
            self.on_settings_change(self.settings)
        self.render()

    def _render_editor_screen(self) -> None:
        self._setting_toggle_row(
            "Antigravity Tab Suggestions",
            "Show inline ghost-text completions while editing files",
            self.settings.tab_suggestions_in_editor,
            lambda v: self._update_setting("tab_suggestions_in_editor", v),
        )
        self._setting_select_row(
            "Tab Completion Speed",
            "Balance latency vs context depth for inline completions",
            self.settings.tab_speed,
            ["fast", "balanced", "thorough"],
            lambda v: self._update_setting("tab_speed", v),
        )
        self._setting_toggle_row(
            "Tab to Auto-Import Symbols",
            "Automatically insert Python/TypeScript imports on Tab accept",
            self.settings.tab_to_import,
            lambda v: self._update_setting("tab_to_import", v),
        )

    def _render_billing_screen(self) -> None:
        with ui.column().classes(
            "w-full p-4 bg-[#191919] border border-[#222222] rounded-xl gap-2"
        ):
            with ui.row().classes("items-center justify-between w-full"):
                ui.label(self.settings.plan_name).classes(
                    "text-[15px] font-semibold text-[#cccccc]"
                )
                ui.label("ACTIVE").classes(
                    "px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 text-[10px] font-mono"
                )
            ui.label(
                f"Available AI Credits: {self.settings.available_ai_credits:,} credits remaining this cycle"
            ).classes("text-[12px] text-[#6e6e6e]")
        self._setting_toggle_row(
            "Enable AI Credit Overages",
            "Continue uninterrupted with pay-as-you-go credits when monthly quota is reached",
            self.settings.enable_ai_credit_overages,
            lambda v: self._update_setting("enable_ai_credit_overages", v),
        )

    def _render_models_screen(self) -> None:
        models_quota = [
            ("Gemini 3.8 Pro", "Thinking & Deep Architecture", "94% remaining"),
            ("Gemini 3.8 Flash High", "High-Speed Agentic Coding", "98% remaining"),
            ("Claude Opus 4.6", "Anthropic Extended Reasoning", "88% remaining"),
            ("Claude Sonnet 4.6", "Balanced Code Generation", "92% remaining"),
            ("GPT-5.4", "OpenAI Frontier Reasoning", "90% remaining"),
        ]
        for mname, mdesc, mquota in models_quota:
            with ui.row().classes(
                "w-full p-3 bg-[#191919] border border-[#222222] rounded-xl items-center justify-between"
            ):
                with ui.column().classes("gap-0.5"):
                    ui.label(mname).classes("text-[13px] font-medium text-[#cccccc]")
                    ui.label(mdesc).classes("text-[11px] text-[#6e6e6e]")
                ui.label(mquota).classes("text-[11px] font-mono text-emerald-400")

    def _render_customizations_screen(self) -> None:
        self._setting_toggle_row(
            "Include Built-in Antigravity Customizations",
            "Load default system skills from ~/.gemini/antigravity/builtin/skills",
            self.settings.include_default_customizations,
            lambda v: self._update_setting("include_default_customizations", v),
        )
        self._setting_drilldown_row(
            "Model Context Protocol (MCP) Servers",
            f"{len(self.settings.mcp_servers)} configured servers",
            lambda: self.set_subview("mcp-servers"),
        )
        self._setting_drilldown_row(
            "Agent Skills & Discovery Paths",
            f"{len(self.skills)} installed skills",
            lambda: self.set_subview("skills-manager"),
        )
        self._setting_drilldown_row(
            "Lifecycle Hooks (PreToolUse / PostInvocation)",
            f"{len(self.settings.hooks)} active hooks",
            lambda: self.set_subview("hooks-manager"),
        )

    def _render_advanced_screen(self) -> None:
        self._setting_toggle_row(
            "Prevent System Sleep During Active Goal Loops",
            "Keep host awake while background tasks or subagents are running",
            self.settings.prevent_sleep,
            lambda v: self._update_setting("prevent_sleep", v),
        )
        self._setting_toggle_row(
            "Enable Remote Control Server",
            f"Host nickname: {self.settings.remote_control_nickname}",
            self.settings.enable_remote_control,
            lambda v: self._update_setting("enable_remote_control", v),
        )
        with ui.column().classes("w-full gap-1.5 pt-2"):
            ui.label("ConnectRPC Runtime Endpoint Override").classes(
                "text-[12px] font-medium text-[#cccccc]"
            )
            ui.input(
                value=self.settings.runtime_env_override,
                on_change=lambda e: self._update_setting(
                    "runtime_env_override", str(e.value), rerender=False
                ),
            ).props("outlined dense dark").classes(
                "w-full font-mono text-[12px] bg-[#191919]"
            )

    def _render_about_screen(self) -> None:
        with ui.column().classes(
            "w-full p-5 bg-[#191919] border border-[#222222] rounded-xl items-center text-center gap-2"
        ):
            AntigravityIcon("antigravity_logo", size=32, classes="text-[#cccccc]")
            ui.label("Google Antigravity Desktop (NiceGUI 1:1 Edition)").classes(
                "text-[15px] font-semibold text-[#cccccc]"
            )
            ui.label("Version 2.0.0-rea • ConnectRPC Port 46349 • Python 3.13 + NiceGUI").classes(
                "text-[11px] font-mono text-[#6e6e6e]"
            )

    def _render_project_screen(self, project_id: str) -> None:
        proj = next(
            (p for p in self.settings.projects if p.id == project_id),
            self.settings.projects[0] if self.settings.projects else None,
        )
        if not proj:
            ui.label("Project not found").classes("text-[12px] text-[#6e6e6e]")
            return
        with ui.column().classes(
            "w-full p-3.5 bg-[#191919] border border-[#222222] rounded-xl gap-1"
        ):
            ui.label(proj.name).classes("text-[14px] font-semibold text-[#cccccc]")
            ui.label(", ".join(proj.folders)).classes(
                "text-[11px] font-mono text-[#6e6e6e]"
            )
        self._setting_select_row(
            "Project Security Preset Override",
            "Override global security preset for this workspace",
            proj.security_preset,
            ["inherit", "strict", "default", "auto", "turbo"],
            lambda v: self._update_project_field(proj, "security_preset", v),
        )
        self._setting_select_row(
            "Project Artifact Review Policy",
            "Override artifact approval policy for this workspace",
            proj.artifact_review_mode,
            ["inherit", "always", "review", "auto"],
            lambda v: self._update_project_field(proj, "artifact_review_mode", v),
        )
        self._setting_toggle_row(
            "Allow Network Inside Sandbox",
            "Permit outbound HTTP/HTTPS inside sandboxed commands for this project",
            proj.sandbox_allow_network,
            lambda v: self._update_project_field(proj, "sandbox_allow_network", v),
        )

    def _update_project_field(
        self, proj: ProjectConfig, attr: str, value: object
    ) -> None:
        setattr(proj, attr, value)
        if self.on_settings_change:
            self.on_settings_change(self.settings)
        self.render()

    def _render_not_in_project_screen(self) -> None:
        ui.label(
            "Conversations not associated with a workspace folder use global sandbox and scratch directory defaults (~/.gemini/antigravity/scratch)."
        ).classes("text-[12px] text-[#6e6e6e]")

    def _render_shortcuts_screen(self) -> None:
        shortcuts = [
            ("Search Conversations Command Palette", "Ctrl+K"),
            ("New Conversation", "Ctrl+N"),
            ("Open Settings Modal", "Ctrl+,"),
            ("Toggle Right Auxiliary Pane", "Ctrl+Shift+B"),
            ("Toggle Interactive Terminal", "Ctrl+`"),
            ("Slash Command Fastpick", "/"),
            ("Context & File Mentions", "@"),
        ]
        for label, keys in shortcuts:
            with ui.row().classes(
                "w-full px-3.5 py-2 bg-[#191919] border border-[#222222] rounded-lg items-center justify-between"
            ):
                ui.label(label).classes("text-[12px] text-[#cccccc]")
                ui.label(keys).classes(
                    "px-2 py-0.5 bg-[#272727] rounded text-[11px] font-mono text-[#cccccc]"
                )

    def _render_feedback_screen(self) -> None:
        ui.label("Send Diagnostic Feedback to the Antigravity Team").classes(
            "text-[13px] font-medium text-[#cccccc]"
        )
        ui.textarea(
            placeholder="Describe UI/UX feedback or attach trajectory logs...",
            value=self.feedback_text,
            on_change=lambda e: setattr(self, "feedback_text", str(e.value)),
        ).props("outlined dense autogrow dark").classes(
            "w-full text-[12px] bg-[#191919]"
        )
        ui.button(
            "Submit Feedback",
            on_click=lambda: setattr(self, "feedback_text", ""),
        ).props("flat dense no-caps").classes(
            "px-3.5 py-1.5 bg-[#cccccc] text-[#101010] rounded-lg text-[12px] font-medium"
        )

    def _render_account_screen(self) -> None:
        with ui.column().classes(
            "w-full p-4 bg-[#191919] border border-[#222222] rounded-xl gap-1.5"
        ):
            ui.label(self.settings.account_name).classes(
                "text-[15px] font-semibold text-[#cccccc]"
            )
            ui.label(self.settings.account_email).classes(
                "text-[12px] font-mono text-[#6e6e6e]"
            )
            ui.label(f"Cloud Project ID: {self.settings.project_id}").classes(
                "text-[11px] font-mono text-[#6e6e6e]"
            )

    # =========================================================================
    # DRILL-DOWN SUBVIEWS
    # =========================================================================
    def _render_subview_content(self, subview: str) -> None:
        if subview == "mcp-servers":
            for srv in self.settings.mcp_servers:
                with ui.column().classes(
                    "w-full p-3.5 bg-[#191919] border border-[#222222] rounded-xl gap-2"
                ):
                    with ui.row().classes("items-center justify-between w-full"):
                        with ui.row().classes("items-center gap-2"):
                            ui.label(srv.name).classes(
                                "text-[13px] font-medium text-[#cccccc]"
                            )
                            ui.label(srv.status).classes(
                                "text-[10px] font-mono text-emerald-400"
                            )
                        ui.label(f"{srv.command} {' '.join(srv.args)}").classes(
                            "text-[11px] font-mono text-[#6e6e6e]"
                        )
                    for tool in srv.tools:
                        with ui.row().classes(
                            "w-full px-2.5 py-1 bg-[#151515] rounded items-center justify-between text-[11px]"
                        ):
                            ui.label(tool.name).classes("font-mono text-[#cccccc]")
                            ui.label(tool.description).classes(
                                "text-[#6e6e6e] truncate max-w-[340px]"
                            )
        elif subview == "skills-manager":
            for sk in self.skills:
                with ui.row().classes(
                    "w-full p-3 bg-[#191919] border border-[#222222] rounded-xl items-center justify-between"
                ):
                    with ui.column().classes("gap-0.5"):
                        ui.label(sk.name).classes(
                            "text-[12px] font-mono font-medium text-[#cccccc]"
                        )
                        ui.label(sk.description).classes("text-[11px] text-[#6e6e6e]")
                    ui.label("Enabled" if sk.active else "Disabled").classes(
                        "text-[10px] font-mono text-emerald-400"
                    )
        elif subview == "hooks-manager":
            for hk in self.settings.hooks:
                with ui.row().classes(
                    "w-full p-3 bg-[#191919] border border-[#222222] rounded-xl items-center justify-between"
                ):
                    ui.label(f"{hk.event} ({hk.matcher})").classes(
                        "text-[12px] font-medium text-[#cccccc]"
                    )
                    ui.label(hk.command).classes("text-[11px] font-mono text-[#6e6e6e]")
        elif subview == "browser-urls":
            ui.label("Allowed Browser URL Patterns").classes(
                "text-[12px] font-medium text-[#cccccc]"
            )
            for u in self.settings.browser_allowed_urls:
                ui.label(u).classes(
                    "w-full px-3 py-1.5 bg-[#191919] border border-[#222222] rounded font-mono text-[11px] text-[#cccccc]"
                )
        else:
            for r in (
                self.settings.file_read_rules + self.settings.terminal_command_rules
            ):
                with ui.row().classes(
                    "w-full px-3 py-1.5 bg-[#191919] border border-[#222222] rounded items-center justify-between"
                ):
                    ui.label(r.value).classes("font-mono text-[11px] text-[#cccccc]")
                    ui.label(r.policy.upper()).classes(
                        "text-[10px] font-mono text-emerald-400"
                    )

    # =========================================================================
    # REUSABLE ROW HELPERS
    # =========================================================================
    def _setting_toggle_row(
        self,
        title: str,
        subtitle: str,
        value: bool,
        on_toggle: Callable[[bool], None],
    ) -> None:
        with ui.row().classes(
            "w-full p-3.5 bg-[#191919] border border-[#222222] rounded-xl items-center justify-between"
        ):
            with ui.column().classes("gap-0.5 max-w-[75%]"):
                ui.label(title).classes("text-[13px] font-medium text-[#cccccc]")
                ui.label(subtitle).classes("text-[11px] text-[#6e6e6e]")
            ui.button(
                "ON" if value else "OFF",
                on_click=lambda: on_toggle(not value),
            ).props("flat dense no-caps").classes(
                f"px-3 py-1 rounded-md text-[11px] font-mono min-h-0 "
                f"{'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' if value else 'bg-[#272727] text-[#6e6e6e]'}"
            )

    def _setting_select_row(
        self,
        title: str,
        subtitle: str,
        current_value: str,
        options: list[str],
        on_select: Callable[[str], None],
    ) -> None:
        with ui.row().classes(
            "w-full p-3.5 bg-[#191919] border border-[#222222] rounded-xl items-center justify-between"
        ):
            with ui.column().classes("gap-0.5 max-w-[60%]"):
                ui.label(title).classes("text-[13px] font-medium text-[#cccccc]")
                ui.label(subtitle).classes("text-[11px] text-[#6e6e6e]")
            with ui.row().classes("items-center gap-1 bg-[#151515] p-1 rounded-lg border border-[#222222]"):
                for opt in options:
                    active = current_value == opt
                    ui.button(
                        opt.capitalize(),
                        on_click=lambda o=opt: on_select(o),
                    ).props("flat dense no-caps").classes(
                        f"px-2.5 py-0.5 rounded text-[11px] min-h-0 font-normal "
                        f"{'bg-[#272727] text-[#cccccc] font-medium' if active else 'text-[#6e6e6e] hover:text-[#cccccc]'}"
                    )

    def _setting_drilldown_row(
        self,
        title: str,
        summary: str,
        on_click: Callable[[], None],
    ) -> None:
        with (
            ui.button(on_click=on_click)
            .props("flat dense no-caps")
            .classes(
                "w-full p-3.5 bg-[#191919] hover:bg-[#272727]/60 border border-[#222222] rounded-xl flex items-center justify-between text-left font-normal"
            )
        ):
            with ui.column().classes("gap-0.5"):
                ui.label(title).classes("text-[13px] font-medium text-[#cccccc]")
                ui.label(summary).classes("text-[11px] text-[#6e6e6e]")
            ui.label("Configure ▸").classes("text-[11px] text-[#cccccc]")

    def _update_setting(
        self, attr: str, value: object, *, rerender: bool = True
    ) -> None:
        setattr(self.settings, attr, value)
        if self.on_settings_change:
            self.on_settings_change(self.settings)
        if rerender:
            self.render()
