"""nicegui-ai: Modern AI agent UI primitives for NiceGUI."""

from nicegui_ai.approval_modal import ApprovalModal
from nicegui_ai.artifact import ArtifactCard
from nicegui_ai.branch import BranchPicker
from nicegui_ai.code_block import CodeBlock
from nicegui_ai.composer import AiComposer
from nicegui_ai.drawer import SlideOverDrawer
from nicegui_ai.header import FloatingHeader, TokenRing
from nicegui_ai.icons import LucideIcon, get_lucide_svg
from nicegui_ai.markdown import AiMarkdown, parse_markdown_blocks
from nicegui_ai.message import AgentMessage, AssistantMessage, UserMessage
from nicegui_ai.model_selector import (
    ModelOption,
    ModelSelector,
    ReasoningEffortSelector,
)
from nicegui_ai.queued_messages import QueuedMessagesTray
from nicegui_ai.reasoning import ReasoningCard
from nicegui_ai.task_tray import TaskHandle, TaskTray
from nicegui_ai.theme import THEME_CSS, setup_ai_theme
from nicegui_ai.thread import AiThread
from nicegui_ai.tool_call import ToolCallCard
from nicegui_ai.types import (
    ChatMessage,
    MessageRole,
    QueuedMessage,
    ReasoningStep,
    RunningTask,
    SuggestionPrompt,
    ToolCall,
    ToolStatus,
)
from nicegui_ai.voice_pill import VoicePill

__version__ = "0.2.0"

__all__ = [
    "AgentMessage",
    "AiComposer",
    "AiMarkdown",
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
    "ModelOption",
    "ModelSelector",
    "QueuedMessage",
    "QueuedMessagesTray",
    "ReasoningCard",
    "ReasoningEffortSelector",
    "ReasoningStep",
    "RunningTask",
    "SlideOverDrawer",
    "SuggestionPrompt",
    "THEME_CSS",
    "TaskHandle",
    "TaskTray",
    "TokenRing",
    "ToolCall",
    "ToolCallCard",
    "ToolStatus",
    "UserMessage",
    "VoicePill",
    "get_lucide_svg",
    "parse_markdown_blocks",
    "setup_ai_theme",
]
