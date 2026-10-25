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
from nicegui_ai.schema import MessageBranch, ToolCall, ToolStatus
from nicegui_ai.tool_call import ToolCallCard


class UserMessage(ui.row):
    """User message bubble aligned right with subtle corner flair."""

    def __init__(
        self,
        text: str,
        user_name: str = "User",
        current_branch: int = 1,
        total_branches: int = 1,
        on_branch_change: Callable[[int, str], Any] | None = None,
    ) -> None:
        super().__init__()
        self.text = text
        self.user_name = user_name
        self.branches: list[str] = [text]
        self.current_branch_index: int = current_branch
        self.on_branch_change_callback = on_branch_change
        self.classes("justify-end w-full my-3 no-wrap")

        with self:
            with ui.column().classes(
                "max-w-[85%] bg-[#1c2333] border border-gray-700/70 "
                "rounded-2xl rounded-tr-sm p-3.5 text-xs text-gray-100 shadow-md gap-1"
            ):
                with ui.row().classes(
                    "items-center justify-between w-full text-[10px] text-gray-400 font-mono mb-1"
                ):
                    self.branch_picker = BranchPicker(
                        current_index=current_branch,
                        total_branches=max(total_branches, len(self.branches)),
                        on_change=self.switch_branch,
                    )

                    with ui.row().classes("items-center gap-1.5 justify-end"):
                        ui.label(user_name)
                        LucideIcon("user", size=12, classes="text-purple-400")

                self.text_label = ui.label(text).classes(
                    "leading-relaxed whitespace-pre-wrap font-sans text-[13px]"
                )

    def add_branch(self, text: str, switch_to: bool = True) -> int:
        """Add an alternative prompt branch to this user turn."""
        self.branches.append(text)
        new_idx = len(self.branches)
        self.branch_picker.set_branch(
            new_idx if switch_to else self.current_branch_index,
            len(self.branches),
        )
        if switch_to:
            self.switch_branch(new_idx)
        return new_idx

    def switch_branch(self, index: int) -> None:
        """Switch active prompt text to specified branch index (1-based)."""
        if 1 <= index <= len(self.branches):
            self.current_branch_index = index
            self.text = self.branches[index - 1]
            self.text_label.set_text(self.text)
            self.branch_picker.set_branch(index, len(self.branches))
            if self.on_branch_change_callback:
                self.on_branch_change_callback(index, self.text)


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
        on_branch_change: Callable[[int, MessageBranch], Any] | None = None,
        on_fork: Callable[["AgentMessage", int], Any] | None = None,
    ) -> None:
        super().__init__()
        self.agent_name = agent_name
        self.text = text or (initial_text or "")
        self.tokens_used = tokens_used
        self.is_generating: bool = is_generating
        self.on_branch_change_callback = on_branch_change
        self.on_fork_callback = on_fork

        # Initialize branch tracking
        initial_branch = MessageBranch(
            index=1,
            text=self.text,
            reasoning=reasoning,
            tool_calls=list(tool_calls or []),
            tokens_used=tokens_used,
        )
        self.branches: list[MessageBranch] = [initial_branch]
        self.current_branch_index: int = current_branch

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
                        self.branch_picker = BranchPicker(
                            current_index=current_branch,
                            total_branches=max(total_branches, len(self.branches)),
                            on_change=self.switch_branch,
                        )
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
                            "p-1 rounded text-gray-500 hover:text-purple-300 hover:bg-gray-800/60 "
                            "transition-colors cursor-pointer border-none bg-transparent"
                        )
                        .on("click", lambda: self.fork())
                    ):
                        LucideIcon("git-branch", size=12, classes="text-inherit")
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

    def add_branch(
        self,
        branch: MessageBranch | None = None,
        *,
        text: str = "",
        reasoning: str | None = None,
        tool_calls: list[ToolCall] | None = None,
        tokens_used: int = 0,
        switch_to: bool = True,
    ) -> int:
        """Add an alternative branch variation to this agent turn."""
        new_index = len(self.branches) + 1
        if branch is None:
            branch = MessageBranch(
                index=new_index,
                text=text,
                reasoning=reasoning,
                tool_calls=list(tool_calls or []),
                tokens_used=tokens_used,
            )
        else:
            branch.index = new_index
        self.branches.append(branch)
        self.branch_picker.set_branch(
            new_index if switch_to else self.current_branch_index,
            len(self.branches),
        )
        if switch_to:
            self.switch_branch(new_index)
        return new_index

    def switch_branch(self, index: int) -> None:
        """Switch displayed content to specified branch index (1-based)."""
        if 1 <= index <= len(self.branches):
            self.current_branch_index = index
            branch = self.branches[index - 1]
            self.text = branch.text
            self.tokens_used = branch.tokens_used
            self.token_pill.set_text(f"+{self.tokens_used:,} tokens")
            self.markdown.set_content(branch.text)

            # Re-render reasoning
            self.reasoning_container.clear()
            self.reasoning_card = None
            if branch.reasoning:
                with self.reasoning_container:
                    self.reasoning_card = ReasoningCard(
                        thought_text=branch.reasoning,
                        default_open=False,
                        on_change=self._sync_reasoning,
                    )

            # Re-render tool calls
            self.tools_container.clear()
            if branch.tool_calls:
                with self.tools_container:
                    for tool in branch.tool_calls:
                        ToolCallCard(tool, default_open=False)

            self.branch_picker.set_branch(index, len(self.branches))
            if self.on_branch_change_callback:
                self.on_branch_change_callback(index, branch)

    def fork(self) -> int:
        """Create a new alternative branch for this agent turn."""
        new_index = self.add_branch(text="", switch_to=True)
        if self.on_fork_callback:
            self.on_fork_callback(self, new_index)
        else:
            ui.notify(
                f"Turn forked to branch {new_index}",
                type="info",
                timeout=1200,
            )
        return new_index

    def append_text(self, chunk: str) -> None:
        """Stream an additional text delta into the message."""
        self.text += chunk
        if self.branches and 1 <= self.current_branch_index <= len(self.branches):
            self.branches[self.current_branch_index - 1].text = self.text
        self.markdown.set_content(self.text)

    def set_tokens(self, tokens: int) -> None:
        """Update token consumption badge."""
        self.tokens_used = tokens
        if self.branches and 1 <= self.current_branch_index <= len(self.branches):
            self.branches[self.current_branch_index - 1].tokens_used = tokens
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
        if self.branches and 1 <= self.current_branch_index <= len(self.branches):
            branch = self.branches[self.current_branch_index - 1]
            if tool not in branch.tool_calls:
                branch.tool_calls.append(tool)
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
                    on_change=self._sync_reasoning,
                )
        else:
            self.reasoning_card.append_thought(thought_text)
        if self.branches and 1 <= self.current_branch_index <= len(self.branches):
            self.branches[
                self.current_branch_index - 1
            ].reasoning = self.reasoning_card.thought_text
        return self.reasoning_card

    def _sync_reasoning(self, text: str) -> None:
        """Keep active MessageBranch reasoning synchronized with streaming updates."""
        if self.branches and 1 <= self.current_branch_index <= len(self.branches):
            self.branches[self.current_branch_index - 1].reasoning = text

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
