"""1:1 Antigravity Desktop Clone Component Suite for NiceGUI (`nicegui_ai.antigravity`)."""

from .app import AntigravityApp, main, register_antigravity_routes
from .automations_view import AutomationsView
from .auxiliary_pane import AuxiliaryPane, AuxTabType, ChangedFile, DiffLine
from .chat_view import ChatView
from .customizations_view import (
    CustomAgentEntry,
    PluginEntry,
    SkillRuleEntry,
    WorkspaceCustomizationsView,
)
from .history_view import ConversationHistoryView, SearchConversationsModal
from .icons import AntigravityIcon, get_antigravity_svg
from .model_selector import AntigravityModelSelector
from .settings_modal import SettingsModal
from .sidebar import CenterViewType, Sidebar
from .state import (
    AppSettings,
    ArtifactItem,
    AutomationItem,
    ContextAttachment,
    FeatureFlagConfig,
    HookConfig,
    McpServerConfig,
    McpToolConfig,
    Message,
    ProjectConfig,
    SecurityRule,
    Session,
    SkillItem,
    SubagentItem,
    ThinkingBlock,
    ToolCallItem,
    create_default_artifact,
    create_default_automations,
    create_default_sessions,
    create_default_settings,
    create_default_skills,
    create_default_subagents,
)
from .theme import (
    ANTIGRAVITY_THEME_CSS,
    apply_antigravity_theme_mode,
    setup_antigravity_theme,
)
from .title_bar import MenuEntry, TitleBar

__all__ = [
    "ANTIGRAVITY_THEME_CSS",
    "AntigravityApp",
    "AntigravityIcon",
    "AntigravityModelSelector",
    "AppSettings",
    "ArtifactItem",
    "AutomationItem",
    "AutomationsView",
    "AuxTabType",
    "AuxiliaryPane",
    "CenterViewType",
    "ChangedFile",
    "ChatView",
    "ContextAttachment",
    "ConversationHistoryView",
    "CustomAgentEntry",
    "DiffLine",
    "FeatureFlagConfig",
    "HookConfig",
    "McpServerConfig",
    "McpToolConfig",
    "MenuEntry",
    "Message",
    "PluginEntry",
    "ProjectConfig",
    "SearchConversationsModal",
    "SecurityRule",
    "Session",
    "SettingsModal",
    "Sidebar",
    "SkillItem",
    "SkillRuleEntry",
    "SubagentItem",
    "ThinkingBlock",
    "TitleBar",
    "ToolCallItem",
    "WorkspaceCustomizationsView",
    "apply_antigravity_theme_mode",
    "create_default_artifact",
    "create_default_automations",
    "create_default_sessions",
    "create_default_settings",
    "create_default_skills",
    "create_default_subagents",
    "get_antigravity_svg",
    "main",
    "register_antigravity_routes",
    "setup_antigravity_theme",
]
