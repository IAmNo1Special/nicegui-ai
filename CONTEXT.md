# nicegui-ai

Modern, reactive user interface primitives for autonomous AI agents, tool inspection, and human-in-the-loop steering built on NiceGUI.

## Conversation & Messages

**Thread**:
The vertical conversation stream displaying chronological exchanges between a user and an AI agent.
_Avoid_: Chat history, message log, feed

**User Message**:
A message bubble containing user input and intent directed to the agent.
_Avoid_: User prompt, query bubble, human message

**Agent Message**:
A structured message card presenting agent narrative, reasoning chains, and tool execution cards.
_Avoid_: Bot response, AI reply, assistant turn

**Branch**:
An alternative completion or conversational fork spawned from a previous user turn or agent retry, tracked as a `MessageBranch` dataclass encapsulating text, reasoning, tool calls, and token usage.
_Avoid_: Version, alternative, variation, fork

## Input & Steering

**Composer**:
The primary input dock where users author prompts, select models, activate voice recording, and queue follow-up steering instructions.
_Avoid_: Prompt bar, input box, text area, message sender

**Queued Message**:
A user prompt submitted while the agent is actively executing, held in a staged FIFO buffer to send once generation completes.
_Avoid_: Pending message, buffered prompt, draft

**Queued Messages Tray**:
A collapsed or expandable drawer anchored above the composer displaying staged messages awaiting agent completion.
_Avoid_: Queue list, buffer drawer, pending bar

**Task Tray**:
A status panel anchored directly above the composer displaying active asynchronous background operations.
_Avoid_: Spinner panel, job monitor, loading strip

## Model Execution & Inspection

**Reasoning Card**:
A collapsible thought container displaying the model's internal chain-of-thought, reflection steps, and elapsed deliberation time.
_Avoid_: Thinking block, thought log, scratchpad

**Tool Call Card**:
An inspectable card detailing an invoked agent tool, including runtime status, structured arguments, execution outputs, and approval gates.
_Avoid_: Action card, function box, tool widget

**Approval Gate**:
A human-in-the-loop decision checkpoint requiring user authorization before a sensitive or irreversible tool executes.
_Avoid_: Confirmation modal, veto dialog, permission prompt

**Artifact**:
A standalone file, document, or code product produced by an agent that persists independently of conversation messages.
_Avoid_: Generated file, attachment, output document

**Artifact Viewer Drawer**:
An off-canvas side drawer (`ArtifactViewerDrawer`) providing comprehensive tabbed inspection for an artifact: syntax-highlighted code with line numbers, live render (HTML/SVG, Mermaid diagrams, Markdown), and unified diff with line delta statistics.
_Avoid_: Artifact inspector, file preview modal, code popout

**Code Block**:
A styled syntax-highlighted code container with copy capabilities, language badges, and optional line numbers.
_Avoid_: Snippet box, pre block, code viewer

## Streaming & Protocol

**Stream Adapter**:
An object-oriented adapter translating heterogeneous LLM provider streaming chunks (e.g. OpenRouter, OpenAI, Gemini SDK, OpenCode, SSE) into normalized AG-UI events.
_Avoid_: Provider parser, chunk transformer, stream reader

**Stream Bridge**:
The reactive orchestrator consuming normalized AG-UI events from any stream adapter to drive message rendering, reasoning cards, tool call inspection, header tokens, and task trays.
_Avoid_: Event listener, stream handler, stream consumer

## Session & Identity

**Floating Header**:
A detached top glassmorphism bar communicating current agent identity, active model, and session context utilization.
_Avoid_: Top bar, nav bar, header strip

**Token Ring**:
A circular progress meter indicating context window consumption against the active model's maximum context budget.
_Avoid_: Token pie, budget circle, context gauge

**Model Selector**:
A dropdown selector allowing the user to switch the underlying LLM and adjust reasoning effort levels.
_Avoid_: Model picker, engine selector, LLM dropdown

**Voice Pill**:
An interactive push-to-talk pill displaying live audio waveform visualizations during voice interactions.
_Avoid_: Mic button, audio badge, speech widget

**Slide-Over Drawer**:
An off-canvas side sheet sliding in from the viewport edge to inspect conversation branches, artifacts, or session settings.
_Avoid_: Sidebar, side panel, slideout
