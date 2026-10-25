"""OpenCode coding agent execution stream adapter mapping 100% of events to AG-UI."""

import uuid
from collections.abc import AsyncIterable, AsyncIterator
from typing import Any

from nicegui_ai.adapters.base import BaseStreamAdapter
from nicegui_ai.schema import AgUiEvent, AgUiEventType


class OpenCodeStreamAdapter(BaseStreamAdapter):
    """Adapter for OpenCode and agentic coding execution streams."""

    def __init__(self, source: AsyncIterable[Any]) -> None:
        super().__init__(source)
        self._run_id: str = f"opencode-{uuid.uuid4().hex[:8]}"

    async def stream_events(self) -> AsyncIterator[AgUiEvent]:
        """Convert OpenCode agent execution chunks into standardized AG-UI events."""
        yield AgUiEvent(
            type=AgUiEventType.RUN_STARTED,
            run_id=self._run_id,
            metadata={"source": "opencode"},
        )

        async for chunk in self.source:
            for event in self._process_chunk(chunk):
                yield event

        yield AgUiEvent(
            type=AgUiEventType.RUN_FINISHED,
            run_id=self._run_id,
            metadata={"finish_reason": self.finish_reason or "completed"},
        )

    def _process_chunk(self, chunk: Any) -> list[AgUiEvent]:
        events: list[AgUiEvent] = []

        if isinstance(chunk, str):
            events.append(
                AgUiEvent(
                    type=AgUiEventType.TEXT_MESSAGE_CONTENT,
                    content=chunk,
                    run_id=self._run_id,
                    raw_event=chunk,
                )
            )
            return events

        if not isinstance(chunk, dict):
            # Object with attributes
            chunk = getattr(chunk, "__dict__", {})

        event_type = chunk.get("type", "")

        match event_type:
            # 1. Plan / Step events
            case "step_start" | "step_started":
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.STEP_STARTED,
                        step_id=chunk.get("step_id") or chunk.get("id"),
                        step_name=chunk.get("step_name")
                        or chunk.get("title")
                        or chunk.get("name"),
                        run_id=self._run_id,
                        raw_event=chunk,
                    )
                )

            case "step_finish" | "step_finished" | "step_end":
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.STEP_FINISHED,
                        step_id=chunk.get("step_id") or chunk.get("id"),
                        run_id=self._run_id,
                        raw_event=chunk,
                    )
                )

            # 2. Reasoning / Thinking
            case "thought" | "thinking" | "reasoning":
                thought_content = chunk.get("content") or chunk.get("text") or ""
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.REASONING_MESSAGE_CONTENT,
                        content=str(thought_content),
                        run_id=self._run_id,
                        raw_event=chunk,
                    )
                )

            # 3. Tool Calls / Commands
            case "tool_call" | "tool_use" | "command":
                tool_id = (
                    chunk.get("tool_call_id")
                    or chunk.get("id")
                    or f"tool-{uuid.uuid4().hex[:6]}"
                )
                tool_name = (
                    chunk.get("tool_name")
                    or chunk.get("name")
                    or chunk.get("command", "tool")
                )
                args = (
                    chunk.get("args")
                    or chunk.get("arguments")
                    or chunk.get("parameters", {})
                )

                events.append(
                    AgUiEvent(
                        type=AgUiEventType.TOOL_CALL_START,
                        tool_call_id=str(tool_id),
                        tool_name=str(tool_name),
                        args=args if isinstance(args, dict) else {"raw": str(args)},
                        run_id=self._run_id,
                        raw_event=chunk,
                    )
                )

            case "tool_result" | "command_result":
                tool_id = chunk.get("tool_call_id") or chunk.get("id")
                result_val = chunk.get("result") or chunk.get("output")
                is_err = bool(chunk.get("is_error") or chunk.get("error"))

                events.append(
                    AgUiEvent(
                        type=AgUiEventType.TOOL_CALL_RESULT,
                        tool_call_id=str(tool_id),
                        result=result_val,
                        is_error=is_err,
                        run_id=self._run_id,
                        raw_event=chunk,
                    )
                )

            # 4. File Diffs / Code Modifications
            case "diff" | "file_diff" | "patch":
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.CUSTOM,
                        custom_type="file_diff",
                        snapshot={
                            "path": chunk.get("path") or chunk.get("file"),
                            "diff": chunk.get("diff") or chunk.get("patch"),
                        },
                        run_id=self._run_id,
                        raw_event=chunk,
                    )
                )

            # 5. Background Tasks / Activities
            case "activity" | "progress" | "task":
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.ACTIVITY_DELTA,
                        activity_id=chunk.get("task_id") or chunk.get("id"),
                        delta={
                            "text": chunk.get("text")
                            or chunk.get("message")
                            or chunk.get("status"),
                            "progress": chunk.get("progress"),
                        },
                        run_id=self._run_id,
                        raw_event=chunk,
                    )
                )

            # 6. Narrative / Messages
            case "text" | "message" | "content":
                msg_content = chunk.get("content") or chunk.get("text") or ""
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.TEXT_MESSAGE_CONTENT,
                        content=str(msg_content),
                        run_id=self._run_id,
                        raw_event=chunk,
                    )
                )

            # 7. Errors
            case "error":
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.RUN_ERROR,
                        error=str(chunk.get("error") or chunk.get("message", "Error")),
                        code=str(chunk.get("code", "")),
                        run_id=self._run_id,
                        raw_event=chunk,
                    )
                )

            # Fallback
            case _:
                if "text" in chunk or "content" in chunk:
                    events.append(
                        AgUiEvent(
                            type=AgUiEventType.TEXT_MESSAGE_CONTENT,
                            content=str(chunk.get("text") or chunk.get("content")),
                            run_id=self._run_id,
                            raw_event=chunk,
                        )
                    )
                else:
                    events.append(
                        AgUiEvent(
                            type=AgUiEventType.RAW,
                            raw_event=chunk,
                            run_id=self._run_id,
                        )
                    )

        return events
