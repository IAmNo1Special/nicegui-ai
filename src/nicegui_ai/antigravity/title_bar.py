"""35px Native Top Window Menu Bar (title-menu-bar) for Antigravity Desktop Clone."""

from collections.abc import Callable
from dataclasses import dataclass

from nicegui import ui


@dataclass
class MenuEntry:
    label: str
    shortcut: str | None = None
    action_key: str | None = None
    divider_after: bool = False


class TitleBar(ui.element):
    """Frameless 35px top menu bar with Antigravity, File, View, and Window dropdowns."""

    def __init__(
        self,
        on_new_conversation: Callable[[], None] | None = None,
        on_toggle_sidebar: Callable[[], None] | None = None,
        on_toggle_aux: Callable[[], None] | None = None,
        on_open_settings: Callable[[], None] | None = None,
        on_open_history: Callable[[], None] | None = None,
        on_open_automations: Callable[[], None] | None = None,
        on_open_customizations: Callable[[], None] | None = None,
        on_open_search: Callable[[], None] | None = None,
        on_select_aux_tab: Callable[[str], None] | None = None,
        initial_open_menu: str | None = None,
    ) -> None:
        super().__init__("div")
        self.on_new_conversation = on_new_conversation
        self.on_toggle_sidebar = on_toggle_sidebar
        self.on_toggle_aux = on_toggle_aux
        self.on_open_settings = on_open_settings
        self.on_open_history = on_open_history
        self.on_open_automations = on_open_automations
        self.on_open_customizations = on_open_customizations
        self.on_open_search = on_open_search
        self.on_select_aux_tab = on_select_aux_tab
        self.open_menu_name: str | None = initial_open_menu

        self.props('data-testid="title-menu-bar"')
        self.classes(
            "relative flex shrink-0 items-center justify-between w-full h-[35px] min-h-[35px] "
            "bg-background px-2 select-none z-50 border-b border-border/40"
        )

        self._menus: dict[str, list[MenuEntry]] = {
            "Antigravity": [
                MenuEntry("About Antigravity", action_key="settings", divider_after=True),
                MenuEntry("Settings...", "Ctrl+,", "settings"),
                MenuEntry("Customizations...", action_key="customizations"),
                MenuEntry("Automations...", action_key="automations", divider_after=True),
                MenuEntry("Check for Updates...", action_key="settings", divider_after=True),
                MenuEntry("Quit Antigravity", "Ctrl+Q", "quit"),
            ],
            "File": [
                MenuEntry("New Conversation", "Ctrl+N", "new_conversation"),
                MenuEntry("Open Workspace...", "Ctrl+O", "settings", divider_after=True),
                MenuEntry("Search Conversations...", "Ctrl+K", "search"),
                MenuEntry("Conversation History", "Ctrl+H", "history", divider_after=True),
                MenuEntry("Close Conversation", "Ctrl+W", "new_conversation"),
            ],
            "View": [
                MenuEntry("Toggle Sidebar", "Ctrl+B", "toggle_sidebar"),
                MenuEntry("Toggle Auxiliary Pane", action_key="toggle_aux", divider_after=True),
                MenuEntry("Overview Panel", action_key="aux_overview"),
                MenuEntry("Review Changes", action_key="aux_review"),
                MenuEntry("Terminal", "Ctrl+`", "aux_terminal"),
                MenuEntry("Browser Preview", action_key="aux_browser", divider_after=True),
                MenuEntry("Reload Window", "Ctrl+R", "reload"),
                MenuEntry("Toggle Developer Tools", "Ctrl+Shift+I", "devtools"),
            ],
            "Window": [
                MenuEntry("Minimize", "Ctrl+M", "minimize"),
                MenuEntry("Zoom", action_key="zoom"),
                MenuEntry("Full Screen", "F11", "fullscreen", divider_after=True),
                MenuEntry("Bring All to Front", action_key="front"),
            ],
        }

        with self:
            self._bar_container = ui.row().classes("items-center gap-0.5 pl-1 relative")
            ui.element("div").classes("flex-1 h-full")

        self.refresh_bar()

    def _trigger_action(self, key: str | None) -> None:
        self.open_menu_name = None
        self.refresh_bar()
        if key == "new_conversation" and self.on_new_conversation:
            self.on_new_conversation()
        elif key == "toggle_sidebar" and self.on_toggle_sidebar:
            self.on_toggle_sidebar()
        elif key == "toggle_aux" and self.on_toggle_aux:
            self.on_toggle_aux()
        elif key == "settings" and self.on_open_settings:
            self.on_open_settings()
        elif key == "history" and self.on_open_history:
            self.on_open_history()
        elif key == "automations" and self.on_open_automations:
            self.on_open_automations()
        elif key == "customizations" and self.on_open_customizations:
            self.on_open_customizations()
        elif key == "search" and self.on_open_search:
            self.on_open_search()
        elif key and key.startswith("aux_") and self.on_select_aux_tab:
            self.on_select_aux_tab(key.removeprefix("aux_"))

    def toggle_menu(self, menu_name: str) -> None:
        self.open_menu_name = None if self.open_menu_name == menu_name else menu_name
        self.refresh_bar()

    def refresh_bar(self) -> None:
        self._bar_container.clear()
        with self._bar_container:
            for menu_name, entries in self._menus.items():
                is_open = self.open_menu_name == menu_name
                with ui.element("div").classes("relative"):
                    btn_cls = (
                        "px-2 py-0.5 rounded text-xs cursor-pointer transition-colors border-none "
                        + (
                            "bg-secondary text-foreground font-medium"
                            if is_open
                            else "bg-transparent text-muted-foreground hover:text-foreground hover:bg-secondary/50"
                        )
                    )
                    with (
                        ui.element("button")
                        .props('type="button" data-testid="title-menu-bar-item"')
                        .classes(btn_cls)
                        .on("click", lambda _, m=menu_name: self.toggle_menu(m))
                    ):
                        ui.label(menu_name)

                    if is_open:
                        with (
                            ui.element("div")
                            .props(f'data-testid="title-menu-dropdown-{menu_name.lower()}"')
                            .classes(
                                "absolute left-0 top-full mt-1 w-56 rounded-xl border border-card-border "
                                "bg-card shadow-2xl py-1 z-50 text-xs flex flex-col"
                            )
                        ):
                            for entry in entries:
                                with (
                                    ui.element("button")
                                    .props('type="button" data-testid="title-menu-bar-option"')
                                    .classes(
                                        "w-full flex items-center justify-between px-3 py-1.5 text-left "
                                        "text-secondary-foreground hover:text-foreground hover:bg-secondary "
                                        "border-none bg-transparent cursor-pointer transition-colors"
                                    )
                                    .on(
                                        "click",
                                        lambda _, k=entry.action_key: self._trigger_action(k),
                                    )
                                ):
                                    ui.label(entry.label)
                                    if entry.shortcut:
                                        ui.label(entry.shortcut).classes(
                                            "text-[10px] font-mono text-muted-foreground ml-3"
                                        )
                                if entry.divider_after:
                                    ui.element("div").classes(
                                        "my-1 border-t border-card-border"
                                    )
