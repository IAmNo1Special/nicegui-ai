"""Data models and types for nicegui-ai primitives."""

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class MessageRole(StrEnum):
    USER = "user"
    AGENT = "agent"
    ASSISTANT = "agent"
    SYSTEM = "system"


class ToolStatus(StrEnum):
    PENDING = "pending"
    EXECUTING = "executing"
    RESOLVED = "resolved"
    FAILED = "failed"
    APPROVAL_REQUIRED = "approval_required"
    VETOED = "vetoed"


@dataclass
class ToolCall:
    """Represents a tool execution request and its result."""

    id: str
    name: str
    args: dict[str, Any] = field(default_factory=dict)
    result: Any | None = None
    status: ToolStatus = ToolStatus.PENDING
    action_phrase: str = ""
    summary: str = ""
    duration_ms: int | None = None


@dataclass
class ReasoningStep:
    """Represents reasoning effort / chain-of-thought steps."""

    text: str
    step_number: int = 1


@dataclass
class SuggestionPrompt:
    """Prompt pill shown on the empty thread state."""

    label: str
    prompt: str
    icon: str = "sparkles"


@dataclass
class ChatMessage:
    """A conversational message part in an AiThread."""

    id: str
    role: MessageRole
    content: str = ""
    reasoning: str | None = None
    tool_calls: list[ToolCall] = field(default_factory=list)
    tokens_used: int = 0
    created_at: str = ""
