"""Basic chat interface example using nicegui-ai."""

import asyncio

from nicegui import ui

from nicegui_ai import AiComposer, AiThread, setup_ai_theme


@ui.page("/")
def main_page() -> None:
    # 1. Apply dark ambient glassmorphism theme
    setup_ai_theme()

    # 2. Main layout container
    with ui.element("main").classes(
        "flex flex-col items-center justify-center p-4 w-full h-screen bg-[#0d1017] overflow-hidden"
    ):
        with ui.element("div").classes(
            "w-full max-w-3xl h-full flex flex-col bg-[#11151f]/60 backdrop-blur "
            "border border-gray-800/60 rounded-2xl shadow-2xl overflow-hidden min-h-0"
        ):
            # 3. Thread container
            thread = AiThread(
                suggestions=[
                    "Explain async generators in Python",
                    "How does WebSockets streaming work?",
                ],
                on_select_suggestion=lambda text: asyncio.create_task(
                    send_message(text)
                ),
            )

            async def send_message(user_text: str) -> None:
                # Add user bubble
                thread.add_user_message(user_text)
                composer.set_running(True)

                # Add agent response bubble
                agent_msg = thread.add_agent_message(
                    agent_name="ai-agent",
                    initial_text="",
                    is_generating=True,
                )

                # Simulate streaming response
                chunks = [
                    "Hello! ",
                    "I am an AI agent built with **nicegui-ai**.\n\n",
                    f'You asked: *"{user_text}"*\n\n',
                    "Here is a quick overview:\n",
                    "- Native Lucide outline icons\n",
                    "- Monospace code styling\n",
                    "- Smooth streaming updates\n",
                ]
                for chunk in chunks:
                    agent_msg.append_text(chunk)
                    await asyncio.sleep(0.2)

                agent_msg.set_generating(False)
                composer.set_running(False)

            # 4. Docked composer input
            composer = AiComposer(
                placeholder="Message AI agent...",
                on_send=lambda text: asyncio.create_task(send_message(text)),
            )


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8080, title="nicegui-ai Basic Chat")
