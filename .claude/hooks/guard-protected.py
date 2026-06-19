#!/usr/bin/env python3
"""PreToolUse hook (Write|Edit): soft guard for frozen raw/ and protected files.

Does NOT hard-deny. When a Write/Edit targets a path that CLAUDE.md treats as frozen
(raw/** after triage, §B.2) or protected (§B.12), it returns permissionDecision "ask"
with a reason, forcing a confirm-with-the-user step even under acceptEdits. Confirm and
the action proceeds; nothing is blocked outright.

Triage routes files into raw/ with `mv` (Bash), not Write/Edit, so this only fires on the
abnormal case: editing a landed raw file or a protected config/schema file in the editor.

Any internal error -> exit 0 silently (normal permission flow). A hook must never break
the user's workflow.
"""

import sys
import json


def rule(norm):
    """Return (label, reason) if the path is guarded, else None."""
    if "/raw/" in norm:
        return (
            "raw-frys",
            "raw/ er frosset arkiv etter triage (§B.2). Skriving/redigering her er "
            "normalt feil — triage flytter filer inn med mv, ikke Write/Edit. "
            "Bekreft at dette er en bevisst triage-destinasjon.",
        )
    if norm.endswith("/CLAUDE.md"):
        return ("beskyttet", "CLAUDE.md er beskyttet (§B.12) — krever uttrykkelig godkjenning.")
    if norm.endswith("/AGENTS.md"):
        return ("beskyttet", "AGENTS.md er en read-only peker (§B.12) — skal normalt ikke endres.")
    if "/.claude/skills/" in norm:
        return ("beskyttet", ".claude/skills/** er beskyttet (§B.12) — krever uttrykkelig godkjenning.")
    if "/.obsidian/" in norm:
        return ("beskyttet", ".obsidian/** endres bare ved eksplisitt Obsidian-config-arbeid (§B.12).")
    if "/meta/" in norm and "/meta/handovers/" not in norm:
        return ("beskyttet", "meta/ er menneske-kuratert (§B.2/§B.12) — endre bare når du blir bedt om det.")
    return None


def main():
    data = json.loads(sys.stdin.read())
    file_path = (data.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0

    norm = file_path.replace("\\", "/")
    hit = rule(norm)
    if not hit:
        return 0  # normal flow

    label, reason = hit
    out = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": f"[{label}] {reason}",
        }
    }
    sys.stdout.write(json.dumps(out))
    return 0


try:
    sys.exit(main())
except Exception:
    sys.exit(0)  # never break the workflow over a hook bug
