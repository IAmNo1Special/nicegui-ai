# Isolated `nicegui_ai.antigravity` Subpackage for 1:1 Antigravity Desktop Parity

## Context

`nicegui-ai` originally provided 17 ambient glassmorphic primitives (`AiComposer`, `AiThread`, `FloatingHeader`, `SlideOverDrawer`, `ArtifactViewerDrawer`, etc.) modeled on `assistant-ui` and the Vercel AI SDK with a `#0d1017` purple/slate palette. We now also need a 100% 1-to-1 Python + NiceGUI reconstruction of the Google Antigravity desktop application (`/home/vanluther/Downloads/Antigravity/Antigravity-x64/antigravity`), which uses a distinct monochrome token system (`#101010` background, `#151515` sidebar, `#191919` card, `#222222` border), persistent 256px left `Sidebar`, 35px native `TitleBar`, multi-view center router (`ChatView`, `ZeroStateHome`, `ConversationHistoryView`, `AutomationsView`, `WorkspaceCustomizationsView`), 6-tab `AuxiliaryPane`, and 2-column 13-screen `SettingsModal`.

## Decision

We house the complete 1:1 Antigravity desktop reconstruction in a dedicated `nicegui_ai.antigravity` subpackage while keeping the root `nicegui_ai` (`assistant-ui`) primitives and their `#0d1017` purple theme intact:

1. **Coexistence without Breaking Changes**: Existing imports (`from nicegui_ai import AiComposer, AiThread, ...`) and existing unit/integration tests continue to pass without modification.
2. **Shared Streaming Adapters**: `nicegui_ai.antigravity` reuses `nicegui_ai.adapters` (`GeminiStreamAdapter`, `OpenRouterStreamAdapter`, `OpenCodeStreamAdapter`) to drive live streaming turns, reasoning steps, tool call executions, and turn branching inside Antigravity conversations.
3. **Dedicated CLI Entrypoints & Gallery Integration**: `pyproject.toml` exposes `nicegui-antigravity` and `nicegui-ai-antigravity` (`nicegui_ai.antigravity.app:main`) alongside `nicegui-ai` (`gallery.py`) and `nicegui-ai-demo` (`demo.py`), and `gallery.py` includes a dedicated Antigravity 1:1 showcase section.
4. **Deterministic URL Query Parameter Verification**: `nicegui_ai.antigravity.app` supports the exact 26 URL query parameter states used in our React/CDP verification suite so headless Chromium (`scripts/capture_screenshots.py`) and `pytest` can verify every view, modal, tab, and popover to 100% parity.
