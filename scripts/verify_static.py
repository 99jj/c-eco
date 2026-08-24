from __future__ import annotations

import json
import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
LINK_ATTRS = {"href", "src", "poster", "action"}
IGNORED_PREFIXES = ("#", "mailto:", "tel:", "javascript:", "data:", "blob:")
REMOVED_PATHS = (
    "api/review.js",
    "assets/index-C_KiMpFd.js",
    "manifest.json",
    "offline.html",
    "docs/migrate.sh",
)
SUSPENDED_PATHS = (
    "tdr/tdr-mathematics.html",
    "tfp/protocol.html",
    "science-clause/index.html",
)
FORBIDDEN = {
    "monte_carlo": re.compile(r"Monte\s*Carlo", re.I),
    "creative_commons": re.compile(r"Creative Commons|CC\s*-?\s*BY|BY-NC-SA", re.I),
    "operational_scoring": re.compile(r"scoring systems|operational score", re.I),
    "weights_parameters": re.compile(
        r"weights and parameters|pesos e parâmetros|sectoral parameters|parâmetros setoriais",
        re.I,
    ),
}


def public_files() -> list[Path]:
    paths: list[Path] = []
    for current, directories, filenames in os.walk(ROOT):
        directories[:] = [
            name for name in directories if name not in {".git", ".hermes", "__pycache__"}
        ]
        paths.extend(Path(current) / name for name in filenames)
    return paths


class RefCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.refs.extend(value for key, value in attrs if key.lower() in LINK_ATTRS and value)

    handle_startendtag = handle_starttag


def candidates(source: Path, raw: str) -> list[Path]:
    value = raw.strip()
    if not value or value.startswith(IGNORED_PREFIXES):
        return []
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return []
    path = unquote(parsed.path)
    target = ROOT / path.lstrip("/") if path.startswith("/") else source.parent / path
    targets = [target]
    if not target.suffix:
        targets.extend((target.with_suffix(".html"), target / "index.html"))
    return targets


def main() -> int:
    errors: list[str] = []
    files = public_files()
    html_files = sorted(path for path in files if path.suffix.lower() in {".html", ".htm"})
    reference_count = 0

    for source in html_files:
        text = source.read_text(encoding="utf-8", errors="replace")
        parser = RefCollector()
        try:
            parser.feed(text)
            parser.close()
        except Exception as exc:
            errors.append(f"HTML parse error: {source.relative_to(ROOT)}: {exc}")
            continue
        reference_count += len(parser.refs)
        for raw in parser.refs:
            targets = candidates(source, raw)
            if targets and not any(target.exists() for target in targets):
                errors.append(f"Missing internal reference: {source.relative_to(ROOT)} -> {raw}")

    for relative in REMOVED_PATHS:
        if (ROOT / relative).exists():
            errors.append(f"Removed technical artifact is present: {relative}")

    for relative in SUSPENDED_PATHS:
        path = ROOT / relative
        if not path.exists() or "Temporarily unavailable" not in path.read_text(
            encoding="utf-8", errors="replace"
        ):
            errors.append(f"Suspension notice missing: {relative}")

    model_law = ROOT / "doctrine/model-law.html"
    if not model_law.exists() or "Model Law" not in model_law.read_text(
        encoding="utf-8", errors="replace"
    ):
        errors.append("Canonical Model Law is missing")

    searchable_suffixes = {".html", ".htm", ".js", ".ts", ".tsx", ".md", ".json"}
    for path in sorted(path for path in files if path.suffix.lower() in searchable_suffixes):
        if path == model_law:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for name, pattern in FORBIDDEN.items():
            if pattern.search(text):
                errors.append(f"Forbidden public signal ({name}): {path.relative_to(ROOT)}")

    result = {
        "ok": not errors,
        "html_files": len(html_files),
        "references": reference_count,
        "errors": errors,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
