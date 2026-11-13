import json
import os
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

root = Path(__file__).resolve().parents[1]
axe = Path(os.environ["AXE_CORE_PATH"])
evidence = root / "docs" / "validation" / "product-v2"
server = ThreadingHTTPServer(("127.0.0.1", 0), partial(SimpleHTTPRequestHandler, directory=str(root)))
Thread(target=server.serve_forever, daemon=True).start()
origin = f"http://127.0.0.1:{server.server_port}"
results = []

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True)
    for page_name in ("index.html", "server.html", "player.html", "fullstack.html"):
        for theme in ("dark", "light"):
            page = browser.new_page(viewport={"width": 390, "height": 844}, reduced_motion="reduce")
            page.goto(f"{origin}/{page_name}", wait_until="domcontentloaded")
            page.evaluate("theme => document.documentElement.dataset.theme = theme", theme)
            page.add_script_tag(path=str(axe))
            report = page.evaluate("async () => await axe.run(document, {runOnly: {type: 'tag', values: ['wcag2a','wcag2aa','wcag21aa']}})")
            violations = [
                {
                    "id": item["id"],
                    "impact": item["impact"],
                    "nodes": len(item["nodes"]),
                    "targets": [node["target"] for node in item["nodes"]],
                }
                for item in report["violations"]
                if item["impact"] in ("serious", "critical")
            ]
            results.append({"page": page_name, "theme": theme, "violations": violations})
            page.close()
    browser.close()

server.shutdown()
(evidence / "accessibility-results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
print(json.dumps(results, indent=2))
assert not any(item["violations"] for item in results)
