# Vault config

> **Imported by `CLAUDE.md` via `@import`. Not a wiki page.** No `kind:` frontmatter; outside wiki operations (§B.2). This file holds *this vault's instance parameters*: the values that instantiate the portable VaultOS pattern for this specific vault. The pattern (rules) lives in `CLAUDE.md` Part B; this file holds only the values those rules point into. Norwegian language/form details live in the swappable pack `meta/vaultos-lang-no.md`.

## Language
- **Wiki content** (`wiki/` page bodies, summaries, index/log entries, source pages): **Norwegian**.
- **Meta/operational docs** (`CLAUDE.md`, `AGENTS.md`, `meta/**`, skills): **English**, unless the user explicitly requests otherwise.
- Sources may arrive in any language; wiki summaries are normalized to Norwegian.

## Collaboration mode (solo / shared)
Set at setup; governs the §B.1 premises and §B.6 dedup / multi-author handling.
- **`solo`** — a single person's vault; one author drops sources.
- **`shared`** — multiple colleagues drop sources into one shared wiki; dedup (§B.6) and multi-author handling are active.

Either mode keeps the **wiki layer single-author** (the agent). Current: **`solo`** (the setup wizard sets this).

## Canonical instruction file (CLAUDE.md / AGENTS.md)
Which file holds the full schema; the other is a thin pointer to it. Set at setup from the user's primary AI tool (§B.12).
- **`CLAUDE.md`** — canonical for Claude Code, which auto-loads it and resolves the `@import` lines. `AGENTS.md` is the pointer.
- **`AGENTS.md`** — canonical for Codex and other tools that auto-load `AGENTS.md`. `CLAUDE.md` becomes the pointer. Claude Code's `@import` resolves only in `CLAUDE.md`, so when `AGENTS.md` is canonical the parameter files (`vault-config.md`, the language pack) are referenced by path rather than `@import`-ed.

Current: **`CLAUDE.md`**.

## Hovedtags (top-level domains)
Canonical **live** registry: `wiki/tags.md`. Read it before tagging. Current hovedtags:
`kultur`, `vitenskap`, `ai_og_software`, `familie_og_okonomi`, `hus_og_hage`, `helse_og_trening`.
These are tags + homepage entry points, **not folders** (no `wiki/01 Kultur/`-style taxonomy).

## Entity types (frontmatter `entity_type:` + infobox `Type`)
Every `kind: entity` page carries `entity_type:` from this enum; the infobox `Type` line mirrors the value. Lint flags missing or out-of-enum values (Check 9h).
- `person` — an individual human.
- `org` — a named collective: company, institution, fund, band, label, public body, NGO.
- `product` — a made artifact used as a tool or good: software, AI model, app, device, service.
- `work` — a named creative work treated as an entity (book, film, album, artwork), only when discussed as a thing across pages and not itself an ingested source.
- `place` — a geographic location: country, city, region, landscape.
- `event` — a bounded happening: conference, summit, named historical event.
- `dataset` — a structured data import: media-log export, corpus.
- `publication` — a media outlet: newspaper, journal, podcast series, blog.

Routing for ambiguous cases: band/ensemble → `org`; newspaper/podcast/blog → `publication`; a country → `place`; a theory or idea → not an entity (`kind: concept`); a work with its own source page stays on the source page (use `work` only when the work is referenced as a thing across pages).

## Personal domains (`personal/<domain>/`)
health, finance, home & garden, … (extensible). Personal-layer rules: §B.10.

## Source-type folders (under `raw/`)
`articles/`, `papers/`, `transcripts/`, `media_logs/`, `assets/`.
- `raw/articles/<corpus>/`: multi-file archives from a single publication (preserves original filenames).
- `raw/media_logs/<export-name>/`: structured item-card exports (Goodreads/Letterboxd); the **folder** is the canonical raw source unit, not each item file.

## Plugin-sync roots
Subfolders synced live by Obsidian plugins (triage skipped; layout follows the plugin):
- **`raw/Snipd/`:** Snipd podcast highlights. Layout: `raw/Snipd/Data/<Podcast>/<Episode>.md`.
- **Overhead files** (not sources; lint must not flag, ingest must not process): `raw/Snipd/Base/Snipd.base`, `raw/Snipd/README.md`.
- **Cover/logo URLs:** Snipd episode frontmatter carries `image_url` and `show_image_url` (CDN proxies via `wsrv.nl`). Valid cover/logo sources for wiki source/entity pages. Reference inline (`![Cover](url)`); do **not** mirror into `raw/assets/`.

## Snipd ingest gating (which episodes, and when)
Snipd syncs highlights live and grows an episode file over time, so "ingest all un-ingested Snipd" is the wrong default. Two gates run at the front of any Snipd ingest (procedure: `wiki-ingest` Phase 0). The values below are the tunable thresholds the skill points into.
- **Readiness — `last_snip_date` settling window (default 7 days).** Ingest an episode only when `last_snip_date` is ≥ 7 days before today: the user has stopped adding snips, so the episode is settled. Recompute from frontmatter each session; never trust a stale standing batch list. An in-file marker does **not** survive the next Snipd export (the plugin regenerates the file — `episode_export_date`/`snips_count` change each sync), so `last_snip_date`, a plugin-written field, is the durable signal. Override: "ingest X now" forces early; "hold X" keeps a paused episode out.
- **Worthiness — selectivity (soft `snips_count` floor, default ≤ 2).** Don't auto-take every settled episode. Present the settled, not-yet-ingested candidates (topic · podcast · `snips_count` · age) and let the user confirm the cut. `snips_count` is a soft engagement proxy: ≤ 2 snips flags a likely-skip passing highlight; an off-domain topic flags "skip?". Soft, not hard — a single snip worth a citation is ingested if the user says so. Empty/overhead episodes (no real snips) are skipped outright.

## Reserved Vault DNA names
The agent-instruction filenames AI tooling auto-loads as project context. Wiki entity/source/concept filenames must not collide (case-insensitively) with these (mechanism + disambiguation rule: §B.3 "Reserved Vault DNA names"). Maintain the list here; extend when new auto-load conventions emerge.
`CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `MEMORY.md`, `SKILL.md`, `README.md`.

## Model-id baseline (lint Check 6 model-parity)
Current default model id: **`claude-opus-4-8`**. Lint flags sources still on an older id as re-ingest candidates. Update this when the default model advances.

## Ingest-recommended tier (model floor at ingest time)
**Practical standard:** Sonnet or GPT-5.3-Codex does the job for ingest; for a little extra polish, run a top-tier model (Opus or GPT-5.5) at **high**. Max is never needed. Avoid the Haiku class.

Detail, from a blind benchmark. **Top (tied, 48/48):** Opus/high and GPT-5.5/high. **One notch down, fully usable (~42–43):** Sonnet and GPT-5.3-Codex (effort barely matters: Sonnet/medium ≈ Sonnet/max; Codex lost only a fixable index first-line, the prose was top). **Avoid for ingest (34, prose collapse):** the Haiku class, with cross-language bleed and gender errors (author-driven, not an artifact). Reasoning effort above "high" adds nothing. This drives the `wiki-ingest` opening note (§B.4.0), which warns **only** on the Haiku class (never on Sonnet/Opus/GPT-5.5/5.3-Codex), and the batch-plan gate's model confirmation. Revisit when the model-id baseline above advances.
