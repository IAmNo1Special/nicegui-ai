"""Lucide outline SVG icons for modern AI agent interfaces."""

from nicegui import ui

LUCIDE_SVG_NODES: dict[str, str] = {
    "sparkles": (
        '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962'
        "L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5"
        "A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437"
        'l-1.582 6.135a.5.5 0 0 1-.963 0z" />'
        '<path d="M20 3v4" /><path d="M22 5h-4" /><path d="M4 17v2" /><path d="M5 18H3" />'
    ),
    "brain": (
        '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z" />'
        '<path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z" />'
        '<path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4" />'
        '<path d="M17.599 6.5a3 3 0 0 0-.399-1.375" />'
        '<path d="M6.003 5.125A3 3 0 0 0 6.401 6.5" />'
        '<path d="M3.477 10.896a4 4 0 0 1 .585-.396" />'
        '<path d="M19.938 10.5a4 4 0 0 1 .585.396" />'
        '<path d="M6 18a4 4 0 0 1-1.967-.516" />'
        '<path d="M19.967 17.484A4 4 0 0 1 18 18" />'
    ),
    "brain-circuit": (
        '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z" />'
        '<path d="M9 13a4.5 4.5 0 0 0 3-4" />'
        '<path d="M6.003 5.125A3 3 0 0 0 6.401 6.5" />'
        '<path d="M3.477 10.896a4 4 0 0 1 .585-.396" />'
        '<path d="M6 18a4 4 0 0 1-1.967-.516" />'
        '<path d="M12 13h4" />'
        '<path d="M12 18h6a2 2 0 0 1 2 2v1" />'
        '<path d="M12 8h8" />'
        '<path d="M16 8V5a2 2 0 0 1 2-2" />'
        '<circle cx="16" cy="13" r=".5" />'
        '<circle cx="18" cy="3" r=".5" />'
        '<circle cx="20" cy="21" r=".5" />'
        '<circle cx="20" cy="8" r=".5" />'
    ),
    "scroll": (
        '<path d="M19 17V5a2 2 0 0 0-2-2H4" />'
        '<path d="M8 21h12a2 2 0 0 0 2-2v-1a1 1 0 0 0-1-1H11a1 1 0 0 0-1 1v1a2 2 0 1 1-4 0V5a2 2 0 1 0-4 0v2a1 1 0 0 0 1 1h3" />'
    ),
    "gauge": ('<path d="m12 14 4-4" /><path d="M3.34 19a10 10 0 1 1 17.32 0" />'),
    "history": (
        '<path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />'
        '<path d="M3 3v5h5" />'
        '<path d="M12 7v5l4 2" />'
    ),
    "git-commit": (
        '<circle cx="12" cy="12" r="3" />'
        '<line x1="3" x2="9" y1="12" y2="12" />'
        '<line x1="15" x2="21" y1="12" y2="12" />'
    ),
    "check-circle": ('<circle cx="12" cy="12" r="10" /><path d="m9 12 2 2 4-4" />'),
    "clock": (
        '<circle cx="12" cy="12" r="10" /><polyline points="12 6 12 12 16 14" />'
    ),
    "terminal": (
        '<polyline points="4 17 10 11 4 5" /><line x1="12" x2="20" y1="19" y2="19" />'
    ),
    "file-code": (
        '<path d="M10 12.5 8 15l2 2.5" />'
        '<path d="m14 12.5 2 2.5-2 2.5" />'
        '<path d="M14 2v4a2 2 0 0 0 2 2h4" />'
        '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7z" />'
    ),
    "shield-alert": (
        '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1'
        'c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z" />'
        '<path d="M12 8v4" />'
        '<path d="M12 16h.01" />'
    ),
    "chevron-down": '<path d="m6 9 6 6 6-6" />',
    "chevron-right": '<path d="m9 18 6-6-6-6" />',
    "chevron-left": '<path d="m15 18-6-6 6-6" />',
    "copy": (
        '<rect width="14" height="14" x="8" y="8" rx="2" ry="2" />'
        '<path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" />'
    ),
    "check": '<path d="M20 6 9 17l-5-5" />',
    "download": (
        '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />'
        '<polyline points="7 10 12 15 17 10" />'
        '<line x1="12" x2="12" y1="15" y2="3" />'
    ),
    "external-link": (
        '<path d="M15 3h6v6" /><path d="M10 14 21 3" />'
        '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />'
    ),
    "arrow-up": ('<path d="m5 12 7-7 7 7" /><path d="M12 19V5" />'),
    "square": '<rect width="18" height="18" x="3" y="3" rx="2" fill="currentColor" />',
    "user": (
        '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />'
        '<circle cx="12" cy="7" r="4" />'
    ),
    "bot": (
        '<path d="M12 8V4H8" />'
        '<rect width="16" height="12" x="4" y="8" rx="2" />'
        '<path d="M2 14h2" />'
        '<path d="M20 14h2" />'
        '<path d="M15 13v2" />'
        '<path d="M9 13v2" />'
    ),
    "zap": (
        '<path d="M4 14a1 1 0 0 1-.78-1.63l9.9-10.2a.5.5 0 0 1 .86.46l-1.92 6.02'
        'A1 1 0 0 0 13 10h7a1 1 0 0 1 .78 1.63l-9.9 10.2a.5.5 0 0 1-.86-.46l1.92-6.02A1 1 0 0 0 11 14z" />'
    ),
    "x": '<path d="M18 6 6 18" /><path d="m6 6 12 12" />',
    "wand": (
        '<path d="m21.64 3.64-1.28-1.28a1.21 1.21 0 0 0-1.72 0L2.36 18.64a1.21 1.21 0 0 0 0 1.72'
        'l1.28 1.28a1.2 1.2 0 0 0 1.72 0L21.64 5.36a1.2 1.2 0 0 0 0-1.72" />'
        '<path d="m14 7 3 3" />'
        '<path d="M5 6v4" />'
        '<path d="M19 14v4" />'
        '<path d="M10 2v2" />'
        '<path d="M7 8H3" />'
    ),
    "mic": (
        '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />'
        '<path d="M19 10v2a7 7 0 0 1-14 0v-2" />'
        '<line x1="12" x2="12" y1="19" y2="22" />'
    ),
    "volume-2": (
        '<polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5" />'
        '<path d="M15.54 8.46a5 5 0 0 1 0 7.07" />'
        '<path d="M19.07 4.93a10 10 0 0 1 0 14.14" />'
    ),
    "sliders": (
        '<line x1="4" x2="4" y1="21" y2="14" /><line x1="4" x2="4" y1="10" y2="3" />'
        '<line x1="12" x2="12" y1="21" y2="12" /><line x1="12" x2="12" y1="8" y2="3" />'
        '<line x1="20" x2="20" y1="21" y2="16" /><line x1="20" x2="20" y1="12" y2="3" />'
        '<line x1="1" x2="7" y1="14" y2="14" /><line x1="9" x2="15" y1="8" y2="8" /><line x1="17" x2="23" y1="16" y2="16" />'
    ),
    "arrow-right": '<path d="M5 12h14" /><path d="m12 5 7 7-7 7" />',
    "pencil": (
        '<path d="M21.174 6.812a1 1 0 0 0-3.986-3.987L3.842 16.174a2 2 0 0 0-.5.83l-1.321 4.352a.5.5 0 0 0 .623.622l4.353-1.32a2 2 0 0 0 .83-.497z" />'
        '<path d="m15 5 4 4" />'
    ),
    "trash": (
        '<path d="M3 6h18" /><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />'
        '<path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />'
        '<line x1="10" x2="10" y1="11" y2="17" /><line x1="14" x2="14" y1="11" y2="17" />'
    ),
    "plus": '<path d="M5 12h14" /><path d="M12 5v14" />',
    "chevron-up": '<path d="m18 15-6-6-6 6" />',
    "loader": '<path d="M21 12a9 9 0 1 1-6.219-8.56" />',
    "thumbs-up": (
        '<path d="M7 10v12" /><path d="M15 5.88 14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a3.13 3.13 0 0 1 3 3.88Z" />'
    ),
    "thumbs-down": (
        '<path d="M17 14V2" /><path d="M9 18.12 10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 22a3.13 3.13 0 0 1-3-3.88Z" />'
    ),
}

# Synonyms
LUCIDE_SVG_NODES["wand-2"] = LUCIDE_SVG_NODES["wand"]
LUCIDE_SVG_NODES["circle-check"] = LUCIDE_SVG_NODES["check-circle"]
LUCIDE_SVG_NODES["commit"] = LUCIDE_SVG_NODES["git-commit"]
LUCIDE_SVG_NODES["edit"] = LUCIDE_SVG_NODES["pencil"]
LUCIDE_SVG_NODES["edit-2"] = LUCIDE_SVG_NODES["pencil"]
LUCIDE_SVG_NODES["trash-2"] = LUCIDE_SVG_NODES["trash"]
LUCIDE_SVG_NODES["loader-2"] = LUCIDE_SVG_NODES["loader"]


def get_lucide_svg(
    name: str,
    size: int = 16,
    stroke_width: float = 2.0,
    classes: str = "",
) -> str:
    """Render a standalone Lucide SVG string."""
    inner = LUCIDE_SVG_NODES.get(name, LUCIDE_SVG_NODES["sparkles"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" class="{classes}">{inner}</svg>'
    )


class LucideIcon(ui.html):
    """Lucide outline SVG icon component matching contemporary AI developer tooling."""

    def __init__(
        self,
        name: str,
        size: int = 16,
        stroke_width: float = 2.0,
        classes: str = "",
    ) -> None:
        self.icon_name = name
        self.size = size
        self.stroke_width = stroke_width
        self.extra_classes = classes
        super().__init__()
        self.classes("inline-flex items-center justify-center shrink-0 leading-none")
        self.set_icon(name, size, stroke_width, classes)

    def set_icon(
        self,
        name: str,
        size: int | None = None,
        stroke_width: float | None = None,
        classes: str | None = None,
    ) -> None:
        """Update the rendered SVG icon."""
        self.icon_name = name
        if size is not None:
            self.size = size
        if stroke_width is not None:
            self.stroke_width = stroke_width
        if classes is not None:
            self.extra_classes = classes
        self.content = get_lucide_svg(
            self.icon_name,
            size=self.size,
            stroke_width=self.stroke_width,
            classes=self.extra_classes,
        )
