"""Abstract base class for all AG-UI streaming adapters adhering 100% to OOP principles."""

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any

from nicegui_ai.schema import AgUiEvent, AgUiEventType, ToolCall, ToolStatus


class BaseStreamAdapter(ABC):
    """Abstract object-oriented stream adapter converting provider streams into AG-UI events."""

    def __init__(self, source: Any) -> None:
        self.source = source
        self.text: str = ""
        self.thought: str = ""
        self.tool_calls: list[ToolCall] = []
        self._tool_calls_by_id: dict[str, ToolCall] = {}
        self.tool_results: dict[str, Any] = {}
        self.usage: dict[str, int] = {}
        self.finish_reason: str | None = None
        self.error: Any | None = None
        self.metadata: dict[str, Any] = {}
        self.events: list[AgUiEvent] = []

    @abstractmethod
    def stream_events(self) -> AsyncIterator[AgUiEvent]:
        """Asynchronously yield standardized AG-UI events from the underlying stream."""
        ...

    async def __aiter__(self) -> AsyncIterator[AgUiEvent]:
        """Asynchronously iterate over AG-UI events, tracking state accumulation."""
        async for event in self.stream_events():
            self._accumulate_state(event)
            self.events.append(event)
            yield event

    def _accumulate_state(self, event: AgUiEvent) -> None:
        """Update internal state snapshot from event properties."""
        if event.metadata:
            self.metadata.update(event.metadata)
            if "usage" in event.metadata and isinstance(event.metadata["usage"], dict):
                self.usage.update(event.metadata["usage"])

        match event.type:
            case AgUiEventType.TEXT_MESSAGE_CONTENT | AgUiEventType.TEXT_MESSAGE_CHUNK:
                if event.content:
                    self.text += event.content

            case (
                AgUiEventType.REASONING_MESSAGE_CONTENT
                | AgUiEventType.REASONING_MESSAGE_CHUNK
            ):
                if event.content:
                    self.thought += event.content

            case AgUiEventType.TOOL_CALL_START:
                if event.tool_call_id:
                    tool = ToolCall(
                        id=event.tool_call_id,
                        name=event.tool_name or "",
                        args=event.args if isinstance(event.args, dict) else {},
                        status=ToolStatus.EXECUTING,
                    )
                    self._tool_calls_by_id[event.tool_call_id] = tool
                    if tool not in self.tool_calls:
                        self.tool_calls.append(tool)

            case AgUiEventType.TOOL_CALL_ARGS:
                if event.tool_call_id and event.tool_call_id in self._tool_calls_by_id:
                    tool = self._tool_calls_by_id[event.tool_call_id]
                    if isinstance(event.args, dict):
                        tool.args.update(event.args)

            case AgUiEventType.TOOL_CALL_END:
                if event.tool_call_id and event.tool_call_id in self._tool_calls_by_id:
                    tool = self._tool_calls_by_id[event.tool_call_id]
                    if isinstance(event.args, dict):
                        tool.args = event.args

            case AgUiEventType.TOOL_CALL_RESULT:
                if event.tool_call_id:
                    self.tool_results[event.tool_call_id] = event.result
                    if event.tool_call_id in self._tool_calls_by_id:
                        tool = self._tool_calls_by_id[event.tool_call_id]
                        tool.result = event.result
                        tool.status = (
                            ToolStatus.FAILED if event.is_error else ToolStatus.RESOLVED
                        )

            case AgUiEventType.RUN_FINISHED:
                if "finish_reason" in event.metadata:
                    self.finish_reason = str(event.metadata["finish_reason"])

            case AgUiEventType.RUN_ERROR:
                self.error = event.error or event.code or "Execution failed"

    async def collect(self) -> list[AgUiEvent]:
        """Consume and collect all events into an in-memory list."""
        collected: list[AgUiEvent] = []
        async for event in self:
            collected.append(event)
        return collected
