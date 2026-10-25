"""Component Gallery showcasing all nicegui-ai primitives in every state."""

from nicegui import ui

from nicegui_ai import (
    AgentMessage,
    AiComposer,
    AiMarkdown,
    AiThread,
    ApprovalModal,
    ArtifactCard,
    BranchPicker,
    FloatingHeader,
    LucideIcon,
    ModelOption,
    ModelSelector,
    QueuedMessagesTray,
    ReasoningCard,
    SlideOverDrawer,
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

        # Section 8: ArtifactCard
        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("ArtifactCard").classes(
                "text-xs font-bold uppercase tracking-wider text-purple-400"
            )
            ArtifactCard(
                title="src/nicegui_ai/demo.py",
                artifact_type="file",
                content="from nicegui import ui\n\nprint('Component loaded successfully!')",
                language="python",
                size_bytes=480,
                default_open=True,
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

        # Section 10: BranchPicker
        with ui.column().classes(
            "w-full gap-3 p-4 bg-[#11151f]/60 rounded-2xl border border-gray-800/60"
        ):
            ui.label("BranchPicker").classes(
                "text-xs font-bold uppercase tracking-wider text-gray-300"
            )
            with ui.row().classes("items-center gap-3"):
                BranchPicker(
                    current_index=1,
                    total_branches=4,
                    on_change=lambda idx: ui.notify(
                        f"Switched to branch {idx}", type="info"
                    ),
                )


def main() -> None:
    ui.run(title="nicegui-ai Component Gallery", port=8080, reload=False)


if __name__ in {"__main__", "__mp_main__"}:
    main()
