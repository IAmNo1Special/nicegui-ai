"""User and Agent message bubbles matching modern AI agent visual geometry."""

import uuid
from collections.abc import Callable
from typing import Any

from nicegui import ui

from nicegui_ai.artifact import ArtifactCard
from nicegui_ai.branch import BranchPicker
from nicegui_ai.code_block import CodeBlock
from nicegui_ai.icons import LucideIcon
from nicegui_ai.markdown import AiMarkdown
from nicegui_ai.reasoning import ReasoningCard
from nicegui_ai.schema import ToolCall, ToolStatus
from nicegui_ai.tool_call import ToolCallCard


class UserMessage(ui.row):
    """User message bubble aligned right with subtle corner flair."""

    def __init__(
        self,
        text: str,
        user_name: str = "User",
        current_branch: int = 1,
        total_branches: int = 1,
    ) -> None:
        super().__init__()
        self.text = text
        self.classes("justify-end w-full my-3 no-wrap")

        with self:
            with ui.column().classes(
                "max-w-[85%] bg-[#1c2333] border border-gray-700/70 "
                "rounded-2xl rounded-tr-sm p-3.5 text-xs text-gray-100 shadow-md gap-1"
            ):
                with ui.row().classes(
                    "items-center justify-between w-full text-[10px] text-gray-400 font-mono mb-1"
                ):
                    if total_branches > 1:
                        BranchPicker(current_branch, total_branches)
                    else:
                        ui.element("div")

                    with ui.row().classes("items-center gap-1.5 justify-end"):
                        ui.label(user_name)
                        LucideIcon("user", size=12, classes="text-purple-400")

                self.text_label = ui.label(text).classes(
                    "leading-relaxed whitespace-pre-wrap font-sans text-[13px]"
                )


class AgentMessage(ui.row):
    """AI agent message with avatar, reasoning, tool cards, and streamed text."""

    def __init__(
        self,
        agent_name: str = "Agent",
        text: str = "",
        reasoning: str | None = None,
        tool_calls: list[ToolCall] | None = None,
        tokens_used: int = 0,
        current_branch: int = 1,
        total_branches: int = 1,
        initial_text: str | None = None,
        is_generating: bool = False,
    ) -> None:
        super().__init__()
        self.agent_name = agent_name
        self.text = text or (initial_text or "")
        self.tokens_used = tokens_used
        self.is_generating: bool = is_generating
        self.classes("justify-start w-full my-4 no-wrap gap-3")

        with self:
            # Avatar
            with ui.element("div").classes(
                "w-8 h-8 rounded-lg bg-gradient-to-tr from-purple-700 to-indigo-600 "
                "flex items-center justify-center shrink-0 shadow-md border border-purple-400/40 mt-1"
            ):
                LucideIcon("sparkles", size=16, classes="text-white")

            # Bubble Container
            self.bubble_container = ui.column().classes(
                "flex-1 max-w-[92%] bg-[#121620] border border-gray-800/90 "
                "rounded-2xl rounded-tl-sm p-4 text-xs shadow-md gap-2"
            )
            with self.bubble_container:
                # Header
                with ui.row().classes(
                    "items-center justify-between w-full pb-1.5 border-b border-gray-800/60 text-[11px]"
                ):
                    with ui.row().classes("items-center gap-2"):
                        ui.label(self.agent_name).classes(
                            "font-bold text-white tracking-wide"
                        )
                        self.status_pill = ui.label("Done").classes(
                            "bg-purple-950/80 text-purple-300 border border-purple-500/30 text-[9px] px-1.5 py-0.2 rounded font-mono"
                        )
                    with ui.row().classes(
                        "items-center gap-2 font-mono text-[10px] text-gray-500"
                    ):
                        if total_branches > 1:
                            BranchPicker(current_branch, total_branches)
                        with ui.row().classes("items-center gap-1"):
                            LucideIcon("zap", size=10, classes="text-purple-400")
                            self.token_pill = ui.label(
                                f"+{self.tokens_used:,} tokens"
                                if self.tokens_used > 0
                                else "+0 tokens"
                            ).classes("text-purple-400/80")

                # Reasoning container
                self.reasoning_container = ui.column().classes("w-full gap-1")
                self.reasoning_card: ReasoningCard | None = None
                if reasoning:
                    with self.reasoning_container:
                        self.reasoning_card = ReasoningCard(
                            thought_text=reasoning, default_open=False
                        )

                # Tool calls container
                self.tools_container = ui.column().classes("w-full gap-1")
                if tool_calls:
                    with self.tools_container:
                        for tool in tool_calls:
                            ToolCallCard(tool, default_open=False)

                # Markdown text content powered by AiMarkdown
                self.markdown = AiMarkdown(self.text)

                # Action and reaction footer
                with ui.row().classes(
                    "items-center justify-end w-full pt-1.5 gap-2 text-gray-500 text-[10px] select-none"
                ):
                    ui.label("just now").classes(
                        "font-mono text-gray-500 text-[10px] mr-1"
                    )
                    with (
                        ui.element("button")
                        .classes(
                            "p-1 rounded text-gray-500 hover:text-gray-300 hover:bg-gray-800/60 "
                            "transition-colors cursor-pointer border-none bg-transparent"
                        )
                        .on("click", self.copy_text)
                    ):
                        LucideIcon("copy", size=12, classes="text-inherit")
                    with (
                        ui.element("button")
                        .classes(
                            "p-1 rounded text-gray-500 hover:text-emerald-400 hover:bg-gray-800/60 "
                            "transition-colors cursor-pointer border-none bg-transparent"
                        )
                        .on(
                            "click",
                            lambda: ui.notify(
                                "Feedback recorded: positive",
                                type="positive",
                                timeout=800,
                            ),
                        )
                    ):
                        LucideIcon("thumbs-up", size=12, classes="text-inherit")
                    with (
                        ui.element("button")
                        .classes(
                            "p-1 rounded text-gray-500 hover:text-red-400 hover:bg-gray-800/60 "
                            "transition-colors cursor-pointer border-none bg-transparent"
                        )
                        .on(
                            "click",
                            lambda: ui.notify(
                                "Feedback recorded: negative", type="info", timeout=800
                            ),
                        )
                    ):
                        LucideIcon("thumbs-down", size=12, classes="text-inherit")

        if is_generating:
            self.set_generating(True)

    def append_text(self, chunk: str) -> None:
        """Stream an additional text delta into the message."""
        self.text += chunk
        self.markdown.set_content(self.text)

    def set_tokens(self, tokens: int) -> None:
        """Update token consumption badge."""
        self.tokens_used = tokens
        self.token_pill.set_text(f"+{tokens:,} tokens")

    async def copy_text(self) -> None:
        """Copy message content to system clipboard."""
        safe_text = (
            self.text.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
        )
        await ui.run_javascript(f"navigator.clipboard.writeText(`{safe_text}`)")
        ui.notify("Message copied to clipboard", type="positive", timeout=1000)

    def set_generating(self, is_generating: bool = True) -> None:
        """Update status badge between Generating... and Done."""
        self.is_generating = is_generating
        if is_generating:
            self.status_pill.set_text("Generating...")
            self.status_pill.classes(
                "animate-pulse text-cyan-300 border-cyan-500/40 bg-cyan-950/80"
            )
        else:
            self.status_pill.set_text("Done")
            self.status_pill.classes(
                "text-purple-300 border-purple-500/30 bg-purple-950/80"
            )

    def add_tool_call(
        self,
        tool: ToolCall | None = None,
        *,
        name: str = "",
        args: dict[str, Any] | None = None,
        summary: str = "",
        status: ToolStatus = ToolStatus.PENDING,
        default_open: bool = False,
    ) -> ToolCallCard:
        """Dynamically attach a tool call card to this message."""
        if tool is None:
            tool = ToolCall(
                id=str(uuid.uuid4())[:8],
                name=name,
                args=args or {},
                summary=summary,
                status=status,
            )
        with self.tools_container:
            card = ToolCallCard(tool, default_open=default_open)
        return card

    def add_reasoning(
        self,
        thought_text: str = "",
        *,
        title: str = "Reasoning (Thinking Process)",
        steps: list[str] | None = None,
        duration_ms: int | None = None,
        default_open: bool = False,
    ) -> ReasoningCard:
        """Attach or update the reasoning effort card."""
        if self.reasoning_card is None:
            with self.reasoning_container:
                self.reasoning_card = ReasoningCard(
                    thought_text=thought_text,
                    title=title,
                    steps=steps,
                    duration_ms=duration_ms,
                    default_open=default_open,
                )
        else:
            self.reasoning_card.append_thought(thought_text)
        return self.reasoning_card

    def add_artifact(
        self,
        title: str,
        artifact_type: str = "file",
        content: str = "",
        language: str = "text",
        size_bytes: int | None = None,
        default_open: bool = False,
        diff_content: str | None = None,
        drawer: Any = None,
        on_open: Callable[[], None] | None = None,
        on_download: Callable[[], None] | None = None,
    ) -> ArtifactCard:
        """Dynamically attach an artifact card to this message."""
        with self.bubble_container:
            card = ArtifactCard(
                title=title,
                artifact_type=artifact_type,
                content=content,
                language=language,
                size_bytes=size_bytes,
                default_open=default_open,
                diff_content=diff_content,
                drawer=drawer,
                on_open=on_open,
                on_download=on_download,
            )
        return card

    def add_code_block(
        self,
        code: str,
        language: str = "text",
        filename: str | None = None,
        line_numbers: bool = False,
    ) -> CodeBlock:
        """Dynamically attach a code block component to this message."""
        with self.bubble_container:
            block = CodeBlock(
                code=code,
                language=language,
                filename=filename,
                line_numbers=line_numbers,
            )
        return block

    async def consume(
        self,
        adapter: Any,
        header: Any = None,
    ) -> Any:
        """Consume an AG-UI stream adapter reactively into this message."""
        from nicegui_ai.stream import StreamBridge

        bridge = StreamBridge(message=self, header=header)
        return await bridge.consume(adapter)
