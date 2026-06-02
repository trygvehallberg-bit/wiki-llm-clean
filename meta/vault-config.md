# Vault config — <vault name>

> **Imported by `CLAUDE.md` via `@import` — not a wiki page.** Holds this vault's instance parameters — the values that instantiate the portable VaultOS pattern. The pattern (rules) lives in `CLAUDE.md` Part B; this file holds the values. **Set during first-time setup.** The language/form pack is the swappable `meta/vaultos-lang-<xx>.md`.

## Language
- **Wiki content** (page bodies, summaries, index/log entries, source pages) — **\<set during first-time setup\>**.
- **Meta/operational docs** (`CLAUDE.md`, `AGENTS.md`, `meta/**`, skills) — **English** by default (optional cosmetic translation during setup; no effect on how the vault works).
- Sources may arrive in any language; wiki summaries are normalised to the wiki language.

## Hovedtags (top-level domains)
Canonical **live** registry: `wiki/tags.md` — read it before tagging. Set during first-time setup; starter suggestions:
`teknologi`, `vitenskap`, `kultur`, `samfunn_og_okonomi`, `helse`, `personlig`.
These are tags + homepage entry points, **not folders**.

## Personal layer folder
Name of the private folder outside wiki operations (§B.10): **`personal`** (default; set during setup, or `none` if declined).

## Coach domains (`<personal>/coach/<domain>/`)
Optional sub-areas under the personal layer (extensible). Personal-layer rules: §B.10.

## Source-type folders (under `raw/`)
`articles/`, `papers/`, `transcripts/`, `media_logs/`, `assets/`.
- `raw/articles/<corpus>/` — multi-file archives from a single publication (preserves original filenames).
- `raw/media_logs/<export-name>/` — structured item-card exports (Goodreads/Letterboxd); the **folder** is the canonical raw source unit, not each item file.

## Plugin-sync roots
Subfolders synced live by Obsidian plugins (triage skipped; layout follows the plugin). **None by default.** If you wire a sync plugin (e.g. a podcast highlighter), add it here with its overhead-file names (lint must not flag them; ingest must not process them) and any cover-image URL convention.

## Reserved Vault DNA names
Agent-instruction filenames AI tooling auto-loads as project context. Wiki entity/source/concept filenames must not collide (case-insensitively); mechanism + disambiguation in §B.3.
`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `MEMORY.md`, `SKILL.md`, `README.md`.

## Model-id baseline (lint Check 6 model-parity)
The agent stamps its own model-id in page frontmatter and records the baseline here on first ingest. Lint flags pages on an older id as re-ingest candidates. Update when the default model advances.

## Ingest-recommended tier (model floor at ingest time)
Ingest prose quality is model-dependent. The top tier gives the best results; the workhorse tier one notch down is fully usable with slightly less polish; the smallest/cheapest tier can collapse prose quality (cross-language intrusion, grammatical errors — most visible in non-English wiki languages). Set this per vault: name the tiers you trust and the one to avoid, ideally backed by a quick blind benchmark on your own language and sources. Reasoning effort above "high" is typically wasted spend. Drives the `wiki-ingest` opening note (§B.4.0) — which warns **only** at the avoid-tier, never on a workhorse-or-better model — and the batch plan-gate model confirmation.
