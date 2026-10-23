"""Hermetic unit tests for nicegui-ai primitives."""

from nicegui_ai import (
    AgentMessage,
    AiComposer,
    AiThread,
    AssistantMessage,
    BranchPicker,
    FloatingHeader,
    ReasoningCard,
    SlideOverDrawer,
    SuggestionPrompt,
    TokenRing,
    ToolCall,
    ToolCallCard,
    ToolStatus,
    UserMessage,
)


def test_token_ring_initialization():
    ring = TokenRing(used=25000, limit=100000)
    assert ring.used == 25000
    assert ring.limit == 100000
    assert "<svg" in ring.content


def test_token_ring_update():
    ring = TokenRing(used=10, limit=100)
    ring.update_progress(50, 100)
    assert ring.used == 50
    assert ring.limit == 100


def test_reasoning_card():
    card = ReasoningCard(thought_text="Initial thought", step_count=1)
    assert card.step_count == 1
    assert "Initial thought" in card.thought_text

    card.append_thought("\nSecond thought", step_count=2)
    assert card.step_count == 2
    assert "Second thought" in card.thought_text


def test_tool_call_card():
    tool = ToolCall(
        id="tool-1",
        name="view_file",
        args={"path": "test.txt"},
        status=ToolStatus.EXECUTING,
    )
    card = ToolCallCard(tool)
    assert card.tool_call.name == "view_file"
    assert card.tool_call.status == ToolStatus.EXECUTING

    card.resolve("file content here", duration_ms=42)
    assert card.tool_call.status == ToolStatus.RESOLVED
    assert card.tool_call.result == "file content here"
    assert card.tool_call.duration_ms == 42


def test_branch_picker():
    changed_indices = []
    picker = BranchPicker(
        current_index=1,
        total_branches=3,
        on_change=lambda idx: changed_indices.append(idx),
    )
    assert picker.current_index == 1
    assert picker.total_branches == 3

    picker.next()
    assert picker.current_index == 2
    assert changed_indices == [2]

    picker.previous()
    assert picker.current_index == 1
    assert changed_indices == [2, 1]


def test_slide_over_drawer():
    drawer = SlideOverDrawer(title="Test Drawer", side="right")
    assert drawer.title == "Test Drawer"
    assert not drawer.is_open

    drawer.open()
    assert drawer.is_open

    drawer.close()
    assert not drawer.is_open


def test_floating_header():
    header = FloatingHeader(
        agent_name="TestAgent",
        model="gpt-4o",
        tokens_used=1000,
        token_limit=10000,
    )
    assert header.token_ring.used == 1000
    header.update_tokens(2500)
    assert header.token_ring.used == 2500


def test_composer_state():
    submitted = []
    composer = AiComposer(
        on_send=lambda text: submitted.append(text),
        model_name="Claude 3.7",
    )
    assert not composer.is_running
    composer.set_running(True)
    assert composer.is_running
    composer.set_running(False)
    assert not composer.is_running


def test_thread_messages():
    thread = AiThread(
        welcome_title="Welcome",
        suggestions=[SuggestionPrompt(label="Test", prompt="Hello")],
    )
    user_msg = thread.add_user_message("Hello Agent")
    assert isinstance(user_msg, UserMessage)
    assert len(thread.messages) == 1

    agent_msg = thread.add_agent_message(agent_name="Agent", text="Hello User")
    assert isinstance(agent_msg, AgentMessage)
    assert len(thread.messages) == 2

    # Backward compatibility alias check
    asst_msg = thread.add_assistant_message(agent_name="Agent", text="Hello User 2")
    assert isinstance(asst_msg, AgentMessage)
    assert isinstance(asst_msg, AssistantMessage)
    assert len(thread.messages) == 3

    thread.clear()
    assert len(thread.messages) == 0
