"""Interactive showcase application for nicegui-ai primitives."""

import asyncio

from nicegui import ui

from nicegui_ai import (
    AiComposer,
    AiThread,
    FloatingHeader,
    SlideOverDrawer,
    SuggestionPrompt,
    ToolCall,
    ToolStatus,
    setup_ai_theme,
)


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
        title="Workspace Canvas", icon="dashboard", side="right"
    )

    with header.left_container:
        with (
            ui.button(on_click=sessions_drawer.toggle)
            .props("flat dense round size=sm")
            .classes(
                "text-gray-300 hover:text-white px-2 py-1 rounded-full hover:bg-gray-800 transition-colors flex items-center gap-1.5"
            )
        ):
            ui.icon("history").classes("text-amber-400 text-xs")
            ui.label("History").classes("font-medium text-xs")
            ui.label("3").classes(
                "bg-gray-800 text-[10px] px-1.5 rounded-full font-mono text-gray-400"
            )

    with header.right_container:
        with (
            ui.button(on_click=canvas_drawer.toggle)
            .props("flat dense round size=sm")
            .classes(
                "text-gray-300 hover:text-white px-2 py-1 rounded-full hover:bg-gray-800 transition-colors flex items-center gap-1.5"
            )
        ):
            ui.icon("commit").classes("text-purple-400 text-xs")
            ui.label("Canvas").classes("font-medium text-xs")
            ui.element("span").classes("w-2 h-2 rounded-full bg-red-500 animate-ping")

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

    # 4. Centered Conversation Canvas & Composer
    with ui.column().classes(
        "w-full max-w-3xl mx-auto h-screen pt-20 pb-4 px-4 overflow-hidden"
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

        # Execution handler
        async def handle_submit(prompt: str) -> None:
            if state["is_running"]:
                # In-flight steering!
                thread.add_user_message(f"🔄 [Steer]: {prompt}", user_name="User")
                return

            state["is_running"] = True
            state["abort_requested"] = False
            composer.set_running(True)

            # 1. Add User Message
            thread.add_user_message(prompt, user_name="User")

            # 2. Create Agent Message in Generating state
            agent_msg = thread.add_agent_message(
                agent_name="Agent",
                text="",
            )
            agent_msg.set_generating(True)

            # 3. Stream Reasoning (Thinking Process)
            reasoning_card = agent_msg.add_reasoning("")
            steps = [
                "Analyzing user invocation against codebase...\n",
                "Evaluating tool candidates: view_file, run_command, replace_code...\n",
                "Checking approval gate security boundaries for target paths...\n",
                "Formulating execution trajectory with zero proprietary polyfills.\n",
            ]
            for i, step in enumerate(steps, start=1):
                if state["abort_requested"]:
                    break
                reasoning_card.append_thought(f"• {step}", step_count=i)
                await asyncio.sleep(0.3)

            # 4. Execute a Tool Call
            tool_call = ToolCall(
                id="call-001",
                name="view_file",
                args={"Path": "pyproject.toml", "StartLine": 1, "EndLine": 40},
                summary="Inspect package configuration",
                status=ToolStatus.EXECUTING,
            )
            tool_card = agent_msg.add_tool_call(tool_call)
            await asyncio.sleep(0.6)
            tool_card.resolve(
                "Lines 1-40 returned: 5 dependencies resolved successfully.",
                duration_ms=48,
            )

            # 5. Stream Agent Response text
            chunks = [
                "I have analyzed your request.\n\n",
                "The **nicegui-ai** runtime processed the turn and synchronized the session:\n\n",
                "```python\n",
                "# Verified component integration\n",
                "from nicegui_ai import AiThread, FloatingHeader\n",
                "\n",
                "thread = AiThread()\n",
                "thread.add_user_message('Hello world')\n",
                "```\n\n",
                "- **Model**: `claude-3-7-sonnet`\n",
                "- **Tool execution**: `view_file` executed cleanly.\n",
                "- **Approval Gate**: Clear, zero policy violations.",
            ]
            for chunk in chunks:
                if state["abort_requested"]:
                    break
                agent_msg.append_text(chunk)
                await asyncio.sleep(0.2)

            # 6. Finalize Turn & Update Token Ring
            agent_msg.set_generating(False)
            state["tokens_used"] += 420
            header.update_tokens(state["tokens_used"])
            state["is_running"] = False
            composer.set_running(False)

        def handle_cancel() -> None:
            state["abort_requested"] = True
            ui.notify("Generation aborted by user", type="warning")

        # 5. Composer Input Bar
        composer = AiComposer(
            placeholder="Message AI agent... (type / for commands, @ for files)",
            on_send=lambda text: asyncio.create_task(handle_submit(text)),
            on_cancel=handle_cancel,
            model_name="Claude 3.7",
        )


def main() -> None:
    ui.run(title="nicegui-ai — Modern AI Agent Primitives", port=8080, reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
