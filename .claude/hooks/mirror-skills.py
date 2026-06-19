#!/usr/bin/env python3
"""PostToolUse hook (Write|Edit): mirror .claude/skills/** -> .agents/skills/**.

The vault authors skills in .claude/skills/ (Claude Code) and keeps a parallel copy
in .agents/skills/ for non-Claude agents that read by the AGENTS.md convention. This
hook keeps the mirror in sync automatically, so the two trees can't drift the way they
do when the copy is done by hand.

Direction is one-way: .claude/skills/ is canonical, .agents/skills/ is the mirror.
Binary-safe (copies SKILL.md, .yaml, .png, .pdf, .svg, ... alike).

Any internal error -> exit 0 silently, except a copy failure which is surfaced to
Claude via exit 2. A hook must never break the user's workflow.
"""

import sys
import os
import json
import shutil

SRC_MARKER = "/.claude/skills/"
DST_MARKER = "/.agents/skills/"


def main():
    data = json.loads(sys.stdin.read())
    file_path = (data.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0

    src = file_path.replace("\\", "/")
    if SRC_MARKER not in src:
        return 0  # not a skill file

    if not os.path.isfile(src):
        return 0  # nothing to copy (deleted / never written)

    dst = src.replace(SRC_MARKER, DST_MARKER, 1)
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)
    except OSError as e:
        sys.stderr.write(f"[mirror-skills] kunne ikke speile {src} -> {dst}: {e}\n")
        return 2

    return 0


try:
    sys.exit(main())
except Exception:
    sys.exit(0)  # never break the workflow over a hook bug
