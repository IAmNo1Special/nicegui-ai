# Interactive Artifact Viewer Drawer and Message Turn Branching

## Context

In complex AI agent applications, agents generate both conversational explanations and tangible artifacts (code files, schema definitions, markdown reports, architecture diagrams). Users need to inspect these generated products in-depth without cluttering the main conversation thread.

Furthermore, autonomous workflows and iterative user prompts often require exploring alternative generation branches:
- Retrying an agent completion with a different model or prompt configuration.
- Branching a conversational turn to compare multiple problem-solving approaches side by side.
- Maintaining isolated state (reasoning chains, tool calls, and token metrics) for each branch variation without corrupting the DOM or message history.

## Decision

1. **Interactive Artifact Viewer Drawer (`ArtifactViewerDrawer`)**:
   - Subclasses `SlideOverDrawer` with an off-canvas drawer anchored on the right viewport margin (`w-[540px] max-w-full`).
   - Implements tabbed multi-mode inspection:
     - **Code Tab**: Full-height syntax-highlighted code container with line numbers and a 1-click clipboard copy button.
     - **Live Render Tab**: Renders Mermaid diagrams dynamically (`ui.mermaid`), HTML/SVG elements (`ui.html`), or formatted Markdown (`AiMarkdown`).
     - **Unified Diff Tab**: Displays +/- line changes with added/removed line count badges and highlighted color styling.
   - `ArtifactCard` exposes an `open_in_drawer()` method and an expand button in its header to launch `ArtifactViewerDrawer` seamlessly.

2. **Message Turn Branching (`MessageBranch` & `BranchPicker`)**:
   - Defined `MessageBranch` dataclass encapsulating `index`, `text`, `reasoning`, `tool_calls`, and `tokens_used`.
   - `UserMessage`: Tracks `branches: list[str]`, supporting `add_branch()` and `switch_branch(index)`.
   - `AgentMessage`: Tracks `branches: list[MessageBranch]`, automatically synchronizing active branch text, dynamically attached `ToolCall` items, streamed reasoning chains, and token metrics.
   - Reactive switching (`switch_branch(index)`):
     - Clears and reconstructs sub-containers (`reasoning_container`, `tools_container`) cleanly.
     - Updates `markdown` content and `token_pill` badge.
     - Updates `BranchPicker` navigation state (`< current / total >`).
   - Integrated `fork()` method and a `git-branch` action button in the message footer, triggering `on_fork(message, new_index)` to stream alternative completions into new branches.

## Considered Options

- **Modal Dialog for Artifacts**: Modals block the conversation view and cannot be kept open side-by-side while authoring next prompts in the composer.
- **In-place Version Swapping without Branch State**: Loses tool call results and reasoning steps from previous attempts when toggling between variations.
- **Dedicated ArtifactViewerDrawer + MessageBranch Dataclass**: Provides rich, non-blocking side-by-side inspection and clean encapsulation of state per turn variation with 100% OOP structure.
