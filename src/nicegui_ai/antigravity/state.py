"""Typed state models and initial data for the 1:1 Antigravity Desktop Clone."""

from dataclasses import dataclass, field
from typing import Literal


@dataclass
class ArtifactItem:
    id: str
    title: str
    type: Literal["markdown", "code", "diff", "json", "html"]
    content: str
    description: str | None = None


@dataclass
class ToolCallItem:
    id: str
    tool_name: str
    action: str
    parameters: dict[str, object]
    output: str
    status: Literal["running", "completed", "error"] = "completed"
    artifacts: list[ArtifactItem] = field(default_factory=list)


@dataclass
class ThinkingBlock:
    duration: str
    steps: list[str]


@dataclass
class ContextAttachment:
    id: str
    label: str
    category: Literal[
        "file", "folder", "symbol", "skill", "rule", "media", "browser", "action"
    ]
    detail: str | None = None


@dataclass
class Message:
    id: str
    role: Literal["user", "agent", "system"]
    content: str
    timestamp: str
    thinking: ThinkingBlock | None = None
    tool_calls: list[ToolCallItem] = field(default_factory=list)
    attachments: list[ContextAttachment] = field(default_factory=list)


@dataclass
class Session:
    id: str
    title: str
    timestamp: str
    token_count: int
    messages: list[Message] = field(default_factory=list)
    project_id: str | None = None
    pinned: bool = False
    archived: bool = False


@dataclass
class SubagentItem:
    id: str
    name: str
    role: str
    type: Literal["self", "researcher", "coder", "reviewer"]
    state: Literal["running", "idle", "completed", "error"]
    last_activity: str


@dataclass
class SkillItem:
    id: str
    name: str
    description: str
    category: str
    active: bool = True


@dataclass
class AutomationItem:
    id: str
    display_name: str
    project_id: str
    prompt: str
    schedule_summary: str
    frequency: Literal["daily", "weekly", "hourly", "weekdays"]
    hour: str
    enabled: bool
    last_run: str | None = None
    day_of_week: str | None = None


@dataclass
class SecurityRule:
    id: str
    value: str
    policy: Literal["allow", "ask", "deny"]


@dataclass
class McpToolConfig:
    name: str
    description: str
    enabled: bool = True


@dataclass
class McpServerConfig:
    id: str
    name: str
    command: str
    args: list[str]
    enabled: bool
    status: Literal["connected", "disconnected", "error"]
    tools: list[McpToolConfig] = field(default_factory=list)


@dataclass
class HookConfig:
    id: str
    event: Literal["PreToolUse", "PostToolUse", "PreInvocation", "PostInvocation"]
    matcher: str
    command: str
    timeout: int


@dataclass
class FeatureFlagConfig:
    name: str
    enabled: bool


@dataclass
class ProjectConfig:
    id: str
    name: str
    folders: list[str]
    active_conversations: int
    archived_conversations: int
    security_preset: Literal["inherit", "strict", "default", "auto", "turbo"] = "inherit"
    artifact_review_mode: Literal["inherit", "always", "review", "auto"] = "inherit"
    sandbox_enabled: bool = True
    sandbox_allow_network: bool = False
    auto_execution_policy: Literal["off", "sandbox", "always"] = "sandbox"


@dataclass
class AppSettings:
    queued_message_strategy: Literal["send", "queue"] = "queue"
    security_preset: Literal["strict", "default", "auto", "turbo", "custom"] = "default"
    artifact_review_mode: Literal["always", "review", "auto"] = "review"
    sandbox_enabled: bool = True
    sandbox_allow_network: bool = False
    auto_execution_policy: Literal["off", "sandbox", "always"] = "sandbox"
    non_workspace_file_access: Literal["block", "ask", "allow"] = "ask"
    file_read_rules: list[SecurityRule] = field(default_factory=list)
    file_write_rules: list[SecurityRule] = field(default_factory=list)
    network_rules: list[SecurityRule] = field(default_factory=list)
    terminal_command_rules: list[SecurityRule] = field(default_factory=list)
    outside_sandbox_rules: list[SecurityRule] = field(default_factory=list)
    mcp_tool_rules: list[SecurityRule] = field(default_factory=list)
    enable_browser_tools: bool = True
    browser_js_execution_policy: Literal["disabled", "review", "always"] = "review"
    enable_agent_notifications: bool = True
    enable_agent_sounds: bool = False
    browser_allowed_urls: list[str] = field(default_factory=list)
    browser_denied_urls: list[str] = field(default_factory=list)
    terminal_setup_script: str = (
        "# Antigravity non-interactive shell setup\nexport PAGER=cat\nexport FORCE_COLOR=1"
    )
    default_workspace_vcs: Literal["git", "jj"] = "git"
    sync_jj_worktrees: bool = True
    use_full_vcs_clones: bool = False
    use_full_git_clones: bool = False
    lab_inline_actions: bool = True
    lab_autonomous_mode: bool = True
    lab_demo_mode: bool = False
    theme_mode: Literal["dark", "light", "oled"] = "dark"
    verbose_agent_chat: bool = True
    conversation_width: Literal["compact", "default", "wide", "full"] = "default"
    artifact_width: Literal["compact", "default", "wide", "full"] = "default"
    custom_context_menus: bool = True
    marketplace_item_url: str = "https://open-vsx.org/vscode/item"
    marketplace_gallery_url: str = "https://open-vsx.org/vscode/gallery"
    show_selection_actions: bool = True
    confirm_window_reload: bool = False
    tab_suggestions_in_editor: bool = True
    tab_speed: Literal["fast", "balanced", "thorough"] = "fast"
    tab_highlight_after_accept: bool = True
    tab_to_import: bool = True
    tab_to_jump: bool = True
    tab_gitignore_access: bool = False
    plan_name: str = "Google AI Ultra"
    enable_ai_credit_overages: bool = True
    available_ai_credits: int = 2500
    include_default_customizations: bool = True
    active_authority: str = "local"
    mcp_servers: list[McpServerConfig] = field(default_factory=list)
    skill_custom_paths: list[str] = field(default_factory=list)
    hooks: list[HookConfig] = field(default_factory=list)
    prevent_sleep: bool = True
    keep_in_menu_bar: bool = True
    enable_remote_control: bool = False
    remote_control_nickname: str = "vanluther-linux-x64"
    auto_check_updates: bool = True
    runtime_env_override: str = "http://127.0.0.1:46349"
    workspace_uri_override: str = "file:///mnt/storage/projects/nicegui-ai"
    feature_flags: list[FeatureFlagConfig] = field(default_factory=list)
    enable_telemetry: bool = False
    marketing_emails: bool = False
    account_name: str = "Van Luther"
    account_email: str = "vanluther@gmail.com"
    project_id: str = "antigravity-studio-local"
    projects: list[ProjectConfig] = field(default_factory=list)


def create_default_artifact() -> ArtifactItem:
    return ArtifactItem(
        id="art-rea-report",
        title="Antigravity 1:1 Architecture & REA Reconstruction",
        type="markdown",
        description="Evidence-backed reverse engineering breakdown of Antigravity Desktop App",
        content=(
            "# Antigravity 1:1 Desktop UI/UX Reconstruction\n"
            "Generated via **[morluto/rea](https://github.com/morluto/rea)** & Live CDP Runtime Inspection\n\n"
            "---\n\n"
            "### Verified Architecture & Tokens\n\n"
            "1. **Native Shell & IPC Protocol**:\n"
            "   - Discovered **3 BrowserWindows**, **12 ContextBridge APIs**, and **37 literal IPC channels**.\n"
            "   - Electron frameless window with native 35px custom titlebar.\n\n"
            "2. **1:1 Color Tokens Extracted from Live DOM**:\n"
            "   - `--background`: `#101010`\n"
            "   - `--sidebar`: `#151515`\n"
            "   - `--card`: `#191919`\n"
            "   - `--card-border`: `#222222`\n"
            "   - `--secondary`: `#272727`\n"
            "   - `--muted`: `#151515`\n"
            "   - `--foreground`: `#cccccc`\n"
            "   - `--muted-foreground`: `#6e6e6e`\n\n"
            "3. **Complete 1:1 Interactive Surfaces in Python + NiceGUI**:\n"
            "   - Zero-State New Conversation Home View (`rYb` & `Q1b`) with workspace selector, environment selector, and recent conversation search.\n"
            "   - Conversation History View (`IRb`) & `Ctrl+K` Search Conversations Command Palette.\n"
            "   - Automations View (`K1b`), `New Automation` modal (`I1b`), and Schedule Editor (`B1b` / `A1b`).\n"
            "   - Dedicated Workspace Customizations View (`xUb` / `wUb`) for Skills, Rules, Plugins, and Custom Agents.\n"
            "   - Composer `+` Add Context (`vBb`), `@` Mentions, `/` Fastpick, Modes (`Autonomous Mode`, `Best of N`), Side Question, and Permissions Preset (`Awb`).\n"
            "   - Auxiliary Pane (`Overview`, `Review Diffs`, `2-Column Terminal`, `Artifact/File Viewer`, `Browser Preview`, `Subagents Inspector`) & 2-Column Settings Modal (13 screens & 11 subviews).\n"
        ),
    )


def create_default_settings() -> AppSettings:
    return AppSettings(
        file_read_rules=[
            SecurityRule(id="fr-1", value="/mnt/storage/projects/**", policy="allow"),
            SecurityRule(id="fr-2", value="~/.agents/skills/**", policy="allow"),
            SecurityRule(id="fr-3", value="~/.ssh/**", policy="deny"),
        ],
        file_write_rules=[
            SecurityRule(
                id="fw-1", value="/mnt/storage/projects/nicegui-ai/**", policy="allow"
            ),
        ],
        network_rules=[
            SecurityRule(
                id="nr-1", value="https://github.com/morluto/rea*", policy="allow"
            ),
            SecurityRule(id="nr-2", value="http://127.0.0.1:*", policy="allow"),
        ],
        terminal_command_rules=[
            SecurityRule(id="tc-1", value="uv run pytest", policy="allow"),
            SecurityRule(id="tc-2", value="uv run ruff check", policy="allow"),
            SecurityRule(id="tc-3", value="git status", policy="allow"),
            SecurityRule(id="tc-4", value="rm -rf /", policy="deny"),
        ],
        outside_sandbox_rules=[
            SecurityRule(id="os-1", value="chromium --headless=new", policy="allow"),
        ],
        mcp_tool_rules=[
            SecurityRule(id="mp-1", value="mcp:morluto/rea:*", policy="allow"),
        ],
        browser_allowed_urls=[
            "http://localhost:*",
            "http://127.0.0.1:*",
            "https://github.com/*",
        ],
        browser_denied_urls=[
            "https://mail.google.com/*",
            "https://accounts.google.com/*",
        ],
        mcp_servers=[
            McpServerConfig(
                id="mcp-rea",
                name="morluto/rea",
                command="uvx",
                args=["rea-mcp-server", "--asar-support"],
                enabled=True,
                status="connected",
                tools=[
                    McpToolConfig(
                        name="rea_analyze_javascript_application",
                        description="Unpack app.asar and project AST boundaries, BrowserWindows, and IPC channels",
                        enabled=True,
                    ),
                    McpToolConfig(
                        name="rea_inspect_cdp_target",
                        description="Attach to live Chrome DevTools Protocol port and dump computed styles & DOM",
                        enabled=True,
                    ),
                    McpToolConfig(
                        name="rea_extract_web_bundle",
                        description="Deobfuscate and slice embedded Webpack/Vite bundles",
                        enabled=True,
                    ),
                ],
            ),
            McpServerConfig(
                id="mcp-fs",
                name="filesystem",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-filesystem", "/mnt/storage/projects"],
                enabled=True,
                status="connected",
                tools=[
                    McpToolConfig(
                        name="read_file",
                        description="Read complete contents of a file from disk",
                        enabled=True,
                    ),
                    McpToolConfig(
                        name="write_file",
                        description="Create or overwrite a file in workspace",
                        enabled=True,
                    ),
                    McpToolConfig(
                        name="list_directory",
                        description="List files and subdirectories",
                        enabled=True,
                    ),
                ],
            ),
            McpServerConfig(
                id="mcp-gh",
                name="github",
                command="npx",
                args=["-y", "@modelcontextprotocol/server-github"],
                enabled=False,
                status="disconnected",
                tools=[
                    McpToolConfig(
                        name="search_repositories",
                        description="Search GitHub repositories",
                        enabled=True,
                    ),
                    McpToolConfig(
                        name="get_file_contents",
                        description="Get contents of a file in a repository",
                        enabled=True,
                    ),
                ],
            ),
        ],
        skill_custom_paths=[
            "/home/vanluther/.agents/skills",
            "/home/vanluther/.gemini/antigravity/builtin/skills",
        ],
        hooks=[
            HookConfig(
                id="hk-1",
                event="PreToolUse",
                matcher="run_command",
                command="agy-audit-command --strict",
                timeout=3000,
            ),
            HookConfig(
                id="hk-2",
                event="PostInvocation",
                matcher="*",
                command='notify-send "Antigravity turn completed"',
                timeout=2000,
            ),
        ],
        feature_flags=[
            FeatureFlagConfig(name="enable_goal_slash_command", enabled=True),
            FeatureFlagConfig(name="enable_gemini_3_8_models", enabled=True),
            FeatureFlagConfig(name="enable_cdp_live_inspector", enabled=True),
        ],
        projects=[
            ProjectConfig(
                id="proj-mvge",
                name="mvge stack",
                folders=["/mnt/storage/projects/mvge"],
                active_conversations=5,
                archived_conversations=1,
                security_preset="auto",
                artifact_review_mode="inherit",
                sandbox_enabled=True,
                sandbox_allow_network=False,
                auto_execution_policy="sandbox",
            ),
            ProjectConfig(
                id="proj-agarmmo",
                name="AgarMMO",
                folders=["/mnt/storage/projects/AgarMMO"],
                active_conversations=0,
                archived_conversations=0,
                security_preset="inherit",
                artifact_review_mode="inherit",
                sandbox_enabled=True,
                sandbox_allow_network=True,
                auto_execution_policy="sandbox",
            ),
            ProjectConfig(
                id="proj-nicegui",
                name="nicegui-ai",
                folders=["/mnt/storage/projects/nicegui-ai"],
                active_conversations=1,
                archived_conversations=0,
                security_preset="inherit",
                artifact_review_mode="inherit",
                sandbox_enabled=True,
                sandbox_allow_network=False,
                auto_execution_policy="sandbox",
            ),
            ProjectConfig(
                id="proj-ag-studio",
                name="antigravity-studio",
                folders=["/mnt/storage/projects/AI/antigravity-studio"],
                active_conversations=1,
                archived_conversations=0,
                security_preset="turbo",
                artifact_review_mode="auto",
                sandbox_enabled=True,
                sandbox_allow_network=True,
                auto_execution_policy="always",
            ),
        ],
    )


def create_default_subagents() -> list[SubagentItem]:
    return [
        SubagentItem(
            id="ag-self",
            name="Primary Orchestrator",
            role="Full execution & tool routing agent",
            type="self",
            state="idle",
            last_activity="Ready for user prompt",
        ),
        SubagentItem(
            id="ag-rea",
            name="REA Reverse Engineer",
            role="Static analysis and AST boundary projector",
            type="researcher",
            state="idle",
            last_activity="Parsed 776 files in app.asar",
        ),
        SubagentItem(
            id="ag-coder",
            name="Code Synthesizer",
            role="Python NiceGUI & TypeScript UI generator",
            type="coder",
            state="idle",
            last_activity="Reconstructed Antigravity in NiceGUI",
        ),
        SubagentItem(
            id="ag-reviewer",
            name="Security Reviewer",
            role="ContextIsolation and IPC audit specialist",
            type="reviewer",
            state="idle",
            last_activity="Audited 37 IPC channels",
        ),
    ]


def create_default_skills() -> list[SkillItem]:
    return [
        SkillItem(
            id="sk-rea",
            name="clean-room-reverse-engineering",
            description="Perform clean-room reverse engineering of any codebase or binary.",
            category="Reverse Engineering",
            active=True,
        ),
        SkillItem(
            id="sk-deep",
            name="codebase-deep-dive",
            description="Exhaustive low-level technical analysis of local or remote codebases.",
            category="Reverse Engineering",
            active=True,
        ),
        SkillItem(
            id="sk-nicegui",
            name="nicegui",
            description="Build Python-first web and native desktop applications with NiceGUI.",
            category="Development",
            active=True,
        ),
        SkillItem(
            id="sk-gemini",
            name="gemini-api-dev",
            description="SDK usage and best practices for Gemini 3.8 Pro & Flash models.",
            category="Development",
            active=True,
        ),
        SkillItem(
            id="sk-mcp",
            name="create-mcp-app",
            description="Scaffold and register Model Context Protocol servers and interactive UIs.",
            category="Development",
            active=True,
        ),
        SkillItem(
            id="sk-agy",
            name="agy-customizations",
            description="Guide and reference for the Antigravity Customization System.",
            category="System",
            active=True,
        ),
    ]


def create_default_automations() -> list[AutomationItem]:
    return [
        AutomationItem(
            id="auto-1",
            display_name="Daily REA Bundle Parity Audit",
            project_id="proj-ag-studio",
            prompt="Inspect extracted-web-bundle/main.js and verify all Python NiceGUI components and CSS variables match the upstream Antigravity release.",
            schedule_summary="Every day at 9:00 AM • antigravity-studio",
            frequency="daily",
            hour="9:00 AM",
            enabled=True,
            last_run="2h ago",
        ),
        AutomationItem(
            id="auto-2",
            display_name="Weekly MVGeos Dependency & Security Sweep",
            project_id="proj-mvge",
            prompt="Run uv run ruff check and pytest across the mvge stack repository and open a summary artifact.",
            schedule_summary="Every Monday at 6:00 AM • mvge stack",
            frequency="weekly",
            day_of_week="Monday",
            hour="6:00 AM",
            enabled=True,
            last_run="3d ago",
        ),
        AutomationItem(
            id="auto-3",
            display_name="Nightly NiceGUI E2E Headless Screenshot Check",
            project_id="proj-nicegui",
            prompt="Launch headless Chromium against nicegui-ai local server and verify all 26 UI views render without console errors.",
            schedule_summary="Every day at 11:00 PM • nicegui-ai",
            frequency="daily",
            hour="11:00 PM",
            enabled=False,
            last_run="Paused",
        ),
    ]


def create_default_sessions() -> list[Session]:
    initial_art = create_default_artifact()
    return [
        Session(
            id="session-zero-state",
            title="New Conversation",
            timestamp="Just now",
            token_count=0,
            project_id="proj-ag-studio",
            messages=[],
        ),
        Session(
            id="session-clone-rea",
            title="Clone Antigravity UI Using Rea",
            timestamp="6h ago",
            token_count=42800,
            project_id="proj-ag-studio",
            pinned=True,
            messages=[
                Message(
                    id="m1",
                    role="user",
                    content="i love the ui/ux for the antigravity destop app(/home/vanluther/Downloads/Antigravity/Antigravity-x64/antigravity) and i want you to use https://github.com/morluto/rea to create my own version of it, if possible.",
                    timestamp="6:05 AM",
                ),
                Message(
                    id="m2",
                    role="agent",
                    content=(
                        "I've started reverse-engineering the Antigravity desktop application using **morluto/rea** (Reverse Engineer Anything).\n\n"
                        "Unpacked `resources/app.asar` and identified the ConnectRPC backend, embedded UI bundle, and 37 IPC channels. "
                        "I've reconstructed the complete 1:1 component suite in `/mnt/storage/projects/nicegui-ai`."
                    ),
                    timestamp="6:07 AM",
                    thinking=ThinkingBlock(
                        duration="8s",
                        steps=[
                            "Targeted Antigravity desktop installation at /home/vanluther/Downloads/Antigravity/Antigravity-x64",
                            "Analyzed app.asar structure and registered IPC channels with REA",
                            "Identified ConnectRPC backend and embedded Web UI bundle",
                        ],
                    ),
                    tool_calls=[
                        ToolCallItem(
                            id="tc-1",
                            tool_name="rea_analyze_javascript_application",
                            action="Analyzing app.asar with REA",
                            parameters={"target": "resources/app.asar"},
                            output="Found 3 BrowserWindows, 12 ContextBridge APIs, 37 literal IPC channels.",
                            status="completed",
                        )
                    ],
                ),
                Message(
                    id="m3",
                    role="user",
                    content="the ui/ux should be 1 to 1. reconstruct all components into python nicegui components in /mnt/storage/projects/nicegui-ai.",
                    timestamp="6:36 AM",
                ),
                Message(
                    id="m4",
                    role="agent",
                    content=(
                        "Understood! I inspected the live running Antigravity instance on port 46349 via Chrome DevTools Protocol (CDP) and extracted its exact runtime DOM hierarchy, CSS tokens, and Google Material Symbol SVG paths.\n\n"
                        "### 1-to-1 UI/UX Reconstruction Complete:\n"
                        "1. **Window Frame & Menu**: Minimal 35px native title bar (`Antigravity  File  View  Window`) with interactive dropdowns.\n"
                        "2. **Sidebar (256px)**: Exact icon strip (Antigravity logo, toggle, arrows, search), action buttons, pinned conversations with dots/kebabs, and project trees.\n"
                        "3. **Conversation View & Zero-State Home**:\n"
                        "   - Centered Zero-State home screen (`rYb` & `Q1b`) with workspace selector, environment selector, and inline conversation search.\n"
                        "   - User message card (`lifted-context-menu-trigger`) with hover timestamp, copy, undo, and Lifted Context Menu.\n"
                        "   - Agent thought & tool execution collapsible (`Exploring files, running commands`) with `Thought for 12s`, sub-steps, and inline artifact preview.\n"
                        "4. **Floating Composer, Context Picker & Model Picker**:\n"
                        "   - `+` Add Context menu, `@` Mentions, `/` Fastpick, Modes (`Autonomous Mode`, `Best of N`), Side Question, Permissions Preset (`Awb`), and `Gemini 3.8 Flash High` model selector.\n"
                        "5. **Conversation History, Automations, Customizations, Settings Modal & Auxiliary Pane**:\n"
                        "   - Dedicated `Conversation History` (`IRb`), `Automations` (`K1b` & `B1b`), `Workspace Customizations` (`xUb`), 2-Column `SettingsModal`, and 6-tab `AuxiliaryPane`."
                    ),
                    timestamp="6:38 AM",
                    thinking=ThinkingBlock(
                        duration="12s",
                        steps=[
                            "Connected to live Antigravity instance at ws://127.0.0.1:46349 via CDP",
                            "Extracted computed CSS variables, colors, and SVG paths",
                            "Reconstructed all views, modals, and popovers in Python NiceGUI with 100% pixel fidelity",
                        ],
                    ),
                    tool_calls=[
                        ToolCallItem(
                            id="tc-2",
                            tool_name="run_command",
                            action="Checking running Antigravity processes",
                            parameters={"command": "ps aux | grep -i antigravity"},
                            output="PID 3366: /home/vanluther/Downloads/Antigravity/Antigravity-x64/antigravity\nPID 3560: language_server",
                            status="completed",
                        ),
                        ToolCallItem(
                            id="tc-3",
                            tool_name="view_file",
                            action="Analyzed language_server.log #L0-49",
                            parameters={
                                "path": "/home/vanluther/.config/Antigravity/logs/language_server.log"
                            },
                            output="Started ConnectRPC server on loopback port 46349",
                            status="completed",
                            artifacts=[initial_art],
                        ),
                    ],
                ),
            ],
        ),
        Session(
            id="session-mvge-reorg",
            title="Reorganizing Mvgeos Project Structure",
            timestamp="1d ago",
            token_count=19400,
            project_id="proj-mvge",
            pinned=True,
            messages=[
                Message(
                    id="mv-1",
                    role="user",
                    content="Reorganize the mvge stack modules into clean domain packages.",
                    timestamp="Yesterday",
                ),
                Message(
                    id="mv-2",
                    role="agent",
                    content="Completed modularizing the `mvge stack` packages and verified all unit tests pass.",
                    timestamp="Yesterday",
                ),
            ],
        ),
        Session(
            id="session-nicegui-efforts",
            title="ModelSelector Reasoning Effects",
            timestamp="2d ago",
            token_count=14200,
            project_id="proj-nicegui",
            pinned=True,
            messages=[
                Message(
                    id="ng-1",
                    role="user",
                    content="Wire up the reasoning effort levels in nicegui-ai.",
                    timestamp="2d ago",
                )
            ],
        ),
        Session(
            id="proj-1",
            title="Building MVGeos Frontend",
            timestamp="6h",
            token_count=12300,
            project_id="proj-mvge",
            messages=[
                Message(
                    id="p1-m1",
                    role="user",
                    content="Build the MVGeos frontend components.",
                    timestamp="6h ago",
                )
            ],
        ),
        Session(
            id="proj-2",
            title="MageOS Marketplace User Guide",
            timestamp="2d",
            token_count=8900,
            project_id="proj-mvge",
            messages=[
                Message(
                    id="p2-m1",
                    role="user",
                    content="Draft the MageOS Marketplace user documentation.",
                    timestamp="2d ago",
                )
            ],
        ),
        Session(
            id="proj-3",
            title="Documentation Slop Cleanup",
            timestamp="2d",
            token_count=6400,
            project_id="proj-mvge",
            messages=[
                Message(
                    id="p3-m1",
                    role="user",
                    content="Clean up AI slop across README files.",
                    timestamp="2d ago",
                )
            ],
        ),
        Session(
            id="proj-4",
            title="Codebase Deep Dive Mvgeos",
            timestamp="4d",
            token_count=31200,
            project_id="proj-mvge",
            messages=[
                Message(
                    id="p4-m1",
                    role="user",
                    content="Run codebase-deep-dive on mvge stack.",
                    timestamp="4d ago",
                )
            ],
        ),
        Session(
            id="proj-5",
            title="Codebase Deep Dive Architecture",
            timestamp="5d",
            token_count=28500,
            project_id="proj-mvge",
            messages=[
                Message(
                    id="p5-m1",
                    role="user",
                    content="Map out the architecture boundaries.",
                    timestamp="5d ago",
                )
            ],
        ),
        Session(
            id="conv-1",
            title="Agent Skills Not Showing Up",
            timestamp="15d",
            token_count=5100,
            messages=[
                Message(
                    id="c1-m1",
                    role="user",
                    content="Why are my custom skills in ~/.agents/skills not showing up?",
                    timestamp="15d ago",
                )
            ],
        ),
        Session(
            id="conv-2",
            title="Adding New Skills",
            timestamp="15d",
            token_count=4300,
            messages=[
                Message(
                    id="c2-m1",
                    role="user",
                    content="How do I scaffold a new skill following agentskills.io?",
                    timestamp="15d ago",
                )
            ],
        ),
    ]
