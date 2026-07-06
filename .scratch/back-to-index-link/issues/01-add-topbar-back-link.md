Status: done

## What to build

Add a "back to index" link in the top navbar of lesson pages. Currently the topbar brand (`<span class="brand">Claude Code <b>Master</b></span>` in `PAGE`, `generators/html_template.py:71`) is plain text with no link. Since `PAGE` is the shared HTML shell used both for lesson pages (`render_html.py`) and for `index.html` (`build_index()` in `build.py`), wrapping the brand in `<a href="index.html">` gives every lesson page a one-click way back to the program overview.

Add matching CSS in `generators/tokens.css` so the link doesn't visually read as a generic hyperlink — no underline, inherits the existing brand text color, subtle hover state only.

## Acceptance criteria

- [ ] Topbar brand on any lesson page (e.g. `output/gun01-*.html`, `output/gun02-*.html`) is a clickable link to `index.html`
- [ ] Link resolves correctly whether lesson pages are opened directly from `output/` or served via the relative path used in production
- [ ] index.html's own topbar brand link doesn't break anything (a self-link back to itself is fine)
- [ ] No visual regression — brand still reads as a logo/wordmark, not a generic styled link (no underline, no color change from current brand style, hover state subtle)
- [ ] Verified via `python build.py all` and opening the regenerated `output/gun01-*.html`, `output/gun02-*.html`, and `output/index.html` in a browser

## Blocked by

None - can start immediately
