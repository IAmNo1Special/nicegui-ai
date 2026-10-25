"""StreamBridge: Object-oriented AG-UI ingestion engine driving nicegui-ai UI components."""

import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from nicegui_ai.adapters.agui import AgUiStreamAdapter
from nicegui_ai.adapters.base import BaseStreamAdapter
from nicegui_ai.adapters.gemini import GeminiStreamAdapter
from nicegui_ai.adapters.opencode import OpenCodeStreamAdapter
from nicegui_ai.adapters.openrouter import OpenRouterStreamAdapter
from nicegui_ai.schema import AgUiEvent, AgUiEventType, ToolCall, ToolStatus

if TYPE_CHECKING:
    from nicegui_ai.composer import AiComposer
    from nicegui_ai.header import FloatingHeader
    from nicegui_ai.message import AgentMessage
    from nicegui_ai.reasoning import ReasoningCard
    from nicegui_ai.task_tray import TaskHandle, TaskTray
    from nicegui_ai.thread import AiThread
    from nicegui_ai.tool_call import ToolCallCard


@dataclass
class StreamResult:
    """Accumulated summary resulting from an ingested stream."""

    text: str = ""
    thought: str = ""
    tool_calls: list[ToolCall] = field(default_factory=list)
    tool_results: dict[str, Any] = field(default_factory=dict)
    usage: dict[str, int] = field(default_factory=dict)
    finish_reason: str = "completed"
    error: str | None = None
    events: list[AgUiEvent] = field(default_factory=list)
    duration_ms: int = 0


class StreamBridge:
    """Object-oriented AG-UI protocol ingestion bridge driving NiceGUI components.

    Coordinates reactive streaming between AG-UI compliant stream adapters and
    nicegui-ai UI primitives (AgentMessage, ReasoningCard, ToolCallCard, Header, TaskTray).
    """

    def __init__(
        self,
        message: "AgentMessage | None" = None,
        thread: "AiThread | None" = None,
        header: "FloatingHeader | None" = None,
        composer: "AiComposer | None" = None,
        task_tray: "TaskTray | None" = None,
        on_event: Callable[[AgUiEvent], None] | None = None,
    ) -> None:
        self.message = message
        self.thread = thread
        self.header = header
        self.composer = composer
        self.task_tray = task_tray
        self.on_event = on_event

        self._reasoning_card: ReasoningCard | None = None
        self._tool_cards: dict[str, ToolCallCard] = {}
        self._active_tasks: dict[str, TaskHandle] = {}
        self._step_counter: int = 1

    # Factory methods returning specialized stream adapters
    @classmethod
    def from_openrouter(cls, source: Any) -> OpenRouterStreamAdapter:
        """Create an OpenRouter / OpenAI protocol adapter."""
        return OpenRouterStreamAdapter(source)

    @classmethod
    def from_gemini(cls, source: Any) -> GeminiStreamAdapter:
        """Create a Google GenAI (Gemini) protocol adapter."""
        return GeminiStreamAdapter(source)

    @classmethod
    def from_agui(cls, source: Any) -> AgUiStreamAdapter:
        """Create a native AG-UI protocol adapter."""
        return AgUiStreamAdapter(source)

    @classmethod
    def from_opencode(cls, source: Any) -> OpenCodeStreamAdapter:
        """Create an OpenCode coding agent protocol adapter."""
        return OpenCodeStreamAdapter(source)

    async def consume(self, adapter: BaseStreamAdapter) -> StreamResult:
        """Consume all events from an adapter, dispatching reactively to bound UI primitives."""
        start_time = time.monotonic()

        if self.composer is not None:
            self.composer.set_running(True)
        if self.message is not None:
            self.message.set_generating(True)

        try:
            async for event in adapter:
                self._dispatch_event(event)
                if self.on_event is not None:
                    self.on_event(event)

        except Exception as exc:
            if self.message is not None:
                self.message.append_text(f"\n\n**Error**: {exc}")
            raise

        finally:
            duration_ms = int((time.monotonic() - start_time) * 1000)

            if self.message is not None:
                self.message.set_generating(False)
            if self.composer is not None:
                self.composer.set_running(False)

        return StreamResult(
            text=adapter.text,
            thought=adapter.thought,
            tool_calls=adapter.tool_calls,
            tool_results=adapter.tool_results,
            usage=adapter.usage,
            finish_reason=adapter.finish_reason or "completed",
            error=str(adapter.error) if adapter.error else None,
            events=adapter.events,
            duration_ms=duration_ms,
        )

    def _dispatch_event(self, event: AgUiEvent) -> None:
        """Dispatch a single AG-UI event to the appropriate bound UI component."""
        match event.type:
            # 1. Lifecycle
            case AgUiEventType.RUN_STARTED:
                if self.composer is not None:
                    self.composer.set_running(True)
                if self.message is not None:
                    self.message.set_generating(True)

            case AgUiEventType.RUN_FINISHED:
                if self.message is not None:
                    self.message.set_generating(False)
                if self.composer is not None:
                    self.composer.set_running(False)

            case AgUiEventType.RUN_ERROR:
                if self.message is not None:
                    self.message.set_generating(False)
                    err_msg = event.error or event.code or "Execution failed"
                    self.message.append_text(f"\n\n**Stream Error**: {err_msg}")
                if self.composer is not None:
                    self.composer.set_running(False)

            # 2. Text Message
            case AgUiEventType.TEXT_MESSAGE_CONTENT | AgUiEventType.TEXT_MESSAGE_CHUNK:
                if event.content and self.message is not None:
                    self.message.append_text(event.content)

            # 3. Reasoning / Chain-of-thought
            case AgUiEventType.REASONING_START | AgUiEventType.REASONING_MESSAGE_START:
                if self.message is not None and self._reasoning_card is None:
                    self._reasoning_card = self.message.add_reasoning("")

            case (
                AgUiEventType.REASONING_MESSAGE_CONTENT
                | AgUiEventType.REASONING_MESSAGE_CHUNK
            ):
                if event.content and self.message is not None:
                    if self._reasoning_card is None:
                        self._reasoning_card = self.message.add_reasoning("")
                    self._reasoning_card.append_thought(
                        event.content, step_count=self._step_counter
                    )

            case AgUiEventType.REASONING_END | AgUiEventType.REASONING_MESSAGE_END:
                self._step_counter += 1

            # 4. Tool Calls
            case AgUiEventType.TOOL_CALL_START:
                if self.message is not None and event.tool_call_id:
                    tool = ToolCall(
                        id=event.tool_call_id,
                        name=event.tool_name or "tool",
                        args=event.args if isinstance(event.args, dict) else {},
                        status=ToolStatus.EXECUTING,
                    )
                    card = self.message.add_tool_call(tool)
                    self._tool_cards[event.tool_call_id] = card

            case AgUiEventType.TOOL_CALL_ARGS:
                if event.tool_call_id and event.tool_call_id in self._tool_cards:
                    card = self._tool_cards[event.tool_call_id]
                    if isinstance(event.args, dict):
                        card.update_args(event.args)

            case AgUiEventType.TOOL_CALL_END:
                if event.tool_call_id and event.tool_call_id in self._tool_cards:
                    card = self._tool_cards[event.tool_call_id]
                    if isinstance(event.args, dict):
                        card.set_args(event.args)

            case AgUiEventType.TOOL_CALL_RESULT:
                if event.tool_call_id and event.tool_call_id in self._tool_cards:
                    card = self._tool_cards[event.tool_call_id]
                    if event.is_error:
                        card.fail(str(event.result or "Tool execution failed"))
                    else:
                        card.resolve(event.result or "Success")

            # 5. Background Activity / Tasks
            case AgUiEventType.ACTIVITY_SNAPSHOT | AgUiEventType.ACTIVITY_DELTA:
                if self.task_tray is not None and event.activity_id:
                    task_text = (
                        event.delta.get("text", "Processing...")
                        if isinstance(event.delta, dict)
                        else "Running background task..."
                    )
                    if event.activity_id not in self._active_tasks:
                        handle = self.task_tray.add_task(task_text)
                        self._active_tasks[event.activity_id] = handle
                    else:
                        self._active_tasks[event.activity_id].update_text(task_text)

            # 6. State / Usage metrics
            case AgUiEventType.STATE_DELTA:
                if isinstance(event.delta, dict) and "usage" in event.delta:
                    usage = event.delta["usage"]
                    total_tokens = usage.get("total_tokens", 0)
                    if total_tokens > 0:
                        if self.message is not None:
                            self.message.set_tokens(total_tokens)
                        if self.header is not None:
                            self.header.update_tokens(total_tokens)
