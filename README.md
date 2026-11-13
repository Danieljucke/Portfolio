# Daniel Joy — Engineering Portfolio

A four-page, static, English-language portfolio for Daniel Joy and Mélo Technology. The design uses compact product panels, a connected-systems illustration, a minimal shared stylesheet, and an entirely local interactive demonstration console.

## Pages

- `index.html` — introduction, six featured projects, engineering principles, terminal, and contact.
- `server.html` — NetShare Server project details.
- `player.html` — NetShare Player project details.
- `fullstack.html` — frontend, mobile, backend, data, and automation stacks.

Shared resources: `assets/css/site.css`, `assets/js/site.js`, and `assets/favicon.svg`.

## Preview locally

Run `python -m http.server 8000` from this directory, then visit `http://localhost:8000/`.

No build tool, package manager, analytics, or third-party JavaScript is required. The site is intended for the `Portfolio` GitHub Pages project repository at `https://danieljucke.github.io/Portfolio/`.

## Social links

The Mélo Technology GitHub organization is configured as `https://github.com/Melo-Technology` and the personal GitHub profile is `https://github.com/Danieljucke`.

**The official Mélo Technology X/Twitter account is not verified.** Its UI entry is intentionally a non-clickable `handle pending` label rather than an invented or potentially incorrect link. To enable it, edit the single `brandTwitter` setting at the top of `assets/js/site.js`:

```js
brandTwitter: 'https://x.com/YOUR_VERIFIED_BRAND_HANDLE',
```

The `data-brand-social="twitter"` placeholders will then automatically become links on the pages that include them. Verify the account belongs to Mélo Technology first. Do not silently substitute the developer's personal account.

## Project accuracy

- NetShare: distinct Server and Player pages; do not claim an App Store release until verified.
- MeloShelf: Windows application using Python and SQLite, not Flutter.
- AntMap: in development; no unverified public link.
- ECG Research: explicitly experimental and **not** a clinical diagnosis system.
- Dream-Teller: in development; detailed functionality and public links not yet verified.
- Clustriva: **Coming soon**, described conservatively as a local file/folder workflow tool with a Python core and web UI.

The mini-application panels on the cards are **illustrative CSS mockups**, not claimed screenshots of real applications.

## Interactive terminal

The terminal is a **browser-local demo**. It cannot execute real system commands or connect to private infrastructure. Available examples:

```
help
projects
project meloshelf
project dream-teller
project clustriva
stack
stack frontend
stack backend
stack data
stack tooling
links
github
twitter
contact
status
ping server
theme light
accent copper
date
uptime
history
clear
```

Features include command history (Up/Down), Tab completion, one-click quick commands, safe text-only output, simulated signaling, link display, local theme/accent preferences, and reduced-motion support. `ping` is clearly marked as a simulation.

## Validation

Static HTML/CSS/JS checks are supported, and responsive/manual browser testing is required prior to merging or deploying. The artifact's included `VALIDATION.md` records the actual verification status; do not infer that real browser validation succeeded if that report says it was blocked.

## Release discipline

Create a feature branch and a **draft pull request**. Capture current GitHub Pages before/after screenshots and test mobile, tablet, desktop, light, dark, keyboard access, terminal commands, and reduced motion. **Do not merge or publish without the owner's approval.**

## Credits

An earlier version of this site used the iPortfolio template by BootstrapMade. Third-party files retained under `assets/` keep their original license and attribution notices pending a dedicated licensing review.
