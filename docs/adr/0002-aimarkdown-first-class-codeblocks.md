# AiMarkdown with Incremental Block Patching for First-Class CodeBlocks

Native `ui.markdown` renders plain HTML `<pre><code>` blocks lacking modern IDE features like language headers, line numbers, and copy-to-clipboard buttons, but naively replacing it with custom components caused severe visual flickering and DOM destruction on every token received. We created `AiMarkdown` with incremental block patching: fenced code blocks become interactive `CodeBlock` components, while prose segments remain smooth markdown blocks whose content is diffed and updated in-place without tearing down existing DOM nodes.

## Considered Options

- **Standard `ui.markdown` with client-side JavaScript hack**: Injecting copy buttons via injected script tags after render, which is brittle, desynchronizes with NiceGUI component lifecycles, and lacks Quasar UI polish.
- **Complete container clear and rebuild per chunk**: Recreating the entire list of text and code blocks on every token stream event, which caused unacceptable CPU spikes, scrolling jitter, and lost user selection.
- **Incremental block patching**: Scanning blocks into prose and code tokens, reusing intact existing components across streaming steps, and only mutating the actively changing block at the tail.
