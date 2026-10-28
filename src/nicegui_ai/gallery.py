import asyncio
from collections.abc import AsyncIterator
from typing import Any

from nicegui import ui

from nicegui_ai import (
    AgentMessage,
    AiComposer,
    AiMarkdown,
    AiThread,
    ApprovalModal,
    ArtifactCard,
    ArtifactViewerDrawer,
    BranchPicker,
    FloatingHeader,
    GeminiStreamAdapter,
    LucideIcon,
    MessageBranch,
    ModelOption,
    ModelSelector,
    OpenCodeStreamAdapter,
    OpenRouterStreamAdapter,
    QueuedMessagesTray,
    ReasoningCard,
    SlideOverDrawer,
    StreamBridge,
    SuggestionPrompt,
    TaskTray,
    TokenRing,
    ToolCall,
    ToolCallCard,
    ToolStatus,
    UserMessage,
    VoicePill,
    setup_ai_theme,
)


@ui.page("/")
def gallery_page() -> None:
    setup_ai_theme()

    # Floating Header Demo
    header = FloatingHeader(
        agent_name="gallery-agent",
        model="claude-opus-5.5",
        tokens_used=42100,
        token_limit=128000,
    )

    # Slide-over Drawers for inspection
    left_drawer = SlideOverDrawer(
        title="Components Sitemap", icon="history", side="left"
    )
    right_drawer = SlideOverDrawer(
        title="Tokens & System Info", icon="sliders", side="right"
    )

    with header.left_container:
        with (
            ui.element("button")
            .classes(
                "flex items-center gap-1.5 text-xs text-gray-300 hover:text-white px-2 py-1 "
                "rounded-full hover:bg-gray-800 transition-colors cursor-pointer bg-transparent border-none"
            )
            .on("click", left_drawer.toggle)
        ):
            LucideIcon("history", size=14, classes="text-purple-400")
            ui.label("Sitemap").classes("text-xs font-medium")

    with header.right_container:
        with (
            ui.element("button")
            .classes(
                "flex items-center gap-1.5 text-xs text-gray-300 hover:text-white px-2 py-1 "
                "rounded-full hover:bg-gray-800 transition-colors cursor-pointer bg-transparent border-none"
            )
            .on("click", right_drawer.toggle)
        ):
            LucideIcon("sliders", size=14, classes="text-cyan-400")
            ui.label("Inspector").classes("text-xs font-medium")

    with left_drawer.content:
        ui.label("Component Navigation").classes("font-bold text-white text-xs mb-2")
        sections = [
            "Composer & Trays",
            "Message Bubbles",
            "Reasoning Effort",
            "Tool Executions",
            "Code & Artifacts",
            "Model & Voice Controls",
            "Approval Security Gates",
        ]
        for sec in sections:
            with ui.element("div").classes(
                "p-2 rounded-lg bg-[#141924] border border-gray-800/80 text-xs text-gray-300 "
                "hover:border-purple-500/50 cursor-pointer transition-colors"
            ):
                ui.label(sec)

    with right_drawer.content:
        ui.label("Context Window Budget").classes("font-bold text-white text-xs")
        with ui.row().classes("items-center gap-3 my-2"):
            TokenRing(used=42100, limit=128000, size=32)
            with ui.column().classes("gap-0 font-mono text-xs text-gray-400"):
                ui.label("42,100 / 128,000 used")
                ui.label("32.8% capacity").classes("text-purple-400")

    # Main gallery body
    with ui.element("main").classes(
        "w-full h-screen overflow-y-auto pt-20 pb-16 px-4 max-w-5xl mx-auto flex flex-col gap-8"
    ):
        # Section 1: Title & Overview
        with ui.column().classes("gap-1"):
            ui.label("nicegui-ai Component Gallery").classes(
                "text-xl font-bold text-white"
            )
            ui.label(
                "Comprehensive visual catalog and state verification for all 17 modern AI primitives."
            ).classes("text-xs text-gray-400")

        # Section 2: ModelSelector & VoicePill
        with ui.column().classes(
            "w-full gap-2 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("ModelSelector & VoicePill Controls").classes(
                "text-xs font-bold uppercase tracking-wider text-purple-400"
            )
            with ui.row().classes("items-center gap-4 flex-wrap"):
                ui.label("Pill Variant:").classes("text-xs text-gray-400")
                ModelSelector(
                    models=[
                        ModelOption(
                            name="Gemini 4 Argon", effort="Medium", badge="New"
                        ),
                        ModelOption(name="Gemini 3.8 Flash", effort="High"),
                        ModelOption(
                            name="Claude Opus 5.5", effort="Medium", badge="New"
                        ),
                        ModelOption(
                            name="Claude Sonnet 5.5", effort="Medium", badge="New"
                        ),
                        ModelOption(name="GPT-OSS 120B (Medium)", badge="Notice"),
                    ],
                    current_model="Gemini 3.8 Flash",
                    reasoning_effort="High",
                    variant="pill",
                    on_view_usage=lambda: ui.notify(
                        "Usage: 14,200 / 128,000 tokens", type="info"
                    ),
                )
                ui.label("Inline Variant (Cascading):").classes(
                    "text-xs text-gray-400 ml-4"
                )
                ModelSelector(
                    models=[
                        ModelOption(
                            name="Gemini 4 Argon", effort="Medium", badge="New"
                        ),
                        ModelOption(name="Gemini 3.8 Flash", effort="High"),
                        ModelOption(
                            name="Claude Opus 5.5", effort="Medium", badge="New"
                        ),
                        ModelOption(
                            name="Claude Sonnet 5.5", effort="Medium", badge="New"
                        ),
                        ModelOption(name="GPT-OSS 120B (Medium)", badge="Notice"),
                    ],
                    current_model="Gemini 3.8 Flash",
                    reasoning_effort="High",
                    variant="inline",
                    on_view_usage=lambda: ui.notify(
                        "Usage: 14,200 / 128,000 tokens", type="info"
                    ),
                )
            with ui.row().classes("items-center gap-3 mt-2 flex-wrap"):
                ui.label("VoicePill States:").classes("text-xs text-gray-400")
                VoicePill(state="idle")
                VoicePill(state="listening")
                VoicePill(state="thinking")
                VoicePill(state="speaking")

        # Section 3: QueuedMessagesTray & TaskTray
        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("QueuedMessagesTray & TaskTray").classes(
                "text-xs font-bold uppercase tracking-wider text-purple-400"
            )
            demo_queue = QueuedMessagesTray(
                on_send_now=lambda m: ui.notify(
                    f"Sending immediately: {m.text}", type="positive"
                ),
                on_edit=lambda m: ui.notify(f"Editing: {m.text}", type="info"),
                on_delete=lambda m: ui.notify(f"Deleted: {m.text}", type="warning"),
            )
            demo_queue.add_message("Analyze system architecture diff")
            demo_queue.add_message("Prepare release notes for v0.2.0")

            demo_task_tray = TaskTray()
            demo_task_tray.add_task(
                "Timer: 30s, Prompt: 30 seconds have elapsed. Let the user know the wait is complete."
            )
            demo_task_tray.add_task(
                "Crawling remote repository tree to resolve type definitions..."
            )

        # Section 4: AiComposer in Action
        # Section 4: Message Bubbles (UserMessage & AgentMessage)
        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("Message Bubbles & Thread").classes(
                "text-xs font-bold uppercase tracking-wider text-purple-400"
            )
            UserMessage(
                text="Can you optimize our database schema?",
                user_name="Operator",
                current_branch=1,
                total_branches=2,
            )
            demo_agent = AgentMessage(
                agent_name="OpsAgent",
                text="Here is the execution plan with zero breaking changes:\n\n```sql:schema.sql\nALTER TABLE users ADD INDEX (tenant_id, email);\n```",
                tokens_used=180,
            )
            demo_agent.add_tool_call(
                name="validate_indexes",
                args={"table": "users", "fields": ["email", "tenant_id"]},
                summary="Inspect compound indexes",
                status=ToolStatus.RESOLVED,
            )

            with ui.column().classes(
                "w-full border border-gray-800 rounded-xl p-3 bg-[#0a0d14] mt-2"
            ):
                ui.label("AiThread Empty State with Suggestions:").classes(
                    "text-[11px] text-gray-400 mb-1"
                )
                with ui.element("div").classes(
                    "h-[220px] w-full overflow-hidden flex flex-col"
                ):
                    AiThread(
                        welcome_title="Welcome to nicegui-ai",
                        welcome_subtitle="Ready to assist with coding and tools.",
                        suggestions=[
                            SuggestionPrompt(label="Run Tests", prompt="uv run pytest"),
                            SuggestionPrompt(
                                label="Check Schema", prompt="inspect table users"
                            ),
                        ],
                    )

        # Section 5: AiComposer in Action
        with ui.column().classes(
            "w-full gap-2 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("AiComposer with Unified Action Button").classes(
                "text-xs font-bold uppercase tracking-wider text-purple-400"
            )
            ui.label(
                "Includes inline model picker, full VoicePill, queued messages tray, and task tray."
            ).classes("text-[11px] text-gray-400")
            comp = AiComposer(
                placeholder="Type a message or Shift+Enter for multiline...",
                on_send=lambda text: ui.notify(f"Sent prompt: {text}", type="positive"),
                on_cancel=lambda: ui.notify("Generation canceled", type="warning"),
            )
            comp.add_task("Asynchronous indexing in background...")

        # Section 5: ToolCallCard in All Execution States
        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("ToolCallCard States").classes(
                "text-xs font-bold uppercase tracking-wider text-cyan-400"
            )
            ToolCallCard(
                ToolCall(
                    id="t-exec",
                    name="view_file",
                    args={"path": "src/core.py"},
                    status=ToolStatus.EXECUTING,
                ),
                default_open=False,
            )
            ToolCallCard(
                ToolCall(
                    id="t-res",
                    name="run_command",
                    args={"command": "uv run pytest"},
                    result="17 passed in 0.52s",
                    duration_ms=52,
                    status=ToolStatus.RESOLVED,
                ),
                default_open=True,
            )
            ToolCallCard(
                ToolCall(
                    id="t-appr",
                    name="drop_table",
                    args={"table": "legacy_users", "cascade": True},
                    status=ToolStatus.APPROVAL_REQUIRED,
                ),
                on_approve=lambda tc: ui.notify(
                    f"Approved: {tc.name}", type="positive"
                ),
                on_veto=lambda tc: ui.notify(f"Vetoed: {tc.name}", type="negative"),
                default_open=True,
            )
            ToolCallCard(
                ToolCall(
                    id="t-fail",
                    name="fetch_url",
                    args={"url": "https://invalid.example/api"},
                    result="HTTP 502 Bad Gateway: upstream server unavailable",
                    status=ToolStatus.FAILED,
                ),
                default_open=True,
            )

        # Section 6: ReasoningCard
        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("ReasoningCard (Chain-of-Thought)").classes(
                "text-xs font-bold uppercase tracking-wider text-amber-400"
            )
            ReasoningCard(
                title="Reasoning (Thinking Process)",
                steps=[
                    "Parsing abstract syntax tree for nicegui-ai primitives...",
                    "Validating Human-in-the-Loop policy gate boundaries...",
                    "Synthesizing incremental markdown blocks without DOM flicker.",
                ],
                duration_ms=380,
                default_open=True,
            )

        # Section 7: CodeBlock and AiMarkdown
        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("AiMarkdown & CodeBlock").classes(
                "text-xs font-bold uppercase tracking-wider text-purple-400"
            )
            markdown_content = (
                "Here is an example with code fences automatically converted into interactive `CodeBlock` components:\n\n"
                "```python:main.py\n"
                "from nicegui import ui\n"
                "from nicegui_ai import AiThread, AiComposer\n\n"
                "# Initialize components\n"
                "thread = AiThread()\n"
                "composer = AiComposer()\n"
                "ui.run(port=8080)\n"
                "```\n\n"
                "All code blocks feature language indicators, file tags, line numbers, and clipboard copy."
            )
            AiMarkdown(markdown_content)

        # Section 8: ArtifactCard & ArtifactViewerDrawer
        artifact_viewer = ArtifactViewerDrawer(
            title="Artifact Inspector",
            width_px=680,
            on_download=lambda title, content: ui.notify(
                f"Downloaded {title}", type="positive"
            ),
        )

        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("ArtifactCard & ArtifactViewerDrawer").classes(
                "text-xs font-bold uppercase tracking-wider text-purple-400"
            )
            ui.label(
                "Click the panel icon on the card to inspect in the slide-over drawer with Code, Live Render, and Unified Diff tabs."
            ).classes("text-[11px] text-gray-400")
            ArtifactCard(
                title="src/nicegui_ai/demo.py",
                artifact_type="file",
                content=(
                    "from nicegui import ui\n"
                    "from nicegui_ai import ArtifactViewerDrawer\n\n"
                    "print('Component loaded successfully!')\n"
                ),
                diff_content=(
                    "--- a/src/nicegui_ai/demo.py\n"
                    "+++ b/src/nicegui_ai/demo.py\n"
                    "@@ -1,3 +1,4 @@\n"
                    " from nicegui import ui\n"
                    "+from nicegui_ai import ArtifactViewerDrawer\n"
                    " \n"
                    " print('Component loaded successfully!')\n"
                ),
                language="python",
                size_bytes=480,
                default_open=True,
                drawer=artifact_viewer,
                on_download=lambda: ui.notify("Downloading artifact...", type="info"),
            )

        # Section 9: ApprovalModal Trigger
        modal = ApprovalModal(
            title="Database Schema Migration",
            danger_level="critical",
            tool_call=ToolCall(
                id="sec-01",
                name="apply_migration",
                args={"version": "2026_10_25_v2", "destructive": True},
                summary="Execute irreversible migration step",
            ),
            on_approve=lambda: ui.notify("Migration approved", type="positive"),
            on_veto=lambda: ui.notify("Migration vetoed", type="negative"),
        )
        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("ApprovalModal Gate").classes(
                "text-xs font-bold uppercase tracking-wider text-red-400"
            )
            with (
                ui.element("button")
                .classes(
                    "px-4 py-2 rounded-xl bg-red-950/60 hover:bg-red-900 border border-red-500/40 "
                    "text-red-300 text-xs font-medium cursor-pointer transition-colors flex items-center gap-2"
                )
                .on("click", modal.open)
            ):
                LucideIcon("shield-alert", size=14, classes="text-red-400")
                ui.label("Open Approval Gate Modal")

        # Section 10: Turn Branching & Fork Navigation
        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("Turn Branching & Fork Navigation").classes(
                "text-xs font-bold uppercase tracking-wider text-purple-400"
            )
            ui.label(
                "Reactive turn variations and fork branching directly inside UserMessage and AgentMessage."
            ).classes("text-[11px] text-gray-400")

            ui.label("Standalone BranchPicker:").classes(
                "text-[11px] text-gray-400 font-mono mt-1"
            )
            with ui.row().classes("items-center gap-3"):
                BranchPicker(
                    current_index=1,
                    total_branches=4,
                    on_change=lambda idx: ui.notify(
                        f"Standalone picker switched to branch {idx}", type="info"
                    ),
                )

            ui.label("Interactive User & Agent Message Branching:").classes(
                "text-[11px] text-gray-400 font-mono mt-2"
            )
            branch_user = UserMessage(
                text="Branch 1: Can you provide an async Python generator example?",
                user_name="Operator",
            )
            branch_user.add_branch(
                "Branch 2: Could you show an object-oriented async iterator instead?",
                switch_to=False,
            )

            branch_agent = AgentMessage(
                agent_name="CodeAgent",
                text="```python\nasync def count_up(n: int):\n    for i in range(n):\n        yield i\n```",
                reasoning="Producing a standard lightweight async generator function.",
                tokens_used=145,
            )
            branch_agent.add_branch(
                MessageBranch(
                    index=2,
                    text=(
                        "```python\n"
                        "class CountUpIterator:\n"
                        "    def __init__(self, n: int):\n"
                        "        self.n = n\n"
                        "        self.current = 0\n\n"
                        "    def __aiter__(self):\n"
                        "        return self\n\n"
                        "    async def __anext__(self):\n"
                        "        if self.current < self.n:\n"
                        "            val = self.current\n"
                        "            self.current += 1\n"
                        "            return val\n"
                        "        raise StopAsyncIteration\n"
                        "```"
                    ),
                    reasoning="Alternative object-oriented approach implementing __aiter__ and __anext__.",
                    tokens_used=280,
                ),
                switch_to=False,
            )

        # Section 11: AG-UI Streaming Bridge & Adapters
        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("AG-UI Streaming Bridge & Adapters").classes(
                "text-xs font-bold uppercase tracking-wider text-purple-400"
            )
            ui.label(
                "Live reactive streaming with OpenRouter, Gemini, and OpenCode adapters."
            ).classes("text-[11px] text-gray-400")

            stream_container = ui.column().classes("w-full")

            async def run_openrouter_demo() -> None:
                stream_container.clear()
                with stream_container:
                    msg = AgentMessage(
                        agent_name="openrouter-agent", is_generating=True
                    )

                async def mock_or_chunks() -> AsyncIterator[dict[str, Any]]:
                    for t in [
                        "Analyzing query parameters...\n",
                        "Selecting optimal code transformation.\n",
                    ]:
                        yield {"choices": [{"delta": {"reasoning": t}}]}
                        await asyncio.sleep(0.15)
                    yield {
                        "choices": [
                            {
                                "delta": {
                                    "tool_calls": [
                                        {
                                            "index": 0,
                                            "id": "gallery_tool_1",
                                            "function": {
                                                "name": "format_code",
                                                "arguments": '{"style": "ruff"}',
                                            },
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                    await asyncio.sleep(0.2)
                    for text in [
                        "Formatted python buffer cleanly with **OpenRouterStreamAdapter**:\n",
                        "- 0 linter violations\n",
                        "- Reconstructed arguments via `update_args`\n",
                    ]:
                        yield {"choices": [{"delta": {"content": text}}]}
                        await asyncio.sleep(0.1)
                    yield {
                        "choices": [{"delta": {}, "finish_reason": "stop"}],
                        "usage": {"total_tokens": 310},
                    }

                adapter = OpenRouterStreamAdapter(mock_or_chunks())
                bridge = StreamBridge(message=msg, header=header)
                res = await bridge.consume(adapter)
                for tc in res.tool_calls:
                    if tc.id in bridge._tool_cards:
                        bridge._tool_cards[tc.id].resolve(
                            "Clean formatting applied", duration_ms=35
                        )

            async def run_gemini_demo() -> None:
                stream_container.clear()
                with stream_container:
                    msg = AgentMessage(agent_name="gemini-agent", is_generating=True)

                async def mock_gemini_chunks() -> AsyncIterator[dict[str, Any]]:
                    for t in [
                        "Gemini 2.5 thinking process initiated...\n",
                        "Validating type annotations with strict mypy flags.\n",
                    ]:
                        yield {
                            "candidates": [
                                {"content": {"parts": [{"text": t, "thought": True}]}}
                            ]
                        }
                        await asyncio.sleep(0.15)
                    yield {
                        "candidates": [
                            {
                                "content": {
                                    "parts": [
                                        {
                                            "function_call": {
                                                "name": "type_check",
                                                "args": {"target": "schema.py"},
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                    await asyncio.sleep(0.2)
                    yield {
                        "candidates": [
                            {
                                "content": {
                                    "parts": [
                                        {
                                            "function_response": {
                                                "name": "type_check",
                                                "response": {
                                                    "result": "Success: no issues found in 1 source file"
                                                },
                                            }
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                    await asyncio.sleep(0.15)
                    yield {
                        "candidates": [
                            {
                                "content": {
                                    "parts": [
                                        {
                                            "text": "Gemini stream verified: zero type discrepancies detected."
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                    yield {"usage_metadata": {"total_token_count": 290}}

                adapter = GeminiStreamAdapter(mock_gemini_chunks())
                bridge = StreamBridge(message=msg, header=header)
                await bridge.consume(adapter)

            async def run_opencode_demo() -> None:
                stream_container.clear()
                with stream_container:
                    msg = AgentMessage(agent_name="opencode-agent", is_generating=True)

                async def mock_opencode_events() -> AsyncIterator[dict[str, Any]]:
                    yield {
                        "type": "thought",
                        "thought": "OpenCode planning execution steps.\n",
                    }
                    await asyncio.sleep(0.15)
                    yield {
                        "type": "step_start",
                        "step_id": "step_lint",
                        "name": "Run Ruff Linter",
                    }
                    yield {"type": "command", "command": "uv run ruff check ."}
                    await asyncio.sleep(0.2)
                    yield {
                        "type": "command_result",
                        "output": "All checks passed!",
                    }
                    yield {"type": "step_finish", "step_id": "step_lint"}
                    await asyncio.sleep(0.15)
                    yield {
                        "type": "content",
                        "content": "OpenCode agent workflow finished with zero errors.",
                    }

                adapter = OpenCodeStreamAdapter(mock_opencode_events())
                bridge = StreamBridge(message=msg, header=header)
                await bridge.consume(adapter)

            with ui.row().classes("gap-2"):
                with (
                    ui.element("button")
                    .classes(
                        "px-3 py-1.5 rounded-lg bg-purple-950/80 hover:bg-purple-900 border border-purple-500/40 text-purple-200 text-xs font-medium cursor-pointer transition-colors"
                    )
                    .on("click", lambda: asyncio.create_task(run_openrouter_demo()))
                ):
                    ui.label("OpenRouter Stream")

                with (
                    ui.element("button")
                    .classes(
                        "px-3 py-1.5 rounded-lg bg-blue-950/80 hover:bg-blue-900 border border-blue-500/40 text-blue-200 text-xs font-medium cursor-pointer transition-colors"
                    )
                    .on("click", lambda: asyncio.create_task(run_gemini_demo()))
                ):
                    ui.label("Gemini Stream")

                with (
                    ui.element("button")
                    .classes(
                        "px-3 py-1.5 rounded-lg bg-emerald-950/80 hover:bg-emerald-900 border border-emerald-500/40 text-emerald-200 text-xs font-medium cursor-pointer transition-colors"
                    )
                    .on("click", lambda: asyncio.create_task(run_opencode_demo()))
                ):
                    ui.label("OpenCode Stream")

        # Section 9: 1:1 Antigravity Desktop UI/UX Suite Showcase
        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#101010] rounded-2xl border border-[#222222]"
        ):
            with ui.row().classes("w-full items-center justify-between"):
                with ui.column().classes("gap-0.5"):
                    ui.label("Antigravity 1:1 Desktop UI/UX Suite (nicegui_ai.antigravity)").classes(
                        "text-xs font-bold uppercase tracking-wider text-emerald-400"
                    )
                    ui.label(
                        "Full 1:1 Antigravity desktop clone: TitleBar, Sidebar, Zero-State Home, ChatView, ModelSelector, History, Automations, Customizations, 6-Tab AuxiliaryPane, and 2-Column SettingsModal."
                    ).classes("text-xs text-gray-400")
                ui.link(
                    "Open 1:1 Antigravity App →",
                    "/antigravity",
                ).classes(
                    "px-3.5 py-1.5 rounded-lg bg-[#272727] hover:bg-[#333333] text-[#cccccc] text-xs font-medium no-underline border border-[#222222]"
                )


def main() -> None:
    from nicegui_ai.antigravity import register_antigravity_routes

    register_antigravity_routes("/antigravity")
    ui.run(title="nicegui-ai Component Gallery", port=8080, reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()

