# Unified Action Button and In-Flight Queued Messages Tray

Users naturally type subsequent instructions, corrections, or steering prompts while an agent is actively running. Rather than disabling the composer or spawning chaotic concurrent agent streams, we implemented a 3-state Action Button (Send when idle, Stop when running and input is empty, Queue when running with text) coupled with an attached FIFO `QueuedMessagesTray` that buffers staged prompts and automatically drains them sequentially as the agent finishes.

## Considered Options

- **Disable the input textarea while running**: Standard in simple chat UIs, but breaks flow when users notice an agent diverging and want to line up corrective instructions.
- **Immediate parallel turn execution**: Allowing simultaneous submissions creates race conditions in thread state, context window limits, and confusing interleaved message bubbles.
- **FIFO Auto-Draining Tray with Manual Controls**: Allows users to type freely mid-run; queued items display clearly above the composer with Send Now, Edit, and Delete actions, pausing automatic drain if the user explicitly presses Stop.
