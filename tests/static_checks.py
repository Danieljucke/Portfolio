from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
PAGES = [ROOT / name for name in ("index.html", "server.html", "player.html", "fullstack.html")]


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.attrs = []
        self.ids = set()
        self.lang = None
        self.titles = []
        self._title = False

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        self.attrs.append((tag, values))
        if tag == "html":
            self.lang = values.get("lang")
        if tag == "title":
            self._title = True
        if values.get("id"):
            self.ids.add(values["id"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False

    def handle_data(self, data):
        if self._title:
            self.titles.append(data.strip())


documents = {}
for page in PAGES:
    parser = Document()
    parser.feed(page.read_text(encoding="utf-8"))
    assert parser.lang == "en", page
    assert "".join(parser.titles).strip(), page
    documents[page.name] = parser

for page in PAGES:
    document = documents[page.name]
    canonicals = [a.get("href") for tag, a in document.attrs if tag == "link" and a.get("rel") == "canonical"]
    assert canonicals == [f"https://danieljucke.github.io/Portfolio/{page.name}"], (page, canonicals)
    for tag, attrs in document.attrs:
        for key in ("href", "src"):
            value = attrs.get(key)
            if not value or value.startswith(("mailto:", "http://", "https://", "data:")):
                continue
            target, fragment = (value.split("#", 1) + [""])[:2] if "#" in value else (value, "")
            target_page = page if not target else ROOT / urlsplit(target).path
            assert target_page.exists(), (page.name, value)
            if fragment and target_page.suffix == ".html":
                assert fragment in documents[target_page.name].ids, (page.name, value)

source = "\n".join(page.read_text(encoding="utf-8") for page in PAGES)
script = (ROOT / "assets/js/site.js").read_text(encoding="utf-8")
assert "Dream-Teller" in source and "In development" in source
assert "Clustriva" in source and "Coming soon" in source
assert "https://github.com/Melo-Technology" in source
assert "brandTwitter: ''" in script
assert "MeloShelf — Python-based" in script
assert "not a medical diagnostic tool" in script
print("Static checks passed for 4 HTML pages and shared assets.")
