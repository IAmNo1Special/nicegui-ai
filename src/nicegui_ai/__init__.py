"""nicegui-ai: Modern AI agent UI primitives for NiceGUI."""

from nicegui_ai.approval_modal import ApprovalModal
from nicegui_ai.artifact import ArtifactCard
from nicegui_ai.branch import BranchPicker
from nicegui_ai.code_block import CodeBlock
from nicegui_ai.composer import AiComposer
from nicegui_ai.drawer import SlideOverDrawer
from nicegui_ai.header import FloatingHeader, TokenRing
from nicegui_ai.icons import LucideIcon, get_lucide_svg
from nicegui_ai.message import AgentMessage, AssistantMessage, UserMessage
from nicegui_ai.reasoning import ReasoningCard
from nicegui_ai.theme import THEME_CSS, setup_ai_theme
from nicegui_ai.thread import AiThread
from nicegui_ai.tool_call import ToolCallCard
from nicegui_ai.types import (
    ChatMessage,
    MessageRole,
    ReasoningStep,
    SuggestionPrompt,
    ToolCall,
    ToolStatus,
)

__version__ = "0.2.0"

__all__ = [
    "AgentMessage",
    "AiComposer",
    "AiThread",
    "ApprovalModal",
    "ArtifactCard",
    "AssistantMessage",
    "BranchPicker",
    "ChatMessage",
    "CodeBlock",
    "FloatingHeader",
    "LucideIcon",
    "MessageRole",
    "ReasoningCard",
    "ReasoningStep",
    "SlideOverDrawer",
    "SuggestionPrompt",
    "THEME_CSS",
    "TokenRing",
    "ToolCall",
    "ToolCallCard",
    "ToolStatus",
    "UserMessage",
    "get_lucide_svg",
    "setup_ai_theme",
]
