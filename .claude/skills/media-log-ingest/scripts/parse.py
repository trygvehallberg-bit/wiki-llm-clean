#!/usr/bin/env python3
"""Stage 1 (mechanical): parse media-log item cards into one aggregate JSON.

Reads every *.md under raw/media_logs/<subdir>/, pulls the frontmatter fields and
the first cover image + outbound link from the body, and writes a flat JSON list.
Pure mechanical step: no attribution, no curation. Those are LLM-in-the-loop steps
(see SKILL.md).

Usage:
  python parse.py --subdir media_logs/letterboxd_films --out work/films.json
  python parse.py --subdir media_logs/goodreads_books   --out work/books.json --vault "C:/path/to/vault"

--vault defaults to $CLAUDE_PROJECT_DIR, then the current directory.
"""

import os
import re
import glob
import json
import argparse

LONG = "\\\\?\\"  # Windows long-path prefix


def read_long(path):
    ap = os.path.abspath(path)
    try:
        return open(ap, encoding="utf-8").read()
    except FileNotFoundError:
        return open(LONG + ap, encoding="utf-8").read()


def parse_frontmatter(text):
    fm, body = {}, text
    m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n?(.*)$", text, re.S)
    if m:
        body = m.group(2)
        for line in m.group(1).splitlines():
            mm = re.match(r'^(\w[\w_-]*):\s*"?(.*?)"?\s*$', line)
            if mm:
                fm[mm.group(1)] = mm.group(2)
    return fm, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default=os.environ.get("CLAUDE_PROJECT_DIR", "."))
    ap.add_argument("--subdir", required=True, help="path under raw/, e.g. media_logs/letterboxd_films")
    ap.add_argument("--out", required=True, help="output JSON path")
    args = ap.parse_args()

    src = os.path.join(args.vault, "raw", args.subdir)
    items, fails = [], []
    for p in sorted(glob.glob(os.path.join(src, "*.md"))):
        try:
            fm, body = parse_frontmatter(read_long(p))
        except Exception:
            fails.append(os.path.basename(p))
            continue
        name = os.path.splitext(os.path.basename(p))[0]
        cover = re.search(r"!\[[^\]]*\]\((https?://[^)]+)\)", body)
        link = re.search(r"(?<!!)\[[^\]]+\]\((https?://[^)]+)\)", body)
        rec = dict(fm)
        rec["name"] = name
        rec["cover"] = cover.group(1) if cover else ""
        rec["link"] = link.group(1) if link else ""
        items.append(rec)

    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    json.dump(items, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"parsed {len(items)} items from {src} -> {args.out}"
          + (f" ({len(fails)} unreadable: {fails})" if fails else ""))


if __name__ == "__main__":
    main()
