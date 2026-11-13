# Product portfolio v2 validation

Validated locally on 13 November 2026 before opening the draft pull request. GitHub Pages was not deployed or changed.

## Visual evidence

- `before-desktop.png` and `before-mobile.png`: current public `main` site captured from GitHub Pages before applying this branch.
- `after-desktop-dark.png`, `after-desktop-light.png`, and `after-mobile-dark.png`: branch output rendered by Playwright Chromium with animations disabled for stable evidence.

## Browser results

`tests/browser_smoke.py` passed in real Playwright Chromium.

- Landing page: 360, 390, 768, 1024, and 1440 CSS pixels.
- Dark and light themes at every landing-page viewport.
- No horizontal overflow and no JavaScript page or browser-console errors.
- `server.html`, `player.html`, and `fullstack.html` checked at 390 CSS pixels.
- All four pages loaded their shared CSS and JavaScript over a local HTTP server.
- Terminal commands, quick commands, Up/Down history, Tab completion, text-only input handling, simulated `ping`, theme and accent persistence, internal anchors, disabled X/Twitter placeholder, and Mélo Technology GitHub destination passed.
- Keyboard skip-link focus and `prefers-reduced-motion: reduce` passed.

Machine-readable output is stored in `browser-results.json`.

## Accessibility

`tests/accessibility_smoke.py` passed axe WCAG 2 A/AA and WCAG 2.1 AA checks for all four pages in dark and light themes. No serious or critical violations remained, including color contrast. Machine-readable output is stored in `accessibility-results.json`.

## Static validation

- `python tests/static_checks.py`: passed local assets, internal fragments, canonical URLs, English language metadata, titles, and required project/social facts.
- `node --check assets/js/site.js`: passed.
- `html-validate index.html server.html player.html fullstack.html`: passed.
- `csstree-validator assets/css/site.css`: passed.
- `git diff --check`: passed.
- Private credential-pattern scan of HTML, CSS, JavaScript, JSON, Markdown, and Python files: no matching secrets.

## Product constraints retained

- Dream-Teller remains marked `In development`.
- Clustriva remains marked `Coming soon`.
- Mélo Technology links to `https://github.com/Melo-Technology`.
- No X/Twitter URL is configured; the placeholder remains non-clickable pending confirmation.
- Terminal execution is browser-local and allowlisted. It does not evaluate visitor input, execute shell commands, access secrets, or perform real network health checks.
