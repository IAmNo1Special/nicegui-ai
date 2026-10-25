"""Pytest configuration registering NiceGUI user testing plugin and client context."""

import pytest
from nicegui import Client, ui

pytest_plugins = ["nicegui.testing.user_plugin"]


@pytest.fixture(autouse=True)
def client_context(request: pytest.FixtureRequest):
    """Ensure unit tests without User fixture have a valid NiceGUI client context."""
    if "user" in request.fixturenames:
        yield
        return
    with Client(ui.page("/_test_slot")):
        yield
