"""Interactive showcase application for nicegui-ai primitives."""

import asyncio
from collections.abc import AsyncIterator, Callable
from typing import Any

from nicegui import ui

from nicegui_ai import (
    AiComposer,
    AiThread,
    ApprovalModal,
    BaseStreamAdapter,
    FloatingHeader,
    GeminiStreamAdapter,
    LucideIcon,
    OpenCodeStreamAdapter,
    OpenRouterStreamAdapter,
    SlideOverDrawer,
    StreamBridge,
    SuggestionPrompt,
    ToolCall,
    ToolStatus,
    setup_ai_theme,
)


class DemoStreamFactory:
    """Object-oriented factory creating simulated provider streams for showcase interaction."""

    def __init__(self, abort_check: Callable[[], bool] | None = None) -> None:
        self.abort_check = abort_check or (lambda: False)

    def create_adapter(
        self,
        model_name: str,
        prompt: str,
        effort: str | None = None,
    ) -> BaseStreamAdapter:
        """Create the appropriate provider stream adapter based on selected model."""
        name_lower = model_name.lower()
        if "gemini" in name_lower:
            return GeminiStreamAdapter(
                self._generate_gemini_chunks(prompt, effort, model_name)
            )
        if "opencode" in name_lower or "oss" in name_lower:
            return OpenCodeStreamAdapter(
                self._generate_opencode_events(prompt, model_name)
            )
        return OpenRouterStreamAdapter(
            self._generate_openrouter_chunks(prompt, effort, model_name)
        )

    async def _generate_gemini_chunks(
        self, prompt: str, effort: str | None, model_name: str
    ) -> AsyncIterator[dict[str, Any]]:
        """Simulate Google GenAI SDK stream with candidate parts and usage metadata."""
        thoughts = [
            f"Analyzing user prompt: '{prompt[:40]}...'\n",
            f"Reasoning effort budget: {effort or 'Medium'}. Scanning workspace modules...\n",
            "Synthesizing tool trajectory with zero standard library shadowing.\n",
        ]
        for t in thoughts:
            if self.abort_check():
                return
            yield {
                "candidates": [
                    {
                        "content": {
                            "parts": [{"text": t, "thought": True}],
                            "role": "model",
                        }
                    }
                ]
            }
            await asyncio.sleep(0.2)

        # Tool call
        if self.abort_check():
            return
        yield {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "function_call": {
                                    "name": "view_file",
                                    "args": {
                                        "path": "pyproject.toml",
                                        "start_line": 1,
                                        "end_line": 40,
                                    },
                                }
                            }
                        ]
                    }
                }
            ]
        }
        await asyncio.sleep(0.35)

        # Tool response
        if self.abort_check():
            return
        yield {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "function_response": {
                                    "name": "view_file",
                                    "response": {
                                        "result": "File pyproject.toml inspected: 5 core dependencies resolved."
                                    },
                                }
                            }
                        ]
                    }
                }
            ]
        }
        await asyncio.sleep(0.2)

        # Text chunks
        text_chunks = [
            "I have inspected the project structure using **Google Gemini GenAI**.\n\n",
            "The turn was consumed through `GeminiStreamAdapter`:\n\n",
            "```python:gemini_stream.py\n",
            "# Ingested via GeminiStreamAdapter & StreamBridge\n",
            "from nicegui_ai import GeminiStreamAdapter, StreamBridge\n\n",
            "bridge = StreamBridge(message=agent_msg, header=header)\n",
            "await bridge.consume(GeminiStreamAdapter(gemini_stream))\n",
            "```\n\n",
            f"- **Active Model**: `{model_name}`\n",
            f"- **Effort Level**: `{effort or 'Medium'}`\n",
            "- **Streaming Protocol**: AG-UI Normalized via `GeminiStreamAdapter`\n",
        ]
        for chunk in text_chunks:
            if self.abort_check():
                return
            yield {
                "candidates": [
                    {
                        "content": {
                            "parts": [{"text": chunk}],
                            "role": "model",
                        }
                    }
                ]
            }
            await asyncio.sleep(0.12)

        # Usage metadata
        yield {
            "usage_metadata": {
                "prompt_token_count": 142,
                "candidates_token_count": 338,
                "total_token_count": 480,
            }
        }

    async def _generate_openrouter_chunks(
        self, prompt: str, effort: str | None, model_name: str
    ) -> AsyncIterator[dict[str, Any]]:
        """Simulate OpenRouter / OpenAI SSE chunk stream with reasoning and tool fragments."""
        thoughts = [
            f"Analyzing query: '{prompt[:40]}...'\n",
            f"Selected reasoning effort: {effort or 'High'}. Evaluating tool candidates...\n",
            "Formulating modular architecture with clean OOP contracts.\n",
        ]
        for t in thoughts:
            if self.abort_check():
                return
            yield {
                "choices": [
                    {
                        "delta": {"reasoning": t},
                        "finish_reason": None,
                    }
                ]
            }
            await asyncio.sleep(0.2)

        # Tool call streaming
        if self.abort_check():
            return
        yield {
            "choices": [
                {
                    "delta": {
                        "tool_calls": [
                            {
                                "index": 0,
                                "id": "call_view_01",
                                "function": {
                                    "name": "view_file",
                                    "arguments": '{"path": "src/',
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
                                    "arguments": 'nicegui_ai/schema.py"}',
                                },
                            }
                        ]
                    }
                }
            ]
        }
        await asyncio.sleep(0.3)

        # Text chunks
        text_chunks = [
            f"I analyzed your request using **{model_name}**.\n\n",
            "The turn was consumed through `OpenRouterStreamAdapter`:\n\n",
            "```python:openrouter_stream.py\n",
            "# Ingested via OpenRouterStreamAdapter & StreamBridge\n",
            "from nicegui_ai import OpenRouterStreamAdapter, StreamBridge\n\n",
            "adapter = OpenRouterStreamAdapter(openrouter_stream)\n",
            "result = await agent_msg.consume(adapter, header=header)\n",
            "```\n\n",
            f"- **Engine**: `{model_name}`\n",
            f"- **Reasoning Effort**: `{effort or 'High'}`\n",
            "- **Tool Args**: Reconstructed incremental JSON arguments cleanly.\n",
        ]
        for chunk in text_chunks:
            if self.abort_check():
                return
            yield {
                "choices": [
                    {
                        "delta": {"content": chunk},
                        "finish_reason": None,
                    }
                ]
            }
            await asyncio.sleep(0.12)

        # Finish and token usage
        yield {
            "choices": [{"delta": {}, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": 120,
                "completion_tokens": 300,
                "total_tokens": 420,
            },
        }

    async def _generate_opencode_events(
        self, prompt: str, model_name: str
    ) -> AsyncIterator[dict[str, Any]]:
        """Simulate OpenCode coding agent event stream."""
        if self.abort_check():
            return
        yield {
            "type": "thought",
            "thought": f"OpenCode reasoning for '{prompt[:40]}...'\nFormulating plan steps.\n",
        }
        await asyncio.sleep(0.25)

        if self.abort_check():
            return
        yield {
            "type": "step_start",
            "step_id": "step_1",
            "name": "Verify dependencies",
        }
        yield {
            "type": "command",
            "command": "uv run pytest tests/test_stream.py",
        }
        await asyncio.sleep(0.3)
        yield {
            "type": "command_result",
            "output": "6 passed in 0.45s",
        }
        yield {
            "type": "step_finish",
            "step_id": "step_1",
        }
        await asyncio.sleep(0.2)

        if self.abort_check():
            return
        yield {
            "type": "content",
            "content": (
                f"**OpenCode Execution Completed** using `{model_name}`.\n\n"
                "- Plan steps validated successfully\n"
                "- All test suites executed hermetically\n"
            ),
        }


@ui.page("/")
def demo_page() -> None:
    # 1. Setup dark ambient theme
    setup_ai_theme()

    # Shared demo state
    state = {
        "tokens_used": 24890,
        "token_limit": 128000,
        "is_running": False,
        "abort_requested": False,
    }

    # 2. Top floating glassmorphism header dock
    header = FloatingHeader(
        agent_name="code-agent",
        model="claude-3-7-sonnet",
        tokens_used=state["tokens_used"],
        token_limit=state["token_limit"],
    )

    # 3. Slide-over Drawers (Sessions & Canvas)
    sessions_drawer = SlideOverDrawer(
        title="Conversations", icon="history", side="left"
    )
    canvas_drawer = SlideOverDrawer(
        title="Workspace Canvas", icon="git-commit", side="right"
    )

    with header.left_container:
        with (
            ui.element("button")
            .classes(
                "flex items-center gap-1.5 text-xs text-gray-300 hover:text-white px-2 py-1 "
                "rounded-full hover:bg-gray-800 transition-colors cursor-pointer bg-transparent border-none outline-none"
            )
            .on("click", sessions_drawer.toggle)
        ):
            LucideIcon("history", size=14, classes="text-amber-400")
            ui.label("History").classes("font-medium text-xs")
            ui.label("3").classes(
                "bg-gray-800 text-[10px] px-1.5 py-0.2 rounded-full font-mono text-gray-400"
            )

    with header.right_container:
        with (
            ui.element("button")
            .classes(
                "flex items-center gap-1.5 text-xs text-gray-300 hover:text-white px-2 py-1 "
                "rounded-full hover:bg-gray-800 transition-colors cursor-pointer relative bg-transparent border-none outline-none"
            )
            .on("click", canvas_drawer.toggle)
        ):
            LucideIcon("git-commit", size=14, classes="text-purple-400")
            ui.label("Canvas").classes("font-medium text-xs")
            ui.element("span").classes(
                "w-2 h-2 rounded-full bg-red-500 animate-ping absolute -top-0.5 -right-0.5"
            )

    # Populate Sessions Drawer
    with sessions_drawer.content:
        for idx, (title, date_str, tokens) in enumerate(
            [
                ("AI Agent Component Library", "Just now", 24890),
                ("Database Schema Migration & Indexing", "2 hours ago", 12100),
                ("High-Throughput WebSocket Gateway Benchmark", "Yesterday", 45600),
            ],
            start=1,
        ):
            with ui.column().classes(
                "p-3 rounded-xl border border-gray-800/80 bg-[#161c28] hover:border-purple-500/50 "
                "cursor-pointer transition-all gap-1 w-full"
            ):
                ui.label(title).classes("font-semibold text-white text-xs")
                with ui.row().classes(
                    "items-center justify-between w-full text-[10px] text-gray-400 font-mono"
                ):
                    ui.label(f"Thread #{idx}")
                    ui.label(date_str)
                    ui.label(f"{tokens:,} tokens")

    # Approval Gate Modal
    approval_modal = ApprovalModal(
        title="Security Approval Required",
        tool_call=ToolCall(
            id="gate-1",
            name="delete_database_table",
            args={"table": "sessions_v1", "force": True},
            summary="Permanently drop legacy sessions table",
        ),
        danger_level="critical",
        on_approve=lambda: ui.notify("Action approved by operator", type="positive"),
        on_veto=lambda: ui.notify("Action vetoed by operator", type="negative"),
        on_always_allow=lambda: ui.notify("Permission cached for session", type="info"),
    )

    # Populate Canvas Drawer
    with canvas_drawer.content:
        ui.label("Staged Git Diff (+22 / -4)").classes(
            "font-semibold text-white text-xs"
        )
        with ui.element("pre").classes(
            "p-3 bg-[#0a0d14] rounded-lg border border-gray-800 font-mono text-[11px] leading-relaxed overflow-x-auto text-gray-300"
        ):
            diff_text = (
                "--- a/src/api/router.py\n"
                "+++ b/src/api/router.py\n"
                "@@ -42,6 +42,22 @@ class ApiRouter:\n"
                "+    # Auto-fallback for streaming completions\n"
                "+    if route_name == 'stream':\n"
                "+        router = StreamRouter(model_id=model_id)\n"
                "+        self._routes[route_name] = router\n"
                "+        return router"
            )
            ui.label(diff_text)

        ui.label("Human-in-the-Loop Security Gate").classes(
            "font-semibold text-white text-xs mt-3"
        )
        with (
            ui.element("button")
            .classes(
                "w-full p-2.5 rounded-xl border border-red-500/40 bg-red-950/40 hover:bg-red-900/60 "
                "text-red-300 font-sans text-xs flex items-center justify-center gap-2 cursor-pointer transition-colors"
            )
            .on("click", approval_modal.open)
        ):
            LucideIcon("shield-alert", size=14, classes="text-red-400")
            ui.label("Trigger Approval Modal")

    # 4. Main Studio Canvas Card
    with ui.element("main").classes(
        "flex-1 flex flex-col items-center justify-center pt-16 pb-6 px-4 w-full h-full min-h-0 overflow-hidden"
    ):
        with ui.element("div").classes(
            "w-full max-w-3xl h-full flex flex-col bg-[#11151f]/60 backdrop-blur "
            "border border-gray-800/60 rounded-2xl shadow-2xl overflow-hidden min-h-0"
        ):
            thread = AiThread(
                welcome_title="How can I help you today?",
                welcome_subtitle="Ask questions, execute tools, or steer autonomous coding workflows.",
                suggestions=[
                    SuggestionPrompt(
                        label="Inspect Project Architecture",
                        prompt="view_file pyproject.toml lines 1-40 to examine project dependencies",
                    ),
                    SuggestionPrompt(
                        label="Run Test Suite with Coverage",
                        prompt="run_command uv run pytest tests/ --cov",
                    ),
                    SuggestionPrompt(
                        label="Synthesize Workspace Diff",
                        prompt="Inspect staged changes and calculate line additions and deletions",
                    ),
                    SuggestionPrompt(
                        label="Check Context Window & Tokens",
                        prompt="Report current context window budget and token consumption",
                    ),
                ],
                on_suggestion_click=lambda p: composer.input.set_value(p),
            )

            stream_factory = DemoStreamFactory(
                abort_check=lambda: state["abort_requested"]
            )

            # Execution handler using object-oriented StreamBridge
            async def handle_submit(prompt: str) -> None:
                state["is_running"] = True
                state["abort_requested"] = False
                composer.set_running(True)

                # 1. Add User Message
                thread.add_user_message(prompt, user_name="User")

                # Show background task in task tray
                task = composer.add_task(
                    f"Executing tool trajectory for: {prompt[:30]}..."
                )

                # 2. Create Agent Message in Generating state
                agent_msg = thread.add_agent_message(
                    agent_name="Agent",
                    text="",
                    is_generating=True,
                )

                # 3. Create adapter and consume through StreamBridge
                adapter = stream_factory.create_adapter(
                    model_name=composer.current_model,
                    prompt=prompt,
                    effort=composer.current_effort,
                )

                bridge = StreamBridge(
                    message=agent_msg,
                    header=header,
                    composer=composer,
                    task_tray=composer.task_tray,
                )
                result = await bridge.consume(adapter)
                task.complete()

                # 4. Resolve any remaining executing tool calls in the demo
                for tc in result.tool_calls:
                    if tc.id in bridge._tool_cards:
                        card = bridge._tool_cards[tc.id]
                        if card.tool_call.status == ToolStatus.EXECUTING:
                            card.resolve(
                                "Lines 1-40 returned: 5 dependencies resolved successfully.",
                                duration_ms=48,
                            )

                # 5. Attach generated ArtifactCard
                if not state["abort_requested"]:
                    agent_msg.add_artifact(
                        title="src/api/stream_router.py",
                        artifact_type="file",
                        content=(
                            "from nicegui_ai import AiThread, StreamBridge\n\n"
                            "class StreamRouter:\n"
                            "    def __init__(self, model_id: str):\n"
                            "        self.model_id = model_id\n\n"
                            "    async def stream_turn(self, prompt: str, message, header):\n"
                            "        bridge = StreamBridge(message=message, header=header)\n"
                            "        await bridge.consume(self.get_adapter(prompt))\n"
                        ),
                        language="python",
                        size_bytes=285,
                        default_open=False,
                    )

                # 6. Finalize Turn & Update Token Ring
                if result.usage and "total_tokens" in result.usage:
                    state["tokens_used"] += result.usage["total_tokens"]
                    header.update_tokens(state["tokens_used"])
                state["is_running"] = False
                composer.set_running(False)

            def handle_cancel() -> None:
                state["abort_requested"] = True
                composer.set_running(False)
                ui.notify("Generation aborted by user", type="warning")

            def handle_model_change(model: str, effort: str | None) -> None:
                display_name = f"{model} ({effort})" if effort else model
                header.set_model(display_name)

            # 5. Composer Input Bar Docked into the Studio Card
            composer = AiComposer(
                placeholder="Message AI agent... (type / for commands, @ for files)",
                on_send=lambda text: asyncio.create_task(handle_submit(text)),
                on_cancel=handle_cancel,
                model_name="Claude Sonnet 5.5",
                reasoning_effort="Medium",
                on_model_change=handle_model_change,
            )


def main() -> None:
    ui.run(title="nicegui-ai — Modern AI Agent Primitives", port=8080, reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
