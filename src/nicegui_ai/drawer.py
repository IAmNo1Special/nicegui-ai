"""Slide-over sheet with soft backdrop blur for sessions, diffs, and artifacts."""

from nicegui import ui

from nicegui_ai.icons import LucideIcon


class SlideOverDrawer(ui.element):
    """Off-canvas drawer sliding in from left or right with backdrop scrim."""

    def __init__(
        self,
        title: str = "Details",
        icon: str = "scroll",
        side: str = "right",
        width_px: int = 420,
    ) -> None:
        super().__init__("div")
        self.title = title
        self.icon_name = icon
        self.side = side
        self.width_px = width_px
        self.is_open = False

        self.classes("fixed inset-0 z-50 pointer-events-none")

        with self:
            # Backdrop scrim
            self.scrim = ui.element("div").classes(
                "fixed inset-0 bg-black/60 backdrop-blur-sm opacity-0 pointer-events-none "
                "transition-opacity duration-300"
            )
            self.scrim.on("click", self.close)

            # Slide-over panel container
            translate_initial = (
                "-translate-x-full" if side == "left" else "translate-x-full"
            )
            alignment_class = (
                "left-0 border-r" if side == "left" else "right-0 border-l"
            )

            self.panel = ui.column().classes(
                f"fixed top-0 bottom-0 {alignment_class} border-gray-800 "
                f"bg-[#121620] shadow-2xl {translate_initial} transition-transform duration-300 "
                "pointer-events-auto flex flex-col h-full z-10 overflow-hidden"
            )
            self.panel.style(f"width: {width_px}px; max-width: 90vw;")

            with self.panel:
                # Header
                with ui.row().classes(
                    "items-center justify-between w-full p-3.5 border-b border-gray-800 "
                    "bg-[#161c28] text-xs font-semibold text-white shrink-0"
                ):
                    with ui.row().classes("items-center gap-2"):
                        LucideIcon(self.icon_name, size=16, classes="text-purple-400")
                        ui.label(self.title).classes("font-bold text-sm tracking-wide")

                    with (
                        ui.element("button")
                        .classes(
                            "text-gray-400 hover:text-white p-1 rounded hover:bg-gray-800 "
                            "transition-colors cursor-pointer"
                        )
                        .on("click", self.close)
                    ):
                        LucideIcon(
                            "x", size=16, classes="text-gray-400 hover:text-white"
                        )

                # Scrollable content area
                self.content = ui.column().classes(
                    "flex-1 w-full p-4 overflow-y-auto space-y-3 text-xs"
                )

    def open(self) -> None:
        """Slide open the drawer."""
        self.is_open = True
        self.classes(remove="pointer-events-none", add="pointer-events-auto")
        self.scrim.classes(
            remove="opacity-0 pointer-events-none",
            add="opacity-100 pointer-events-auto",
        )
        self.panel.classes(
            remove="-translate-x-full translate-x-full", add="translate-x-0"
        )

    def close(self) -> None:
        """Slide closed the drawer."""
        self.is_open = False
        translate_class = (
            "-translate-x-full" if self.side == "left" else "translate-x-full"
        )
        self.scrim.classes(
            remove="opacity-100 pointer-events-auto",
            add="opacity-0 pointer-events-none",
        )
        self.panel.classes(remove="translate-x-0", add=translate_class)
        self.classes(remove="pointer-events-auto", add="pointer-events-none")

    def toggle(self) -> None:
        """Toggle open/closed state."""
        if self.is_open:
            self.close()
        else:
            self.open()
