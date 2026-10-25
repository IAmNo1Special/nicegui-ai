"""Artifact cards, code blocks, and slide-over drawers example using nicegui-ai."""

import asyncio

from nicegui import ui

from nicegui_ai import (
    AiComposer,
    AiThread,
    CodeBlock,
    FloatingHeader,
    LucideIcon,
    SlideOverDrawer,
    setup_ai_theme,
)


@ui.page("/")
def main_page() -> None:
    setup_ai_theme()

    tokens = {"used": 18450, "max": 128000}

    # Floating header with TokenRing meter
    header = FloatingHeader(
        agent_name="fullstack-agent",
        model="claude-3-7-sonnet",
        tokens_used=tokens["used"],
        token_limit=tokens["max"],
    )

    # Left history drawer and right canvas drawer
    history_drawer = SlideOverDrawer(title="Tome History", icon="history", side="left")
    canvas_drawer = SlideOverDrawer(
        title="Asset Canvas", icon="file-code", side="right"
    )

    with header.left_container:
        with (
            ui.element("button")
            .classes(
                "flex items-center gap-1.5 text-xs text-gray-300 hover:text-white px-2 py-1 "
                "rounded-full hover:bg-gray-800 transition-colors cursor-pointer bg-transparent border-none"
            )
            .on("click", history_drawer.toggle)
        ):
            LucideIcon("history", size=14, classes="text-amber-400")
            ui.label("History").classes("text-xs font-medium")

    with header.right_container:
        with (
            ui.element("button")
            .classes(
                "flex items-center gap-1.5 text-xs text-gray-300 hover:text-white px-2 py-1 "
                "rounded-full hover:bg-gray-800 transition-colors cursor-pointer bg-transparent border-none"
            )
            .on("click", canvas_drawer.toggle)
        ):
            LucideIcon("file-code", size=14, classes="text-cyan-400")
            ui.label("Canvas").classes("text-xs font-medium")

    # Populate canvas drawer
    with canvas_drawer.content:
        ui.label("Generated Component").classes("text-xs font-bold text-gray-200")
        CodeBlock(
            code="""from nicegui_ai import AiThread\n\nthread = AiThread()\nprint('Ready')""",
            language="python",
            filename="quickstart.py",
        )

    # Populate history drawer
    with history_drawer.content:
        ui.label("Saved Sessions").classes("text-xs font-bold text-gray-200")
        for session in ["Refactor Router", "Fix Auth Token Expiry", "Add Token Meter"]:
            with ui.element("div").classes(
                "p-2.5 rounded-lg border border-gray-800/80 bg-[#121622] hover:bg-[#1a2133] "
                "cursor-pointer text-xs text-gray-300 flex items-center justify-between transition-colors"
            ):
                ui.label(session)
                LucideIcon("chevron-right", size=12, classes="text-gray-500")

    # Main studio container
    with ui.element("main").classes(
        "flex flex-col items-center justify-center pt-16 pb-4 px-4 w-full h-screen bg-[#0d1017] overflow-hidden"
    ):
        with ui.element("div").classes(
            "w-full max-w-3xl h-full flex flex-col bg-[#11151f]/60 backdrop-blur "
            "border border-gray-800/60 rounded-2xl shadow-2xl overflow-hidden min-h-0"
        ):
            thread = AiThread(
                suggestions=["Generate a FastAPI endpoint", "Create an ArtifactCard"],
                on_select_suggestion=lambda text: asyncio.create_task(run_turn(text)),
            )

            async def run_turn(text: str) -> None:
                thread.add_user_message(text)
                composer.set_running(True)

                agent_msg = thread.add_agent_message(
                    agent_name="fullstack-agent",
                    initial_text="I have generated the requested implementation:\n\n",
                    is_generating=True,
                )

                # Attach generated ArtifactCard
                agent_msg.add_artifact(
                    title="src/routes/auth.py",
                    artifact_type="file",
                    content=(
                        "from fastapi import APIRouter, Depends\n\n"
                        "router = APIRouter(prefix='/auth')\n\n"
                        "@router.post('/login')\n"
                        "async def login():\n"
                        "    return {'token': 'jwt_secret_token_here'}\n"
                    ),
                    language="python",
                    size_bytes=184,
                    default_open=True,
                )

                agent_msg.set_generating(False)
                composer.set_running(False)
                tokens["used"] += 450
                header.update_tokens(tokens["used"])

            composer = AiComposer(
                placeholder="Ask fullstack agent...",
                on_send=lambda text: asyncio.create_task(run_turn(text)),
            )


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(port=8080, title="nicegui-ai Artifacts & Drawers")
