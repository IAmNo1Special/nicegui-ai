# Context Map

## Contexts

- [Assistant-UI Primitives](./CONTEXT.md) — ambient glassmorphic AI chat, reasoning, tool execution, and streaming primitives (`nicegui_ai`)
- [Antigravity Desktop Clone](./src/nicegui_ai/antigravity/CONTEXT.md) — 1:1 desktop UI/UX clone of Google Antigravity built in Python and NiceGUI (`nicegui_ai.antigravity`)

## Relationships

- **Assistant-UI Primitives → Antigravity Desktop Clone**: `nicegui_ai.antigravity` consumes `BaseStreamAdapter`, `GeminiStreamAdapter`, `OpenRouterStreamAdapter`, and `OpenCodeStreamAdapter` (`nicegui_ai.adapters`) to stream normalized AG-UI events into Antigravity conversation turns.
- **Assistant-UI Primitives ↔ Antigravity Desktop Clone**: Both contexts coexist inside the `nicegui-ai` package with isolated theme tokens (`#0d1017` ambient purple vs. `#101010` / `#151515` / `#191919` Antigravity monochrome), showcased side by side in `nicegui_ai.gallery`.
