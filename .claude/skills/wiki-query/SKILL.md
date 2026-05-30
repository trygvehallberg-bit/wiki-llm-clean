---
name: wiki-query
description: Answer a question against this vault's wiki. Triggers when the user asks a substantive question whose answer lives in the vault — "what does X say about Y?", "compare X and Y", "what's the position on Z?", "summarize the cluster around W", "find sources that argue P". The skill reads the index first, drills into relevant pages, follows wikilinks one hop, and answers with wikilink citations to source pages. If a strong cross-source thesis emerges, surface it as a possible synthesis direction; do not file a synthesis unless the user explicitly asks. Do NOT invoke for ingest, lint, schema edits, generic chat, or open-ended "create synthesis" prompts.
---

# /wiki-query

Read the wiki, answer the question, and surface synthesis directions without filing them by default.

This skill is procedure. **All conventions live in [CLAUDE.md](../../../CLAUDE.md) §B.3.** Page templates and naming rules come from there.

## When this skill runs

- The user asks a substantive question whose answer is in the vault.
- The user asks for a comparison, summary, or position-survey across multiple sources.
- The user names a topic or entity and asks "what do we know about this?"

Skip this skill if:
- The user is asking how the schema or skills work — answer directly from CLAUDE.md, no query ceremony needed.
- The user is asking for the *list* of something (e.g., "what sources are about robotics?") — that's an index-lookup, just read `index.md` and answer.
- The user is doing chitchat or meta-discussion of the vault — no query ceremony.

## Phase 1 — Read the index

Read `wiki/index.md` first. It's the catalog — the LLM Wiki pattern depends on it being the entry point. Find candidate pages by name/topic match, not by full-text intuition.

Then read `wiki/tags.md`. The tag spine is an extra navigation primitive alongside the index — useful when the question is thematic (e.g., "what do we have on agentic workflows?") rather than named-entity.

## Phase 2 — Drill in

For each candidate page identified from the index:

1. Read the full page.
2. Follow `[[wikilinks]]` **one hop** out — don't recurse further unless the question explicitly needs deeper traversal.
3. Collect citations (which source page each claim came from) as you go.

If after drilling you realize the question is broader than the candidates suggest, return to the index — but don't fall into a search-everything trap. The index is the navigation primitive.

## Phase 3 — Answer

Compose the answer with **every claim backed by a wikilink to a `wiki/sources/` page.** No naked claims; no citations to `raw/`; no fabricated references.

Form:

- For factual lookups: short, direct, with citations.
- For comparison / position-survey: structured — claim, sources that agree, sources that disagree, where they actually diverge.
- For "what do we know about X": a short narrative built from the relevant entity / concept / source pages, citing as you go.

Brevity wins. If the wiki doesn't have the answer, say so explicitly — don't pad.

**Lean on the stranger-test first lines and infoboxes when summarizing.** Per CLAUDE.md B.3, every source/entity/concept page's first line and `[!infobox]` (when present) are written to be readable cold. If your synthesis needs to introduce a source, prefer to crib from its first line rather than inventing a fresh summary — the first line already passed the stranger test. If the first line is itself jargon-heavy or assumes prior reading, that's a Check 10 lint finding — flag it in passing per Phase 5.

## Phase 4 — Surface synthesis directions

If the answer required **real synthesis** — 3+ pages combined, a novel comparison, or an argument that didn't exist on any single page before — name it as a possible synthesis direction in one short sentence.

Do not offer casual filing as the default. File only if the user explicitly asks to create/write/file the synthesis page, or if they select a candidate and ask for it to be written. When that happens:

1. Create the synthesis page per CLAUDE.md B.3 (kind: synthesis, frontmatter shape, sources list, body). Set `trigger_skill: wiki-query` and `trigger_mode:` per CLAUDE.md §B.4.1: `user-requested` if they explicitly asked to file, `user-selected` if they picked from a slate, `agent-followon` only when filing was inferred from a clear user gesture (kryssref hint, "go ahead", an existing pre-filed-by-user stub).
2. Add backlinks: a one-line reference from each cited source page's `## Kryssreferanser` section pointing back to the synthesis (Norwegian section name per CLAUDE.md B.3).
3. Add the synthesis to `wiki/index.md` under `## Syntheses`.
4. Append a log entry: `## [YYYY-MM-DD] synthesis | <title>` with a one-line summary. The log narrative complements the frontmatter trigger fields; both exist so audit doesn't depend on either alone.

Otherwise, the answer stays as conversation only — don't file it.

### Special case — overview.md

The question *"hva handler denne vaulten om akkurat nå?"* (what is this vault currently about?) is a **standing query** whose filed answer is `wiki/overview.md` — not a dated synthesis under `wiki/syntheses/`. When the user asks it, or asks to refresh overview because material has shifted, run the query and overwrite `overview.md` with the new answer. Overview is navigational per CLAUDE.md §B.3 — no callouts, no infobox. Lint flags staleness (Check 12); lint never regenerates.

## Phase 5 — Spot follow-up work (optional)

If during the query you notice something lint-worthy (a contradiction, a missing cross-reference, a clear hub-concept gap), mention it in passing but **don't act on it.** Lint is the place for that.

## Synthesis page template (skeleton; conventions in CLAUDE.md B.3)

```markdown
---
kind: synthesis
title: "<Descriptive title in sentence case>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
ingest_model: <model id>
sources:
  - "[[<source slug>]]"
  - "[[<source slug>]]"
trigger_skill: wiki-query
trigger_mode: <user-requested | user-selected | agent-followon>
tags: []
---

<One-sentence lead stating the synthesis claim.>

## <Section heading suited to the synthesis>

<Body. Wikilink every claim to its supporting source. Use `> [!warning] Conflict` if sources disagree.>

## Åpne spørsmål

- <Where the synthesis is incomplete; what would extend it.>

## Kryssreferanser

- Kilder syntetisert: <wikilinks>
- Relaterte konsepter: <wikilinks>
- Relaterte synteser: <wikilinks>
```

## What query does NOT do

- Query **does not** ingest new sources, even if it finds a gap.
- Query **does not** modify source / entity / concept pages. The only writes allowed are for an explicitly requested synthesis filing: a new synthesis page, backlinks on cited source pages (a one-line cross-reference), index entry, and log entry.
- Query **does not** speculate. If the wiki doesn't have it, say so.

## Neighbor awareness

- **/wiki-ingest** — if the user's question reveals an obvious source gap ("I read X recently but it's not in the vault"), suggest ingesting it. Don't ingest as part of query.
- **/wiki-lint** — if the question surfaces multiple lint-worthy issues, suggest a lint pass. Don't run one inline.
