# Claude portfolio correction — validation evidence

## Scope

This branch replaces the closed product-dashboard proposal with the owner-supplied Claude portfolio: the full-screen Lio hero, pointer-reactive tunnel canvas, reading rail, project accordions, local terminal, and three project detail pages.

Two narrowly scoped corrections were made after applying the supplied files:

- Changed the remaining French performance label from `Chargée en` to `Loaded in`.
- Changed small metadata labels from the variable accent to the theme's muted text color after automated contrast testing found that cyan accent values could fall below WCAG AA in light mode.

## Visual evidence

| View | Before (current `main`) | After (this branch) |
| --- | --- | --- |
| Desktop | [before-desktop.png](before-desktop.png) | [after-desktop-light.png](after-desktop-light.png) |
| Desktop dark | [before-desktop.png](before-desktop.png) | [after-desktop-dark.png](after-desktop-dark.png) |
| Mobile | [before-mobile.png](before-mobile.png) | [after-mobile-dark.png](after-mobile-dark.png) |

The screenshots were captured from a local HTTP server with real Playwright Chromium. They are full-page captures; the canvas is rendered by the supplied animation code.

## Results

- Responsive Chromium checks passed at 320×720, 390×844, 768×1024, and 1440×1000 in light and dark modes.
- No horizontal overflow, browser console errors, or uncaught page errors were observed.
- axe WCAG 2 A/AA and WCAG 2.1 AA found no serious or critical violations on the landing page in all eight viewport/theme combinations, or on the three detail pages at mobile width.
- Keyboard focus, terminal submission, command history, and single-match Tab completion passed.
- Nineteen representative terminal commands passed, including project status, stack, local shell simulation, links, theme, hue, history, and simulated ping commands.
- Internal navigation and the supplied page sweep transition passed on a round trip between the landing and server pages.
- Reduced-motion emulation passed.
- All local links and fragments resolve; the four documents use `lang="en"`.
- Dream-Teller remains `In development`; Clustriva remains `Coming soon`.
- The Mélo Technology GitHub URL is preserved. No X/Twitter URL is published.
- `html-validate`, Node syntax checks for all eight inline JavaScript blocks, and `git diff --check` passed.

Machine-readable browser results are in [browser-results.json](browser-results.json). Reproducible validation scripts are stored in `tests/`.

## Limits

Automated accessibility checks do not replace a full assistive-technology audit. No deployment or production smoke test was performed because this change is intentionally limited to a draft pull request pending visual approval.
