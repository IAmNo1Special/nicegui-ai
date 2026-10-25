"""Human-in-the-Loop approval modal for high-stakes tool executions."""

import json
from collections.abc import Callable
from typing import Self

from nicegui import ui

from nicegui_ai.icons import LucideIcon
from nicegui_ai.schema import ToolCall


class ApprovalModal(ui.element):
    """Ambient glassmorphism modal dialog for human-in-the-loop tool approval gates."""

    def __init__(
        self,
        tool_call: ToolCall | None = None,
        title: str = "Action Approval Required",
        danger_level: str = "warning",
        on_approve: Callable[[], None] | None = None,
        on_veto: Callable[[], None] | None = None,
        on_always_allow: Callable[[], None] | None = None,
    ) -> None:
        super().__init__("div")
        self.tool_call = tool_call
        self.title = title
        self.danger_level = danger_level
        self.on_approve_callback = on_approve
        self.on_veto_callback = on_veto
        self.on_always_allow_callback = on_always_allow
        self.is_open = False

        with self:
            self.dialog = ui.dialog().props("backdrop-filter='blur(4px)'")
            with self.dialog:
                with ui.element("div").classes(
                    "w-[480px] max-w-[95vw] bg-[#121622] border border-gray-700/80 "
                    "rounded-2xl p-5 shadow-2xl flex flex-col gap-4 text-xs text-gray-200"
                ):
                    # Header
                    badge_color = "text-amber-400 bg-amber-950/60 border-amber-500/30"
                    if danger_level == "critical":
                        badge_color = "text-red-400 bg-red-950/60 border-red-500/30"
                    elif danger_level == "safe":
                        badge_color = "text-cyan-400 bg-cyan-950/60 border-cyan-500/30"

                    with ui.row().classes("items-center justify-between w-full"):
                        with ui.row().classes("items-center gap-2"):
                            LucideIcon(
                                "shield-alert", size=18, classes=badge_color.split()[0]
                            )
                            ui.label(self.title).classes("font-bold text-sm text-white")

                        ui.label(danger_level.upper()).classes(
                            f"text-[9px] font-mono border px-2 py-0.5 rounded {badge_color}"
                        )

                    # Tool call description
                    if self.tool_call:
                        with ui.column().classes("gap-1.5 w-full"):
                            ui.label(
                                f"Target Tool: call {self.tool_call.name}()"
                            ).classes("font-mono font-semibold text-cyan-300")
                            if self.tool_call.summary:
                                ui.label(self.tool_call.summary).classes(
                                    "text-gray-400 text-xs"
                                )

                            ui.label("Invocation Arguments:").classes(
                                "text-[10px] uppercase text-gray-500 font-bold mt-1"
                            )
                            with ui.element("pre").classes(
                                "p-2.5 bg-[#0a0d14] rounded-lg border border-gray-800 "
                                "font-mono text-[11px] overflow-x-auto text-gray-300 w-full"
                            ):
                                ui.label(
                                    json.dumps(self.tool_call.args, indent=2)
                                ).classes("whitespace-pre font-mono text-inherit")

                    # Action buttons
                    with ui.row().classes(
                        "items-center justify-end gap-2 pt-2 border-t border-gray-800 w-full"
                    ):
                        with (
                            ui.element("button")
                            .classes(
                                "text-xs text-red-300 bg-red-950/40 border border-red-500/40 "
                                "hover:bg-red-900/60 rounded-lg px-3 py-1.5 font-sans cursor-pointer transition-colors"
                            )
                            .on("click", self.veto)
                        ):
                            ui.label("Veto")

                        if on_always_allow:
                            with (
                                ui.element("button")
                                .classes(
                                    "text-xs text-gray-300 bg-gray-800/80 border border-gray-700 "
                                    "hover:bg-gray-700 rounded-lg px-3 py-1.5 font-sans cursor-pointer transition-colors"
                                )
                                .on("click", self.always_allow)
                            ):
                                ui.label("Always Allow")

                        with (
                            ui.element("button")
                            .classes(
                                "text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-500 "
                                "rounded-lg px-3 py-1.5 font-sans shadow-sm cursor-pointer transition-colors"
                            )
                            .on("click", self.approve)
                        ):
                            ui.label("Approve Once")

    def open(self) -> Self:
        """Open the approval gate modal."""
        self.is_open = True
        self.dialog.open()
        return self

    def close(self) -> Self:
        """Close the approval gate modal."""
        self.is_open = False
        self.dialog.close()
        return self

    def approve(self) -> None:
        """Approve and dismiss."""
        self.close()
        if self.on_approve_callback:
            self.on_approve_callback()

    def veto(self) -> None:
        """Veto and dismiss."""
        self.close()
        if self.on_veto_callback:
            self.on_veto_callback()

    def always_allow(self) -> None:
        """Always allow and dismiss."""
        self.close()
        if self.on_always_allow_callback:
            self.on_always_allow_callback()
