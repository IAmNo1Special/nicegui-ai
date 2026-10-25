"""Hermetic unit tests for nicegui-ai primitives."""

from nicegui_ai import (
    AgentMessage,
    AiComposer,
    AiThread,
    ApprovalModal,
    ArtifactCard,
    BranchPicker,
    CodeBlock,
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
    assert "<svg" in ring.svg_html.content


def test_token_ring_update():
    ring = TokenRing(used=10, limit=100)
    ring.update_progress(50, 100)
    assert ring.used == 50
    assert ring.limit == 100


def test_reasoning_card():
    card = ReasoningCard(thought_text="Initial thought", step_count=1)
    assert card.step_count == 1
    assert "Initial thought" in card.thought_text
    assert not card.is_open

    card.toggle()
    assert card.is_open
    card.toggle()
    assert not card.is_open

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
    assert not card.is_open

    card.toggle()
    assert card.is_open

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

    thread.clear()
    assert len(thread.messages) == 0


def test_code_block():
    code = "print('Hello World')"
    block = CodeBlock(code=code, language="python", filename="test.py")
    assert block.code == code
    assert block.language == "python"
    assert block.filename == "test.py"


def test_artifact_card():
    card = ArtifactCard(
        title="Generated Script",
        artifact_type="file",
        content="import os\nprint(os.getcwd())",
        language="python",
        size_bytes=1024,
    )
    assert card.title == "Generated Script"
    assert card.artifact_type == "file"
    assert not card.is_open

    card.toggle()
    assert card.is_open
    card.close()
    assert not card.is_open


def test_approval_modal():
    tool = ToolCall(
        id="tool-del-1",
        name="delete_file",
        args={"path": "sensitive.txt"},
        status=ToolStatus.APPROVAL_REQUIRED,
    )
    modal = ApprovalModal(tool_call=tool, danger_level="critical")
    assert modal.tool_call == tool
    assert modal.danger_level == "critical"
    assert not modal.is_open

    modal.open()
    assert modal.is_open

    modal.close()
    assert not modal.is_open


def test_package_version():
    import nicegui_ai

    assert nicegui_ai.__version__ == "0.2.0"


def test_examples_importable():
    import importlib.util
    from pathlib import Path

    examples_dir = Path(__file__).parent.parent / "examples"
    for name in ["basic_chat.py", "tools_and_reasoning.py", "artifacts_and_drawers.py"]:
        file_path = examples_dir / name
        assert file_path.exists()
        spec = importlib.util.spec_from_file_location(
            name.removesuffix(".py"), file_path
        )
        assert spec is not None
        assert spec.loader is not None
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        assert hasattr(mod, "main_page")


def test_model_selector():
    from nicegui_ai import ModelOption, ModelSelector, ReasoningEffortSelector

    changes = []
    view_usage_calls = []

    selector = ModelSelector(
        models=[
            ModelOption(name="Gemini 4 Argon", effort="Medium", badge="New"),
            ModelOption(name="Gemini 3.8 Flash", effort="High"),
            "Claude Opus 5.5",
        ],
        current_model="Gemini 3.8 Flash",
        reasoning_effort="High",
        on_change=lambda m, eff: changes.append((m, eff)),
        on_view_usage=lambda: view_usage_calls.append(True),
    )
    assert selector.current_model == "Gemini 3.8 Flash"
    assert selector.reasoning_effort == "High"
    assert selector.model_label.text == "Gemini 3.8 Flash"
    assert selector.effort_badge.text == "High"
    assert len(selector.models) == 3

    # Change model and effort
    selector.set_model_and_effort("Gemini 4 Argon", "Low")
    assert selector.current_model == "Gemini 4 Argon"
    assert selector.reasoning_effort == "Low"
    assert selector.model_label.text == "Gemini 4 Argon"
    assert selector.effort_badge.text == "Low"
    assert changes[-1] == ("Gemini 4 Argon", "Low")

    # Change model only
    selector.set_model("Claude Opus 5.5")
    assert selector.current_model == "Claude Opus 5.5"
    assert selector.reasoning_effort == "Low"
    assert changes[-1] == ("Claude Opus 5.5", "Low")

    # Change effort only
    selector.set_reasoning_effort(None)
    assert selector.reasoning_effort is None
    assert not selector.effort_badge.visible
    assert changes[-1] == ("Claude Opus 5.5", None)

    # Standalone ReasoningEffortSelector
    standalone_efforts = []
    effort_sel = ReasoningEffortSelector(
        current_effort="medium",
        on_change=lambda eff: standalone_efforts.append(eff),
    )
    assert effort_sel.current_effort == "medium"
    assert effort_sel.label.text == "Medium"
    effort_sel.set_effort("max")
    assert effort_sel.current_effort == "max"
    assert effort_sel.label.text == "Max"
    assert standalone_efforts == ["max"]


def test_model_selector_effort_update_in_menu():
    from nicegui import ui

    from nicegui_ai import ModelOption, ModelSelector
    from nicegui_ai.icons import LucideIcon

    selector = ModelSelector(
        models=[
            ModelOption(
                name="Gemini 3.8 Flash",
                effort="High",
                effort_options=["Low", "Medium", "High"],
            ),
            ModelOption(
                name="Gemini 4 Argon",
                effort="Medium",
                effort_options=["Low", "Medium", "High"],
            ),
        ],
        current_model="Gemini 3.8 Flash",
        reasoning_effort="High",
    )

    # In model menu, the row for Gemini 3.8 Flash
    flash_item = selector.model_items[0]
    flash_row = flash_item.default_slot.children[1]
    flash_flyout = flash_item.default_slot.children[2]

    # Find the effort label in the Flash row
    row_labels = [c for c in flash_row.default_slot.children if isinstance(c, ui.label)]
    assert len(row_labels) >= 1
    assert row_labels[0].text == "High"

    # Select new reasoning effort: "Low"
    selector.set_reasoning_effort("Low")

    # 1. Verify text for currently selected effort in model menu updates
    assert row_labels[0].text == "Low"

    # 2. Verify check mark in effort submenu updates
    low_opt_div = flash_flyout.default_slot.children[0]
    high_opt_div = flash_flyout.default_slot.children[2]

    low_checks = [
        c for c in low_opt_div.default_slot.children if isinstance(c, LucideIcon)
    ]
    high_checks = [
        c for c in high_opt_div.default_slot.children if isinstance(c, LucideIcon)
    ]

    # Low option should have a visible checkmark
    assert len(low_checks) == 1
    assert "opacity-0" not in low_checks[0].extra_classes
    assert low_checks[0].visible is not False

    # High option should NOT have a visible checkmark
    assert len(high_checks) == 1
    assert "opacity-0" in high_checks[0].extra_classes

    # Switch model to Gemini 4 Argon
    argon_item = selector.model_items[1]
    argon_row = argon_item.default_slot.children[1]
    argon_flyout = argon_item.default_slot.children[2]
    argon_row_labels = [
        c for c in argon_row.default_slot.children if isinstance(c, ui.label)
    ]

    selector.set_model_and_effort("Gemini 4 Argon", "Medium")
    assert selector.current_model == "Gemini 4 Argon"
    assert selector.reasoning_effort == "Medium"
    assert argon_row_labels[0].text == "Medium"
    assert argon_row_labels[0].visible is True

    # Check model row icons
    flash_model_icon = selector._model_icons["Gemini 3.8 Flash"]
    argon_model_icon = selector._model_icons["Gemini 4 Argon"]
    assert flash_model_icon.icon_name == "chevron-right"
    assert argon_model_icon.icon_name == "check"

    # Check flyout checkmarks on Argon
    argon_med_div = argon_flyout.default_slot.children[1]
    argon_med_checks = [
        c for c in argon_med_div.default_slot.children if isinstance(c, LucideIcon)
    ]
    assert len(argon_med_checks) == 1
    assert "opacity-0" not in argon_med_checks[0].extra_classes

    # Flash flyout checkmark should now be hidden
    assert "opacity-0" in low_checks[0].extra_classes

    # Clear effort
    selector.set_reasoning_effort(None)
    assert selector.reasoning_effort is None
    assert argon_row_labels[0].visible is False
    assert "opacity-0" in argon_med_checks[0].extra_classes


def test_voice_pill():
    from nicegui_ai import VoicePill

    pill = VoicePill(state="idle")
    assert pill.state == "idle"
    assert not pill.is_active

    pill.set_state("listening")
    assert pill.state == "listening"
    assert pill.is_active

    pill.set_state("speaking")
    assert pill.state == "speaking"
    assert pill.is_active

    pill.set_state("idle")
    assert pill.state == "idle"
    assert not pill.is_active


def test_ai_markdown_parser():
    from nicegui_ai import parse_markdown_blocks

    text = "Here is some code:\n```python:main.py\nprint('hello')\n```\nDone."
    blocks = parse_markdown_blocks(text)
    assert len(blocks) == 3
    assert blocks[0]["type"] == "text"
    assert "Here is some code:" in blocks[0]["content"]

    assert blocks[1]["type"] == "code"
    assert blocks[1]["language"] == "python"
    assert blocks[1]["filename"] == "main.py"
    assert "print('hello')" in blocks[1]["code"]

    assert blocks[2]["type"] == "text"
    assert "Done." in blocks[2]["content"]


def test_queued_messages_tray():
    from nicegui_ai import QueuedMessagesTray

    send_now_calls = []
    edit_calls = []
    delete_calls = []

    tray = QueuedMessagesTray(
        on_send_now=lambda m: send_now_calls.append(m.text),
        on_edit=lambda m: edit_calls.append(m.text),
        on_delete=lambda m: delete_calls.append(m.text),
    )
    assert len(tray) == 0
    assert not tray.visible

    tray.add_message("Prompt 1")
    assert len(tray) == 1
    assert tray.visible
    assert tray.count_badge.text == "1"

    m2 = tray.add_message("Prompt 2")
    assert len(tray) == 2
    assert tray.count_badge.text == "2"

    # FIFO popping
    popped = tray.pop_next()
    assert popped is not None
    assert popped.text == "Prompt 1"
    assert len(tray) == 1

    # Edit callback
    tray._handle_edit(m2)
    assert edit_calls == ["Prompt 2"]
    assert len(tray) == 0


def test_task_tray():
    from nicegui_ai import TaskTray

    tray = TaskTray()
    assert len(tray) == 0
    assert not tray.visible

    h1 = tray.add_task("Indexing files...")
    assert len(tray) == 1
    assert tray.visible
    assert "1 task running" in tray.title_label.text

    h2 = tray.add_task("Checking policies...")
    assert len(tray) == 2
    assert "2 tasks running" in tray.title_label.text

    h1.set_text("Indexing files (45/100)...")
    assert h1.text == "Indexing files (45/100)..."

    h1.complete()
    assert len(tray) == 1
    assert "1 task running" in tray.title_label.text

    h2.complete()
    assert len(tray) == 0
    assert not tray.visible


def test_composer_unified_action_button():
    from nicegui_ai import AiComposer

    sent = []
    cancelled = []
    composer = AiComposer(
        on_send=lambda text: sent.append(text),
        on_cancel=lambda: cancelled.append(True),
    )

    # 1. Idle + empty: disabled send
    assert not composer.is_running
    assert "cursor-not-allowed" in composer.action_btn._classes

    # 2. Idle + text: enabled send
    composer.input.set_value("Hello agent")
    composer._update_action_button()
    assert "cursor-pointer" in composer.action_btn._classes
    assert "bg-purple-600" in composer.action_btn._classes

    # Submitting sends
    composer.submit()
    assert sent == ["Hello agent"]
    assert composer.input.value == ""

    # 3. Running + empty: stop
    composer.set_running(True)
    assert composer.is_running
    assert "bg-gray-200" in composer.action_btn._classes
    assert composer.action_icon.icon_name == "square"

    # 4. Running + text: queue
    composer.input.set_value("Queued follow-up")
    composer._update_action_button()
    assert "bg-purple-600" in composer.action_btn._classes
    assert composer.action_icon.icon_name == "arrow-right"

    # Submitting while running adds to queued_tray!
    composer.submit()
    assert len(composer.queued_tray) == 1
    assert composer.queued_tray.messages[0].text == "Queued follow-up"

    # 5. Agent finishes -> auto-drains queue
    composer.set_running(False)
    assert sent == ["Hello agent", "Queued follow-up"]
    assert len(composer.queued_tray) == 0


def test_tool_call_card_methods():
    from nicegui_ai import ToolCall, ToolCallCard, ToolStatus

    tool = ToolCall(id="t-1", name="search", status=ToolStatus.EXECUTING)
    card = ToolCallCard(tool)
    assert card.tool_call.status == ToolStatus.EXECUTING

    card.set_status(ToolStatus.SUCCESS)
    assert card.tool_call.status == ToolStatus.RESOLVED

    card.set_result("found 3 items")
    assert card.tool_call.result == "found 3 items"

    card.fail("timeout error")
    assert card.tool_call.status == ToolStatus.FAILED
    assert card.tool_call.result == "timeout error"


def test_agent_message_set_tokens_and_markdown():
    from nicegui_ai import AgentMessage, AiMarkdown

    msg = AgentMessage(agent_name="TestBot", text="# Title\n\n```python\nprint(1)\n```")
    assert isinstance(msg.markdown, AiMarkdown)
    assert msg.tokens_used == 0

    msg.set_tokens(850)
    assert msg.tokens_used == 850
    assert "+850 tokens" in msg.token_pill.text


def test_thread_string_suggestions():
    from nicegui_ai import AiThread, SuggestionPrompt

    thread = AiThread(
        suggestions=[
            "First Prompt",
            SuggestionPrompt(label="Second", prompt="Second Prompt"),
        ]
    )
    assert len(thread.suggestions) == 2
    assert thread.suggestions[0].label == "First Prompt"
    assert thread.suggestions[0].prompt == "First Prompt"
    assert thread.suggestions[1].label == "Second"


def test_gallery_module_importable():
    from nicegui_ai import gallery

    assert hasattr(gallery, "gallery_page")
