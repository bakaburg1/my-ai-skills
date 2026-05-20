#!/usr/bin/env python3
"""Index and extract sections from Markdown-like files."""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE_RE = re.compile(r"^[ \t]*(```|~~~)")
ATTR_RE = re.compile(r"[ \t]+\{[#.][^}]*\}[ \t]*$")


@dataclass
class Heading:
    level: int
    title: str
    line: int
    end_line: int
    slug: str


def slugify(title: str) -> str:
    value = re.sub(r"[^\w\s-]", "", title.lower(), flags=re.UNICODE)
    value = re.sub(r"[\s_-]+", "-", value).strip("-")
    return value or "section"


def clean_title(title: str) -> str:
    return ATTR_RE.sub("", title).strip()


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8-sig").splitlines()
    except UnicodeDecodeError:
        return path.read_text().splitlines()


def parse_headings(lines: list[str]) -> list[Heading]:
    raw: list[tuple[int, str, int]] = []
    in_fence = False

    for idx, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            raw.append((len(match.group(1)), clean_title(match.group(2)), idx))

    headings: list[Heading] = []
    for pos, (level, title, line) in enumerate(raw):
        end_line = len(lines)
        for next_level, _next_title, next_line in raw[pos + 1 :]:
            if next_level <= level:
                end_line = next_line - 1
                break
        headings.append(Heading(level, title, line, end_line, slugify(title)))
    return headings


def find_sections(headings: list[Heading], queries: list[str], fuzzy: bool) -> list[tuple[str, Heading | None, float]]:
    results: list[tuple[str, Heading | None, float]] = []
    title_map = {heading.title.lower(): heading for heading in headings}
    titles = [heading.title for heading in headings]

    for query in queries:
        exact = title_map.get(query.lower())
        if exact:
            results.append((query, exact, 1.0))
            continue

        if not fuzzy:
            results.append((query, None, 0.0))
            continue

        scored = [
            (difflib.SequenceMatcher(None, query.lower(), title.lower()).ratio(), heading)
            for title, heading in zip(titles, headings)
        ]
        score, heading = max(scored, default=(0.0, None), key=lambda item: item[0])
        results.append((query, heading if score >= 0.45 else None, score))

    return results


def format_index(headings: list[Heading]) -> str:
    if not headings:
        return "No ATX Markdown headings found."
    rows = []
    for heading in headings:
        indent = "  " * (heading.level - 1)
        rows.append(f"{indent}- L{heading.line}-L{heading.end_line} H{heading.level}: {heading.title}")
    return "\n".join(rows)


def section_text(lines: list[str], heading: Heading) -> str:
    return "\n".join(lines[heading.line - 1 : heading.end_line])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Markdown-like file to inspect")
    parser.add_argument("--section", "-s", action="append", default=[], help="Heading title to extract. Repeatable.")
    parser.add_argument("--fuzzy", action="store_true", help="Fuzzy-match requested section titles")
    parser.add_argument("--json", action="store_true", help="Write structured JSON")
    args = parser.parse_args(argv)

    if not args.file.exists():
        parser.error(f"file not found: {args.file}")

    lines = read_lines(args.file)
    headings = parse_headings(lines)

    if args.json:
        payload = {
            "file": str(args.file),
            "headings": [asdict(heading) for heading in headings],
        }
        if args.section:
            payload["sections"] = [
                {
                    "query": query,
                    "match_score": round(score, 3),
                    "heading": asdict(heading) if heading else None,
                    "content": section_text(lines, heading) if heading else None,
                }
                for query, heading, score in find_sections(headings, args.section, args.fuzzy)
            ]
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    if not args.section:
        print(format_index(headings))
        return 0

    missing = False
    for query, heading, score in find_sections(headings, args.section, args.fuzzy):
        if not heading:
            print(f"[not found] {query}", file=sys.stderr)
            missing = True
            continue
        suffix = f" (matched '{heading.title}', score {score:.2f})" if heading.title != query else ""
        print(f"<!-- section: {query}{suffix}; lines {heading.line}-{heading.end_line} -->")
        print(section_text(lines, heading))
        print()
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
