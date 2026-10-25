"""Google GenAI (Gemini) streaming protocol adapter mapping 100% of provider events to AG-UI."""

import uuid
from collections.abc import AsyncIterable, AsyncIterator
from typing import Any

from nicegui_ai.adapters.base import BaseStreamAdapter
from nicegui_ai.schema import AgUiEvent, AgUiEventType


class GeminiStreamAdapter(BaseStreamAdapter):
    """Adapter for Google GenAI SDK (client.aio.models.generate_content_stream)."""

    def __init__(self, source: AsyncIterable[Any]) -> None:
        super().__init__(source)
        self._text_started: bool = False
        self._reasoning_started: bool = False
        self._model_version: str | None = None
        self._run_id: str = f"gemini-{uuid.uuid4().hex[:8]}"

    async def stream_events(self) -> AsyncIterator[AgUiEvent]:
        """Convert Google GenAI stream chunks into complete AG-UI events."""
        yield AgUiEvent(
            type=AgUiEventType.RUN_STARTED,
            run_id=self._run_id,
            metadata={"source": "gemini"},
        )

        async for chunk in self.source:
            for event in self._process_chunk(chunk):
                yield event

        # Close any active streams
        if self._reasoning_started:
            yield AgUiEvent(
                type=AgUiEventType.REASONING_END,
                run_id=self._run_id,
            )
            self._reasoning_started = False

        if self._text_started:
            yield AgUiEvent(
                type=AgUiEventType.TEXT_MESSAGE_END,
                run_id=self._run_id,
            )
            self._text_started = False

        yield AgUiEvent(
            type=AgUiEventType.RUN_FINISHED,
            run_id=self._run_id,
            metadata={
                "finish_reason": self.finish_reason or "STOP",
                "model_version": self._model_version,
                "usage": self.usage,
            },
        )

    def _process_chunk(self, chunk: Any) -> list[AgUiEvent]:
        events: list[AgUiEvent] = []

        model_version = getattr(chunk, "model_version", None) or (
            chunk.get("model_version") if isinstance(chunk, dict) else None
        )
        if model_version:
            self._model_version = str(model_version)

        # 1. Usage metadata
        usage = getattr(chunk, "usage_metadata", None) or (
            chunk.get("usage_metadata") if isinstance(chunk, dict) else None
        )
        if usage:
            prompt_tokens = getattr(usage, "prompt_token_count", 0) or (
                usage.get("prompt_token_count", 0) if isinstance(usage, dict) else 0
            )
            candidates_tokens = getattr(usage, "candidates_token_count", 0) or (
                usage.get("candidates_token_count", 0) if isinstance(usage, dict) else 0
            )
            total_tokens = getattr(usage, "total_token_count", 0) or (
                usage.get("total_token_count", 0) if isinstance(usage, dict) else 0
            )
            cached_tokens = getattr(usage, "cached_content_token_count", 0) or (
                usage.get("cached_content_token_count", 0)
                if isinstance(usage, dict)
                else 0
            )

            self.usage.update(
                {
                    "prompt_tokens": int(prompt_tokens or 0),
                    "completion_tokens": int(candidates_tokens or 0),
                    "total_tokens": int(total_tokens or 0),
                    "cached_tokens": int(cached_tokens or 0),
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

        # 2. Candidates
        candidates = getattr(chunk, "candidates", None) or (
            chunk.get("candidates") if isinstance(chunk, dict) else []
        )
        if not candidates:
            # Fallback for direct text chunks
            direct_text = getattr(chunk, "text", None)
            if direct_text:
                if not self._text_started:
                    self._text_started = True
                    events.append(
                        AgUiEvent(
                            type=AgUiEventType.TEXT_MESSAGE_START,
                            role="model",
                            run_id=self._run_id,
                        )
                    )
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.TEXT_MESSAGE_CONTENT,
                        content=str(direct_text),
                        raw_event=chunk,
                    )
                )
            return events

        for cand in candidates:
            finish_reason = getattr(cand, "finish_reason", None) or (
                cand.get("finish_reason") if isinstance(cand, dict) else None
            )
            if finish_reason:
                self.finish_reason = str(finish_reason)

            # Safety ratings
            safety_ratings = getattr(cand, "safety_ratings", None) or (
                cand.get("safety_ratings") if isinstance(cand, dict) else None
            )
            if safety_ratings:
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.CUSTOM,
                        custom_type="safety_ratings",
                        snapshot=safety_ratings,
                        raw_event=safety_ratings,
                    )
                )

            # Grounding metadata (Google Search citations and queries)
            grounding = getattr(cand, "grounding_metadata", None) or (
                cand.get("grounding_metadata") if isinstance(cand, dict) else None
            )
            if grounding:
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.CUSTOM,
                        custom_type="grounding_metadata",
                        snapshot=grounding,
                        raw_event=grounding,
                    )
                )

            # Citation metadata
            citations = getattr(cand, "citation_metadata", None) or (
                cand.get("citation_metadata") if isinstance(cand, dict) else None
            )
            if citations:
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.CUSTOM,
                        custom_type="citation_metadata",
                        snapshot=citations,
                        raw_event=citations,
                    )
                )

            # Content parts
            content = getattr(cand, "content", None) or (
                cand.get("content") if isinstance(cand, dict) else None
            )
            if not content:
                continue

            raw_parts = getattr(content, "parts", None) or (
                content.get("parts") if isinstance(content, dict) else None
            )
            parts = raw_parts if isinstance(raw_parts, list) else []
            for part in parts:
                events.extend(self._process_part(part))

        return events

    def _process_part(self, part: Any) -> list[AgUiEvent]:
        events: list[AgUiEvent] = []

        # Check if thought / reasoning block
        is_thought = getattr(part, "thought", False) or (
            part.get("thought", False) if isinstance(part, dict) else False
        )
        text = getattr(part, "text", None) or (
            part.get("text") if isinstance(part, dict) else None
        )

        if is_thought and text:
            if not self._reasoning_started:
                self._reasoning_started = True
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.REASONING_START,
                        run_id=self._run_id,
                    )
                )
            events.append(
                AgUiEvent(
                    type=AgUiEventType.REASONING_MESSAGE_CONTENT,
                    content=str(text),
                    run_id=self._run_id,
                    raw_event=part,
                )
            )
            return events

        # Standard text part
        if text:
            if self._reasoning_started:
                self._reasoning_started = False
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.REASONING_END,
                        run_id=self._run_id,
                    )
                )

            if not self._text_started:
                self._text_started = True
                events.append(
                    AgUiEvent(
                        type=AgUiEventType.TEXT_MESSAGE_START,
                        role="model",
                        run_id=self._run_id,
                    )
                )

            events.append(
                AgUiEvent(
                    type=AgUiEventType.TEXT_MESSAGE_CONTENT,
                    content=str(text),
                    run_id=self._run_id,
                    raw_event=part,
                )
            )

        # Function / Tool Call
        fn_call = getattr(part, "function_call", None) or (
            part.get("function_call") if isinstance(part, dict) else None
        )
        if fn_call:
            fn_name = getattr(fn_call, "name", "") or (
                fn_call.get("name", "") if isinstance(fn_call, dict) else ""
            )
            fn_args = getattr(fn_call, "args", {}) or (
                fn_call.get("args", {}) if isinstance(fn_call, dict) else {}
            )
            call_id = (
                getattr(fn_call, "id", None)
                or (fn_call.get("id") if isinstance(fn_call, dict) else None)
                or f"gemini-fn-{uuid.uuid4().hex[:6]}"
            )

            # Convert map/protobuf struct to dict if needed
            args_dict = (
                dict(fn_args)
                if isinstance(fn_args, dict)
                else (getattr(fn_args, "__dict__", {}) if fn_args else {})
            )

            events.append(
                AgUiEvent(
                    type=AgUiEventType.TOOL_CALL_START,
                    tool_call_id=call_id,
                    tool_name=str(fn_name),
                    args=args_dict,
                    raw_event=fn_call,
                )
            )
            events.append(
                AgUiEvent(
                    type=AgUiEventType.TOOL_CALL_ARGS,
                    tool_call_id=call_id,
                    tool_name=str(fn_name),
                    args=args_dict,
                    raw_event=fn_call,
                )
            )
            events.append(
                AgUiEvent(
                    type=AgUiEventType.TOOL_CALL_END,
                    tool_call_id=call_id,
                    tool_name=str(fn_name),
                    args=args_dict,
                    raw_event=fn_call,
                )
            )

        # Function Response (Tool Execution Result)
        fn_resp = getattr(part, "function_response", None) or (
            part.get("function_response") if isinstance(part, dict) else None
        )
        if fn_resp:
            resp_name = getattr(fn_resp, "name", "") or (
                fn_resp.get("name", "") if isinstance(fn_resp, dict) else ""
            )
            resp_val = getattr(fn_resp, "response", None) or (
                fn_resp.get("response") if isinstance(fn_resp, dict) else None
            )
            call_id = (
                getattr(fn_resp, "id", None)
                or (fn_resp.get("id") if isinstance(fn_resp, dict) else None)
                or f"gemini-fn-{resp_name}"
            )

            events.append(
                AgUiEvent(
                    type=AgUiEventType.TOOL_CALL_RESULT,
                    tool_call_id=call_id,
                    tool_name=str(resp_name),
                    result=resp_val,
                    raw_event=fn_resp,
                )
            )

        # Executable Code (Code Execution Tool Invocation)
        exec_code = getattr(part, "executable_code", None) or (
            part.get("executable_code") if isinstance(part, dict) else None
        )
        if exec_code:
            lang = getattr(exec_code, "language", "python")
            code = getattr(exec_code, "code", "")
            events.append(
                AgUiEvent(
                    type=AgUiEventType.CUSTOM,
                    custom_type="code_execution_call",
                    snapshot={"language": lang, "code": code},
                    raw_event=exec_code,
                )
            )

        # Code Execution Result
        code_result = getattr(part, "code_execution_result", None) or (
            part.get("code_execution_result") if isinstance(part, dict) else None
        )
        if code_result:
            outcome = getattr(code_result, "outcome", "")
            output = getattr(code_result, "output", "")
            events.append(
                AgUiEvent(
                    type=AgUiEventType.CUSTOM,
                    custom_type="code_execution_result",
                    snapshot={"outcome": outcome, "output": output},
                    raw_event=code_result,
                )
            )

        return events
