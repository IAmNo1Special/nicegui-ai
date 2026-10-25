"""OpenRouter and OpenAI streaming protocol adapter mapping 100% of provider events to AG-UI."""

import json
from collections.abc import AsyncIterable, AsyncIterator
from typing import Any

from nicegui_ai.adapters.base import BaseStreamAdapter
from nicegui_ai.schema import AgUiEvent, AgUiEventType


class OpenRouterStreamAdapter(BaseStreamAdapter):
    """Adapter for OpenRouter and OpenAI-compatible streaming chunks with reasoning and tools."""

    def __init__(self, source: AsyncIterable[Any]) -> None:
        super().__init__(source)
        self._text_started: bool = False
        self._reasoning_started: bool = False
        self._active_tools: dict[int, dict[str, Any]] = {}
        self._message_id: str | None = None
        self._model: str | None = None

    async def stream_events(self) -> AsyncIterator[AgUiEvent]:
        """Convert OpenRouter / OpenAI SSE stream chunks into complete AG-UI events."""
        yield AgUiEvent(
            type=AgUiEventType.RUN_STARTED, metadata={"source": "openrouter"}
        )

        async for chunk in self.source:
            for event in self._process_chunk(chunk):
                yield event

        # Close any lingering open streams
        if self._reasoning_started:
            yield AgUiEvent(
                type=AgUiEventType.REASONING_END,
                message_id=self._message_id,
            )
            self._reasoning_started = False

        if self._text_started:
            yield AgUiEvent(
                type=AgUiEventType.TEXT_MESSAGE_END,
                message_id=self._message_id,
            )
            self._text_started = False

        for tool_info in self._active_tools.values():
            parsed_args = self._try_parse_json(tool_info["args_buffer"])
            yield AgUiEvent(
                type=AgUiEventType.TOOL_CALL_END,
                tool_call_id=tool_info["id"],
                tool_name=tool_info["name"],
                args=parsed_args,
            )

        yield AgUiEvent(
            type=AgUiEventType.RUN_FINISHED,
            metadata={
                "finish_reason": self.finish_reason or "stop",
                "model": self._model,
                "usage": self.usage,
            },
        )

    def _process_chunk(self, chunk: Any) -> list[AgUiEvent]:
        events: list[AgUiEvent] = []

        # Extract top-level chunk attributes
        chunk_id = getattr(chunk, "id", None) or (
            chunk.get("id") if isinstance(chunk, dict) else None
        )
        if chunk_id:
            self._message_id = str(chunk_id)

        model = getattr(chunk, "model", None) or (
            chunk.get("model") if isinstance(chunk, dict) else None
        )
        if model:
            self._model = str(model)

        # Check for top-level usage (OpenRouter / OpenAI stream_options={"include_usage": true})
        usage = getattr(chunk, "usage", None) or (
            chunk.get("usage") if isinstance(chunk, dict) else None
        )
        if usage:
            usage_dict = (
                usage.model_dump()
                if hasattr(usage, "model_dump")
                else (dict(usage) if isinstance(usage, dict) else {})
            )
            self.usage.update(
                {
                    "prompt_tokens": usage_dict.get("prompt_tokens", 0),
                    "completion_tokens": usage_dict.get("completion_tokens", 0),
                    "total_tokens": usage_dict.get("total_tokens", 0),
                    "reasoning_tokens": (
                        usage_dict.get("completion_tokens_details", {}).get(
                            "reasoning_tokens", 0
                        )
                        if isinstance(usage_dict.get("completion_tokens_details"), dict)
                        else 0
                    ),
                }
            )
            events.append(
                AgUiEvent(
                    type=AgUiEventType.STATE_DELTA,
                    delta={"usage": self.usage},
                    metadata={"usage": self.usage},
                    raw_event=usage,
                )
            )

        # Check for stream errors
        error = getattr(chunk, "error", None) or (
            chunk.get("error") if isinstance(chunk, dict) else None
        )
        if error:
            err_msg = str(error)
            events.append(
                AgUiEvent(
                    type=AgUiEventType.RUN_ERROR,
                    error=err_msg,
                    raw_event=chunk,
                )
            )
            return events

        # Inspect choices
        choices = getattr(chunk, "choices", None) or (
            chunk.get("choices") if isinstance(chunk, dict) else []
        )
        if not choices:
            return events

        choice = choices[0]
        delta = getattr(choice, "delta", None) or (
            choice.get("delta") if isinstance(choice, dict) else None
        )
        finish_reason = getattr(choice, "finish_reason", None) or (
            choice.get("finish_reason") if isinstance(choice, dict) else None
        )
        if finish_reason:
            self.finish_reason = str(finish_reason)

        if delta is None:
            return events

        # 1. Reasoning / Thinking delta (OpenRouter 'reasoning' or DeepSeek 'reasoning_content')
        thought = (
            getattr(delta, "reasoning", None)
            or getattr(delta, "reasoning_content", None)
            or (delta.get("reasoning") if isinstance(delta, dict) else None)
            or (delta.get("reasoning_content") if isinstance(delta, dict) else None)
        )
        if thought:
            if not self._reasoning_started:
                self._reasoning_started = True
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.REASONING_START,
                        message_id=self._message_id,
                    )
                )
            events.append(
                AgUiEvent(
                    type=AgUiEventType.REASONING_MESSAGE_CONTENT,
                    message_id=self._message_id,
                    content=str(thought),
                    raw_event=chunk,
                )
            )

        # 2. Text Content delta
        content = getattr(delta, "content", None) or (
            delta.get("content") if isinstance(delta, dict) else None
        )
        if content:
            # If transitioning from reasoning to content, close reasoning
            if self._reasoning_started:
                self._reasoning_started = False
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.REASONING_END,
                        message_id=self._message_id,
                    )
                )

            if not self._text_started:
                self._text_started = True
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.TEXT_MESSAGE_START,
                        message_id=self._message_id,
                        role="assistant",
                    )
                )

            events.append(
                AgUiEvent(
                    type=AgUiEventType.TEXT_MESSAGE_CONTENT,
                    message_id=self._message_id,
                    content=str(content),
                    raw_event=chunk,
                )
            )

        # 3. Model Refusal
        refusal = getattr(delta, "refusal", None) or (
            delta.get("refusal") if isinstance(delta, dict) else None
        )
        if refusal:
            events.append(
                AgUiEvent(
                    type=AgUiEventType.CUSTOM,
                    custom_type="refusal",
                    content=str(refusal),
                    raw_event=chunk,
                )
            )

        # 4. Tool calls
        tool_calls = getattr(delta, "tool_calls", None) or (
            delta.get("tool_calls") if isinstance(delta, dict) else None
        )
        if tool_calls:
            for tc in tool_calls:
                idx = getattr(tc, "index", 0) or (
                    tc.get("index", 0) if isinstance(tc, dict) else 0
                )
                tc_id = getattr(tc, "id", None) or (
                    tc.get("id") if isinstance(tc, dict) else None
                )
                fn = getattr(tc, "function", None) or (
                    tc.get("function") if isinstance(tc, dict) else None
                )
                fn_name = getattr(fn, "name", None) or (
                    fn.get("name") if isinstance(fn, dict) else None
                )
                fn_args = getattr(fn, "arguments", None) or (
                    fn.get("arguments") if isinstance(fn, dict) else None
                )

                if idx not in self._active_tools:
                    self._active_tools[idx] = {
                        "id": str(tc_id or f"tool-{idx}"),
                        "name": str(fn_name or ""),
                        "args_buffer": "",
                    }
                    events.append(
                        AgUiEvent(
                            type=AgUiEventType.TOOL_CALL_START,
                            tool_call_id=self._active_tools[idx]["id"],
                            tool_name=self._active_tools[idx]["name"],
                            raw_event=tc,
                        )
                    )
                else:
                    if tc_id and not self._active_tools[idx]["id"]:
                        self._active_tools[idx]["id"] = str(tc_id)
                    if fn_name and not self._active_tools[idx]["name"]:
                        self._active_tools[idx]["name"] = str(fn_name)

                if fn_args:
                    self._active_tools[idx]["args_buffer"] += str(fn_args)
                    events.append(
                        AgUiEvent(
                            type=AgUiEventType.TOOL_CALL_ARGS,
                            tool_call_id=self._active_tools[idx]["id"],
                            tool_name=self._active_tools[idx]["name"],
                            args=str(fn_args),
                            raw_event=tc,
                        )
                    )

        # 5. Logprobs
        logprobs = getattr(choice, "logprobs", None) or (
            choice.get("logprobs") if isinstance(choice, dict) else None
        )
        if logprobs:
            events.append(
                AgUiEvent(
                    type=AgUiEventType.RAW,
                    raw_event=logprobs,
                    metadata={"logprobs": logprobs},
                )
            )

        return events

    @staticmethod
    def _try_parse_json(val: str) -> dict[str, Any] | str:
        if not val.strip():
            return {}
        try:
            return json.loads(val)
        except Exception:
            return val
