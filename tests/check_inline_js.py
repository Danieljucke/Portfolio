import subprocess
import tempfile
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Scripts(HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.blocks = []

    def handle_starttag(self, tag, attrs):
        if tag == "script" and not dict(attrs).get("src"):
            self.active = True
            self.blocks.append("")

    def handle_data(self, data):
        if self.active:
            self.blocks[-1] += data

    def handle_endtag(self, tag):
        if tag == "script":
            self.active = False


count = 0
for page in ("index.html", "server.html", "player.html", "fullstack.html"):
    parser = Scripts()
    parser.feed((ROOT / page).read_text(encoding="utf-8"))
    for script in parser.blocks:
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as handle:
            handle.write(script)
            path = handle.name
        try:
            subprocess.run(["node", "--check", path], check=True)
            count += 1
        finally:
            Path(path).unlink(missing_ok=True)

print(f"Node syntax validation passed for {count} inline JavaScript blocks.")
