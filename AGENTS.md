# AGENTS.md

**This file is the pointer; the canonical schema lives in [CLAUDE.md](CLAUDE.md).**

That is the default arrangement. Which file is canonical is a per-vault setup choice (`meta/vault-config.md` → "Canonical instruction file"): if this vault chose `AGENTS.md` as canonical, the roles are reversed — the full schema lives here and `CLAUDE.md` points back. All agents — Claude Code, Codex, or any other — read the **canonical** file for instructions.

## Rules for agents

- **Read the canonical file** (by default `CLAUDE.md`) and follow it as if it were named for your tool. A non-Claude agent that only reads `AGENTS.md` by convention should open the canonical file and obey it.
- **Treat the pointer file as read-only during normal work.** If schema changes are needed, edit the canonical file. The canonical/pointer split itself is managed by the setup wizard (`first-time.md`), not changed by hand.
- **Don't duplicate the canonical content into the pointer file.** A second copy drifts out of sync.
