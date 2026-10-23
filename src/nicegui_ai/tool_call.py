"""Interactive tool call execution card with approval gate support."""

import json
from collections.abc import Callable
from typing import Any

from nicegui import ui

from nicegui_ai.types import ToolCall, ToolStatus


class ToolCallCard(ui.expansion):
    """Tool execution card with inspectable args, results, and approval gates."""

    def __init__(
        self,
        tool_call: ToolCall,
        on_approve: Callable[[ToolCall], None] | None = None,
        on_veto: Callable[[ToolCall], None] | None = None,
        default_open: bool = False,
    ) -> None:
        super().__init__(value=default_open)
        self.tool_call = tool_call
        self.on_approve_callback = on_approve
        self.on_veto_callback = on_veto

        self.classes(
            "w-full rounded-xl border border-cyan-500/30 bg-[#10141d] "
            "text-xs text-gray-200 overflow-hidden shadow-md my-2 transition-all"
        )
        self.props("dense header-class='p-2.5 bg-[#141924] hover:bg-[#18202e]'")

        icon_name = "auto_fix_high"
        if "file" in tool_call.name:
            icon_name = "description"
        elif "command" in tool_call.name or "bash" in tool_call.name:
            icon_name = "terminal"
        elif "replace" in tool_call.name or "write" in tool_call.name:
            icon_name = "edit_note"

        with self.add_slot("header"):
            with ui.row().classes("items-center justify-between w-full pr-1"):
                with ui.row().classes("items-center gap-2 max-w-[70%] truncate"):
                    ui.icon(icon_name).classes("text-cyan-400 text-sm shrink-0")
                    ui.label(f"call {tool_call.name}()").classes(
                        "font-mono text-cyan-300 font-semibold text-xs shrink-0"
                    )
                    arg_preview = tool_call.summary or (
                        str(next(iter(tool_call.args.values())))
                        if tool_call.args
                        else ""
                    )
                    if arg_preview:
                        ui.label(f'("{arg_preview[:36]}...")').classes(
                            "text-[10px] text-gray-400 font-mono truncate"
                        )

                # Status pill container
                self.status_container = ui.row().classes("items-center gap-2 shrink-0")
                self._render_status_badge()

        with self:
            with ui.column().classes(
                "p-3 bg-[#0a0d14] w-full border-t border-gray-800 space-y-2 font-mono text-[11px]"
            ):
                # Arguments inspector
                ui.label("Invocation Arguments:").classes(
                    "text-[10px] uppercase text-gray-500 font-bold tracking-wider"
                )
                with ui.element("pre").classes(
                    "p-2 bg-[#121620] rounded-lg text-gray-300 overflow-x-auto border border-gray-800/80 w-full"
                ):
                    ui.label(json.dumps(self.tool_call.args, indent=2)).classes(
                        "font-mono whitespace-pre text-inherit select-text"
                    )

                # Results inspector
                self.result_container = ui.column().classes("w-full space-y-1")
                if self.tool_call.result is not None:
                    self._render_result()

                # Approval Gate buttons
                self.approval_container = ui.row().classes(
                    "w-full items-center justify-end gap-2 pt-2 border-t border-gray-800"
                )
                if self.tool_call.status == ToolStatus.APPROVAL_REQUIRED:
                    self._render_approval_buttons()

    def _render_status_badge(self) -> None:
        self.status_container.clear()
        with self.status_container:
            if self.tool_call.status == ToolStatus.RESOLVED:
                with ui.row().classes(
                    "items-center gap-1 text-[10px] text-emerald-300 "
                    "bg-emerald-950/70 border border-emerald-500/30 px-2 py-0.5 rounded"
                ):
                    ui.icon("check_circle").classes("text-xs")
                    ui.label("Resolved")
                    if self.tool_call.duration_ms:
                        ui.label(f"({self.tool_call.duration_ms}ms)").classes(
                            "text-[9px] text-emerald-400/80 font-mono"
                        )
            elif self.tool_call.status == ToolStatus.APPROVAL_REQUIRED:
                with ui.row().classes(
                    "items-center gap-1 text-[10px] text-amber-300 "
                    "bg-amber-950/70 border border-amber-500/30 px-2 py-0.5 rounded animate-pulse"
                ):
                    ui.icon("shield").classes("text-xs")
                    ui.label("Approval Gate")
            elif self.tool_call.status == ToolStatus.EXECUTING:
                with ui.row().classes(
                    "items-center gap-1 text-[10px] text-cyan-300 "
                    "bg-cyan-950/70 border border-cyan-500/30 px-2 py-0.5 rounded"
                ):
                    ui.spinner("dots", size="xs", color="cyan")
                    ui.label("Executing...")
            elif self.tool_call.status == ToolStatus.VETOED:
                with ui.row().classes(
                    "items-center gap-1 text-[10px] text-red-300 "
                    "bg-red-950/70 border border-red-500/30 px-2 py-0.5 rounded"
                ):
                    ui.icon("cancel").classes("text-xs")
                    ui.label("Vetoed")
            elif self.tool_call.status == ToolStatus.FAILED:
                with ui.row().classes(
                    "items-center gap-1 text-[10px] text-red-400 "
                    "bg-red-950/70 border border-red-500/30 px-2 py-0.5 rounded"
                ):
                    ui.icon("error").classes("text-xs")
                    ui.label("Failed")

    def _render_result(self) -> None:
        self.result_container.clear()
        with self.result_container:
            ui.label("Execution Result:").classes(
                "text-[10px] uppercase text-emerald-400 font-bold tracking-wider"
            )
            res_str = (
                self.tool_call.result
                if isinstance(self.tool_call.result, str)
                else json.dumps(self.tool_call.result, indent=2)
            )
            with ui.element("pre").classes(
                "p-2 bg-[#121620] rounded-lg text-emerald-300/90 overflow-x-auto border border-gray-800/80 w-full"
            ):
                ui.label(res_str).classes(
                    "font-mono whitespace-pre text-inherit select-text"
                )

    def _render_approval_buttons(self) -> None:
        self.approval_container.clear()
        with self.approval_container:
            ui.button("Veto", on_click=self._handle_veto).classes(
                "text-xs text-red-300 bg-red-950/40 border border-red-500/40 "
                "hover:bg-red-900/60 rounded-lg px-3 py-1 font-sans"
            )
            ui.button("Approve & Execute", on_click=self._handle_approve).classes(
                "text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-500 "
                "rounded-lg px-3 py-1 font-sans shadow-sm"
            )

    def _handle_approve(self) -> None:
        if self.on_approve_callback:
            self.on_approve_callback(self.tool_call)

    def _handle_veto(self) -> None:
        self.tool_call.status = ToolStatus.VETOED
        self._render_status_badge()
        self.approval_container.clear()
        if self.on_veto_callback:
            self.on_veto_callback(self.tool_call)

    def resolve(self, result: Any, duration_ms: int | None = None) -> None:
        """Mark the tool call as resolved with its output."""
        self.tool_call.status = ToolStatus.RESOLVED
        self.tool_call.result = result
        if duration_ms is not None:
            self.tool_call.duration_ms = duration_ms
        self._render_status_badge()
        self._render_result()
        self.approval_container.clear()
