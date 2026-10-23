"""Ambient dark styling and theme helpers for nicegui-ai."""

from nicegui import ui

THEME_CSS = """
:root {
  --ai-bg: #0d1017;
  --ai-surface: #161c26;
  --ai-card: #121620;
  --ai-border: rgba(55, 65, 81, 0.7);
  --ai-primary: #8b5cf6;
  --ai-amber: #eab308;
  --ai-cyan: #06b6d4;
  --ai-emerald: #10b981;
}

body {
  background-color: var(--ai-bg) !important;
  color: #e6edf3 !important;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
  overflow: hidden;
}

/* Custom dark scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #252d3d;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #364156;
}

/* Prose markdown tweaks */
.nicegui-markdown {
  font-size: 0.8125rem !important;
  line-height: 1.625 !important;
  color: #e2e8f0 !important;
}

.nicegui-markdown p {
  margin-bottom: 0.5rem !important;
}

.nicegui-markdown p:last-child {
  margin-bottom: 0 !important;
}

.nicegui-markdown pre {
  background-color: #0b0e14 !important;
  border: 1px solid rgba(55, 65, 81, 0.6) !important;
  border-radius: 0.5rem !important;
  padding: 0.75rem !important;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  font-size: 0.75rem !important;
}

.nicegui-markdown code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
  background-color: rgba(30, 41, 59, 0.7) !important;
  color: #c084fc !important;
  padding: 0.1rem 0.3rem !important;
  border-radius: 0.25rem !important;
}
"""


def setup_ai_theme() -> None:
    """Inject the dark ambient theme styles and scrollbars into NiceGUI."""
    ui.add_head_html(f"<style>{THEME_CSS}</style>")
    ui.query("body").classes("bg-[#0d1017] text-gray-100 antialiased")
