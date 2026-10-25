"""AG-UI stream adapters for OpenRouter, Gemini, OpenCode, and native AG-UI sources."""

from nicegui_ai.adapters.agui import AgUiStreamAdapter
from nicegui_ai.adapters.base import BaseStreamAdapter
from nicegui_ai.adapters.gemini import GeminiStreamAdapter
from nicegui_ai.adapters.opencode import OpenCodeStreamAdapter
from nicegui_ai.adapters.openrouter import OpenRouterStreamAdapter

__all__ = [
    "AgUiStreamAdapter",
    "BaseStreamAdapter",
    "GeminiStreamAdapter",
    "OpenCodeStreamAdapter",
    "OpenRouterStreamAdapter",
]
