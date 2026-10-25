"""AG-UI native stream adapter supporting all AG-UI protocol events."""

import json
from collections.abc import AsyncIterable, AsyncIterator
from typing import Any

from nicegui_ai.adapters.base import BaseStreamAdapter
from nicegui_ai.schema import AgUiEvent, AgUiEventType


class AgUiStreamAdapter(BaseStreamAdapter):
    """Adapter for native AG-UI streaming protocol sources."""

    def __init__(self, source: AsyncIterable[AgUiEvent | dict[str, Any] | str]) -> None:
        super().__init__(source)

    async def stream_events(self) -> AsyncIterator[AgUiEvent]:
        """Yield AG-UI events directly or parse from dict / JSON representation."""
        async for raw_item in self.source:
            event = self._normalize_item(raw_item)
            if event is not None:
                yield event

    def _normalize_item(self, item: Any) -> AgUiEvent | None:
        if isinstance(item, AgUiEvent):
            return item

        if isinstance(item, str):
            item_str = item.strip()
            if item_str.startswith("data:"):
                item_str = item_str[5:].strip()
            if not item_str:
                return None
            try:
                item = json.loads(item_str)
            except Exception:
                # Text fallback chunk
                return AgUiEvent(
                    type=AgUiEventType.TEXT_MESSAGE_CONTENT,
                    content=item,
                    raw_event=item,
                )

        if isinstance(item, dict):
            # Parse type
            type_val = item.get("type", "TEXT_MESSAGE_CONTENT")
            try:
                event_type = AgUiEventType(type_val)
            except ValueError:
                event_type = AgUiEventType.CUSTOM

            return AgUiEvent(
                type=event_type,
                timestamp=item.get("timestamp"),
                raw_event=item.get("rawEvent") or item,
                metadata=item.get("metadata", {}),
                subagent_run_id=item.get("subagentRunId"),
                run_id=item.get("runId"),
                step_id=item.get("stepId"),
                step_name=item.get("stepName"),
                message_id=item.get("messageId"),
                role=item.get("role"),
                content=item.get("content") or item.get("text"),
                tool_call_id=item.get("toolCallId") or item.get("id"),
                tool_name=item.get("toolName") or item.get("name"),
                args=item.get("args") or item.get("arguments"),
                result=item.get("result"),
                is_error=bool(item.get("isError")),
                error=item.get("error"),
                code=item.get("code"),
                snapshot=item.get("snapshot"),
                delta=item.get("delta"),
                activity_id=item.get("activityId"),
                custom_type=item.get("customType", type_val),
            )

        return None
