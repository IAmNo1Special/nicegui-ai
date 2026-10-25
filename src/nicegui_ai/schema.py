"""Data models and schemas for nicegui-ai primitives."""

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
    SUCCESS = "resolved"
    FAILED = "failed"
    APPROVAL_REQUIRED = "approval_required"
    VETOED = "vetoed"


@dataclass
class QueuedMessage:
    """A user prompt queued while an agent execution is in-flight."""

    id: str
    text: str


@dataclass
class RunningTask:
    """A background task displayed in the TaskTray."""

    id: str
    text: str


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


class AgUiEventType(StrEnum):
    """Standardized event types from the AG-UI specification."""

    # Lifecycle events
    RUN_STARTED = "RUN_STARTED"
    RUN_FINISHED = "RUN_FINISHED"
    RUN_ERROR = "RUN_ERROR"
    STEP_STARTED = "STEP_STARTED"
    STEP_FINISHED = "STEP_FINISHED"

    # Text message events
    TEXT_MESSAGE_START = "TEXT_MESSAGE_START"
    TEXT_MESSAGE_CONTENT = "TEXT_MESSAGE_CONTENT"
    TEXT_MESSAGE_END = "TEXT_MESSAGE_END"
    TEXT_MESSAGE_CHUNK = "TEXT_MESSAGE_CHUNK"

    # Tool call events
    TOOL_CALL_START = "TOOL_CALL_START"
    TOOL_CALL_ARGS = "TOOL_CALL_ARGS"
    TOOL_CALL_END = "TOOL_CALL_END"
    TOOL_CALL_RESULT = "TOOL_CALL_RESULT"

    # Reasoning / thinking events
    REASONING_START = "REASONING_START"
    REASONING_MESSAGE_START = "REASONING_MESSAGE_START"
    REASONING_MESSAGE_CONTENT = "REASONING_MESSAGE_CONTENT"
    REASONING_MESSAGE_END = "REASONING_MESSAGE_END"
    REASONING_MESSAGE_CHUNK = "REASONING_MESSAGE_CHUNK"
    REASONING_END = "REASONING_END"
    REASONING_ENCRYPTED_VALUE = "REASONING_ENCRYPTED_VALUE"

    # State & activity management
    STATE_SNAPSHOT = "STATE_SNAPSHOT"
    STATE_DELTA = "STATE_DELTA"
    MESSAGES_SNAPSHOT = "MESSAGES_SNAPSHOT"
    ACTIVITY_SNAPSHOT = "ACTIVITY_SNAPSHOT"
    ACTIVITY_DELTA = "ACTIVITY_DELTA"

    # Subagent events
    SUBAGENT_STARTED = "SUBAGENT_STARTED"
    SUBAGENT_FINISHED = "SUBAGENT_FINISHED"
    SUBAGENT_ERROR = "SUBAGENT_ERROR"

    # Special events
    RAW = "RAW"
    CUSTOM = "CUSTOM"


@dataclass
class AgUiEvent:
    """AG-UI compliant streaming event structure."""

    type: AgUiEventType
    timestamp: float | None = None
    raw_event: Any = None
    metadata: dict[str, Any] = field(default_factory=dict)
    subagent_run_id: str | None = None

    # Lifecycle
    run_id: str | None = None
    step_id: str | None = None
    step_name: str | None = None

    # Message & text content
    message_id: str | None = None
    role: str | None = None
    content: str | None = None

    # Tool call
    tool_call_id: str | None = None
    tool_name: str | None = None
    args: dict[str, Any] | str | None = None
    result: Any | None = None
    is_error: bool = False

    # Error payload
    error: str | None = None
    code: str | None = None

    # State and Activity
    snapshot: Any | None = None
    delta: Any | None = None
    activity_id: str | None = None

    # Custom extension
    custom_type: str | None = None
