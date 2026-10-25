"""Floating ambient header dock and circular SVG token gauge."""

from nicegui import ui

from nicegui_ai.icons import LucideIcon


class TokenRing(ui.element):
    """Circular SVG progress ring visualizing token consumption and budget limits."""

    def __init__(
        self,
        used: int = 0,
        limit: int = 128000,
        size: int = 24,
        stroke_width: float = 2.5,
        color: str = "#8b5cf6",
    ) -> None:
        super().__init__("div")
        self.used = used
        self.limit = max(limit, 1)
        self.size = size
        self.stroke_width = stroke_width
        self.color = color

        self.classes("relative flex items-center justify-center shrink-0")
        self.style(f"width: {size}px; height: {size}px;")
        with self:
            self.svg_html = ui.html().classes("w-full h-full -rotate-90 block")
            with ui.element("div").classes(
                "absolute inset-0 flex items-center justify-center pointer-events-none"
            ):
                self.icon = LucideIcon(
                    "sparkles",
                    size=max(size // 2, 10),
                    classes="text-purple-300",
                )

        self.update_progress(used, limit)

    def update_progress(self, used: int, limit: int | None = None) -> None:
        """Update the rendered SVG ring with new usage values."""
        self.used = used
        if limit is not None:
            self.limit = max(limit, 1)

        percentage = min(max(self.used / self.limit, 0.0), 1.0)
        radius = (self.size - self.stroke_width) / 2
        circumference = 2 * 3.1415926535 * radius
        offset = circumference - (circumference * percentage)
        center = self.size / 2

        svg = (
            f'<svg width="{self.size}" height="{self.size}" viewBox="0 0 {self.size} {self.size}">'
            f'<circle cx="{center}" cy="{center}" r="{radius}" '
            f'stroke="#1f2937" stroke-width="{self.stroke_width}" fill="none" />'
            f'<circle cx="{center}" cy="{center}" r="{radius}" '
            f'stroke="{self.color}" stroke-width="{self.stroke_width}" '
            f'stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" '
            f'stroke-linecap="round" fill="none" style="transition: stroke-dashoffset 0.4s ease;" />'
            f"</svg>"
        )
        self.svg_html.content = svg


class FloatingHeader(ui.element):
    """Ambient glassmorphism header pill floating at the top of the viewport."""

    def __init__(
        self,
        agent_name: str = "Agent",
        model: str = "default",
        tokens_used: int = 0,
        token_limit: int = 128000,
    ) -> None:
        super().__init__("header")
        self.agent_name = agent_name
        self.model = model
        self.classes(
            "fixed top-4 left-1/2 -translate-x-1/2 z-40 "
            "flex items-center gap-3 px-4 py-2 "
            "bg-[#161c26]/90 backdrop-blur-xl border border-gray-700/60 "
            "rounded-full shadow-2xl ring-1 ring-white/5 text-xs text-gray-200"
        )

        with self:
            # Slot container for custom left actions (e.g. Sessions / History button)
            self.left_container = ui.row().classes("items-center gap-1.5")

            ui.element("div").classes("h-4 w-[1px] bg-gray-700")

            # Center identity & circular token gauge
            with ui.row().classes("items-center gap-2 px-1"):
                self.token_ring = TokenRing(used=tokens_used, limit=token_limit)

                with ui.column().classes("gap-0 leading-tight text-left"):
                    with ui.row().classes("items-center gap-1.5"):
                        self.agent_label = ui.label(agent_name).classes(
                            "font-semibold text-xs text-white"
                        )
                        self.model_badge = ui.label(model).classes(
                            "text-[10px] bg-purple-950/80 text-purple-300 "
                            "border border-purple-500/30 px-1.5 py-0.2 rounded font-mono"
                        )
                    self.tokens_label = ui.label(
                        f"{tokens_used:,} / {token_limit:,} tokens"
                    ).classes("text-[10px] text-gray-400 font-mono -mt-0.5")

            ui.element("div").classes("h-4 w-[1px] bg-gray-700")

            # Slot container for custom right actions (e.g. Canvas / Settings button)
            self.right_container = ui.row().classes("items-center gap-1.5")

    def update_tokens(self, used: int, limit: int | None = None) -> None:
        """Update token ring and label."""
        self.token_ring.update_progress(used, limit)
        curr_limit = limit if limit is not None else self.token_ring.limit
        self.tokens_label.set_text(f"{used:,} / {curr_limit:,} tokens")

    def set_model(self, model: str) -> None:
        """Update displayed model name in badge."""
        self.model = model
        self.model_badge.set_text(model)

    def set_agent_name(self, name: str) -> None:
        """Update displayed agent name."""
        self.agent_name = name
        self.agent_label.set_text(name)
