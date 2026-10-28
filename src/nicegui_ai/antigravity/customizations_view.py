"""1:1 Antigravity Dedicated Workspace Customizations View (xUb / wUb)."""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from nicegui import ui

from nicegui_ai.antigravity.icons import AntigravityIcon
from nicegui_ai.antigravity.state import ProjectConfig


@dataclass
class SkillRuleEntry:
    id: str
    name: str
    description: str
    path: str
    scope: Literal["Workspace", "Global"]
    enabled: bool
    content: str
    trigger: str | None = None


@dataclass
class PluginEntry:
    id: str
    name: str
    version: str
    description: str
    path: str
    enabled: bool
    skills_count: int
    mcp_count: int


@dataclass
class CustomAgentEntry:
    id: str
    name: str
    role: str
    model: str
    path: str
    scope: Literal["Workspace", "Global"]
    enabled: bool


class WorkspaceCustomizationsView(ui.element):
    """Dedicated center view for managing Skills, Rules, Plugins, and Custom Agents."""

    def __init__(
        self,
        projects: list[ProjectConfig],
        active_project_id: str | None,
        on_select_project: Callable[[str], None],
        on_open_global_customizations: Callable[[], None],
        on_open_file_in_aux: Callable[[str, str, str], None] | None = None,
    ) -> None:
        super().__init__("div")
        self.projects = projects
        self.active_project_id = active_project_id
        self.on_select_project = on_select_project
        self.on_open_global_customizations = on_open_global_customizations
        self.on_open_file_in_aux = on_open_file_in_aux

        self.search_query: str = ""
        self.scope_filter: Literal["all", "Workspace", "Global"] = "all"
        self.collapsed_sections: dict[str, bool] = {}

        self.skills: list[SkillRuleEntry] = [
            SkillRuleEntry(
                id="skill-rea-deep-dive",
                name="codebase-deep-dive",
                description="Perform an exhaustive, low-level technical analysis of a local codebase or extracted bundle.",
                path="/mnt/storage/projects/AI/antigravity-studio/.agents/skills/codebase-deep-dive/SKILL.md",
                scope="Workspace",
                enabled=True,
                content="---\nname: codebase-deep-dive\n---\n# Codebase Deep Dive\n",
            ),
            SkillRuleEntry(
                id="skill-nicegui",
                name="nicegui",
                description="Expert guidance for building Python-only web UIs and native desktop apps with NiceGUI.",
                path="~/.agents/skills/nicegui/SKILL.md",
                scope="Global",
                enabled=True,
                content="---\nname: nicegui\n---\n# NiceGUI Skill\n",
            ),
            SkillRuleEntry(
                id="skill-slop-eval",
                name="slop-eval",
                description="Objectively evaluate a UI/web design against anti-slop design rules across 8 weighted axes.",
                path="~/.agents/skills/slop-eval/SKILL.md",
                scope="Global",
                enabled=True,
                content="---\nname: slop-eval\n---\n# Slop Eval\n",
            ),
            SkillRuleEntry(
                id="skill-tdd",
                name="tdd",
                description="Test-driven development red-green-refactor workflow with automated verification.",
                path="~/.agents/skills/tdd/SKILL.md",
                scope="Global",
                enabled=True,
                content="---\nname: tdd\n---\n# Test-Driven Development\n",
            ),
        ]

        self.rules: list[SkillRuleEntry] = [
            SkillRuleEntry(
                id="rule-agents-md",
                name="AGENTS.md",
                description="Workspace architecture, build commands, and 1:1 Antigravity parity invariants.",
                path="/mnt/storage/projects/nicegui-ai/CONTEXT.md",
                scope="Workspace",
                trigger="Always On",
                enabled=True,
                content="# AGENTS.md\n\nMaintain 100% 1:1 Antigravity parity.\n",
            ),
            SkillRuleEntry(
                id="rule-python-strict",
                name="python-strict.md",
                description="Enforce strict mypy types, ruff formatting, and Python-first NiceGUI patterns.",
                path="/mnt/storage/projects/nicegui-ai/.agents/rules/python-strict.md",
                scope="Workspace",
                trigger="Glob: src/**/*.py",
                enabled=True,
                content="# Python Strict Rule\n",
            ),
            SkillRuleEntry(
                id="rule-git-conventions",
                name="git-conventions.md",
                description="Conventional commit messages and atomic change sets.",
                path="~/.agents/rules/git-conventions.md",
                scope="Global",
                trigger="Always On",
                enabled=True,
                content="# Git Conventions\n",
            ),
        ]

        self.plugins: list[PluginEntry] = [
            PluginEntry(
                id="plugin-rea",
                name="morluto-rea-inspector",
                version="1.4.2",
                description="Reverse Engineer Anything (REA) bundle decompiler and live CDP target inspector.",
                path="/home/vanluther/.agents/plugins/morluto-rea-inspector",
                enabled=True,
                skills_count=3,
                mcp_count=1,
            ),
            PluginEntry(
                id="plugin-browser",
                name="chromium-visual-verifier",
                version="1.1.0",
                description="Headless Chromium screenshot diffing and DOM telemetry inspection.",
                path="/mnt/storage/projects/nicegui-ai/.agents/plugins/browser-verifier",
                enabled=False,
                skills_count=1,
                mcp_count=1,
            ),
        ]

        self.agents: list[CustomAgentEntry] = [
            CustomAgentEntry(
                id="agent-rea-auditor",
                name="rea-auditor",
                role="Bundle Decompiler & Spec Extractor",
                model="Gemini 3.1 Pro (High)",
                path="/mnt/storage/projects/nicegui-ai/.agents/agents/rea-auditor.md",
                scope="Workspace",
                enabled=True,
            ),
            CustomAgentEntry(
                id="agent-ui-verifier",
                name="ui-verifier",
                role="Headless Chromium Visual QA Subagent",
                model="Gemini 3.8 Flash (High)",
                path="/mnt/storage/projects/nicegui-ai/.agents/agents/ui-verifier.md",
                scope="Workspace",
                enabled=True,
            ),
        ]

        self.props('data-testid="project-customizations-content"')
        self.classes(
            "flex-1 overflow-y-auto h-full min-h-0 bg-background text-foreground"
        )
        self.render_view()

    def render_view(self) -> None:
        self.clear()
        active_project = next(
            (p for p in self.projects if p.id == self.active_project_id),
            self.projects[3] if len(self.projects) > 3 else (self.projects[0] if self.projects else None),
        )
        q = self.search_query.strip().lower()

        filtered_skills = [
            s
            for s in self.skills
            if (self.scope_filter == "all" or s.scope == self.scope_filter)
            and (not q or q in s.name.lower() or q in s.description.lower())
        ]
        filtered_rules = [
            r
            for r in self.rules
            if (self.scope_filter == "all" or r.scope == self.scope_filter)
            and (not q or q in r.name.lower() or q in r.description.lower())
        ]
        filtered_plugins = [
            p
            for p in self.plugins
            if not q or q in p.name.lower() or q in p.description.lower()
        ]
        filtered_agents = [
            a
            for a in self.agents
            if (self.scope_filter == "all" or a.scope == self.scope_filter)
            and (not q or q in a.name.lower() or q in a.role.lower())
        ]

        with self:
            with ui.element("div").classes(
                "p-8 space-y-6 max-w-3xl mx-auto pb-20 flex flex-col"
            ):
                # Top Header
                with ui.element("div").classes(
                    "flex items-center justify-between gap-4"
                ):
                    with ui.element("div").classes("flex flex-col gap-1 min-w-0"):
                        with ui.element("div").classes("flex items-center gap-2"):
                            ui.label("Customizations").classes(
                                "text-lg font-medium text-foreground select-none"
                            )
                            ui.label(
                                active_project.name if active_project else "Workspace"
                            ).classes(
                                "text-xs px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground border border-card-border"
                            )
                        ui.label(
                            "Manage workspace and global skills, steering rules (`AGENTS.md`), plugins, and custom subagents."
                        ).classes("text-xs text-muted-foreground")

                    with ui.element("div").classes("flex items-center gap-2 shrink-0"):
                        with (
                            ui.element("button")
                            .props('type="button"')
                            .classes(
                                "inline-flex items-center gap-1.5 h-8 px-3 rounded-lg bg-secondary "
                                "hover:bg-secondary/80 text-foreground text-xs font-medium border border-card-border cursor-pointer"
                            )
                        ):
                            AntigravityIcon("plus", size=14)
                            ui.label("New Skill")
                        with (
                            ui.element("button")
                            .props('type="button"')
                            .classes(
                                "inline-flex items-center gap-1.5 h-8 px-3 rounded-lg bg-secondary "
                                "hover:bg-secondary/80 text-foreground text-xs font-medium border border-card-border cursor-pointer"
                            )
                        ):
                            AntigravityIcon("plus", size=14)
                            ui.label("New Rule")
                        with (
                            ui.element("button")
                            .props('type="button"')
                            .classes(
                                "inline-flex items-center gap-1.5 h-8 px-3 rounded-lg bg-card "
                                "hover:bg-secondary text-secondary-foreground hover:text-foreground "
                                "text-xs border border-card-border cursor-pointer"
                            )
                            .on("click", self.on_open_global_customizations)
                        ):
                            AntigravityIcon("settings", size=14)
                            ui.label("Global & MCP")

                # Filter & Workspace Row
                with ui.element("div").classes("flex items-center gap-2"):
                    with ui.element("div").classes(
                        "relative flex-1 flex items-center bg-card border border-card-border rounded-lg px-3 h-8"
                    ):
                        AntigravityIcon(
                            "search", size=14, classes="text-muted-foreground mr-2"
                        )
                        inp = (
                            ui.input(
                                placeholder="Filter skills, rules, plugins, or custom agents...",
                                on_change=lambda e: self._update_search(e.value),
                            )
                            .props('dense borderless data-testid="skills-rules-filter"')
                            .classes("flex-1 text-xs text-foreground bg-transparent")
                        )
                        inp.value = self.search_query

                    with (
                        ui.element("div")
                        .props('data-testid="project-customizations-workspace-filter"')
                        .classes(
                            "flex items-center gap-1.5 h-8 px-2.5 rounded-lg border border-card-border bg-card text-xs text-foreground"
                        )
                    ):
                        AntigravityIcon(
                            "folder", size=14, classes="text-muted-foreground"
                        )
                        ui.label(
                            active_project.name if active_project else "antigravity-studio"
                        )
                        AntigravityIcon("chevron_down", size=12)

                    with (
                        ui.element("div")
                        .props('data-testid="skills-rules-options"')
                        .classes(
                            "flex items-center rounded-lg border border-card-border bg-card p-0.5 text-xs"
                        )
                    ):
                        for sc in ("all", "Workspace", "Global"):
                            with (
                                ui.element("button")
                                .props('type="button"')
                                .classes(
                                    "px-2.5 py-1 rounded-md text-xs border-none cursor-pointer "
                                    + (
                                        "bg-secondary text-foreground font-medium"
                                        if self.scope_filter == sc
                                        else "bg-transparent text-muted-foreground hover:text-foreground"
                                    )
                                )
                                .on("click", lambda _, s=sc: self._set_scope(s))
                            ):
                                ui.label("All" if sc == "all" else sc)

                # Main Stack (wUb)
                with (
                    ui.element("div")
                    .props('data-testid="workspace-customizations-view"')
                    .classes("flex flex-col gap-6")
                ):
                    # 1. Skills
                    with ui.element("div").classes("flex flex-col gap-2"):
                        with ui.element("div").classes(
                            "flex items-center justify-between w-full px-1 py-0.5"
                        ):
                            with ui.element("div").classes("flex items-center gap-2"):
                                AntigravityIcon(
                                    "chevron_down",
                                    size=14,
                                    classes="text-muted-foreground",
                                )
                                ui.label("Skills").classes(
                                    "text-sm font-medium text-foreground"
                                )
                                ui.label(str(len(filtered_skills))).classes(
                                    "text-xs px-1.5 py-0.2 rounded-full bg-secondary text-muted-foreground"
                                )
                            ui.label(".agents/skills/*/SKILL.md").classes(
                                "text-[11px] text-muted-foreground font-mono"
                            )

                        with ui.element("div").classes(
                            "border border-card-border rounded-xl overflow-hidden bg-card divide-y divide-border flex flex-col"
                        ):
                            for sk in filtered_skills:
                                self._render_skill_or_rule_row(sk, is_skill=True)

                    # 2. Rules
                    with ui.element("div").classes("flex flex-col gap-2"):
                        with ui.element("div").classes(
                            "flex items-center justify-between w-full px-1 py-0.5"
                        ):
                            with ui.element("div").classes("flex items-center gap-2"):
                                AntigravityIcon(
                                    "chevron_down",
                                    size=14,
                                    classes="text-muted-foreground",
                                )
                                ui.label("Rules").classes(
                                    "text-sm font-medium text-foreground"
                                )
                                ui.label(str(len(filtered_rules))).classes(
                                    "text-xs px-1.5 py-0.2 rounded-full bg-secondary text-muted-foreground"
                                )
                            ui.label("AGENTS.md & .agents/rules/*.md").classes(
                                "text-[11px] text-muted-foreground font-mono"
                            )

                        with ui.element("div").classes(
                            "border border-card-border rounded-xl overflow-hidden bg-card divide-y divide-border flex flex-col"
                        ):
                            for rl in filtered_rules:
                                self._render_skill_or_rule_row(rl, is_skill=False)

                    # 3. Plugins
                    with ui.element("div").classes("flex flex-col gap-2"):
                        with ui.element("div").classes(
                            "flex items-center justify-between w-full px-1 py-0.5"
                        ):
                            with ui.element("div").classes("flex items-center gap-2"):
                                AntigravityIcon(
                                    "chevron_down",
                                    size=14,
                                    classes="text-muted-foreground",
                                )
                                ui.label("Plugins").classes(
                                    "text-sm font-medium text-foreground"
                                )
                                ui.label(str(len(filtered_plugins))).classes(
                                    "text-xs px-1.5 py-0.2 rounded-full bg-secondary text-muted-foreground"
                                )
                            ui.label(".agents/plugins/*").classes(
                                "text-[11px] text-muted-foreground font-mono"
                            )

                        with ui.element("div").classes(
                            "border border-card-border rounded-xl overflow-hidden bg-card divide-y divide-border flex flex-col"
                        ):
                            for pl in filtered_plugins:
                                with ui.element("div").classes(
                                    "flex items-center justify-between gap-3 px-4 py-3 hover:bg-secondary/40"
                                ):
                                    with ui.element("div").classes(
                                        "flex flex-col gap-0.5 min-w-0 flex-1"
                                    ):
                                        with ui.element("div").classes(
                                            "flex items-center gap-2"
                                        ):
                                            AntigravityIcon(
                                                "customizations",
                                                size=14,
                                                classes="text-primary",
                                            )
                                            ui.label(pl.name).classes(
                                                "text-sm font-medium text-foreground truncate"
                                            )
                                            ui.label(f"v{pl.version}").props(
                                                'data-testid="plugin-detail-footer-version"'
                                            ).classes(
                                                "text-[10px] font-mono px-1.5 py-0.2 rounded bg-secondary text-muted-foreground border border-card-border"
                                            )
                                            ui.label(
                                                f"{pl.skills_count} skills · {pl.mcp_count} MCP"
                                            ).classes(
                                                "text-[10px] text-muted-foreground"
                                            )
                                        ui.label(pl.description).classes(
                                            "text-xs text-muted-foreground truncate"
                                        )

                    # 4. Custom Agents
                    with ui.element("div").classes("flex flex-col gap-2"):
                        with ui.element("div").classes(
                            "flex items-center justify-between w-full px-1 py-0.5"
                        ):
                            with ui.element("div").classes("flex items-center gap-2"):
                                AntigravityIcon(
                                    "chevron_down",
                                    size=14,
                                    classes="text-muted-foreground",
                                )
                                ui.label("Custom Agents").classes(
                                    "text-sm font-medium text-foreground"
                                )
                                ui.label(str(len(filtered_agents))).classes(
                                    "text-xs px-1.5 py-0.2 rounded-full bg-secondary text-muted-foreground"
                                )
                            ui.label(".agents/agents/*.md").classes(
                                "text-[11px] text-muted-foreground font-mono"
                            )

                        with ui.element("div").classes(
                            "border border-card-border rounded-xl overflow-hidden bg-card divide-y divide-border flex flex-col"
                        ):
                            for ag in filtered_agents:
                                with ui.element("div").classes(
                                    "flex items-center justify-between gap-3 px-4 py-3 hover:bg-secondary/40"
                                ):
                                    with ui.element("div").classes(
                                        "flex flex-col gap-0.5 min-w-0 flex-1"
                                    ):
                                        with ui.element("div").classes(
                                            "flex items-center gap-2"
                                        ):
                                            AntigravityIcon(
                                                "terminal_tab",
                                                size=14,
                                                classes="text-primary",
                                            )
                                            ui.label(ag.name).classes(
                                                "text-sm font-medium text-foreground truncate"
                                            )
                                            ui.label(ag.model).classes(
                                                "text-[10px] px-1.5 py-0.2 rounded bg-secondary text-secondary-foreground border border-card-border"
                                            )
                                        ui.label(ag.role).classes(
                                            "text-xs text-muted-foreground truncate"
                                        )

    def _render_skill_or_rule_row(
        self, entry: SkillRuleEntry, is_skill: bool
    ) -> None:
        with ui.element("div").classes(
            "flex items-center justify-between gap-3 px-4 py-3 hover:bg-secondary/40 transition-colors"
        ):
            with ui.element("div").classes("flex flex-col gap-0.5 min-w-0 flex-1"):
                with ui.element("div").classes("flex items-center gap-2"):
                    AntigravityIcon(
                        "sparkles" if is_skill else "file_doc",
                        size=14,
                        classes="text-primary"
                        if is_skill
                        else "text-secondary-foreground",
                    )
                    ui.label(entry.name).classes(
                        "text-sm font-medium text-foreground truncate"
                    )
                    if entry.trigger:
                        ui.label(entry.trigger).classes(
                            "text-[10px] px-1.5 py-0.2 rounded bg-secondary text-secondary-foreground border border-card-border"
                        )
                    scope_cls = (
                        "text-[10px] px-1.5 py-0.2 rounded border "
                        + (
                            "bg-primary/10 text-primary border-primary/30"
                            if entry.scope == "Workspace"
                            else "bg-secondary text-muted-foreground border-card-border"
                        )
                    )
                    ui.label(entry.scope).classes(scope_cls)
                ui.label(entry.description).classes(
                    "text-xs text-muted-foreground truncate"
                )
                ui.label(entry.path).classes(
                    "text-[11px] text-muted-foreground/70 font-mono truncate"
                )

            with ui.element("div").classes("flex items-center gap-1.5 shrink-0"):
                with (
                    ui.element("button")
                    .props('type="button"')
                    .classes(
                        "inline-flex items-center gap-1 h-7 px-2 rounded-md bg-secondary/70 "
                        "hover:bg-secondary text-xs text-secondary-foreground hover:text-foreground "
                        "border border-card-border cursor-pointer"
                    )
                    .on(
                        "click",
                        lambda _, e=entry: (
                            self.on_open_file_in_aux(e.path, e.name, e.content)
                            if self.on_open_file_in_aux
                            else None
                        ),
                    )
                ):
                    AntigravityIcon("file_doc", size=13)
                    ui.label("Open")

                with (
                    ui.element("button")
                    .props('type="button" role="switch"')
                    .classes(
                        "relative inline-flex h-4 w-7 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors "
                        + ("bg-primary" if entry.enabled else "bg-secondary")
                    )
                    .on("click", lambda _, e=entry: self._toggle_entry(e))
                ):
                    ui.element("span").classes(
                        "pointer-events-none inline-block h-3 w-3 transform rounded-full bg-white shadow transition "
                        + ("translate-x-3" if entry.enabled else "translate-x-0")
                    )

    def _update_search(self, val: str) -> None:
        self.search_query = val
        self.render_view()

    def _set_scope(self, sc: str) -> None:
        self.scope_filter = (
            "Workspace"
            if sc == "Workspace"
            else ("Global" if sc == "Global" else "all")
        )
        self.render_view()

    def _toggle_entry(self, entry: SkillRuleEntry) -> None:
        entry.enabled = not entry.enabled
        self.render_view()
