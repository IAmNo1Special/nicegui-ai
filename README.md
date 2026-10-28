<p align="center">
  <img src="https://raw.githubusercontent.com/IAmNo1Special/nicegui-ai/main/assets/hero-banner.png" alt="nicegui-ai: Modern AI Agent UI Primitives for Python" width="100%">
</p>

<p align="center">
  <a href="https://pypi.org/project/nicegui-ai/"><img src="https://img.shields.io/pypi/v/nicegui-ai?color=8b5cf6" alt="PyPI - Version"></a>
  <a href="https://github.com/IAmNo1Special/nicegui-ai/actions"><img src="https://github.com/IAmNo1Special/nicegui-ai/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.13+-blue.svg" alt="Python"></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
</p>

<p align="center">
  <b>Modern, production-grade AI agent UI primitives for NiceGUI.</b><br>
  A clean 1:1 Python port of contemporary AI interface patterns (inspired by <code>@assistant-ui/react</code> and Vercel AI SDK).
</p>

<p align="center">
  <a href="#quickstart">Quickstart</a> •
  <a href="#component-catalog">Component Catalog</a> •
  <a href="#antigravity-desktop-ide-11-parity">Antigravity 1:1 Desktop</a> •
  <a href="#live-showcase-demo--component-gallery">Live Showcase</a> •
  <a href="https://pypi.org/project/nicegui-ai/">PyPI</a>
</p>

---

<p align="center">
  <img src="https://raw.githubusercontent.com/IAmNo1Special/nicegui-ai/main/assets/studio-preview.png" alt="nicegui-ai Studio Preview" width="100%">
</p>

---

## Why `nicegui-ai`?

Python has great AI agent engines, but lacks modern, sleek interfaces. Streamlit is static and full-page refreshes, Gradio is rigid, and NiceGUI out of the box only provides basic Quasar chat bubbles (`ui.chat_message`).

`nicegui-ai` fills this gap by providing **pre-styled, high-polish, reactive components** specifically designed for autonomous agents, tool execution, multi-turn reasoning, and human-in-the-loop steering.

* 🔮 **Ambient Glass & Canvas**: Deep dark-mode canvas (`#0d1017`) with spacious centering and floating glassmorphism docks (`backdrop-blur-xl`).
* 🧠 **Reasoning Blocks**: Amber-gilded collapsible reasoning cards displaying live step counts and monospace thoughts.
* ⚡ **Tool Call Cards**: Runic command cards with live status badges (`Executing...`, `Resolved`, `Failed`), collapsible arguments, and interactive Approval Gate buttons (**[Approve]** and **[Veto]**).
* 🔄 **In-Stream Branching**: `< 1 / 3 >` branch pickers to inspect alternative completions or user edits.
* ✍️ **Steerable Composer**: Auto-expanding dock with 3-state Action Button (Send / Stop / Queue), in-flight message queue tray, background task indicators, and multiline support (`Shift+Enter` for newline, `Enter` to submit).
* 📬 **Queued Messages Tray**: In-flight steering buffer with FIFO auto-draining, Send Now, Edit, and Delete actions.
* ⚙️ **Background Task Tray**: Monospace status indicators with spinners for asynchronous agent jobs.
* 📊 **Organic Token Ring**: Smooth animated circular SVG progress gauge for context window budget tracking.
* 📑 **Slide-Over Drawers**: Ephemeral slide-out sheets for conversation histories, diff reviews, and live artifacts.

---

## Installation

```bash
uv add nicegui-ai
# or with pip fallback:
pip install nicegui-ai
```

---

## Quickstart

```python
import asyncio
from nicegui import ui
from nicegui_ai import (
    setup_ai_theme,
    FloatingHeader,
    AiThread,
    AiComposer,
    ToolCall,
    ToolStatus,
    SuggestionPrompt,
)


@ui.page("/")
def index():
    # 1. Inject ambient dark theme & custom scrollbars
    setup_ai_theme()

    # 2. Ambient floating glass header with circular token gauge
    header = FloatingHeader(
        agent_name="code-agent",
        model="claude-3-7-sonnet",
        tokens_used=14200,
        token_limit=128000,
    )

    # 3. Centered AI conversation thread
    with ui.column().classes(
        "w-full max-w-3xl mx-auto h-screen pt-20 pb-4 px-4 overflow-hidden"
    ):
        thread = AiThread(
            welcome_title="How can I help you today?",
            suggestions=[
                SuggestionPrompt(label="Run Tests", prompt="uv run pytest tests/"),
                SuggestionPrompt(label="Inspect Git Diff", prompt="git diff --staged"),
            ],
            on_suggestion_click=lambda p: composer.input.set_value(p),
        )

        async def handle_submit(prompt: str):
            composer.set_running(True)
            thread.add_user_message(prompt)

            # Agent response with reasoning and tool call
            agent = thread.add_agent_message(agent_name="Agent")
            agent.set_generating(True)

            # Stream reasoning thoughts
            reasoning = agent.add_reasoning("")
            reasoning.append_thought("Analyzing requirements...\n", step_count=1)
            await asyncio.sleep(0.4)
            reasoning.append_thought("Running validation tool...\n", step_count=2)

            # Execute tool call
            tool = agent.add_tool_call(
                ToolCall(id="t1", name="run_command", args={"command": "pytest"})
            )
            await asyncio.sleep(0.5)
            tool.resolve("9 passed in 0.42s")

            # Stream final markdown text
            agent.append_text("All checks passed successfully!")
            agent.set_generating(False)
            composer.set_running(False)
            header.update_tokens(14850)

        # 4. Pill prompt composer with unified action button and steering
        composer = AiComposer(
            placeholder="Message AI agent... (type / for commands, @ for files)",
            on_send=lambda text: asyncio.create_task(handle_submit(text)),
            on_cancel=lambda: ui.notify("Generation stopped", type="warning"),
        )


ui.run(port=8080)
```

---

## Component Catalog

| Component | Description |
| :--- | :--- |
| **`AiThread`** | Spacious conversation container with auto-scrolling and empty suggestion pills. |
| **`UserMessage`** | Right-aligned message bubble with tailored `rounded-tr-sm` corner. |
| **`AgentMessage`** | Left-aligned message bubble with avatar, status badge, reasoning, and tool call slots. |
| **`ReasoningCard`** | Amber-gilded collapsible card displaying model chain-of-thought and step counts. |
| **`ToolCallCard`** | Inspectable tool execution card with arguments, results, and Human-in-the-Loop Approval Gates. |
| **`AiComposer`** | Steerable input dock with 3-state Action Button, integrated model selector, and audio pill. |
| **`QueuedMessagesTray`** | FIFO message queue tray anchored above the composer for in-flight steering with Send Now, Edit, and Delete actions. |
| **`TaskTray`** | Live status tray displaying asynchronous background tasks with spinners and monospace labels. |
| **`BranchPicker`** | Inline `< 1 / 3 >` branch switcher for multi-turn alternative explorations. |
| **`FloatingHeader`** | Ambient glassmorphism pill with model identity and circular token meter. |
| **`TokenRing`** | Standalone animated SVG circular progress ring for context window tracking. |
| **`SlideOverDrawer`** | Smooth off-canvas sheet with soft backdrop scrim for session lists and artifacts. |
| **`CodeBlock`** | Monospace code block with language indicator, filename, line numbers, and copy button. |
| **`ArtifactCard`** | Interactive card representing agent artifacts (code, reports, diffs) with copy and download. |
| **`ArtifactViewerDrawer`** | Full-featured off-canvas drawer with tabbed Code (syntax highlighted, line numbers), Live Render (HTML/SVG, Mermaid, Markdown), and Unified Diff view (+/- line highlights). |
| **`StreamBridge`** | Reactive streaming orchestrator that consumes AG-UI events and drives UI updates (text, reasoning, tools, tasks, tokens). |
| **`BaseStreamAdapter`** | Object-oriented adapter hierarchy (`OpenRouterStreamAdapter`, `GeminiStreamAdapter`, `OpenCodeStreamAdapter`, `AgUiStreamAdapter`) translating provider events to normalized AG-UI protocol. |
| **`MessageBranch`** | Dataclass encapsulating branch state (text, reasoning, tool calls, tokens) for reactive turn switching and forking. |
| **`ApprovalModal`** | Ambient glassmorphism modal dialog for human-in-the-loop security gates. |
| **`ModelSelector`** | Floating pill dropdown or inline composer selector for active model and reasoning effort. |
| **`VoicePill`** | Audio streaming indicator and push-to-talk pill with animated waveforms. |
| **`AiMarkdown`** | Markdown renderer that auto-converts fenced code into interactive `CodeBlock` components with incremental streaming. |
| **`LucideIcon`** | Crisp outline SVG icon primitive matching contemporary AI developer tooling. |

<p align="center">
  <img src="https://raw.githubusercontent.com/IAmNo1Special/nicegui-ai/main/assets/artifact-drawer-preview.png" alt="nicegui-ai Off-Canvas Artifact Drawer with Unified Diff" width="100%">
</p>

---

## Antigravity Desktop IDE (1:1 Parity)

`nicegui-ai` includes a complete, pixel-perfect 1:1 Python + NiceGUI reconstruction of the **Google Antigravity** desktop AI IDE (`nicegui_ai.antigravity`), matching all 26 extracted surfaces, modals, popovers, and auxiliary panels extracted directly from the upstream release via reverse engineering and live DevTools inspection.

### Running the Antigravity Desktop App

Run directly via the included CLI command:

```bash
uv run nicegui-antigravity
# or via module:
uv run python -m nicegui_ai.antigravity.app
```

Then visit **http://localhost:8080** (or embed it directly into your own NiceGUI app via `from nicegui_ai.antigravity import AntigravityApp`).

### Architecture & Reconstructed Surfaces

| Surface | Module | Description |
| :--- | :--- | :--- |
| **Title Bar** | [`title_bar.py`](src/nicegui_ai/antigravity/title_bar.py) | 35px native header (`Antigravity`, `File`, `View`, `Window`). |
| **Sidebar Navigation** | [`sidebar.py`](src/nicegui_ai/antigravity/sidebar.py) | 256px nav tree with Pinned items, collapsible Projects, and Settings footer. |
| **Zero-State Home** | [`chat_view.py`](src/nicegui_ai/antigravity/chat_view.py) | Upstream hero card (`rYb`/`Q1b`) with prompt pill chips and quick-start guides. |
| **Chat & Trajectory** | [`chat_view.py`](src/nicegui_ai/antigravity/chat_view.py) | Message stream, expandable reasoning accordions, tool execution cards, and `ask_question` cards. |
| **Model Selector** | [`model_selector.py`](src/nicegui_ai/antigravity/model_selector.py) | Upward popover with side-by-side Reasoning Effort flyout (`Low`, `Medium`, `High`, `Max`) and quota inspection. |
| **Composer Controls** | [`chat_view.py`](src/nicegui_ai/antigravity/chat_view.py) | Fastpick `/` slash menu, `@` file mentions, `+` Context Picker modal, Modes popover, and Permissions presets. |
| **6-Tab Auxiliary Pane** | [`auxiliary_pane.py`](src/nicegui_ai/antigravity/auxiliary_pane.py) | Overview (`P_b`/`N_b`/`0_b`), Review Changes (unified/split diffs with gutter comments), 2-Column Terminal, File Viewer, Browser Target Preview, and Subagents Inspector. |
| **Conversation History** | [`history_view.py`](src/nicegui_ai/antigravity/history_view.py) | Full-screen timeline (`IRb`) with search filters and `Ctrl+K` command palette modal (`oMb`). |
| **Automations & Schedules** | [`automations_view.py`](src/nicegui_ai/antigravity/automations_view.py) | Grid view (`K1b`), Schedule Editor (`B1b`/`A1b`), and New Automation creator (`I1b`). |
| **Customizations** | [`customizations_view.py`](src/nicegui_ai/antigravity/customizations_view.py) | Workspace & Global Skills (`.agents/skills/`), Rules (`AGENTS.md`), Plugins, and Subagents (`xUb`/`wUb`). |
| **Two-Column Settings** | [`settings_modal.py`](src/nicegui_ai/antigravity/settings_modal.py) | 13 primary categories, 11 subviews, model credentials, and theme modes (`dark`, `light`, `oled`). |

For design rationale, state model, and ubiquitous language, see [ADR 0005](docs/adr/0005-antigravity-subpackage-and-1-to-1-parity.md) and [CONTEXT-MAP.md](CONTEXT-MAP.md).

---

## Live Showcase Demo & Component Gallery

Run the interactive live demo showcasing end-to-end agent streaming with reasoning, tools, and queued steering:

```bash
uv run python -m nicegui_ai.demo
```

Or open the **Component Gallery** to inspect every single primitive across all its visual states:

```bash
uv run python -m nicegui_ai.gallery
```

Then open your browser at **http://localhost:8080**.

---

## Development & Testing

```bash
# Run tests
uv run pytest

# Check formatting and linting
uv run ruff check .
uv run ruff format --check .

# Type checking (strict mode)
uv run mypy src/
```

---

## License

MIT License. Designed for the Python AI agent community.
