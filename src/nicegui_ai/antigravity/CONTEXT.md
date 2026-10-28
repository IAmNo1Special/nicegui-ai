# Antigravity Desktop Clone (`nicegui_ai.antigravity`)

A 1:1 desktop UI/UX reconstruction of the Google Antigravity IDE/Agent application built in pure Python and NiceGUI, preserving exact DOM test IDs, CSS color tokens, SVG icon geometry, and interactive surfaces.

## Shell & Navigation

**Title Bar**:
The 35px frameless top window menu bar housing the `Antigravity`, `File`, `View`, and `Window` dropdown menus and keyboard accelerators (`data-testid="title-menu-bar"`).
_Avoid_: Top header, navbar, app bar

**Sidebar**:
The 256px persistent left navigation panel containing the Antigravity logo, sidebar toggle, Back/Forward history navigation stack, `Search Conversations` (`Ctrl+K`), primary view actions (`New Conversation`, `Conversation History`, `Automations`, `Customizations`), `Pinned Conversations`, collapsible `Projects` tree, and `Settings` footer.
_Avoid_: Left drawer, slide-over sheet, nav drawer

**Conversation Header**:
The 40px top bar inside an active conversation displaying the unread status dot, `project / conversation` breadcrumb title, the `Conversation Kebab` (`⋮`) menu, and the `Auxiliary Pane` toggle button.
_Avoid_: Floating header, chat title bar

**Conversation Kebab Menu**:
The `min-w-[200px]` dropdown menu anchored to the Conversation Header (`data-testid="conversation-kebab"`) providing `Rename`, `Mark Unread/Read`, `View Debug`, `Copy ▸`, `Fork ▸`, `Split ▸`, `Share`, `Archive`, `Delete`, and the `Telemetry` toggle switch.
_Avoid_: Options menu, more menu, context dropdown

## Center Views

**Zero-State Home**:
The centered landing screen for a new conversation (`data-testid="zero-state-home-view"`) featuring the top-left workspace selector pill, centered composer with `Environment` selector (`Local` / `Worktree`), and inline `Conversation History` search and recent conversation rows.
_Avoid_: Welcome screen, empty chat state, splash page

**Conversation History View**:
The dedicated full-page conversation browser (`data-testid="conversation-history-view"`) with search filtering, `Display` popover (`Group By: Project | None`, `Sort By: Recent | Tokens`, `Show Pinned Only`, `Include Archived`), and collapsible project groups.
_Avoid_: Thread list, archive page, session log

**Search Conversations Modal**:
The `Ctrl+K` command palette modal (`data-testid="conversation-picker-modal"`) for instant keyboard-driven search across conversations, projects, and quick actions.
_Avoid_: Spotlight, search dialog, quick open

**Automations View**:
The center view managing scheduled and event-driven background agent tasks (`data-testid="cloud-triggers-view"`), including the `"Create with Prompt"` banner, `New Automation` modal (`data-testid="new-cloud-trigger-modal"`), and `Automation Detail & Schedule Editor` (`data-testid="cloud-trigger-detail"`).
_Avoid_: Cron manager, jobs table, scheduler view

**Workspace Customizations View**:
The dedicated center view (`data-testid="workspace-customizations-view"`) for inspecting, filtering, and toggling workspace and global `Skills` (`SKILL.md`), `Rules` (`AGENTS.md`), `Plugins`, and `Custom Agents`.
_Avoid_: Extensions page, plugins tab, config editor

## Conversation & Composer Controls

**Lifted Context Menu**:
The blurred-backdrop overlay menu (`data-testid="lifted-context-menu-root"`) triggered from a user message bubble, elevating a preview of the message above the dim canvas with `Copy Message`, `Edit & Resend`, `Fork Conversation Here`, and `Revert Conversation to Here` actions.
_Avoid_: Right-click menu, message popover

**Ask Question Card**:
An interactive multiple-choice and write-in decision card rendered inline inside an agent turn (`data-testid="ask-question-option"`, `data-testid="ask-question-writein"`).
_Avoid_: Survey widget, form card, poll block

**Fastpick Menu**:
The upward autocomplete popover (`data-testid="fastpick"`) triggered by typing `/` in the composer to invoke slash commands (`/goal`, `/plan`, `/compact`, `/schedule`, `/browser`, `/grill-me`, `/teamwork-preview`, `/learn`, `/boost`).
_Avoid_: Command menu, slash dropdown

**Add Context Menu**:
The `+` popover in the composer (`Media`, `Mentions`, `Actions`, `Browser`, `Screen Recording`) and `@` mention autocomplete for attaching workspace files, folders, symbols, skills, and rules as removable chips.
_Avoid_: Attachment picker, upload menu

**Modes & Permissions Controls**:
The composer footer popovers controlling `Autonomous Mode` and `Best of N` (`data-testid="internal-modes-trigger"`), the `Side Question Panel` (`data-testid="side-question-panel"`), and the `Permissions Preset Selector` (`data-testid="permissions-selector-trigger"`).
_Avoid_: Agent flags, safety dropdown

**Antigravity Model Selector**:
The two-column upward popover with a side-by-side `Reasoning Effort` flyout (`Low`, `Medium`, `High`, `Max`) and `View Usage & Quotas` footer.
_Avoid_: Engine dropdown, LLM select

## Right Split Inspection

**Auxiliary Pane**:
The docked right split panel (`data-testid="auxiliary-pane"`) with a 40px icon-tab bar (`Overview`, `Review`, `Terminal`, `Artifact / File Viewer`, `Browser Preview`, `Subagents Inspector`) and the `+` tab dropdown menu (`data-testid="aux-panel-plus-dropdown-menu"`).
_Avoid_: Right drawer, canvas sheet, inspector sidebar

**Overview Panel**:
The default Auxiliary Pane tab (`data-testid="overview-panel"`) with a `Customize` section-visibility popover (`data-testid="overview-panel-customize-trigger"`), quick-navigation rows (`Review`, `Files`, `Terminal`, `Plugins`), and collapsible `Goals`, `Subagents`, `Background Tasks`, `Artifacts`, and `Links` sections.
_Avoid_: Dashboard tab, summary panel

**Review Diffs View**:
The Auxiliary Pane code-review tab featuring the `diff-view-mode-trigger` (`All Changes` / `Last Turn` / `Staged`), collapsible file diff accordions (`file-diff-accordion-toggle`), Unified/Split `code-gutter-diff`, and inline gutter review comments (`gutter-comment-button`, `comment-box`, `comment-card`).
_Avoid_: Git diff viewer, patch tab

## Configuration

**Settings Modal**:
The `max-w-5xl max-h-[80vh]` two-column modal dialog (`data-testid="settings-modal"`) with a 200px left sidebar (`13` core settings screens, per-project settings, `Not in Project`, `Shortcuts`, `Provide Feedback`, and `Account` footer) and `11` interactive drill-down subviews.
_Avoid_: Preferences page, options dialog
