"""Advanced tool calling and reasoning example using nicegui-ai and OpenRouter stream adapter."""

import asyncio
from collections.abc import AsyncIterator
from typing import Any

from nicegui import ui

from nicegui_ai import (
    AiComposer,
    AiThread,
    ApprovalModal,
    OpenRouterStreamAdapter,
    StreamBridge,
    ToolCall,
    setup_ai_theme,
)


async def mock_ops_stream(prompt: str) -> AsyncIterator[dict[str, Any]]:
    """Yield simulated OpenRouter/OpenAI chunks with reasoning, tool call, and answer."""
    # 1. Deliberation reasoning chunks
    thoughts = [
        "Analyzing infrastructure state against query...\n",
        "Validating database connection pool and replica lag...\n",
        "Checking cluster load and selecting inspect_schema tool.\n",
    ]
    for thought in thoughts:
        yield {
            "choices": [
                {
                    "delta": {"reasoning": thought},
                    "finish_reason": None,
                }
            ]
        }
        await asyncio.sleep(0.2)

    # 2. Tool call initiation & JSON args chunking
    yield {
        "choices": [
            {
                "delta": {
                    "tool_calls": [
                        {
                            "index": 0,
                            "id": "call_schema_01",
                            "function": {
                                "name": "inspect_schema",
                                "arguments": '{"target": "users_v2", ',
                            },
                        }
                    ]
                }
            }
        ]
    }
    await asyncio.sleep(0.15)
    yield {
        "choices": [
            {
                "delta": {
                    "tool_calls": [
                        {
                            "index": 0,
                            "function": {
                                "arguments": '"read_only": true}',
                            },
                        }
                    ]
                }
            }
        ]
    }
    await asyncio.sleep(0.3)

    # 3. Text completion chunks
    text_chunks = [
        "Schema inspection for `users_v2` completed with 0 locks detected.\n\n",
        "The turn was consumed through `OpenRouterStreamAdapter`:\n\n",
        "```python:ops_turn.py\n",
        "adapter = OpenRouterStreamAdapter(openrouter_stream)\n",
        "bridge = StreamBridge(message=agent_msg)\n",
        "await bridge.consume(adapter)\n",
        "```\n\n",
        "Click the button below to test the Human-in-the-Loop Security Gate.",
    ]
    for chunk in text_chunks:
        yield {
            "choices": [
                {
                    "delta": {"content": chunk},
                    "finish_reason": None,
                }
            ]
        }
        await asyncio.sleep(0.12)

    yield {
        "choices": [{"delta": {}, "finish_reason": "stop"}],
        "usage": {
            "prompt_tokens": 150,
            "completion_tokens": 280,
            "total_tokens": 430,
        },
    }


@ui.page("/")
def main_page() -> None:
    setup_ai_theme()

    # Human-in-the-loop approval gate modal
    approval_modal = ApprovalModal(
        title="Execute Database Query",
        tool_call=ToolCall(
            id="call-db-1",
            name="run_sql_query",
            args={"sql": "DROP TABLE legacy_cache;", "confirm": True},
            summary="Drop legacy cache table",
        ),
        danger_level="critical",
        on_approve=lambda: ui.notify("Query approved by operator", type="positive"),
        on_veto=lambda: ui.notify("Query vetoed by operator", type="negative"),
    )

    with ui.element("main").classes(
        "flex flex-col items-center justify-center p-4 w-full h-screen bg-[#0d1017] overflow-hidden"
    ):
        with ui.element("div").classes(
            "w-full max-w-3xl h-full flex flex-col bg-[#11151f]/60 backdrop-blur "
            "border border-gray-800/60 rounded-2xl shadow-2xl overflow-hidden min-h-0"
        ):
            thread = AiThread(
                suggestions=[
                    "Run system diagnostic",
                    "Query user statistics",
                ],
                on_select_suggestion=lambda text: asyncio.create_task(run_turn(text)),
            )

            async def run_turn(text: str) -> None:
                thread.add_user_message(text)
                composer.set_running(True)

                agent_msg = thread.add_agent_message(
                    agent_name="ops-agent",
                    initial_text="",
                    is_generating=True,
                )

                # Consume through OpenRouter stream adapter
                adapter = OpenRouterStreamAdapter(mock_ops_stream(text))
                bridge = StreamBridge(message=agent_msg, composer=composer)
                result = await bridge.consume(adapter)

                # Resolve simulated tool call with output
                for tc in result.tool_calls:
                    if tc.id in bridge._tool_cards:
                        card = bridge._tool_cards[tc.id]
                        card.resolve(
                            {"columns": ["id", "email", "created_at"], "rows": 1420},
                            duration_ms=62,
                        )

                # Action button to trigger security gate modal
                with (
                    ui.element("button")
                    .classes(
                        "mt-3 px-3 py-1.5 rounded-lg border border-red-500/40 bg-red-950/40 hover:bg-red-900/60 "
                        "text-red-300 font-sans text-xs flex items-center gap-2 cursor-pointer transition-colors"
                    )
                    .on("click", approval_modal.open)
                ):
                    ui.label("Trigger Approval Gate Modal")

            composer = AiComposer(
                placeholder="Ask ops agent...",
                on_send=lambda text: asyncio.create_task(run_turn(text)),
            )


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8080, title="nicegui-ai Tools & Reasoning")
