"""Polished code block primitive with language header, filename, and copy button."""

from nicegui import ui

from nicegui_ai.icons import LucideIcon


class CodeBlock(ui.element):
    """Polished code block component with language tag, filename, and copy button."""

    def __init__(
        self,
        code: str,
        language: str = "text",
        filename: str | None = None,
        line_numbers: bool = False,
    ) -> None:
        super().__init__("div")
        self.code = code
        self.language = language
        self.filename = filename
        self.line_numbers = line_numbers

        self.classes(
            "w-full rounded-xl border border-gray-800 bg-[#0a0d14] "
            "overflow-hidden text-xs my-2 shadow-md"
        )

        with self:
            # Header Bar
            with ui.row().classes(
                "items-center justify-between w-full px-3 py-1.5 bg-[#121620] "
                "border-b border-gray-800/80 text-[11px]"
            ):
                with ui.row().classes("items-center gap-2 font-mono"):
                    LucideIcon("file-code", size=13, classes="text-purple-400")
                    if filename:
                        ui.label(filename).classes("text-gray-200 font-semibold")
                        ui.label(f"({language})").classes("text-gray-500 text-[10px]")
                    else:
                        ui.label(language).classes(
                            "text-gray-300 font-semibold uppercase text-[10px]"
                        )

                # Copy button with feedback
                with (
                    ui.element("button")
                    .classes(
                        "flex items-center gap-1 text-[11px] font-mono text-gray-400 hover:text-white "
                        "px-2 py-0.5 rounded hover:bg-gray-800 transition-colors cursor-pointer border-none bg-transparent"
                    )
                    .on("click", self.copy)
                ) as self.copy_btn:
                    self.copy_icon = LucideIcon(
                        "copy", size=12, classes="text-gray-400"
                    )
                    self.copy_label = ui.label("Copy")

            # Code container
            with ui.element("pre").classes(
                "p-3 overflow-x-auto font-mono text-[11px] leading-relaxed text-gray-200 w-full select-text m-0"
            ):
                if line_numbers:
                    lines = self.code.split("\n")
                    pad = len(str(len(lines)))
                    for i, line in enumerate(lines, 1):
                        with ui.row().classes("gap-3 no-wrap"):
                            ui.label(f"{i:>{pad}}").classes(
                                "text-gray-600 select-none font-mono"
                            )
                            ui.label(line).classes(
                                "font-mono text-inherit whitespace-pre"
                            )
                else:
                    ui.label(self.code).classes("font-mono whitespace-pre text-inherit")

    async def copy(self) -> None:
        """Copy the code contents to the system clipboard with visual feedback."""
        safe_code = (
            self.code.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")
        )
        await ui.run_javascript(f"navigator.clipboard.writeText(`{safe_code}`)")
        self.copy_icon.set_icon("check", classes="text-emerald-400")
        self.copy_label.set_text("Copied!")
        self.copy_label.classes(add="text-emerald-400")
        ui.notify("Copied to clipboard", type="positive", position="top", timeout=1200)
