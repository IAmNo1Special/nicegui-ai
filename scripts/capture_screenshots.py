"""Capture high-resolution screenshots of nicegui-ai for README and docs."""

from nicegui import ui

from nicegui_ai import (
    AgentMessage,
    AiComposer,
    AiThread,
    ArtifactViewerDrawer,
    FloatingHeader,
    ReasoningCard,
    TaskTray,
    ToolCall,
    ToolCallCard,
    ToolStatus,
    UserMessage,
    setup_ai_theme,
)
from nicegui_ai.gallery import gallery_page

PORT = 8099


@ui.page("/studio")
def studio_page():
    setup_ai_theme()

    _header = FloatingHeader(
        agent_name="code-agent",
        model="claude-3-7-sonnet",
        tokens_used=24890,
        token_limit=128000,
    )

    with ui.element("main").classes(
        "flex-1 flex flex-col items-center justify-center pt-16 pb-6 px-4 w-full h-screen min-h-0 overflow-hidden"
    ):
        with ui.element("div").classes(
            "w-full max-w-3xl h-full flex flex-col bg-[#11151f]/60 backdrop-blur "
            "border border-gray-800/60 rounded-2xl shadow-2xl overflow-hidden min-h-0"
        ):
            thread = AiThread()
            thread.welcome_container.set_visibility(False)

            with thread.messages_container:
                # 1. User Message
                UserMessage(
                    text="Can you optimize our database schema and validate compound indexes for high-throughput streaming?",
                    user_name="Operator",
                    current_branch=1,
                    total_branches=2,
                )

                # 2. Agent Message
                agent = AgentMessage(
                    agent_name="Agent",
                    text=(
                        "Here is the execution plan with zero breaking changes:\n\n"
                        "```sql:schema.sql\n"
                        "ALTER TABLE users ADD INDEX idx_tenant_email (tenant_id, email);\n"
                        "```\n\n"
                        "The compound index ensures constant-time lookups across multi-tenant queries."
                    ),
                    tokens_used=420,
                    current_branch=1,
                    total_branches=2,
                )

                # Reasoning Card (Open)
                with agent.reasoning_container:
                    ReasoningCard(
                        thought_text=(
                            "• Analyzed database schema indexes across tenants\n"
                            "• Verified compound index cardinality on (tenant_id, email)\n"
                            "• Calculated query execution cost reduction: ~84%"
                        ),
                        title="Reasoning (Thinking Process)",
                        steps=[
                            "Schema analysis",
                            "Index cardinality verification",
                            "Query cost reduction",
                        ],
                        default_open=True,
                    )

                # Tool Call Card (Resolved)
                with agent.tools_container:
                    tool_card = ToolCallCard(
                        ToolCall(
                            id="call_idx_99",
                            name="validate_indexes",
                            args={"table": "users", "fields": ["tenant_id", "email"]},
                            summary="Inspect compound index cardinality",
                            status=ToolStatus.RESOLVED,
                        ),
                        default_open=False,
                    )
                    tool_card.resolve(
                        "Query plan verified: index scan utilized. (34ms)"
                    )

                # Artifact Card
                agent.add_artifact(
                    title="src/db/migrations/0002_add_compound_index.sql",
                    artifact_type="file",
                    content="ALTER TABLE users ADD INDEX idx_tenant_email (tenant_id, email);\n",
                    language="sql",
                    size_bytes=64,
                )

            # Task Tray with active task
            tray = TaskTray()
            tray.add_task("Indexing schema tables (45/100)...")

            # Composer Dock
            AiComposer(
                placeholder="Message AI agent... (type / for commands, @ for files)",
            )


@ui.page("/drawer")
def drawer_page():
    setup_ai_theme()

    _header = FloatingHeader(
        agent_name="code-agent",
        model="claude-3-7-sonnet",
        tokens_used=24890,
        token_limit=128000,
    )

    drawer = ArtifactViewerDrawer(
        title="Artifact & Workspace Canvas",
        side="right",
        width_px=640,
    )

    diff_content = (
        "--- a/src/api/stream_router.py\n"
        "+++ b/src/api/stream_router.py\n"
        "@@ -1,7 +1,12 @@\n"
        " from nicegui_ai import AiThread\n"
        "+from nicegui_ai import StreamBridge, OpenRouterStreamAdapter\n"
        " \n"
        " class StreamRouter:\n"
        "-    def stream_turn(self, prompt: str):\n"
        "-        pass\n"
        "+    async def stream_turn(self, prompt: str, message, header):\n"
        "+        adapter = OpenRouterStreamAdapter(self.get_stream(prompt))\n"
        "+        bridge = StreamBridge(message=message, header=header)\n"
        "+        return await bridge.consume(adapter)\n"
    )

    drawer.load_artifact(
        title="src/api/stream_router.py",
        content=(
            "from nicegui_ai import AiThread, StreamBridge, OpenRouterStreamAdapter\n\n"
            "class StreamRouter:\n"
            "    async def stream_turn(self, prompt: str, message, header):\n"
            "        adapter = OpenRouterStreamAdapter(self.get_stream(prompt))\n"
            "        bridge = StreamBridge(message=message, header=header)\n"
            "        return await bridge.consume(adapter)\n"
        ),
        diff_content=diff_content,
        language="python",
        artifact_type="diff",
    )
    drawer.open()

    with ui.element("main").classes(
        "flex-1 flex flex-col items-center justify-center pt-16 pb-6 px-4 w-full h-screen min-h-0 overflow-hidden"
    ):
        with ui.element("div").classes(
            "w-full max-w-2xl h-full flex flex-col bg-[#11151f]/60 backdrop-blur "
            "border border-gray-800/60 rounded-2xl shadow-2xl overflow-hidden min-h-0 opacity-80"
        ):
            thread = AiThread()
            thread.welcome_container.set_visibility(False)
            with thread.messages_container:
                UserMessage(
                    "Refactor our streaming router to use StreamBridge.",
                    user_name="User",
                )
                AgentMessage(
                    agent_name="Agent",
                    text="Created `src/api/stream_router.py` with full diff preview in drawer.",
                )


@ui.page("/gallery")
def gallery():
    gallery_page()


def run_server():
    ui.run(port=PORT, show=False, reload=False)


if __name__ == "__main__":
    run_server()
