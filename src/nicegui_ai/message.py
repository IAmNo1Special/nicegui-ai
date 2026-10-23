"""User and Agent message bubbles matching modern AI agent visual geometry."""

from nicegui import ui

from nicegui_ai.artifact import ArtifactCard
from nicegui_ai.branch import BranchPicker
from nicegui_ai.code_block import CodeBlock
from nicegui_ai.icons import LucideIcon
from nicegui_ai.reasoning import ReasoningCard
from nicegui_ai.tool_call import ToolCallCard
from nicegui_ai.types import ToolCall


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
    ) -> None:
        super().__init__()
        self.agent_name = agent_name
        self.text = text
        self.tokens_used = tokens_used
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

                # Markdown text content
                self.markdown = ui.markdown(self.text).classes(
                    "leading-relaxed font-sans text-[13px] text-gray-200 w-full"
                )

    def append_text(self, chunk: str) -> None:
        """Stream an additional text delta into the message."""
        self.text += chunk
        self.markdown.set_content(self.text)

    def set_generating(self, is_generating: bool = True) -> None:
        """Update status badge between Generating... and Done."""
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

    def add_tool_call(self, tool: ToolCall) -> ToolCallCard:
        """Dynamically attach a tool call card to this message."""
        with self.tools_container:
            card = ToolCallCard(tool, default_open=False)
        return card

    def add_reasoning(self, thought_text: str) -> ReasoningCard:
        """Attach or update the reasoning effort card."""
        if self.reasoning_card is None:
            with self.reasoning_container:
                self.reasoning_card = ReasoningCard(
                    thought_text=thought_text, default_open=False
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


# Backwards compatibility alias
AssistantMessage = AgentMessage
