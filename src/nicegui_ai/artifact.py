"""Interactive artifact card for agent-generated files, reports, and diffs."""

from collections.abc import Callable
from typing import Any, Self

from nicegui import ui

from nicegui_ai.icons import LucideIcon


class ArtifactCard(ui.element):
    """Interactive card representing an AI agent artifact with actions and preview."""

    def __init__(
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
    ) -> None:
        super().__init__("div")
        self.title = title
        self.artifact_type = artifact_type
        self.content = content
        self.language = language
        self.size_bytes = size_bytes
        self.is_open = default_open
        self.diff_content = diff_content
        self.drawer = drawer
        self.on_open_callback = on_open
        self.on_download_callback = on_download

        self.classes(
            "w-full rounded-xl border border-purple-500/30 bg-[#121622] "
            "overflow-hidden text-xs my-2.5 shadow-lg transition-all"
        )

        type_icon = "file-code"
        if artifact_type in {"report", "doc", "document"}:
            type_icon = "scroll"
        elif artifact_type in {"diff", "patch"}:
            type_icon = "git-commit"

        with self:
            # Header
            with ui.row().classes(
                "items-center justify-between w-full p-3 bg-[#171c2b] "
                "border-b border-gray-800/80 cursor-pointer select-none"
            ) as self.header_row:
                self.header_row.on("click", self.toggle)

                with ui.row().classes("items-center gap-2.5 truncate max-w-[65%]"):
                    LucideIcon(type_icon, size=16, classes="text-purple-400 shrink-0")
                    ui.label(self.title).classes(
                        "font-bold text-white text-xs truncate"
                    )
                    ui.label(self.artifact_type.upper()).classes(
                        "text-[9px] font-mono bg-purple-950/80 text-purple-300 "
                        "border border-purple-500/30 px-1.5 py-0.2 rounded shrink-0"
                    )

                # Right side action icons
                with ui.row().classes("items-center gap-1.5 shrink-0"):
                    if self.size_bytes is not None:
                        size_str = (
                            f"{self.size_bytes} B"
                            if self.size_bytes < 1024
                            else f"{self.size_bytes / 1024:.1f} KB"
                        )
                        ui.label(size_str).classes(
                            "text-[10px] text-gray-500 font-mono mr-1"
                        )

                    # Action buttons
                    with (
                        ui.element("button")
                        .classes(
                            "p-1 rounded text-gray-400 hover:text-white hover:bg-gray-800 "
                            "cursor-pointer border-none bg-transparent transition-colors"
                        )
                        .on("click", lambda _e: self.copy())
                    ):
                        LucideIcon(
                            "copy", size=13, classes="text-gray-400 hover:text-white"
                        )

                    if on_download:
                        with (
                            ui.element("button")
                            .classes(
                                "p-1 rounded text-gray-400 hover:text-white hover:bg-gray-800 "
                                "cursor-pointer border-none bg-transparent transition-colors"
                            )
                            .on("click", lambda _e: on_download())
                        ):
                            LucideIcon(
                                "download",
                                size=13,
                                classes="text-gray-400 hover:text-white",
                            )

                    # Open in Drawer button
                    with (
                        ui.element("button")
                        .classes(
                            "p-1 rounded text-gray-400 hover:text-purple-300 hover:bg-gray-800 "
                            "cursor-pointer border-none bg-transparent transition-colors"
                        )
                        .on("click", lambda _e: self.open_in_drawer())
                    ):
                        LucideIcon(
                            "panel-right-open",
                            size=13,
                            classes="text-gray-400 hover:text-purple-300",
                        )

                    self.chevron = LucideIcon(
                        "chevron-down" if default_open else "chevron-right",
                        size=14,
                        classes="text-gray-400 ml-1 shrink-0",
                    )

            # Collapsible body preview
            self.body = ui.element("div").classes(
                "p-3 bg-[#0a0d14] font-mono text-[11px] leading-relaxed overflow-x-auto text-gray-200 w-full"
            )
            self.body.set_visibility(default_open)
            with self.body:
                self.content_label = ui.label(self.content).classes(
                    "whitespace-pre text-inherit select-text font-mono"
                )

    def toggle(self) -> None:
        """Toggle artifact preview open/closed."""
        self.is_open = not self.is_open
        self.body.set_visibility(self.is_open)
        self.chevron.set_icon("chevron-down" if self.is_open else "chevron-right")

    def open(self) -> Self:
        """Open artifact preview."""
        self.is_open = True
        self.body.set_visibility(True)
        self.chevron.set_icon("chevron-down")
        return self

    def close(self) -> Self:
        """Close artifact preview."""
        self.is_open = False
        self.body.set_visibility(False)
        self.chevron.set_icon("chevron-right")
        return self

    def open_in_drawer(self, drawer: Any = None) -> Self:
        """Open this artifact in an attached ArtifactViewerDrawer."""
        target_drawer = drawer or self.drawer
        if target_drawer is not None:
            target_drawer.load_artifact(
                title=self.title,
                content=self.content,
                language=self.language,
                diff_content=self.diff_content,
                artifact_type=self.artifact_type,
                size_bytes=self.size_bytes,
            )
            target_drawer.open()
        if self.on_open_callback:
            self.on_open_callback()
        return self

    async def copy(self) -> None:
        """Copy artifact content to clipboard."""
        safe_code = (
            self.content.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
        )
        await ui.run_javascript(f"navigator.clipboard.writeText(`{safe_code}`)")
        ui.notify("Artifact copied to clipboard", type="positive", timeout=1200)
