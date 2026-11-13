import json
import os
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs" / "validation" / "claude-corrected"
AXE = Path(os.environ.get("AXE_CORE_PATH", ROOT / "node_modules" / "axe-core" / "axe.min.js"))
CHROMIUM = os.environ.get("PLAYWRIGHT_CHROMIUM_EXECUTABLE")
BASE = "http://127.0.0.1:8765"
VIEWPORTS = ((320, 720), (390, 844), (768, 1024), (1440, 1000))


def axe_violations(page):
    page.add_script_tag(path=AXE)
    result = page.evaluate(
        """async () => await axe.run(document, {
          runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa']}
        })"""
    )
    return [
        {
            "id": item["id"],
            "impact": item["impact"],
            "nodes": [
                {"target": node["target"], "summary": node["failureSummary"]}
                for node in item["nodes"]
            ],
        }
        for item in result["violations"]
        if item["impact"] in {"serious", "critical"}
    ]


def run_command(page, value):
    terminal = page.locator("#in")
    terminal.fill(value)
    terminal.press("Enter")


results = {"responsive": [], "accessibility": [], "console": {}, "navigation": {}}
with sync_playwright() as playwright:
    launch_options = {"headless": True}
    if CHROMIUM:
        launch_options["executable_path"] = CHROMIUM
    browser = playwright.chromium.launch(**launch_options)
    for width, height in VIEWPORTS:
        for mode in ("light", "dark"):
            context = browser.new_context(
                viewport={"width": width, "height": height}, color_scheme=mode
            )
            page = context.new_page()
            errors = []
            page.on("console", lambda msg: errors.append(f"console:{msg.type}:{msg.text}") if msg.type == "error" else None)
            page.on("pageerror", lambda error: errors.append(f"page:{error}"))
            page.goto(f"{BASE}/index.html", wait_until="networkidle")
            overflow = page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
            assert not overflow, (width, mode, "horizontal overflow")
            assert page.locator("h1[aria-label='Lio'] svg").is_visible()
            assert page.locator("#cv").is_visible()
            assert page.locator("#work details").count() >= 9
            assert not errors, errors
            violations = axe_violations(page)
            assert not violations, (width, mode, violations)
            results["responsive"].append({"width": width, "height": height, "mode": mode, "passed": True})
            results["accessibility"].append({"width": width, "mode": mode, "serious_or_critical": 0})
            if width == 1440:
                page.screenshot(path=EVIDENCE / f"after-desktop-{mode}.png", full_page=True)
            if width == 390 and mode == "dark":
                page.screenshot(path=EVIDENCE / "after-mobile-dark.png", full_page=True)
            context.close()

    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    page = context.new_page()
    page.goto(f"{BASE}/index.html", wait_until="networkidle")
    page.locator("#in").focus()
    commands = [
        "help", "projects", "project dream-teller", "project clustriva",
        "stack backend", "ls -a", "pwd", "cat .tunnel.conf", "whoami",
        "status", "date", "links", "github melo", "twitter", "contact",
        "ping server", "theme dark", "hue 200", "history",
    ]
    for command in commands:
        run_command(page, command)
    output = page.locator("#out").inner_text()
    for expected in ("In development", "Coming soon", "Melo-Technology", "pending verification", "simulated"):
        assert expected.lower() in output.lower(), expected
    page.locator("#in").press("ArrowUp")
    assert page.locator("#in").input_value() == "history"
    page.locator("#in").fill("who")
    page.locator("#in").press("Tab")
    assert page.locator("#in").input_value() == "whoami"
    page.locator("#mode").focus()
    assert page.evaluate("document.activeElement.id") == "mode"
    results["console"] = {"commands": len(commands), "history": True, "tab_completion": True, "keyboard_focus": True}

    page.goto(f"{BASE}/index.html", wait_until="networkidle")
    page.locator("a[href='server.html']").first.click()
    page.wait_for_url("**/server.html")
    assert page.locator("h1").inner_text() == "NetShare Server"
    page.locator("a[href='index.html']").first.click()
    page.wait_for_url("**/index.html")
    results["navigation"] = {"page_transition": True, "server_round_trip": True}
    context.close()

    reduced = browser.new_context(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
    page = reduced.new_page()
    page.goto(f"{BASE}/index.html", wait_until="networkidle")
    assert page.evaluate("matchMedia('(prefers-reduced-motion: reduce)').matches")
    assert not page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
    results["reduced_motion"] = True
    reduced.close()

    for filename in ("server.html", "player.html", "fullstack.html"):
        context = browser.new_context(viewport={"width": 390, "height": 844})
        page = context.new_page()
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(f"{BASE}/{filename}", wait_until="networkidle")
        assert not page.evaluate("document.documentElement.scrollWidth > document.documentElement.clientWidth")
        assert not errors, errors
        violations = axe_violations(page)
        assert not violations, (filename, violations)
        context.close()
    results["detail_pages_mobile"] = True
    browser.close()

(EVIDENCE / "browser-results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print(json.dumps(results, indent=2))
