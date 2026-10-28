"""1:1 Antigravity desktop CSS tokens, utility classes, and theme switcher for NiceGUI."""

from typing import Literal

from nicegui import ui

ThemeMode = Literal["dark", "light", "oled"]

ANTIGRAVITY_THEME_CSS = """
:root {
  --background: #101010;
  --foreground: #cccccc;
  --card: #191919;
  --card-border: #222222;
  --border: #191919;
  --muted: #151515;
  --muted-foreground: #6e6e6e;
  --secondary: #272727;
  --secondary-foreground: #9d9d9d;
  --sidebar: #151515;
  --sidebar-muted: #151515;
  --sidebar-secondary: #1b1b1b;
  --primary: #3b82f6;
  --primary-foreground: #ffffff;
}

body.ag-theme-light {
  --background: #f7f7f8;
  --foreground: #1c1c1e;
  --card: #ffffff;
  --card-border: #e2e2e5;
  --border: #e2e2e5;
  --muted: #ededf0;
  --muted-foreground: #68686e;
  --secondary: #e4e4e9;
  --secondary-foreground: #3a3a3f;
  --sidebar: #f0f0f3;
  --sidebar-muted: #e8e8ec;
  --sidebar-secondary: #e0e0e6;
  --primary: #2563eb;
  --primary-foreground: #ffffff;
}

body.ag-theme-oled {
  --background: #000000;
  --foreground: #d4d4d4;
  --card: #0a0a0a;
  --card-border: #1c1c1c;
  --border: #161616;
  --muted: #0d0d0d;
  --muted-foreground: #707070;
  --secondary: #1c1c1c;
  --secondary-foreground: #a0a0a0;
  --sidebar: #050505;
  --sidebar-muted: #0d0d0d;
  --sidebar-secondary: #161616;
  --primary: #3b82f6;
  --primary-foreground: #ffffff;
}

body, button, input, textarea, select, .q-btn, .q-field, .q-expansion-item {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  background-color: var(--background) !important;
  color: var(--foreground) !important;
  overflow: hidden !important;
  margin: 0 !important;
  padding: 0 !important;
}

.nicegui-content {
  padding: 0 !important;
  margin: 0 !important;
  height: 100vh !important;
  width: 100vw !important;
  overflow: hidden !important;
  display: flex !important;
  flex-direction: column !important;
  background-color: var(--background) !important;
  color: var(--foreground) !important;
}

/* Semantic Antigravity token utility classes */
.bg-background { background-color: var(--background) !important; }
.text-foreground { color: var(--foreground) !important; }
.bg-card { background-color: var(--card) !important; }
.border-card-border { border-color: var(--card-border) !important; }
.border-border { border-color: var(--border) !important; }
.bg-muted { background-color: var(--muted) !important; }
.text-muted-foreground { color: var(--muted-foreground) !important; }
.bg-secondary { background-color: var(--secondary) !important; }
.text-secondary-foreground { color: var(--secondary-foreground) !important; }
.bg-sidebar { background-color: var(--sidebar) !important; }
.bg-sidebar-muted { background-color: var(--sidebar-muted) !important; }
.bg-sidebar-secondary { background-color: var(--sidebar-secondary) !important; }
.bg-primary { background-color: var(--primary) !important; }
.text-primary { color: var(--primary) !important; }
.text-primary-foreground { color: var(--primary-foreground) !important; }
.border-primary { border-color: var(--primary) !important; }

.hover\\:bg-secondary:hover { background-color: var(--secondary) !important; }
.hover\\:bg-sidebar-muted:hover { background-color: var(--sidebar-muted) !important; }
.hover\\:bg-sidebar-secondary:hover { background-color: var(--sidebar-secondary) !important; }
.hover\\:text-foreground:hover { color: var(--foreground) !important; }
.hover\\:border-card-border:hover { border-color: var(--card-border) !important; }

/* Neutralize Quasar button, column wrap & field defaults */
:root {
  --q-primary: #cccccc !important;
}
.column, .flex-col {
  flex-wrap: nowrap !important;
}
.q-btn {
  text-transform: none !important;
  letter-spacing: normal !important;
  box-shadow: none !important;
}
.q-btn__content {
  width: 100%;
  justify-content: inherit;
  align-items: inherit;
  gap: inherit;
}
.q-focus-helper {
  display: none !important;
}
.q-field--borderless .q-field__control {

  padding: 0 !important;
  min-height: 0 !important;
  height: auto !important;
}
.q-field__native, .q-field__input {
  padding: 0 !important;
  min-height: 0 !important;
  line-height: 1.5 !important;
  color: var(--foreground) !important;
}

/* Custom thin dark scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: transparent;
}
::-webkit-scrollbar-thumb {
  background: #2a2a2a;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #3a3a3a;
}

/* Cascading flyout submenus */
.ag-flyout-parent {
  position: relative;
}
.ag-flyout-parent > .ag-flyout-child {
  display: none !important;
}
.ag-flyout-parent:hover > .ag-flyout-child,
.ag-flyout-parent:focus-within > .ag-flyout-child {
  display: flex !important;
}
"""


def setup_antigravity_theme(theme_mode: ThemeMode = "dark") -> None:
    """Inject 1:1 Antigravity CSS variables and utility classes into the NiceGUI page."""
    ui.add_head_html(f"<style>{ANTIGRAVITY_THEME_CSS}</style>")
    apply_antigravity_theme_mode(theme_mode)


def apply_antigravity_theme_mode(theme_mode: ThemeMode) -> None:
    """Switch the active Antigravity theme mode ('dark', 'light', or 'oled')."""
    body = ui.query("body")
    body.classes(remove="ag-theme-light ag-theme-oled")
    if theme_mode == "light":
        body.classes(add="ag-theme-light")
    elif theme_mode == "oled":
        body.classes(add="ag-theme-oled")
