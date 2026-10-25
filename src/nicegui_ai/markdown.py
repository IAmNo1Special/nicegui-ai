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
        self._rendered_blocks: list[dict[str, Any]] = []
        self._elements: list[ui.markdown | CodeBlock] = []
        self.set_content(content)

    @property
    def content(self) -> str:
        return self._content

    def set_content(self, content: str) -> None:
        """Update markdown content incrementally without rebuilding unchanged blocks."""
        self._content = content
        new_blocks = parse_markdown_blocks(content)

        common_len = min(len(self._rendered_blocks), len(new_blocks))
        can_patch = True
        for i in range(common_len):
            old_b = self._rendered_blocks[i]
            new_b = new_blocks[i]
            if old_b["type"] != new_b["type"]:
                can_patch = False
                break
            if old_b["type"] == "code" and (
                old_b.get("language") != new_b.get("language")
                or old_b.get("filename") != new_b.get("filename")
            ):
                can_patch = False
                break

        if can_patch and len(self._rendered_blocks) <= len(new_blocks):
            # Update existing blocks in place
            for i in range(common_len):
                old_b = self._rendered_blocks[i]
                new_b = new_blocks[i]
                el = self._elements[i]
                if old_b != new_b:
                    if new_b["type"] == "text" and isinstance(el, ui.markdown):
                        el.set_content(new_b["content"])
                    elif new_b["type"] == "code" and isinstance(el, CodeBlock):
                        el.set_code(new_b["code"])
                    self._rendered_blocks[i] = new_b

            # Append new blocks
            with self:
                for j in range(common_len, len(new_blocks)):
                    b = new_blocks[j]
                    if b["type"] == "text":
                        nel = ui.markdown(b["content"]).classes(
                            "text-sm text-gray-200 prose prose-invert max-w-none leading-relaxed"
                        )
                        self._elements.append(nel)
                    elif b["type"] == "code":
                        c_el = CodeBlock(
                            code=b["code"],
                            language=b["language"],
                            filename=b.get("filename"),
                            line_numbers=True,
                        )
                        self._elements.append(c_el)
                    self._rendered_blocks.append(b)
        else:
            # Full re-render when structure has changed
            self.clear()
            self._rendered_blocks = []
            self._elements = []
            with self:
                for b in new_blocks:
                    if b["type"] == "text":
                        tel = ui.markdown(b["content"]).classes(
                            "text-sm text-gray-200 prose prose-invert max-w-none leading-relaxed"
                        )
                        self._elements.append(tel)
                    elif b["type"] == "code":
                        c_el = CodeBlock(
                            code=b["code"],
                            language=b["language"],
                            filename=b.get("filename"),
                            line_numbers=True,
                        )
                        self._elements.append(c_el)
                    self._rendered_blocks.append(b)
