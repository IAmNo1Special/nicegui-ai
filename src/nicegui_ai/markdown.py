"""AI-enhanced Markdown renderer with native CodeBlock integration."""

import re
from typing import Any

from nicegui import ui

from nicegui_ai.code_block import CodeBlock


def parse_markdown_blocks(text: str) -> list[dict[str, Any]]:
    """Parse markdown text into sequential text blocks and code fence blocks.

    Handles language tags, optional filename annotations (e.g. ```python:main.py),
    and unclosed code fences during active streaming.
    """
    blocks: list[dict[str, Any]] = []
    # Regex to match code fences ```[lang][:filename] ... ```
    pattern = re.compile(
        r"```([a-zA-Z0-9_\-\.]+)?(?::([a-zA-Z0-9_\-\.\/]+))?\n([\s\S]*?)(?:\n```|\Z)"
    )

    last_end = 0
    for match in pattern.finditer(text):
        start, end = match.span()

        # Preceding text
        if start > last_end:
            prefix = text[last_end:start]
            if prefix.strip():
                blocks.append({"type": "text", "content": prefix})

        raw_lang = match.group(1) or "text"
        filename = match.group(2)
        code = match.group(3)

        # Handle filename in lang tag like ```python filename=test.py
        if " filename=" in raw_lang:
            parts = raw_lang.split(" filename=")
            raw_lang = parts[0]
            filename = parts[1]

        blocks.append(
            {
                "type": "code",
                "language": raw_lang.strip(),
                "filename": filename.strip() if filename else None,
                "code": code.rstrip("\n"),
            }
        )
        last_end = end

    # Remaining text
    if last_end < len(text):
        suffix = text[last_end:]
        if suffix.strip():
            blocks.append({"type": "text", "content": suffix})

    # If empty, return single empty text block
    if not blocks:
        blocks.append({"type": "text", "content": text})

    return blocks


class AiMarkdown(ui.element):
    """Modern AI markdown renderer that transforms fenced code into first-class CodeBlocks."""

    def __init__(self, content: str = "", classes: str = "") -> None:
        super().__init__("div")
        self.classes(f"w-full flex flex-col gap-3 leading-relaxed {classes}")
        self._content = content
        self._render()

    @property
    def content(self) -> str:
        return self._content

    def set_content(self, content: str) -> None:
        """Update markdown content, re-parsing text and code blocks."""
        self._content = content
        self.clear()
        self._render()

    def _render(self) -> None:
        blocks = parse_markdown_blocks(self._content)
        with self:
            for block in blocks:
                if block["type"] == "text":
                    ui.markdown(block["content"]).classes(
                        "text-sm text-gray-200 prose prose-invert max-w-none leading-relaxed"
                    )
                elif block["type"] == "code":
                    CodeBlock(
                        code=block["code"],
                        language=block["language"],
                        filename=block.get("filename"),
                        line_numbers=True,
                    )
