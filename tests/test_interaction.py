"""Interaction tests using NiceGUI's headless User fixture."""

import pytest
from nicegui.testing import User


@pytest.mark.nicegui_main_file("src/nicegui_ai/demo.py")
async def test_demo_page_loads(user: User):
    await user.open("/")
    await user.should_see("How can I help you today?")
    await user.should_see("code-agent")
    await user.should_see("claude-3-7-sonnet")


@pytest.mark.nicegui_main_file("src/nicegui_ai/gallery.py")
async def test_gallery_page_loads(user: User):
    await user.open("/")
    await user.should_see("nicegui-ai Component Gallery")
    await user.should_see("ModelSelector & VoicePill Controls")
    await user.should_see("QueuedMessagesTray & TaskTray")
    await user.should_see("AiComposer with Unified Action Button")


@pytest.mark.nicegui_main_file("examples/basic_chat.py")
async def test_basic_chat_example_loads(user: User):
    await user.open("/")
    await user.should_see("Explain async generators in Python")


@pytest.mark.nicegui_main_file("examples/tools_and_reasoning.py")
async def test_tools_and_reasoning_example_loads(user: User):
    await user.open("/")
    await user.should_see("Run system diagnostic")


@pytest.mark.nicegui_main_file("examples/artifacts_and_drawers.py")
async def test_artifacts_and_drawers_example_loads(user: User):
    await user.open("/")
    await user.should_see("fullstack-agent")
    await user.should_see("Generate a FastAPI endpoint")
