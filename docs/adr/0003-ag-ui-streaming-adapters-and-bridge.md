# AG-UI Streaming Protocol, Provider Adapters, and StreamBridge

## Context

Streaming agent responses across heterogeneous providers (OpenRouter / OpenAI, Google Gemini SDK, OpenCode, and standard Server-Sent Events) requires handling interleaved chain-of-thought deliberations, streaming tool calls with partial JSON arguments, step transitions, activity updates, and token usage telemetry.

Rather than coupling UI elements directly to proprietary vendor SDK payloads or ad-hoc chunk formats, we adopted the open AG-UI protocol specification (`https://github.com/ag-ui-protocol/ag-ui`) as our normalized streaming event model.

## Decision

1. **Normalized Event Layer (`AgUiEventType` and `AgUiEvent`)**:
   - Implemented in `nicegui_ai.schema` representing all AG-UI lifecycle, text chunk, tool call, reasoning/thought, and activity events.

2. **Strict OOP Adapter Hierarchy (`BaseStreamAdapter`)**:
   - `BaseStreamAdapter(ABC)` defines `stream_events()` and `__aiter__()`, maintaining accumulated state (`text`, `thought`, `tool_calls`, `usage`, `finish_reason`, `error`, `metadata`) and providing a synchronous/asynchronous `collect()` inspection interface.
   - Provider-specific concrete adapters (`AgUiStreamAdapter`, `OpenRouterStreamAdapter`, `GeminiStreamAdapter`, `OpenCodeStreamAdapter`) exhaustively map 100% of provider-emitted events into standardized `AgUiEvent` objects.

3. **Decoupled Reactive UI Driving (`StreamBridge`)**:
   - `StreamBridge` consumes any `BaseStreamAdapter` asynchronously.
   - Dynamically mounts and manages `ReasoningCard` for thought streams, creates/updates `ToolCallCard` with incremental JSON argument streaming (`card.update_args`), streams markdown content into `AgentMessage`, updates `FloatingHeader` token counters, and handles activity progress in `TaskTray`.
   - Exposed as an ergonomic method: `await agent_message.consume(adapter, header=header)`.

## Considered Options

- **Direct Provider Chunk Handling in UI Elements**: High coupling; adding or updating a provider would require modifying every UI component.
- **Generic Generator with Raw Strings**: Drops crucial metadata such as reasoning effort, partial tool call JSON fragments, grounding citations, and usage metrics.
- **AG-UI Protocol with OOP Adapters and StreamBridge**: Clean separation of concerns, 100% adherence to object-oriented principles, testable with hermetic async mock streams, and completely agnostic to the underlying LLM provider.
