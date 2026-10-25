"""Centered AI conversation thread with suggestions and auto-scrolling."""

from collections.abc import Callable
from typing import Any, Self

from nicegui import ui

from nicegui_ai.icons import LucideIcon
from nicegui_ai.message import AgentMessage, UserMessage
from nicegui_ai.schema import MessageBranch, SuggestionPrompt, ToolCall


class AiThread(ui.column):
    """Spacious, centered conversation canvas matching modern AI agent aesthetics."""

    def __init__(
        self,
        welcome_title: str = "How can I help you today?",
        welcome_subtitle: str = "Ask a question, run tools, or coordinate autonomous tasks.",
        suggestions: list[SuggestionPrompt | str] | None = None,
        on_suggestion_click: Callable[[str], Any] | None = None,
        on_select_suggestion: Callable[[str], Any] | None = None,
    ) -> None:
        super().__init__()
        self.welcome_title = welcome_title
        self.welcome_subtitle = welcome_subtitle
        raw_suggestions = suggestions or []
        self.suggestions: list[SuggestionPrompt] = [
            s
            if isinstance(s, SuggestionPrompt)
            else SuggestionPrompt(label=s, prompt=s)
            for s in raw_suggestions
        ]
        self.on_suggestion_click_callback = on_suggestion_click or on_select_suggestion
        self.messages: list[UserMessage | AgentMessage] = []

        self.classes("w-full flex-1 flex flex-col overflow-hidden min-h-0")

        with self:
            # Scrollable message list container
            self.scroll_area = ui.scroll_area().classes(
                "flex-1 w-full px-4 py-2 min-h-0"
            )
            with self.scroll_area:
                self.messages_container = ui.column().classes(
                    "w-full gap-2 min-h-[300px]"
                )

                # Welcome empty state
                self.welcome_container = ui.column().classes(
                    "items-center justify-center text-center max-w-lg mx-auto py-8 gap-2 w-full"
                )
                self._render_welcome()

    def _render_welcome(self) -> None:
        with self.welcome_container:
            with ui.element("div").classes(
                "w-12 h-12 rounded-2xl bg-gradient-to-tr from-purple-600 to-indigo-600 "
                "flex items-center justify-center text-white mb-2 shadow-xl border border-purple-400/40"
            ):
                LucideIcon("sparkles", size=24, classes="text-white")

            ui.label(self.welcome_title).classes(
                "text-base font-bold text-white tracking-wide mb-0.5"
            )
            ui.label(self.welcome_subtitle).classes(
                "text-xs text-gray-400 leading-relaxed max-w-md"
            )

            if self.suggestions:
                with ui.element("div").classes(
                    "grid grid-cols-2 gap-2 w-full mt-4 text-left"
                ):
                    for s in self.suggestions:
                        with (
                            ui.element("button")
                            .classes(
                                "p-2.5 bg-[#131722] hover:bg-[#191f2e] border border-gray-800 "
                                "hover:border-purple-500/40 rounded-xl text-left transition-all "
                                "flex flex-col gap-0.5 shadow-sm w-full cursor-pointer outline-none"
                            )
                            .on(
                                "click",
                                lambda _e, p=s.prompt: self._handle_suggestion(p),
                            )
                        ):
                            ui.label(s.label).classes(
                                "font-semibold text-gray-200 text-[11px] mb-0.5"
                            )
                            ui.label(s.prompt).classes(
                                "text-[10px] text-gray-400 font-mono truncate w-full"
                            )

    def _handle_suggestion(self, prompt: str) -> None:
        if self.on_suggestion_click_callback:
            self.on_suggestion_click_callback(prompt)

    def add_user_message(
        self,
        text: str,
        user_name: str = "User",
        current_branch: int = 1,
        total_branches: int = 1,
        on_branch_change: Callable[[int, str], None] | None = None,
    ) -> UserMessage:
        """Add a right-aligned user message bubble."""
        self.welcome_container.set_visibility(False)
        with self.messages_container:
            msg = UserMessage(
                text=text,
                user_name=user_name,
                current_branch=current_branch,
                total_branches=total_branches,
                on_branch_change=on_branch_change,
            )
        self.messages.append(msg)
        self.scroll_to_bottom()
        return msg

    def add_agent_message(
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
        on_branch_change: Callable[[int, MessageBranch], None] | None = None,
        on_fork: Callable[[AgentMessage, int], None] | None = None,
    ) -> AgentMessage:
        """Add a left-aligned agent message with reasoning and tools."""
        self.welcome_container.set_visibility(False)
        with self.messages_container:
            msg = AgentMessage(
                agent_name=agent_name,
                text=text,
                reasoning=reasoning,
                tool_calls=tool_calls,
                tokens_used=tokens_used,
                current_branch=current_branch,
                total_branches=total_branches,
                initial_text=initial_text,
                is_generating=is_generating,
                on_branch_change=on_branch_change,
                on_fork=on_fork,
            )
        self.messages.append(msg)
        self.scroll_to_bottom()
        return msg

    def scroll_to_bottom(self) -> None:
        """Auto-scroll the thread viewport to the latest message."""
        self.scroll_area.scroll_to(percent=1.0)

    def clear(self) -> Self:
        """Clear all messages and restore the welcome state."""
        self.messages_container.clear()
        self.messages.clear()
        self.welcome_container.set_visibility(True)
        return self
