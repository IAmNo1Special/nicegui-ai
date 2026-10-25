"""Advanced tool calling and reasoning example using nicegui-ai."""

import asyncio

from nicegui import ui

from nicegui_ai import (
    AiComposer,
    AiThread,
    ApprovalModal,
    ToolCall,
    ToolStatus,
    setup_ai_theme,
)


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

                # 1. Attach ReasoningCard (amber chain of thought)
                agent_msg.add_reasoning(
                    title="Analyzing infrastructure requirements",
                    steps=[
                        "Validating database connection pool...",
                        "Checking cluster load and memory pressure...",
                        "Determining appropriate schema migration strategy.",
                    ],
                    duration_ms=450,
                    default_open=True,
                )
                await asyncio.sleep(0.5)

                # 2. Attach ToolCallCard (cyan tool execution)
                tool = agent_msg.add_tool_call(
                    name="inspect_schema",
                    args={"target": "users_v2", "read_only": True},
                    summary="Inspecting active table schema",
                    status=ToolStatus.EXECUTING,
                    default_open=True,
                )
                await asyncio.sleep(0.8)

                # Mark tool as resolved with output
                tool.set_status(ToolStatus.SUCCESS)
                tool.set_result(
                    {"columns": ["id", "email", "created_at"], "rows": 1420}
                )

                # Stream response
                agent_msg.append_text(
                    "Schema inspection completed successfully. No locks detected on `users_v2`.\n\n"
                    "Click the button below to test the Human-in-the-Loop Security Gate."
                )
                agent_msg.set_generating(False)
                composer.set_running(False)

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
