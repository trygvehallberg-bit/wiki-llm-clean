---
name: wiki-ingest
description: Ingest a source into this vault's wiki. Triggers on the word "ingest" in user messages, on a path like `raw/.../*.md` or `inbox/*.md` mentioned as the thing to process, on "re-ingest <path>", or when the user drops a file in `inbox/` and asks for next steps. Covers the full lifecycle: triage (if file is still in `inbox/`), fresh ingest, or diff-and-reconcile re-ingest (if a `wiki/sources/<slug>.md` already exists for the source). Do NOT invoke for query questions or for lint passes.
---

# /wiki-ingest

Combined triage + ingest + re-ingest playbook for this vault.

This skill is procedure. **All conventions (frontmatter shape, filename derivation, callout discipline, body sections, transcript extensions, tag policy) live in [CLAUDE.md](../../../CLAUDE.md) §B.3 and are not restated here.** When this skill says "create the source page per conventions," follow B.3.

## When this skill runs

- User says "ingest" (with or without a path).
- User refers to a file in `inbox/` or `raw/` as the thing to process.
- User says "re-ingest <path>" or "re-ingest the concept <name>".
- Inbox is non-empty and the user gives a general "process the inbox" prompt.

If multiple inbox files are involved, **process one at a time** (per the user's ingest-one-by-one preference, recorded in auto-memory). Do not batch.

## Phase 0: Plan-before-run gate and exclusion gate

**Model-awareness at start-up (per CLAUDE.md B.4.0).** State the model this ingest is running on in your opening line. Stay silent on any workhorse-or-better tier (Sonnet, Opus, GPT-5.5, GPT-5.3-Codex and equivalents all do the job); do not nag. Add a one-line note only if the model is at the weakest tier that collapses prose (Haiku-class per `meta/vault-config.md`), e.g. *"running on <model>, which is below the prose bar for ingest; consider a stronger model or re-ingest later."* Awareness, not a gate: do not block. For batch / multi-source ingest, confirm model + effort inside the plan-before-run paragraph below instead of noting per source.

**Plan-before-run.** Per CLAUDE.md B.4.0: if this invocation will touch more than ~15 wiki pages, or will run ingest/re-ingest on more than one source, present a one-paragraph plan first (scope, expected touches, risks) and wait for go. Single-source ingest of a normal transcript (one source page + ~10 entity/concept touches) does not need a plan.

**Large operations split work across model sizes.** For multi-page mechanical work (frontmatter sweeps, infobox retrofits, mass renames) propose the slice split in the plan: Opus for judgment-heavy slices (substantive bios, syntheses, schema), Sonnet via Agent for templated mechanical slices, Bash for purely scripted edits. Surface this at plan time. Don't default everything to Opus.

**Pre-ingest exclusion gate (required when any input file is in `inbox/`).** Per CLAUDE.md B.4: before moving, deeply reading, summarizing, or ingesting any file from `inbox/`, ask the user: *"Are there any files in here we shouldn't use at all and should flag for delete?"* Record any exclusions in the operation notes (or in the active triage report). Do not inspect excluded files beyond the minimum needed to identify them. Skip this gate only when the input path is already under `raw/`. That file has cleared triage already.

**Snipd batch candidate gate (Snipd episodes only).** When the target is Snipd episodes — a `raw/Snipd/Data/**` path, or an "ingest the Snipd episodes / all un-ingested Snipd" request — run two gates before ingesting, using the thresholds in `meta/vault-config.md` "Snipd ingest gating". (1) **Readiness:** include only episodes whose `last_snip_date` is at least the settling window old (default 7 days); recompute from frontmatter each session rather than trusting a stale standing list, since Snipd keeps growing episodes. "ingest X now" overrides early; "hold X" excludes a paused one. (2) **Worthiness:** don't auto-take every settled episode. Present the settled, not-yet-ingested candidates as a short table (topic · podcast · `snips_count` · age), recommend a cut (≤ 2 snips = likely-skip passing highlight; off-domain topic = skip?), and let the user confirm. `snips_count` is a soft signal, not a hard cutoff. For a Snipd batch this folds into the plan-before-run paragraph above.

## Phase 1: Triage (only if source is in `inbox/`)

**Skip this entire phase** if the input path is already under `raw/`. Jump straight to Phase 2.

Only run Phase 1 when the user gives you (or you find) a file in `inbox/`. The Phase 0 exclusion gate must have run already; non-excluded files only from here on.

1. **Read the inbox file.** Open its YAML frontmatter if present. Note any user-comment field (the web-clipper `Egen kommentar`, a margin note, a covering message): it is the user's steering for this source (emphasis + the user's own cross-links), to be applied in Phase 3 per CLAUDE.md B.3 "User notes and source provenance". An empty field means no steering.
2. **Determine type** (`articles`, `papers`, `transcripts`, `media_logs`, `assets`):
   - Frontmatter `source_kind` is authoritative when present (`raw transcript` → `transcripts/`, `article` → `articles/`, `paper` → `papers/`, image-like → `assets/`, exported media log → `media_logs/`).
   - Else: `.pdf` → `papers/`, image extensions → `assets/`, a folder of per-item card files exported from a media-tracking service (Goodreads, Letterboxd, etc.) → `media_logs/`, `.md` / `.txt` with talk-like structure → `transcripts/`, otherwise `articles/`.
   - **If genuinely ambiguous, ask the user.** Do not fall back silently.
3. **Determine date** (the `<YYYY-MM-DD>` prefix):
   - Frontmatter recording or publication date if present.
   - Else file mtime.
   - Else today.
4. **Determine slug / destination name.** Per CLAUDE.md B.3 derivation rules. Lowercase, underscore-separated. Frontmatter `title:` field wins; fall back to filename. For `media_logs`, the destination is a folder (`<export-name>/`), not a single-file slug; see step 5b.
5. **Construct canonical path:**
   - Standard types: `raw/<type>/<YYYY-MM-DD>_<slug>.md`.
   - **Media-logs branch (5b):** `raw/media_logs/<export-name>/`. The **folder** is the canonical raw source unit (CLAUDE.md B.3 "Filenames and slugs" + "Media logs"). Preserve the import filenames inside the export folder unless there is a specific dedup/encoding problem. Do not generate one `raw/<type>/<date>_<slug>.md` per item.
6. **Collision check.** If a file with the same canonical slug already exists in `raw/<type>/` (any date), **do not overwrite**. Switch this invocation to **re-ingest mode** on the existing raw file and log the dedup detection. For media-log export folders, collision check is at the folder name; if it exists, merge into the existing folder (preserving distinct item filenames) rather than overwriting.
7. **Move** `inbox/<original>` → canonical destination. Original file/folder is gone from `inbox/`. **Do not modify the file's contents.** Only the location and name change.
8. **Log a triage line** in `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] triage | <original name> → <canonical path>
   <one line on type-source and date-source>
   ```

Continue to Phase 2 with the canonical raw path as input. For media-log folders, Phase 2 produces an **aggregate** source/synthesis page per CLAUDE.md B.3 "Media logs". Prefer one aggregate page over one wiki page per item.

## Phase 2: Mode selection

Derive the expected wiki source-page filename per CLAUDE.md B.3 source-filename rules (`<Surname> - <Topic>.md` for transcripts, `<Title>.md` for papers/articles; honorific-drop, topic-summarization-when-title-too-long, and full-name disambiguation rules all live in B.3).

Check whether `wiki/sources/<derived-filename>.md` already exists. Two paths:

- **Source page does not exist** → continue to Phase 3 (fresh ingest).
- **Source page exists** → jump to Phase 4 (re-ingest).

## Phase 3: Fresh ingest

1. **Read the source completely** before writing anything. Don't skim.
1a. **Read `wiki/tags.md`** so the current tag universe is fresh. You'll use it both for tagging the new source and for spotting sub-tag candidates in step 7a.
2. **Create `wiki/sources/<source-page-name>.md`** per CLAUDE.md B.3:
   - **Apply any user steering and keep the source type visible** (CLAUDE.md B.3 "User notes and source provenance"). If the source had a user-comment field, let it weight `## Key claims`, the lead, and ordering, and turn the user's stated connections into concrete cross-reference / tag / synthesis-seed candidates (pointers, not dictation). **It is additive emphasis, not a filter:** curate the whole source comprehensively first, then let the note lift and order — don't tunnel onto only the flagged points or skip what the user didn't mention (including anything that complicates the user's take). Record the source type neutrally in the infobox `Type` (talk / paper / article / idea-note / dialogue / clipping) so established fact stays distinguishable from the source's own assertion. For user-authored notes/dialogues, curate as a normal source: provenance as a neutral type, never a reliability disclaimer (CLAUDE.md B.10).
   - **Write to the four-bucket writing standard.** Short checklist (full standard in `meta/vaultos-lang-en.md`, "Writing & structure standard"): **Structure:** define in the first sentence · most important first · one page, one topic · link inline. **Clarity:** stranger test · define each term once. **Prose:** active, full sentences · no anti-patterns. **Content:** attribute · no datestamping · citations point to sources, not raw.
   - Frontmatter shape (kind, title, dates, ingest_model, source_path as a list, tags); see B.3.
   - **First line: one-sentence summary that passes the stranger test** (B.3). Lead with what the source argues / covers; attribution after. If a reader has to know the speaker to parse the sentence, rewrite it.
   - **`[!infobox]` callout at the top** per B.3, default-on for source pages. Content: Type / Speaker (or Author) / Date+venue / `## Key terms` with 3-5 short definitions of vocabulary the body uses. **Do not duplicate Key claims into the infobox**; those live in the body's `## Key claims` section. The infobox is at-a-glance orientation, not a tl;dr. Skip only if the page is trivially short with no specialized vocabulary.
   - Standard sections: `## Key claims`, `## Context`, `## Open questions`, `## Cross-references` (skip sections that don't apply).
   - If `source_path` points into `raw/transcripts/`, add the transcript extension sections (`## Speakers`, `## Talk metadata`, `## Timestamped highlights`, optional `## Q&A`) between `## Context` and `## Open questions`. See B.3.
   - Callouts per B.3 discipline (2–5 per source page ceiling; semantic types only). The `[!infobox]` doesn't count against the 2-5 body-callout ceiling. It's structural, not content.
3. **Update or create entity pages** for every named thing the source meaningfully discusses (people, orgs, products, named events). Add the new source to each entity's `sources:` frontmatter and add a paragraph wherever the new source advances that entity's story. For new entities, create the page with frontmatter per B.3 (including `entity_type:` from the `meta/vault-config.md` enum): **first line passes the stranger test**, **`[!infobox]` at the top** with Type / Role / Affiliations / top sources / Key terms (default-on).
4. **Update or create concept pages** for every concept the source meaningfully discusses or extends. New concept pages: **first line passes the stranger test**, **`[!infobox]` at the top** with one-line definition / argued-by-N-sources / Related concepts / Key terms (default-on).
5. **Cross-reference contradictions.** If the source contradicts an existing claim in another page, use `> [!warning] Conflict` per B.3. Don't pick a side silently.
6. **Role-label cross-references.** In `## Cross-references`, avoid bare "see also" links. When this source belongs with sibling sources or concepts, name the role: "framework layer of the same argument", "contrasting position on X", "runtime example of Y". These labels are synthesis seeds.
6b. **Reciprocal-link audit.** After filing outbound `## Cross-references`, walk back through the 2–3 most relevant existing pages and ask: "should they point back here?" The wiki-ingest workflow is naturally outbound-heavy: new pages get rich kryssreferanser, but existing pages don't update unless explicitly touched. A 2-minute reciprocal-audit closes the silent gap that Check 5 (Missing Cross-References) later flags. Check: the hub-page closest to this source (the entity who said the thing, the parent concept), sibling sources in the same cluster, and any synthesis pages that argue against or alongside. Add 1-line tilbake-lenker where they're missing.
7. **Post-ingest synthesis reflection.** Before logging, ask whether this source makes a 3+ source cluster visible, adds a new vantage to an existing cluster, or leaves a near-threshold idea. If yes, record it as a possible synthesis direction in the log. **Do not create a synthesis page during ingest.**
7a. **Post-ingest tag reflection.** Per CLAUDE.md B.3 tag budget (1 top-level tag + 0–3 sub-tags, max 4 total). Apply top-level tag when fit is clear. Then ask: does this source share a bridge-theme with ≥2 existing pages that would benefit from a sub-tag that doesn't yet exist? If yes, propose the new sub-tag: add it to `wiki/tags.md` with a one-line definition under its nearest top-level tag, apply to this source plus the matching existing pages. Don't create one-page tags or descriptive duplicates of what wikilinks already convey.
8. **Update `wiki/index.md`:** add the new source under `## Sources`, and any new entities/concepts under their sections. One bullet per item, one line per bullet (see existing index for format).
9. **Append to `wiki/log.md`:**
   ```
   ## [YYYY-MM-DD] ingest | <source title>
   <narrative summary of what was touched, which cluster this source joined if any, and any possible synthesis directions now visible>
   ```
10. **Report what changed.** List every page created or modified. That makes audit easy. Don't ask permission for individual entity/concept page creations; per CLAUDE.md B.5, that's the design.

Skip steps that don't apply. Don't fabricate placeholder content. If a concept is mentioned but you don't have enough context for a real page, log it under `## Open questions` on the source page and move on.

## Phase 4: Re-ingest (diff-and-reconcile)

Two flavors:

### Source-driven re-ingest (the common case)

Triggered by `re-ingest raw/.../foo.md` or by a collision detection from Phase 1.

1. Read the source fresh.
2. Read the existing `wiki/sources/<source-page-name>.md`.
3. Produce a diff: what the old page said, what your new read says, where they disagree.
4. Apply the diff. Propagate updates to linked entity/concept pages.
5. Append to a `## Re-ingest history` section at the bottom of the source page:
   ```
   ### YYYY-MM-DD · <model id>
   <one-line summary of what changed>
   ```
6. Bump `updated` and `ingest_model` in the frontmatter.
7. Log:
   ```
   ## [YYYY-MM-DD] reingest | <source title>
   ```

If the re-ingest contradicts an established claim, flag it in both the log entry and the source page's `## Re-ingest history`. Never silently overwrite.

### Topic-driven re-ingest (rare)

Triggered by `re-ingest the concept <name>`.

1. List every source linked from the concept page.
2. Re-read all of them fresh.
3. Rewrite the concept page from scratch.
4. Save the diff against the prior version to `wiki/syntheses/rapporter/Reingest - <topic> - YYYY-MM-DD.md` (natural form per B.3).
5. Log:
   ```
   ## [YYYY-MM-DD] reingest | concept <name>
   ```

## Neighbor awareness

This skill knows about its siblings. Use them when appropriate:

- **/wiki-lint:** if while ingesting you notice the vault has accumulated work that lint should sweep (recurring tag candidates, drift, multiple sources arguing the same thing), make a note in the source page or the log, but don't run lint as part of ingest.
- **/wiki-query:** ingest may surface a question that needs answering against the wiki ("how does this source relate to X?"). Note the question and let the user invoke the query skill if they want it answered.

## Page template: fresh source page (skeleton only; conventions in B.3)

```markdown
---
kind: source
title: "<Source title>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
ingest_model: <model id>
source_path:
  - raw/<type>/<YYYY-MM-DD>_<slug>.md
tags: []
---

> [!infobox]
> **Type:** talk / paper / article
> **Speaker/author:** [[<Name>]] (<role/org>)
> **Date:** YYYY-MM-DD, <venue>
>
> ## Key terms
> - **<Term>:** one-line definition
> - **<Term>:** one-line definition

<One-sentence summary that passes the stranger test. Lead with what the source argues or covers; attribution after.>

## Key claims

- ...

## Context

<Background that helps but isn't core to the claims.>

<!-- For transcripts only: insert between Context and Open questions -->

## Speakers

- <name>: <role>

## Talk metadata

- Venue · Date · Event · Original recording link

## Timestamped highlights

- [HH:MM:SS] <speaker>: <claim or quote>

## Q&A

<Optional. Per-turn attribution.>

<!-- End transcript extension -->

## Open questions

- ...

## Cross-references

- ...
```

## Page template: entity page

```markdown
---
kind: entity
title: "<Name>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
ingest_model: <model id>
entity_type: <person | org | product | work | place | event | dataset | publication>
sources:
  - "[[<source slug>]]"
tags: []
---

> [!infobox]
> **Type:** <entity_type> (person / org / product / work / place / event / dataset / publication)
> **Role:** what they're known for, in one line
> **Affiliations:** [[<org>]] · [[<event>]]
>
> ## Sources
> - [[<source slug>]]
> - [[<source slug>]]
>
> ## Key terms
> - **<Term>:** one-line definition
> - **<Term>:** one-line definition

<One-sentence description that passes the stranger test. Lead with what they are / what they do; affiliation after.>

<Paragraphs about the entity. Add a new paragraph for each source that meaningfully advances the entity's story.>
```

## Page template: concept page

```markdown
---
kind: concept
title: "<Concept name in sentence case>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
ingest_model: <model id>
sources:
  - "[[<source slug>]]"
tags: []
---

> [!infobox]
> **Short definition:** one-line, can be formula-like
> **Argued by:** N sources: [[<source slug>]] · [[<source slug>]]
> **Related:** [[<sister concept>]] · [[<sister concept>]]
>
> ## Key terms
> - **<Term>:** one-line definition
> - **<Term>:** one-line definition

<One-sentence summary that passes the stranger test. Lead with what the concept means in plain language; provenance after.>

<Body. Cross-link related concepts and the sources that argue for them.>
```

## Reminders that are easy to skip

- **First line of every page passes the stranger test** (B.3): readable by someone who hasn't read the source. Index uses it verbatim, so jargon in the first line poisons the index too.
- **`[!infobox]` is default-on** for source/entity/concept pages; skip only for trivially short pages with no specialized vocabulary. See CLAUDE.md B.3 "Infobox sidebar."
- **Cross-references use `[[wikilinks]]`,** never raw paths.
- **Cross-references need role labels** when linking sibling sources or concepts. Bare links make future synthesis harder.
- **Ingest can log synthesis seeds, but does not file syntheses.** Formal synthesis pages require an explicit user request or selected candidate.
- **Citations point at `wiki/sources/` pages,** never directly into `raw/`.
- **Bump `updated` and `ingest_model`** on every edit to an existing page.
- **`sources:` and `source_path:` are always block-style lists,** even with one entry.
- **Same-source dedup:** if two raw files describe the same underlying source, both `source_path:` entries live on one wiki source page (CLAUDE.md B.6).
- **Anti-AI prose per §A.6 + the wiki language's idioms per the pack:** check bullets and infobox text for em-dashes, telegraphic style, reflexive contrastive negation ("it's not X, but Y"), and Latinate nominalizations before logging. These are the most frequent LLM tics in wiki prose.
```
