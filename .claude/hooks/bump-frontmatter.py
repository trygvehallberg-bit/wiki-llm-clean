#!/usr/bin/env python3
"""PostToolUse hook (Write|Edit): auto-bump `updated:` + frontmatter guard for wiki content pages.

Scope: wiki/{entities,concepts,sources,syntheses}/**.md only. Navigational pages
(index/log/overview/tags/home), .base files, raw/, meta/, personal/ are untouched.

Behaviour:
  - Bumps the frontmatter `updated:` date to today, but only when it isn't already today
    (idempotent per day -> no "file modified since read" churn on repeated edits).
  - Validates required frontmatter fields per `kind:` and reports missing ones to Claude
    via exit code 2 (non-blocking; the write already happened).
  - Any internal error -> exit 0 silently. A hook must never break the user's workflow.
"""

import sys
import re
import json
import datetime

COMMON = ["kind", "title", "created", "updated", "ingest_model"]
BY_KIND = {
    "source": ["source_path"],
    "entity": ["sources", "entity_type"],
    "concept": ["sources"],
    "synthesis": ["sources", "trigger_skill", "trigger_mode"],
}

SCOPE_RE = re.compile(r"/wiki/(entities|concepts|sources|syntheses)/[^/]*\.md$", re.IGNORECASE)
FM_RE = re.compile(r"^---\r?\n(.*?)\r?\n---", re.DOTALL)
UPDATED_RE = re.compile(r"(?m)^(updated:[^\S\r\n]*)(\d{4}-\d{2}-\d{2})")
KIND_RE = re.compile(r"""(?m)^kind:[^\S\r\n]*["']?([a-z]+)""")


def main():
    data = json.loads(sys.stdin.read())
    file_path = (data.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0

    norm = file_path.replace("\\", "/")
    if not SCOPE_RE.search(norm):
        return 0  # out of scope

    try:
        with open(file_path, "r", encoding="utf-8") as fh:
            content = fh.read()
    except OSError:
        return 0  # file gone / unreadable

    fm = FM_RE.match(content)
    if not fm:
        sys.stderr.write(
            f"[frontmatter-vakt] {norm}: mangler frontmatter-blokk helt "
            f"(forventet --- ... --- paa toppen).\n"
        )
        return 2

    fm_end = fm.end()
    today = datetime.date.today().isoformat()

    # --- Auto-bump updated: only the date token, only within the frontmatter block ---
    fm_block = content[:fm_end]
    m = UPDATED_RE.search(fm_block)
    if m and m.group(2) != today:
        new_block = UPDATED_RE.sub(r"\g<1>" + today, fm_block, count=1)
        content = new_block + content[fm_end:]
        try:
            with open(file_path, "w", encoding="utf-8", newline="") as fh:
                fh.write(content)
        except OSError:
            pass  # carry on to validation against in-memory content

    # --- Frontmatter guard ---
    block = FM_RE.match(content).group(1)

    def has(field):
        return re.search(r"(?m)^" + re.escape(field) + r":", block) is not None

    kind_m = KIND_RE.search(block)
    kind = kind_m.group(1) if kind_m else None

    missing = [f for f in COMMON if not has(f)]
    if kind and kind in BY_KIND:
        missing += [f for f in BY_KIND[kind] if not has(f)]
    elif not kind:
        missing.append("kind (gyldig: entity|concept|source|synthesis)")

    if missing:
        sys.stderr.write(
            f"[frontmatter-vakt] {norm}: mangler paakrevde frontmatter-felt: "
            f"{', '.join(missing)}.\n"
        )
        return 2

    return 0


try:
    sys.exit(main())
except Exception:
    sys.exit(0)  # never break the workflow over a hook bug
