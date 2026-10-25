"""Unit tests for AG-UI streaming adapters and StreamBridge."""

import pytest
from nicegui import ui

from nicegui_ai import (
    AgentMessage,
    AgUiEvent,
    AgUiEventType,
    AgUiStreamAdapter,
    AiComposer,
    FloatingHeader,
    GeminiStreamAdapter,
    OpenCodeStreamAdapter,
    OpenRouterStreamAdapter,
    StreamBridge,
    TaskTray,
    ToolStatus,
)


@pytest.mark.asyncio
async def test_openrouter_adapter_complete_mapping():
    """Test that OpenRouterStreamAdapter maps 100% of OpenRouter/OpenAI streaming events."""

    async def mock_openrouter_stream():
        # 1. Reasoning chunk (OpenRouter reasoning parameter)
        yield {
            "id": "gen-123",
            "model": "deepseek/deepseek-r1",
            "choices": [{"delta": {"reasoning": "Analyzing user query..."}}],
        }
        # 2. Reasoning chunk (standard reasoning_content)
        yield {
            "id": "gen-123",
            "choices": [{"delta": {"reasoning_content": " Checking filesystem..."}}],
        }
        # 3. Content chunk
        yield {
            "id": "gen-123",
            "choices": [{"delta": {"content": "I found the requested file."}}],
        }
        # 4. Tool call chunks (streaming function arguments)
        yield {
            "id": "gen-123",
            "choices": [
                {
                    "delta": {
                        "tool_calls": [
                            {
                                "index": 0,
                                "id": "call_abc",
                                "function": {
                                    "name": "read_file",
                                    "arguments": '{"path":',
                                },
                            }
                        ]
                    }
                }
            ],
        }
        yield {
            "id": "gen-123",
            "choices": [
                {
                    "delta": {
                        "tool_calls": [
                            {
                                "index": 0,
                                "function": {"arguments": ' "main.py"}'},
                            }
                        ]
                    }
                }
            ],
        }
        # 5. Usage & finish reason
        yield {
            "id": "gen-123",
            "choices": [{"finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": 120,
                "completion_tokens": 85,
                "total_tokens": 205,
                "completion_tokens_details": {"reasoning_tokens": 45},
            },
        }

    adapter = OpenRouterStreamAdapter(mock_openrouter_stream())
    events = await adapter.collect()

    # Verify event types produced
    types = [e.type for e in events]
    assert AgUiEventType.RUN_STARTED in types
    assert AgUiEventType.REASONING_START in types
    assert AgUiEventType.REASONING_MESSAGE_CONTENT in types
    assert AgUiEventType.REASONING_END in types
    assert AgUiEventType.TEXT_MESSAGE_START in types
    assert AgUiEventType.TEXT_MESSAGE_CONTENT in types
    assert AgUiEventType.TOOL_CALL_START in types
    assert AgUiEventType.TOOL_CALL_ARGS in types
    assert AgUiEventType.TOOL_CALL_END in types
    assert AgUiEventType.STATE_DELTA in types
    assert AgUiEventType.RUN_FINISHED in types

    # Verify accumulated state on the adapter (OOP state preservation)
    assert adapter.thought == "Analyzing user query... Checking filesystem..."
    assert adapter.text == "I found the requested file."
    assert len(adapter.tool_calls) == 1
    assert adapter.tool_calls[0].name == "read_file"
    assert adapter.tool_calls[0].args == {"path": "main.py"}
    assert adapter.usage["total_tokens"] == 205
    assert adapter.usage["reasoning_tokens"] == 45
    assert adapter.finish_reason == "stop"


@pytest.mark.asyncio
async def test_gemini_adapter_complete_mapping():
    """Test that GeminiStreamAdapter maps 100% of Google GenAI streaming events."""

    class MockPart:
        def __init__(
            self,
            text=None,
            thought=False,
            function_call=None,
            function_response=None,
            executable_code=None,
            code_execution_result=None,
        ):
            self.text = text
            self.thought = thought
            self.function_call = function_call
            self.function_response = function_response
            self.executable_code = executable_code
            self.code_execution_result = code_execution_result

    class MockUsage:
        prompt_token_count = 50
        candidates_token_count = 110
        total_token_count = 160
        cached_content_token_count = 10

    class MockFnCall:
        id = "gemini-call-1"
        name = "search_code"
        args = {"query": "StreamBridge"}

    class MockFnResp:
        id = "gemini-call-1"
        name = "search_code"
        response = {"matches": 3}

    class MockCandidate:
        finish_reason = "STOP"
        safety_ratings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "probability": "NEGLIGIBLE"}
        ]
        grounding_metadata = {"web_search_queries": ["python nicegui"]}
        citation_metadata = {"citation_sources": ["https://nicegui.io"]}

        def __init__(self, parts):
            self.content = type("Content", (), {"parts": parts})()

    async def mock_gemini_stream():
        # 1. Thought part (Gemini 2.0/2.5 Thinking)
        yield type(
            "Chunk",
            (),
            {
                "candidates": [
                    MockCandidate(
                        [MockPart(text="Deliberating on the schema...", thought=True)]
                    )
                ],
                "model_version": "gemini-2.5-flash",
            },
        )()
        # 2. Text part
        yield type(
            "Chunk",
            (),
            {
                "candidates": [MockCandidate([MockPart(text="Here is the solution.")])],
                "model_version": "gemini-2.5-flash",
            },
        )()
        # 3. Tool invocation part
        yield type(
            "Chunk",
            (),
            {
                "candidates": [MockCandidate([MockPart(function_call=MockFnCall())])],
                "model_version": "gemini-2.5-flash",
            },
        )()
        # 4. Tool response part
        yield type(
            "Chunk",
            (),
            {
                "candidates": [
                    MockCandidate([MockPart(function_response=MockFnResp())])
                ],
                "model_version": "gemini-2.5-flash",
            },
        )()
        # 5. Usage metadata
        yield type(
            "Chunk",
            (),
            {
                "candidates": [],
                "usage_metadata": MockUsage(),
                "model_version": "gemini-2.5-flash",
            },
        )()

    adapter = GeminiStreamAdapter(mock_gemini_stream())
    events = await adapter.collect()

    types = [e.type for e in events]
    assert AgUiEventType.RUN_STARTED in types
    assert AgUiEventType.REASONING_START in types
    assert AgUiEventType.REASONING_MESSAGE_CONTENT in types
    assert AgUiEventType.REASONING_END in types
    assert AgUiEventType.TEXT_MESSAGE_START in types
    assert AgUiEventType.TEXT_MESSAGE_CONTENT in types
    assert AgUiEventType.TOOL_CALL_START in types
    assert AgUiEventType.TOOL_CALL_ARGS in types
    assert AgUiEventType.TOOL_CALL_RESULT in types
    assert (
        AgUiEventType.CUSTOM in types
    )  # safety_ratings, grounding_metadata, citation_metadata
    assert AgUiEventType.STATE_DELTA in types
    assert AgUiEventType.RUN_FINISHED in types

    assert adapter.thought == "Deliberating on the schema..."
    assert adapter.text == "Here is the solution."
    assert len(adapter.tool_calls) == 1
    assert adapter.tool_calls[0].name == "search_code"
    assert adapter.tool_results["gemini-call-1"] == {"matches": 3}
    assert adapter.usage["total_tokens"] == 160


@pytest.mark.asyncio
async def test_opencode_adapter_complete_mapping():
    """Test that OpenCodeStreamAdapter maps plan steps, diffs, commands, and tasks."""

    async def mock_opencode_stream():
        yield {"type": "step_start", "step_name": "Inspect Codebase"}
        yield {"type": "thought", "content": "Checking project dependencies"}
        yield {"type": "step_finish"}
        yield {
            "type": "command",
            "id": "cmd-1",
            "name": "run_command",
            "args": {"cmd": "uv run pytest"},
        }
        yield {
            "type": "command_result",
            "id": "cmd-1",
            "result": "30 passed",
            "is_error": False,
        }
        yield {
            "type": "diff",
            "path": "src/nicegui_ai/schema.py",
            "diff": "+class AgUiEvent:",
        }
        yield {"type": "progress", "task_id": "t-1", "text": "Compiling assets..."}
        yield {"type": "content", "content": "Build succeeded."}

    adapter = OpenCodeStreamAdapter(mock_opencode_stream())
    events = await adapter.collect()

    types = [e.type for e in events]
    assert AgUiEventType.STEP_STARTED in types
    assert AgUiEventType.REASONING_MESSAGE_CONTENT in types
    assert AgUiEventType.STEP_FINISHED in types
    assert AgUiEventType.TOOL_CALL_START in types
    assert AgUiEventType.TOOL_CALL_RESULT in types
    assert AgUiEventType.CUSTOM in types  # file_diff
    assert AgUiEventType.ACTIVITY_DELTA in types  # progress
    assert AgUiEventType.TEXT_MESSAGE_CONTENT in types
    assert AgUiEventType.RUN_FINISHED in types

    assert adapter.text == "Build succeeded."
    assert adapter.thought == "Checking project dependencies"
    assert len(adapter.tool_calls) == 1
    assert adapter.tool_results["cmd-1"] == "30 passed"


@pytest.mark.asyncio
async def test_agui_native_adapter():
    """Test that AgUiStreamAdapter ingests native AG-UI events and JSON SSE lines."""

    async def mock_agui_stream():
        yield AgUiEvent(type=AgUiEventType.RUN_STARTED, run_id="run-42")
        yield 'data: {"type": "TEXT_MESSAGE_CONTENT", "content": "Hello via SSE"}'
        yield {
            "type": "TOOL_CALL_START",
            "toolCallId": "t-1",
            "toolName": "weather",
            "args": {"city": "Boston"},
        }
        yield {"type": "TOOL_CALL_RESULT", "toolCallId": "t-1", "result": "72F Sunny"}
        yield AgUiEvent(type=AgUiEventType.RUN_FINISHED, run_id="run-42")

    adapter = AgUiStreamAdapter(mock_agui_stream())
    events = await adapter.collect()

    assert len(events) == 5
    assert events[1].type == AgUiEventType.TEXT_MESSAGE_CONTENT
    assert events[1].content == "Hello via SSE"
    assert adapter.text == "Hello via SSE"
    assert len(adapter.tool_calls) == 1
    assert adapter.tool_calls[0].name == "weather"
    assert adapter.tool_results["t-1"] == "72F Sunny"


@pytest.mark.asyncio
async def test_stream_bridge_driving_ui_components():
    """Test StreamBridge driving AgentMessage, ReasoningCard, ToolCallCard, Header, and Composer."""
    from nicegui import Client

    client = Client(ui.page("/test_bridge"))
    with client:
        # Set up UI components
        agent_msg = AgentMessage("Agent", is_generating=False)
        header = FloatingHeader(
            "test-agent", "gpt-4", tokens_used=1000, token_limit=10000
        )
        composer = AiComposer(placeholder="Type message...")
        tray = TaskTray()

    async def sample_stream():
        yield {"id": "c1", "choices": [{"delta": {"reasoning": "Thinking step 1..."}}]}
        yield {
            "id": "c1",
            "choices": [{"delta": {"content": "Here is the response: "}}],
        }
        yield {"id": "c1", "choices": [{"delta": {"content": "all complete."}}]}
        yield {
            "id": "c1",
            "choices": [
                {
                    "delta": {
                        "tool_calls": [
                            {
                                "index": 0,
                                "id": "tc1",
                                "function": {
                                    "name": "fetch_info",
                                    "arguments": '{"id": 42}',
                                },
                            }
                        ]
                    }
                }
            ],
        }
        yield {
            "id": "c1",
            "choices": [{"finish_reason": "stop"}],
            "usage": {
                "total_tokens": 1500,
                "prompt_tokens": 1000,
                "completion_tokens": 500,
            },
        }

    bridge = StreamBridge(
        message=agent_msg,
        header=header,
        composer=composer,
        task_tray=tray,
    )

    with client:
        adapter = StreamBridge.from_openrouter(sample_stream())
        result = await bridge.consume(adapter)

    # 1. Verify text was streamed into AgentMessage markdown
    assert agent_msg.text == "Here is the response: all complete."
    assert "Here is the response: all complete." in agent_msg.markdown.content

    # 2. Verify reasoning card was dynamically attached and thoughts accumulated
    assert agent_msg.reasoning_card is not None
    assert "Thinking step 1..." in agent_msg.reasoning_card.thought_text

    # 3. Verify tool call card was dynamically created
    assert len(bridge._tool_cards) == 1
    tool_card = bridge._tool_cards["tc1"]
    assert tool_card.tool_call.name == "fetch_info"
    assert tool_card.tool_call.args == {"id": 42}
    assert tool_card.tool_call.status == ToolStatus.EXECUTING

    # 4. Verify token count on header and message
    assert agent_msg.tokens_used == 1500
    assert header.token_ring.used == 1500

    # 5. Verify composer and message generating state returned to idle
    assert not composer.is_running
    assert not agent_msg.is_generating

    # 6. Verify result summary object
    assert result.text == "Here is the response: all complete."
    assert result.thought == "Thinking step 1..."
    assert result.finish_reason == "stop"
    assert result.usage["total_tokens"] == 1500
    assert result.duration_ms >= 0


@pytest.mark.asyncio
async def test_agent_message_consume_convenience_method():
    """Test AgentMessage.consume(adapter) OOP convenience method."""
    from nicegui import Client

    client = Client(ui.page("/test_consume"))
    with client:
        agent_msg = AgentMessage("Agent")

    async def simple_stream():
        yield {"id": "1", "choices": [{"delta": {"content": "Direct consume works!"}}]}
        yield {"id": "1", "choices": [{"finish_reason": "stop"}]}

    with client:
        adapter = StreamBridge.from_openrouter(simple_stream())
        result = await agent_msg.consume(adapter)

    assert result.text == "Direct consume works!"
    assert agent_msg.text == "Direct consume works!"
