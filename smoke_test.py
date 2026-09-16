from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, _, attrs):
        for name, value in attrs:
            if name in {"href", "src"} and value:
                parsed = urlparse(value)
                if not parsed.scheme and not value.startswith("#"):
                    self.paths.append(parsed.path)


html = Path("index.html").read_text(encoding="utf-8")
assets = Assets()
assets.feed(html)
assert "CHOREO — Every Humanoid Skill as a Trajectory" in html
assert all(Path(path).is_file() for path in assets.paths), assets.paths
print(f"OK: index.html and {len(assets.paths)} local asset references")
