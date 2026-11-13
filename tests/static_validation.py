from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / name for name in ("index.html", "server.html", "player.html", "fullstack.html")]


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.hrefs = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "a" and "href" in attrs:
            self.hrefs.append(attrs["href"])


for page in PAGES:
    parser = Links()
    parser.feed(page.read_text(encoding="utf-8"))
    assert parser.lang == "en", (page.name, parser.lang)
    for href in parser.hrefs:
        parsed = urlparse(href)
        if parsed.scheme in {"http", "https", "mailto"}:
            continue
        target = page if not parsed.path else ROOT / parsed.path
        assert target.exists(), (page.name, href)
        if parsed.fragment:
            target_parser = Links()
            target_parser.feed(target.read_text(encoding="utf-8"))
            assert parsed.fragment in target_parser.ids, (page.name, href)

home = PAGES[0].read_text(encoding="utf-8")
required = [
    "Dream-Teller", "In development", "Clustriva", "Coming soon",
    "https://github.com/Melo-Technology", "X / Twitter link pending verification",
    "Google Play", "Huawei AppGallery", "iOS support planned",
]
for text in required:
    assert text in home, text
assert "twitter.com/" not in home.lower() and "x.com/" not in home.lower()
assert "Chargée en" not in home
print("Static validation passed for four HTML pages and all local links.")
