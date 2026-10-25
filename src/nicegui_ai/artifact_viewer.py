"""Interactive artifact viewer drawer with Code, Live Render, and Unified Diff tabs."""

from collections.abc import Callable
from typing import Any, Self

from nicegui import ui

from nicegui_ai.code_block import CodeBlock
from nicegui_ai.drawer import SlideOverDrawer
from nicegui_ai.icons import LucideIcon
from nicegui_ai.markdown import AiMarkdown


class ArtifactViewerDrawer(SlideOverDrawer):
    """Off-canvas inspection drawer for artifacts featuring Code, Live Render, and Diff views.

    Features:
    - Code tab: syntax-highlighted code block with line numbers and clipboard copy.
    - Live Render tab: live HTML, SVG, Mermaid diagram, or Markdown document rendering.
    - Unified Diff tab: colorized patch viewer highlighting additions and deletions.
    - Export / download action triggers and tab switching state.
    """

    def __init__(
        self,
        title: str = "Artifact Viewer",
        side: str = "right",
        width_px: int = 680,
        on_download: Callable[[str, str], Any] | None = None,
    ) -> None:
        super().__init__(
            title=title,
            icon="file-code",
            side=side,
            width_px=width_px,
        )
        self.on_download_callback = on_download

        # Active artifact state
        self.artifact_title: str = ""
        self.artifact_type: str = "file"
        self.artifact_content: str = ""
        self.language: str = "text"
        self.diff_content: str | None = None
        self.size_bytes: int | None = None
        self.active_tab: str = "code"  # 'code' | 'preview' | 'diff'

        # Build custom tabbed drawer body
        with self.content:
            # Tab bar container
            with ui.row().classes(
                "items-center justify-between w-full pb-2 border-b border-gray-800 shrink-0"
            ):
                with ui.row().classes(
                    "p-0.5 rounded-lg bg-[#0e121a] border border-gray-800 gap-1 text-xs"
                ) as self.tab_buttons_row:
                    self.tab_btns: dict[str, Any] = {}
                    for tab_key, tab_label, tab_icon in [
                        ("code", "Code", "code"),
                        ("preview", "Preview", "eye"),
                        ("diff", "Diff", "git-commit"),
                    ]:
                        btn = (
                            ui.element("button")
                            .classes(
                                "flex items-center gap-1.5 px-3 py-1 rounded-md font-medium "
                                "text-gray-400 hover:text-white transition-colors cursor-pointer border-none bg-transparent"
                            )
                            .on("click", lambda _e, k=tab_key: self.set_tab(k))
                        )
                        with btn:
                            LucideIcon(tab_icon, size=13, classes="shrink-0")
                            ui.label(tab_label)
                        self.tab_btns[tab_key] = btn

                # Actions bar (copy & download)
                with ui.row().classes("items-center gap-1.5 shrink-0"):
                    self.type_badge = ui.label("FILE").classes(
                        "text-[9px] font-mono bg-purple-950/80 text-purple-300 "
                        "border border-purple-500/30 px-2 py-0.5 rounded uppercase"
                    )

                    with (
                        ui.element("button")
                        .classes(
                            "flex items-center gap-1 text-[11px] font-mono text-gray-400 hover:text-white "
                            "px-2 py-1 rounded bg-[#161c28] hover:bg-gray-800 border border-gray-800 transition-colors cursor-pointer"
                        )
                        .on("click", self.copy_content)
                    ):
                        LucideIcon("copy", size=12, classes="text-gray-400")
                        ui.label("Copy")

                    with (
                        ui.element("button")
                        .classes(
                            "flex items-center gap-1 text-[11px] font-mono text-gray-400 hover:text-white "
                            "px-2 py-1 rounded bg-[#161c28] hover:bg-gray-800 border border-gray-800 transition-colors cursor-pointer"
                        )
                        .on("click", self._trigger_download)
                    ):
                        LucideIcon("download", size=12, classes="text-gray-400")
                        ui.label("Download")

            # Dynamic tab viewport
            self.viewport = ui.column().classes("w-full flex-1 min-h-0 pt-2")

        self._update_tab_styles()

    def load_artifact(
        self,
        title: str,
        content: str,
        language: str = "text",
        diff_content: str | None = None,
        artifact_type: str = "file",
        size_bytes: int | None = None,
        default_tab: str | None = None,
    ) -> Self:
        """Load an artifact into the viewer drawer and render its views."""
        self.artifact_title = title
        self.artifact_content = content
        self.language = language
        self.diff_content = diff_content
        self.artifact_type = artifact_type
        self.size_bytes = size_bytes

        # Update drawer title and badge
        self.type_badge.set_text(artifact_type.upper())

        # Determine default tab
        if default_tab:
            self.active_tab = default_tab
        elif artifact_type in {"diff", "patch"} or (
            diff_content and not content
        ):
            self.active_tab = "diff"
        elif artifact_type in {"report", "doc", "document"} or language in {
            "html",
            "svg",
            "mermaid",
            "markdown",
        }:
            self.active_tab = "preview"
        else:
            self.active_tab = "code"

        self._render_current_tab()
        return self

    def set_tab(self, tab: str) -> None:
        """Switch active tab between 'code', 'preview', and 'diff'."""
        if tab in {"code", "preview", "diff"}:
            self.active_tab = tab
            self._update_tab_styles()
            self._render_current_tab()

    def _update_tab_styles(self) -> None:
        for tab_key, btn in self.tab_btns.items():
            if tab_key == self.active_tab:
                btn.classes(
                    remove="text-gray-400 hover:text-white bg-transparent",
                    add="text-white bg-purple-600/30 border border-purple-500/40 shadow-sm",
                )
            else:
                btn.classes(
                    remove="text-white bg-purple-600/30 border border-purple-500/40 shadow-sm",
                    add="text-gray-400 hover:text-white bg-transparent",
                )

    def _render_current_tab(self) -> None:
        self.viewport.clear()
        with self.viewport:
            match self.active_tab:
                case "code":
                    self._render_code_tab()
                case "preview":
                    self._render_preview_tab()
                case "diff":
                    self._render_diff_tab()

    def _render_code_tab(self) -> None:
        if not self.artifact_content:
            ui.label("No source code available for this artifact.").classes(
                "text-gray-500 italic p-4 text-xs font-mono"
            )
            return

        CodeBlock(
            code=self.artifact_content,
            language=self.language,
            filename=self.artifact_title,
            line_numbers=True,
        )

    def _render_preview_tab(self) -> None:
        content_lower = self.artifact_content.strip().lower()
        lang_lower = self.language.lower()

        # 1. Mermaid diagram
        if (
            lang_lower == "mermaid"
            or content_lower.startswith("flowchart")
            or content_lower.startswith("graph")
            or content_lower.startswith("sequencediagram")
        ):
            with ui.column().classes(
                "w-full p-4 bg-[#0a0d14] rounded-xl border border-gray-800 overflow-x-auto items-center"
            ):
                ui.mermaid(self.artifact_content)
            return

        # 2. HTML or SVG live render
        if (
            lang_lower in {"html", "svg"}
            or content_lower.startswith("<svg")
            or content_lower.startswith("<!doctype")
            or content_lower.startswith("<html")
        ):
            with ui.column().classes(
                "w-full p-4 bg-white/5 rounded-xl border border-gray-800 overflow-auto"
            ):
                ui.html(self.artifact_content).classes("w-full")
            return

        # 3. Markdown / Report
        if lang_lower in {"md", "markdown"} or self.artifact_type in {
            "report",
            "doc",
            "document",
        }:
            with ui.column().classes(
                "w-full p-4 bg-[#0a0d14] rounded-xl border border-gray-800 overflow-auto"
            ):
                AiMarkdown(self.artifact_content)
            return

        # 4. Fallback formatted preview
        with ui.column().classes(
            "w-full p-4 bg-[#0a0d14] rounded-xl border border-gray-800 font-mono text-xs text-gray-300 overflow-auto whitespace-pre"
        ):
            ui.label(self.artifact_content)

    def _render_diff_tab(self) -> None:
        diff_text = self.diff_content or (
            self.artifact_content
            if self.artifact_type in {"diff", "patch"}
            else ""
        )
        if not diff_text:
            ui.label("No diff or patch data provided for this artifact.").classes(
                "text-gray-500 italic p-4 text-xs font-mono"
            )
            return

        lines = diff_text.strip().split("\n")
        additions = sum(
            1 for line in lines if line.startswith("+") and not line.startswith("+++")
        )
        deletions = sum(
            1 for line in lines if line.startswith("-") and not line.startswith("---")
        )

        with ui.column().classes(
            "w-full rounded-xl border border-gray-800 bg-[#0a0d14] overflow-hidden text-[11px] font-mono leading-relaxed"
        ):
            # Diff summary banner
            with ui.row().classes(
                "items-center justify-between w-full px-3 py-1.5 bg-[#121620] border-b border-gray-800 text-xs"
            ):
                ui.label(self.artifact_title or "Unified Diff").classes(
                    "text-gray-200 font-semibold"
                )
                with ui.row().classes("items-center gap-2 font-mono text-[10px]"):
                    ui.label(f"+{additions}").classes("text-emerald-400 font-bold")
                    ui.label(f"-{deletions}").classes("text-red-400 font-bold")

            # Diff lines container
            with ui.column().classes("w-full overflow-x-auto p-1 gap-0"):
                for line in lines:
                    if line.startswith("@@"):
                        ui.label(line).classes(
                            "w-full px-2 py-0.5 bg-purple-950/40 text-purple-300 font-mono text-[11px]"
                        )
                    elif line.startswith("+") and not line.startswith("+++"):
                        ui.label(line).classes(
                            "w-full px-2 py-0.5 bg-emerald-950/40 text-emerald-300 border-l-2 border-emerald-500 font-mono text-[11px]"
                        )
                    elif line.startswith("-") and not line.startswith("---"):
                        ui.label(line).classes(
                            "w-full px-2 py-0.5 bg-red-950/40 text-red-300 border-l-2 border-red-500 font-mono text-[11px]"
                        )
                    elif line.startswith("---") or line.startswith("+++"):
                        ui.label(line).classes(
                            "w-full px-2 py-0.5 bg-gray-900 text-cyan-300 font-mono font-bold text-[11px]"
                        )
                    else:
                        ui.label(line).classes(
                            "w-full px-2 py-0.5 text-gray-400 font-mono text-[11px]"
                        )

    async def copy_content(self) -> None:
        """Copy active artifact content to system clipboard."""
        target_text = (
            self.diff_content
            if self.active_tab == "diff" and self.diff_content
            else self.artifact_content
        )
        safe_code = (
            target_text.replace("\\", "\\\\")
            .replace("`", "\\`")
            .replace("$", "\\$")
        )
        await ui.run_javascript(f"navigator.clipboard.writeText(`{safe_code}`)")
        ui.notify("Artifact copied to clipboard", type="positive", timeout=1200)

    def _trigger_download(self) -> None:
        if self.on_download_callback:
            self.on_download_callback(self.artifact_title, self.artifact_content)
        else:
            ui.notify(
                f"Preparing download for '{self.artifact_title}'...",
                type="info",
                timeout=1500,
            )
