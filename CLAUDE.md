# CLAUDE.md

This file is auto-loaded by Claude Code. It has two parts:

- **Part A — Behavioral baseline.** General guidelines for any work in this repo.
- **Part B — Vault schema.** How this specific knowledge vault is structured and operated.

For vault operations, Part B overrides Part A where they conflict (see [§B.5 Schema overrides](#b5-schema-overrides)).

---

# Part A — Behavioral baseline

Behavioral guidelines to reduce common LLM mistakes. Bias toward caution over speed. For trivial tasks, use judgment.

## A.1 Think before coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## A.2 Simplicity first

**Minimum work that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## A.3 Surgical changes

**Touch only what you must. Clean up only your own mess.**

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.
- Remove imports/variables/functions that *your* changes made unused. Don't remove pre-existing dead code.

The test: every changed line should trace directly to the user's request.

## A.4 Goal-driven execution

**Define success criteria. Loop until verified.**

Strong success criteria let you work independently. Weak criteria ("make it work") require constant clarification.

## A.5 Calibrate explanation to stakes

Triage first, then explain:

- **Chore** — routine, reversible, one command. Just do it. A one-line "done" beats a recap.
- **Choice** — real trade-off but low risk. 2-line either/or with a recommendation.
- **Decision** — load-bearing, hard to reverse. Full analysis.

### Default to doing, not asking

The vault exists to be used. Asking permission on chores is itself a cost. Default to acting on reversible work; ask only when:

- The action is destructive or hard to undo (deletion, force-push, mass rename).
- The action edits a protected design doc (`CLAUDE.md`, `.claude/skills/**`, `meta/**`) without prior accept in this thread.
- There's a real trade-off between options the user actually has to pick between.

Don't ask before:

- Applying a change the user just said yes to.
- Routine ingest, lint, query, synthesis on the source currently in front of you.
- Committing or pushing on user instruction.
- Fixing obvious problems (typos, line endings, broken wikilinks, syntax errors, layout glitches).
- Continuing the immediate next step in a flow already in motion.

### Don't manufacture drama

Match the report's tone to the work's actual stakes:

- No crisis framing ("Stort funn:", "alvorlig feil", "⚠️ kritisk") on cosmetic fixes.
- No extended apologies or self-flagellation on routine mistakes — name the fix and move on.
- No bullet-recap of a change that's already self-explanatory from context.
- No restating in different words what you just said.

"Done. [[link]]" beats a five-bullet summary when the work is small.

---

# Part B — Vault schema

This is a shared, LLM-maintained knowledge vault implementing Karpathy's LLM Wiki pattern (full source: [[Karpathy - LLM Wiki]]). Package boundary (portable VaultOS vs this instance's content): `meta/vaultos-manifest.md`.

> [!info] Parametric config (Claude Code `@import`)
> This schema reads parametrically. The per-vault parameters and the Norwegian language/form pack are imported below; Part B sections point into them rather than inlining the values. The pattern (rules) stays here in CLAUDE.md; the parameters (values) live in the imported files. The imports are parameter tables CLAUDE.md routes into, not a competing rulebook.

@meta/vault-config.md
@meta/vaultos-lang-no.md

## B.0 Where to start

**Before your first reply in any session — including a greeting — check whether `first-time.md` exists at the vault root.** If it does, a human is setting up for the first time: **do not** open with a generic greeting or a skill list. Read `first-time.md` immediately and start walking them through its checklist (it points into `README.md`), then offer to delete it. (It is onboarding only — nothing depends on it, so its absence is the normal steady state; then greet and proceed normally.)

Pointers an incoming session should hit before non-trivial work:

- **Before any non-trivial edit, read `handoff.md` and `todo.md` at the vault root.** If they say "No ongoing task" and your work isn't trivial, update them before stopping. For substantial follow-up, also read the linked handover under `meta/handovers/`. The full incoming/outgoing protocol lives in [[meta/handoff-protocol]].
- **Read [[Karpathy - LLM Wiki]] before discussing system structure, intent, or schema changes.** It is Karpathy's original pattern document — the *why* behind the three-layer architecture and the schema-as-configuration premise. Don't propose schema edits without reading it.

## B.1 Purpose and premises

- **Shared.** Multiple colleagues drop sources; one wiki emerges.
- **Multi-author at the human layer, single-author at the wiki layer.** Humans only write to `raw/`. You are the sole author of everything in `wiki/`.
- **Hands-off ingest.** Colleagues trigger ingest without per-source steering. This schema must be precise enough that you don't need to guess.
- **Dynamic.** Old sources get re-ingested as models improve. Wiki pages record which model last touched them.
- **Wiki language vs meta language.** Sources may arrive in any language; wiki content (`wiki/` page bodies, summaries, index entries, log entries, source pages) is written in the vault's wiki language. Operational/meta documentation (`CLAUDE.md`, `AGENTS.md`, `meta/**`, skills) stays in English by default. (Language is a per-vault parameter — see `meta/vault-config.md`; the language/form details live in the swappable pack `meta/vaultos-lang-<xx>.md`, set during first-time setup.)

## B.2 Layout

```
<vault-root>/
├── CLAUDE.md        ← this file
├── AGENTS.md        ← pointer for non-Claude agents (read-only)
├── handoff.md       ← State layer: current ongoing work and next step, updated every session
├── todo.md          ← State layer: short mutable task list for current/remote follow-up
├── meta/            ← human-curated documentation; do not edit unless asked
│   ├── LLM Wiki - Karpathy.md
│   ├── vault-config.md             ← this vault's instance parameters
│   ├── vaultos-lang-<xx>.md        ← swappable language/form pack
│   ├── vaultos-manifest.md         ← portable-vs-instance package boundary
│   ├── handoff-protocol.md         ← rules for handoff.md, todo.md, handovers/
│   └── synthesis-generation-recipe.md
│   (handovers/ appears here once substantial work is handed over)
├── inbox/           ← STAGING. Humans drop files here; triage moves them to raw/.
├── raw/             ← Source documents. READ-ONLY after triage. Frozen archive.
│   ├── articles/
│   │   └── <corpus>/  ← exception for multi-file archives from a single publication; preserves original filenames
│   ├── papers/
│   ├── transcripts/
│   ├── media_logs/  ← Structured imports such as Goodreads/Letterboxd item logs
│   └── assets/      ← images, PDFs referenced from raw files
├── wiki/            ← LLM-OWNED. Create and maintain everything here.
│   ├── home.md      ← human-facing category-chooser launcher (Homepage-plugin entry point); callout-card UX, see B.3 exception
│   ├── index.md     ← catalog of all wiki pages (LLM/query entry point)
│   ├── log.md       ← append-only operations log
│   ├── overview.md  ← top-level narrative; the filed answer to "what is this vault currently about?" — refreshed via /wiki-query when material has shifted (lint flags staleness, never regenerates)
│   ├── tags.md      ← canonical tag registry (see B.3)
│   ├── entities/    ← people, orgs, products, named things
│   ├── concepts/    ← ideas, techniques, themes
│   ├── sources/     ← one summary page per ingested source
│   └── syntheses/   ← analyses, comparisons, lint reports
└── personal/        ← Personal operational layer. OUTSIDE wiki schema and wiki ops. See B.10.
    └── coach/       ← Coach domains (helse, økonomi, hus og hage, …) with personal data and notes
```

**Read/write boundaries:**

- `inbox/` is **staging**. Humans drop files here in any format, any name. The agent has write access — but only via the triage phase of `/wiki-ingest`. Don't modify inbox files in place; just route them.
- `raw/` is read-only **after triage**. The agent writes to `raw/` only as the destination of a triage move. Once a file lands here with its canonical name, it is frozen for the life of the vault.
- `meta/` is human-curated. Don't edit unless explicitly asked.
- `handoff.md` and `todo.md` are the mutable session state layer. Update them at handoff points, before long pauses/remote continuation, and when a task becomes complete or blocked.
- `wiki/` is your domain. Create, edit, and reorganize freely within the conventions below.
- `personal/` is owned by the human. The agent edits there only when explicitly directed — coach work, log entries, plan updates. Wiki operations (ingest/lint/query/synthesis) never touch it. See B.10.
- Protected workflow/config files are changed only after explicit human accept. See B.12. Exception: `/wiki-lint` Phase 6 updates the §B.0 latest-lint pointer as a single-line edit; see the wiki-lint skill.

**Audience: human-first vs. agent-first.**

Noen sider er skrevet for menneskelig lesning: `wiki/{entities,concepts,sources}/**`, substantielle synteser, `wiki/{home,overview,index}.md`. §B.3 Naturlig-norsk-mønstre, infobox-disiplin og first-line stranger-test gjelder her.

Andre sider er agent-først arbeidsartefakter: `handoff.md`, `todo.md`, `meta/handovers/**`, `wiki/log.md`, og daterte outputs som `wiki/syntheses/Triage - YYYY-MM-DD.md`, `wiki/syntheses/Lint - YYYY-MM-DD.md` og `wiki/syntheses/Reingest - <topic> - YYYY-MM-DD.md`. Telegrafisk format, checkbox-tabeller og filsti-enumerering er funksjonelt riktig her — naturlig-norsk-lint, infobox-regel og stranger-test gjelder ikke. Lint og ingest leser denne aksen heller enn å enumerere unntak.

**Plugin-sync roots:**

Some `raw/` subfolders are synced live by Obsidian plugins and differ from triage-canonical paths: folder casing and internal layout follow the plugin (not the lowercase-slug convention in B.3), triage is skipped (`/wiki-ingest` Phase 1 already short-circuits anything under `raw/`), and plugin-owned support files are overhead, not sources (lint must not flag them; ingest must not process them). Some plugins also expose cover/logo URLs in episode frontmatter that are valid inline image sources for wiki pages (reference `![Cover](url)`; do not mirror into `raw/assets/`).

The specific plugin-sync roots, their overhead-file names, and their cover-URL conventions for this vault are parameters — see `meta/vault-config.md`.

## B.3 Page conventions

### Frontmatter (required on every wiki page)

```yaml
---
kind: entity | concept | source | synthesis
title: <human-readable title>
created: YYYY-MM-DD
updated: YYYY-MM-DD
ingest_model: <model id, e.g. claude-opus-4-7>
sources:                          # for entity/concept/synthesis
  - "[[source-slug-1]]"
  - "[[source-slug-2]]"
source_path:                      # for kind: source only; always a list, even with one entry
  - raw/articles/2026-05-20_foo.md
trigger_skill: wiki-synthesis     # for kind: synthesis only; which skill filed the page
trigger_mode: user-requested      # for kind: synthesis only; how the filing was triggered
tags: []                          # optional; draw from wiki/tags.md, see B.3
---
```

**List fields are always lists.** `sources:` and `source_path:` are always block-style lists, even when there's a single entry. Keeps the shape consistent for anything reading frontmatter and makes dedup (multiple raw files → one wiki source page) a no-op rather than a type change.

- `created` is the date you created the page.
- `updated` is bumped on every edit.
- `ingest_model` is your model id at the time of the most recent edit. Use the exact platform-versioned ID (e.g. `claude-opus-4-7`, `claude-sonnet-4-6`, `gpt-5-codex`), not a generic family alias (e.g. `gpt-5`, `claude`). Used by lint to find re-ingest candidates.
- For `kind: source`, omit `sources:` (the source is itself) and set `source_path:`. For other kinds, set `sources:` and omit `source_path:`.
- For `kind: synthesis`, set `trigger_skill:` (`wiki-ingest` | `wiki-query` | `wiki-synthesis` | `wiki-lint` — which skill filed the page) and `trigger_mode:` (`user-requested` | `user-selected` | `agent-followon` — how the filing was triggered). Other kinds omit both. See §B.4.1 for semantics. Lint sub-check 9f flags missing or out-of-vocabulary values.

### Filenames and slugs

Two naming conventions, by kind:

- **All wiki pages use natural form** — capitalized appropriately for the page language (sentence case for concepts, proper case for entities), spaces preserved, ASCII. Why: every folder the user navigates should read like natural language, not like a URL bar.
  - Entities: `Ada Lovelace.md`, `HAL 9000.md`, `RoboCon 2027.md`.
  - Concepts: `Analytical engines.md`, `Recursive self-improvement.md`, `Knowledge compounding.md`.
  - Sources: `<Speaker/Author> - <Topic>.md` for talks (e.g., `Lovelace - Analytical engines.md`); `<Title>.md` for papers/articles (add `(Author Year)` for disambiguation when titles collide).
  - Syntheses: descriptive title in sentence case (e.g., `Attention vs Mamba comparison.md`). Date-stamped exception: `Lint - YYYY-MM-DD.md`, `Reingest - <topic> - YYYY-MM-DD.md`.
- **Sources need a distinguishing element** — speaker/author prefix for talks, title for papers — because a source about "Analytical engines" would otherwise collide with the concept page of the same name. Sources are documents about a topic, not the topic itself.
- **Slugs survive in two places only**: `raw/<type>/<YYYY-MM-DD>_<slug>.md` (machine-organized archive, agent rarely navigates) and tags (labels, not folders).
- `wiki/syntheses/Lint - YYYY-MM-DD.md` and `wiki/syntheses/Reingest - <topic> - YYYY-MM-DD.md` — date-stamped exception for periodic outputs (natural form, consistent with other syntheses).
- `raw/<type>/<YYYY-MM-DD>_<slug>.md` — date-prefixed canonical form. ISO 8601 hyphens in the date, underscore between date and slug, underscores within the slug. This is the **output** of triage, not the input. Humans drop files into `inbox/` with any name; the agent generates this canonical path during the triage phase of `/wiki-ingest`. Raw filenames always use slug form regardless of source kind.
- `raw/media_logs/<export-name>/` — exception for structured media-log item cards exported from services such as Goodreads or Letterboxd. Preserve the import filenames inside the export folder unless there is a specific dedup/encoding problem; the folder, not each item file, is the canonical raw source unit. Prefer aggregate source/synthesis pages over one wiki page per item.
- **Reserved Vault DNA names.** Wiki entity, source and concept filenames must not match (case-insensitively) the agent-instruction filenames that AI tooling auto-loads as project context — the vault's "DNA". When a natural page name would collide (e.g., the AI product family Claude), use parenthetical disambiguation (`Claude (Anthropic).md`) and add the natural form to the page's `aliases:` frontmatter so `[[Claude]]`-wikilinks still resolve. The current reserved-name list is a parameter — see `meta/vault-config.md` (maintain it there; extend when new auto-load conventions emerge).

**Derivation rules:**
- For entities: drop honorifics (`Dr`, `Prof`, `Mr`), preserve given-name + surname order and capitalization, keep accents in ASCII-safe form where reasonable. Org/product/event names stay as commonly written.
- For concepts: sentence case in the page language (first word capitalized + proper nouns/acronyms). `Analytical engines`, `Recursive self-improvement`, `Knowledge compounding`. Avoid title case (`Analytical Engines`) — concepts aren't titles.
- For source pages (transcripts): `<Speaker surname> - <Topic in sentence case>.md`. Drop honorifics. Topic is short — not the full talk title. When the literal title is over-long or multi-clause, summarize the topic from the talk's content (e.g., `Caching strategies, retry semantics, and idempotent writes in distributed queues` → `Reliability lessons for distributed queues`). When `<Surname> - <Topic>` would collide with an existing source, use `<Full given name> <Surname> - <Topic>` instead (e.g., `Ada Lovelace - …`, `Alan Turing - …`).
- For source pages (papers/articles): `<Title in sentence case>.md`. Append `(Author Year)` only if needed to disambiguate.
- For syntheses: descriptive name in sentence case; dated outputs use `Lint - YYYY-MM-DD.md` and `Reingest - <topic> - YYYY-MM-DD.md`.
- For raw filenames and tags (the only remaining slug contexts): lowercase, underscore-separated, ASCII. Strip articles ("the", "a") if the slug gets long. No trailing punctuation. (Hyphens are reserved for ISO 8601 dates and grammatical compounds in titles like `AI-native`, `sim-to-real`.)
- **Frontmatter is authoritative.** If the raw file has a `title:` field, derive the name (or slug) from it. Fall back to the filename only if no title is present.

Same-source dedup still works under this rule: ingesting the Lovelace transcript twice produces the same source filename (`Lovelace - Analytical engines.md`) and the same entity name (`Ada Lovelace.md`) — collision check happens at the filename layer in both cases.

### Tags

Tags exist to connect pages that would otherwise stay far apart — across time, across source, across kind. The canonical registry lives at `wiki/tags.md` — **read it before tagging.**

**Tag budget per page:**
- **1 hovedtag** (top-level domain) — required when a fit is clear. Drawn from the 5–10 hovedtags in `wiki/tags.md`.
- **0–3 sub-tags** — specific themes that bridge this page to ≥2 others. Optional. Not every page needs sub-tags.
- **Maks 4 tags total.** Pages without a clear thematic bridge stay at 1 tag.

**Current hovedtags** are a per-vault parameter — see `meta/vault-config.md` for the list; the canonical live registry is `wiki/tags.md` (read it before tagging). Hovedtags are tags and homepage entry points, **not folders** — do not create a matching `wiki/01 Kultur/`-style taxonomy. Page placement stays governed by page kind (`wiki/sources/`, `wiki/concepts/`, `wiki/entities/`, `wiki/syntheses/`); domain grouping happens through frontmatter tags and the `wiki/home.md` cards.

**Apply an existing tag freely** when it fits the page.

**Propose a new sub-tag when:**
- The tag would apply to **at least 2 existing pages + the page in front of you** (3 total minimum).
- It does **bridge-work**: surfaces a connection between pages distant in source, time, or kind. Descriptive tags that duplicate what wikilinks already convey add nothing.
- Add it to `wiki/tags.md` with a one-line definition under its nearest hovedtag, then apply retroactively to the matching pages.

**Don't create a tag when:**
- One-page topic. The title and wikilinks already locate it.
- The page already has 4 tags.
- The tag would duplicate an existing tag's role.

**Tag form:** lowercase, underscore-separated, ASCII. Short. Hyphens reserved for ISO dates and grammatical compounds elsewhere — not in tag slugs. Flat namespace (no `ai/agents`-style nesting in the tag itself; `tags.md` may visually group sub-tags under their hovedtag).

**Lint actively curates tags** (consolidation checks): dead tags (1 use) flagged for removal, recurring untagged themes flagged for new-tag proposal, existing tags that fit untagged pages flagged for retroactive application. Application of curation findings happens after the human reviews — lint itself never silently changes tags.

### Body conventions

- **First line is a one-sentence Norwegian summary** (used verbatim by `index.md`). It must pass the **stranger test**: readable by someone who hasn't read the source, doesn't know the speaker, and doesn't know the wiki's other content. **Scope of the stranger test is the first line and the `[!infobox]` only.** The body below is free to use the jargon the infobox defines and the page is *about* — the stranger test is the welcome mat, not the wallpaper, and flattening the body to lowest-common-denominator language would make the page useless for the reader who came here to learn. Lead with *what the source argues or what the page covers* — attribution (who said it, in what venue) comes after the substance, not before. "Karpathy om vendepunktet for agentisk AI i 2026" beats "Karpathy/Sequoia: deep argument from the founder fireside." If a reader has to know the speaker to parse the sentence, rewrite it.
- **Don't smuggle the thing you're explaining into the analogy.** If explaining X requires Y, and Y only makes sense via X, the analogy feels satisfying but leaves the reader more confused than before. When you hit something load-bearing for its own field — a primitive — say so: "treat as bedrock for this page" beats a circular analogy. Use a [[wikilink]] downward to the deeper page so readers who want to push further have a door. Honest "this is one of the basic elements" beats a clever but wrong reduction.
- **Jargon must do work, or it's cut.** A technical term is *load-bearing* if the sentence collapses without it. *Decorative* jargon — there to signal expertise rather than do work — is the most common failure mode in summary writing. Test: replace the term with its plain-language definition; if the sentence loses nothing, the term was decorative. The `## Key terms` slot in the infobox is where load-bearing jargon gets defined once so the body can use it freely; jargon used in the body that isn't defined in the infobox or upstream must justify itself in place.
- **Naturlig norsk, ikke LLM-oversettelses-norsk.** Wiki-bodyen skal kjennes som norsk skrevet av en norsk skribent. The six concrete anti-patterns to avoid — wrong prepositions for languages, stranded English-pattern prepositions, Latinate `-or`/`-asjon` nominalizations where a verb form is natural, telegram-bullets without verbs, AI-rhetorical contrastive negation and signal phrases, and unmarked anglicisms — are a language-pack parameter with full definitions and tests in `meta/vaultos-lang-no.md`. (Language-neutral principle: wiki prose must read as mother-tongue, not as machine translation.)
- **Cross-references use `[[wikilinks]]`**, never raw paths — Obsidian's graph view depends on it.
- **Citations** point to `wiki/sources/<slug>` pages, never directly into `raw/`. Source pages are the single point of truth for what a source says.
- **Callouts** add value when they convey *semantic type*, not just visual variety. Use the following types where the content has that shape — and stop. 2–5 callouts per source page is a healthy ceiling; more turns the page into noise.
  - `> [!quote]` — verbatim quotes where wording is part of the value (not paraphrases).
  - `> [!important]` — load-bearing claims, key conclusions, hard constraints.
  - `> [!warning] Conflict` — contradictions between sources or pages. Example:
    ```
    > [!warning] Conflict
    > [[Source A]] claims X, but [[Source B]] claims Y.
    ```
  - `> [!warning]` — risks, open commitments, things to watch.
  - `> [!tip]` — practical advice, rules of thumb, actionable insights.
  - `> [!example]` — concrete stacks or scenarios illustrating an abstract point.
  - `> [!info]` — neutral context or background that helps but isn't core.
  - `> [!question]` — open questions worth tracking (alternative to bullets in `## Open questions`).
  - `> [!infobox]` — Wikipedia-style right-rail sidebar with type/role/key claims/key terms. Default-on for source/entity/concept pages; see "Infobox sidebar" sub-section below.
  - `> [!banner]` — full-width header/footer band on `home.md` (sheds the standard callout chrome via CSS). Reserved for that one page; do not use elsewhere.
  - Navigational pages (`index.md`, `log.md`, `overview.md`, `tags.md`) get no callouts — they're not content. **Exception: `home.md`** is the human-facing category-chooser launcher (Homepage-plugin entry point) and intentionally uses `[!banner]` for its header/footer plus one category callout (`[!tip]`, `[!info]`, `[!example]`, `[!success]`, `[!important]`, `[!question]`, `[!abstract]`) per top-level door; same semantic-type-not-just-decoration discipline still applies (each card's callout type carries meaning).
- **Section headings** on source pages: the canonical Norwegian names live in the always-imported `meta/vaultos-lang-no.md`. Skip sections that don't apply.

### Infobox sidebar (default-on)

Source, entity, and concept pages carry an `> [!infobox]` callout at the top, rendered as a right-rail floated sidebar via `.obsidian/snippets/infobox.css`. Goal: a newcomer reading the page should be able to orient themselves from the infobox alone before the body text — type, who/when, top claims, and any specialized vocabulary defined inline. Infobox field labels should be Norwegian on wiki pages — the field *roles* below are the portable pattern; the Norwegian labels are catalogued in `meta/vaultos-lang-no.md`.

Content varies by `kind`:

**Source pages:**
- **Type** — talk / paper / article (drawn from `source_path` directory)
- **Foredragsholder/forfatter** — one line; wikilink the name (`[[Surname]]` or `[[Full Name]]`) so the source becomes a visible graph edge to the author's entity page. For talks, format as `[[Surname]] (org), role`.
- **Dato / arena** — one line
- **Nøkkelbegreper** — 3-5 short one-line definitions of vocabulary the body uses that a newcomer wouldn't know

The infobox does **not** carry nøkkelpåstander — those live in the body's `## Nøkkelpåstander` section. The infobox is at-a-glance orientation (who/when/jargon), not a tl;dr.

**Entity pages:**
- **Type** — person / org / product / event
- **Rolle** — one line, what they're known for
- **Tilknytninger** — orgs / events / collaborators ([[wikilinks]])
- **Kilder** — top 2-3 wiki source pages for this entity
- **Nøkkelbegreper** — 3-5 short defs; optional if the entity isn't conceptually heavy

**Concept pages:**
- **Kort definisjon** (tighter than the page's first line — can be formula-like)
- **Argumentert av** — "N kilder" with top 2-3 wikilinked
- **Relatert** — sister concepts ([[wikilinks]])
- **Nøkkelbegreper** — 3-5 short defs of vocabulary the body uses

**When to skip:**
- Page is trivially short (stub entity with one source, no specialized terms)
- All vocabulary in the body is common-English and the page is unambiguous from the title alone

**Lint enforces:** any source/entity/concept page with specialized vocabulary or jargon that lacks an `[!infobox]` gets flagged for retrofit.

### Transcripts (extension to source pages)

When `source_path` points into `raw/transcripts/`, extend the standard source page with these sections:

- **`## Talere`** — one bullet per speaker, with name and role (host, guest, panelist, audience). Use the names that appear in cross-references throughout the wiki.
- **`## Metadata for foredraget`** — venue, date of recording (if different from ingest date), event or series name, link to original recording if present in the raw file.
- **`## Tidsstemplede høydepunkter`** — citable moments. Format: `- [HH:MM:SS] <speaker>: <claim or quote>`. Aim for 5–15 entries per hour of transcript, not exhaustive.
- **`## Spørsmål og svar`** (optional) — if the transcript has a Q&A segment, capture it here with per-turn attribution. Audience questions get their own bullets even when the asker is unnamed.

The base sections (`## Nøkkelpåstander`, `## Kontekst`, `## Åpne spørsmål`, `## Kryssreferanser`) still apply. Transcript-specific sections go between `## Kontekst` and `## Åpne spørsmål`.

### Media logs and intent lists

Imported media logs can contain both consumed works (`read`, `watched`) and unconsumed candidates (`to-read`, watchlist, `currently-reading`). Store structured item-card exports under `raw/media_logs/` during triage, and treat their statuses as different epistemic layers:

- **`read` / `watched` items are experience data.** They can support source pages, entity pages, concept pages, rating analysis, and recommendation syntheses.
- **`to-read` / watchlist items are possibility data.** They should not support claims about taste, knowledge, influence, or intellectual formation unless clearly framed as intent, curiosity, or candidate material.
- **`currently-reading` is provisional.** Use it only as active interest, not as completed evaluation.
- **Prefer aggregate source/synthesis pages for media logs** over one wiki source page per book, film, album, or episode.
- **When media logs reveal gaps, record them as knowledge holes or next investigations,** not as established conclusions.

## B.4 Operations

Four live operation skills. **CLAUDE.md is the schema authority on conventions; the skills are the procedure authority.** Skills reference back here; they never restate policy. If they ever drift, lint catches it (Check 9 in `/wiki-lint`).

- **`/wiki-ingest`** — Ingest a source into the wiki. Absorbs the whole source lifecycle: triage (when the source is in `inbox/`), fresh ingest, and diff-and-reconcile re-ingest (when a `wiki/sources/` page already exists for the source). See `.claude/skills/wiki-ingest/SKILL.md`.
- **`/wiki-lint`** — Periodic vault health check. Output is a date-stamped triage checklist at `wiki/syntheses/Lint - YYYY-MM-DD.md`. Never silently fixes anything. See `.claude/skills/wiki-lint/SKILL.md`.
- **`/wiki-query`** — Answer a question against the wiki. Reads the index first, drills via wikilinks, answers with cited claims, and may surface synthesis directions without filing them unless explicitly asked. See `.claude/skills/wiki-query/SKILL.md`.
- **`/wiki-synthesis`** — Generate synthesis ideas or run an explicit vault-backed synthesis workflow. Default mode is idea generation, not a vault scan. See `.claude/skills/wiki-synthesis/SKILL.md`.

### B.4.0 Plan-before-run threshold

Any operation expected to touch more than ~15 wiki pages, or to run on more than one source in a single invocation, presents a one-paragraph plan first (scope, expected touches, risks) and waits for go. Single-source ingest stays fully hands-off (per B.5). Anchored on the LLM Wiki principle: **"Ingest one at a time, stay involved."**

### B.4.1 Synthesis generation modes

The expanded rationale and portable recipe live in `meta/synthesis-generation-recipe.md`; this section is the operational rule for this vault.

**Default interpretation:** when the user says "create synthesis", "make synthesis", or asks for synthesis ideas without naming vault sources, treat it as **idea synthesis**. Generate candidate theses, frames, or questions. Do not assume the vault has enough content, do not scan the vault by default, and do not create files.

**Explicit vault-backed mode:** only run the vault-backed synthesis workflow when the user asks for it with language such as "from the vault", "using existing sources", "scan the vault", "file a synthesis", or when the user has picked a previously proposed candidate to write. In survey mode, propose 3-5 candidates with source basis + one-line thesis and wait for the human to pick before filing.

**During ingest:** notice synthesis seeds, strengthen role-labeled `## Kryssreferanser` entries, and log possible synthesis directions when a real 3+ source cluster appears. Do not auto-file synthesis pages during ingest.

**Synthesis provenance (frontmatter `trigger_skill:` + `trigger_mode:`).** Every filed synthesis carries both fields so audit doesn't have to depend on grepping `log.md`. `trigger_skill:` is the skill that filed the page (`wiki-synthesis`, `wiki-query` filing a followon, `wiki-lint` recording a lint-driven synthesis, or `wiki-ingest` in the rare case where a kryssref gesture during ingest leads to filing). `trigger_mode:` is the authority behind the filing:

- `user-requested` — the user explicitly invoked the skill with a synthesis ask ("file a synthesis on X").
- `user-selected` — the user picked from a slate of candidates the agent proposed.
- `agent-followon` — the agent inferred filing from context: a kryssref gesture to a not-yet-existing synthesis, a prior ingest log seed, or a query that naturally crossed the 3-source threshold and a user gesture interpretable as accept.

The fields record *the filing event*, not edit history. Subsequent edits leave them alone; only re-filing from scratch resets them.

### B.4.2 Git operations and skill commits

**No automatic git.** VaultOS never touches a remote on its own. Normal operations — ingest, lint, query, synthesis — do **zero** git: wiki content syncs through Obsidian Sync, and git is reserved for explicit commits you ask for and the curated `update` operation. You are never pinging GitHub involuntarily just by using the vault. Update-awareness is decoupled: run `update` when you want it, or set up a routine that checks on a cadence (see README → Updates / Automating ingest) — never bound to a per-action preflight.

**Commits:** Do not auto-commit or auto-push during normal vault work. When files Obsidian Sync does not handle (`.claude/skills/`, dotfiles like `.gitattributes`/`.gitignore`, anything in `.gitignore` you've deliberately edited) have been changed in this session, propose a commit at session end — do not commit silently. Everything else flows through Obsidian Sync.

## B.5 Schema overrides

Part A says "minimum work, nothing speculative" and "touch only what you must." For vault operations these still apply *within reason*, but with explicit exceptions:

- **Creating new wiki pages on ingest is the job, not a violation.** Don't ask permission to create entity/concept pages during ingest.
- **Formal syntheses are the exception to that ingest rule.** Idea synthesis is the default; vault-backed synthesis pages are filed only after an explicit user request or after the user selects a candidate.
- **Touching 10–15 files per ingest is normal.** That's the design.
- **Don't refactor unrelated wiki content.** When ingesting source A, only touch pages where source A is genuinely relevant. No drive-by improvements.
- **Lean toward creating a new page** when in doubt about whether an entity/concept deserves one. Cheap to merge later, expensive to discover the omission six months in.

## B.6 Dedup and multi-colleague

- If two `raw/` files describe the same underlying thing, both files stay (raw is immutable). The `wiki/sources/` page is shared: same slug, both paths appear in the `source_path:` list (which is always a list — see B.3), body merges both reads with a note about the duplication.
- Colleagues share the live vault through Obsidian Sync. Git history is a secondary audit trail of the snapshots you commit — taken when you ask, not one commit per operation (see B.7).

## B.7 Commits

This is a personal notes vault, not a team codebase. Commits are snapshots and sync events, not reviewable change-units. The default model is "snapshot when the user asks," not "one commit per operation."

### When the user says "commit" or "commit push"

Treat as "snapshot the whole working tree now, finish the job":
- Stage everything dirty (including `personal/` if the user changed it — it's still their vault).
- One commit, one message, push if "push" was in the request.
- Don't ask for permission. Don't split into per-operation commits unless the user explicitly asks for groupings.

The agent's job is to capture current state, not to curate a clean narrative across many commits.

### Cadence (when not explicitly prompted)

- **No auto-commit.** Nothing commits unless the user asks.
- **Single-source ingest doesn't trigger a commit on its own** (per B.5).
- **No automatic git operations.** VaultOS never touches a remote on its own; update-checking is explicit/curated (see B.4.2).

### Message format

One concise line describing what's in the snapshot. A loose taxonomy helps `git log` scanning but is not required:

`ingest|lint|query|synthesis|schema|config|housekeeping|vault: <one-line summary>`

When the snapshot spans multiple types (typical at end of a long session), pick the dominant one or use `vault:` as a catch-all. Touched-file lists in the commit body are optional — `git show` already exposes the file set, so don't restate it unless it adds judgment a reader couldn't reconstruct.

**No `Co-Authored-By` trailer.** The agent identity is already recorded via `ingest_model:` frontmatter on touched pages.

### When to be more careful

- **Destructive git operations** (force-push, `reset --hard`, branch deletion, history rewrite) — ask first regardless of cadence.
- **Working tree contains files the user clearly didn't intend to commit** (`.env`, credentials, accidental notes) — flag before committing.
- **Amending an existing commit** — prefer a new commit unless the user explicitly says amend.

## B.8 When in doubt

- Source unclear → file the ambiguity in the source page's `## Open questions`, move on.
- Page would conflict with itself → flag via `> [!warning] Conflict`, don't pick a side.
- Don't know if something deserves its own page → create one, lean permissive.
- Asked something this schema doesn't cover → answer the human and propose a schema update at the end of your reply.

## B.9 Not yet in scope

Tracked in [[backlog]]:
- Scheduled/remote automation — all operations are currently triggered live in a session.
- Public-facing slice of the wiki, multi-vault federation.
- Search engine (qmd or similar) — defer until index-file lookup outgrows itself.

## B.10 Personal layer (`personal/`)

`personal/` is a top-level folder for personal operational content — coach projects, personal data, plans, private notes. It is **outside the wiki schema** (no required frontmatter, no slug discipline, no `kind:` field, no infobox), and **outside wiki operations** (`/wiki-ingest`, `/wiki-lint`, `/wiki-query`, `/wiki-synthesis` do not touch it).

**Bridge rule (one-way):**
- `personal/ → wiki/` linking is fine. Personal notes can freely cite wiki concepts/sources for backing (`[[HRV og restitusjon]]`).
- `wiki/ → personal/` linking is not allowed. Wiki claims rest on external sources, never on personal data or experience.

Subfolders under `personal/coach/<domain>/` may include a `delt/` subfolder for content that's a candidate for sharing. **Default policy: `delt/` content stays in `personal/` permanently.** Promotion to `wiki/syntheses/` is not automatic and is not currently supported — revisit if a real need emerges.

See [[personal/README]] for scope details and what belongs where.

## B.11 State layer (`handoff.md`, `todo.md`, `meta/handovers/`)

The state layer is three files, intentionally outside the wiki schema (no frontmatter, no infobox, no index entry, no source authority):

- `handoff.md` — short re-entry prompt for the next agent (current state, next safe action, do-not-do warnings, pointers to deeper context).
- `todo.md` — short ordered active work queue.
- `meta/handovers/<YYYY-MM-DD>-<topic>.md` — detailed narrative handover, created only after substantial work. Linked from `handoff.md`.

Full rules in [[meta/handoff-protocol]].

**Incoming session rule:**
- Before any non-trivial edit, read `handoff.md`, then `todo.md`.
- If `handoff.md` links a handover under `meta/handovers/` and you're doing substantial follow-up, read it too.

**Outgoing session rule (before your last assistant turn):**
- Update `handoff.md` and `todo.md` whenever the session changed vault state, paused work, or finished a task.
- If there is no active task, write `No ongoing task.` clearly in both files.
- Create a detailed handover under `meta/handovers/` only when the work was substantial (many files touched, schema/workflow decisions, unfinished/risky state, or rejected approaches worth recording). See [[meta/handoff-protocol]] for the trigger list.
- Keep `handoff.md` and `todo.md` brief and operational. Permanent knowledge belongs in `wiki/`; operation history belongs in `wiki/log.md`; deferred design belongs in [[backlog]].

## B.12 Protected files and agent-owned zones

Some files define the operating rules rather than ordinary vault content. They need a higher barrier than wiki pages.

**Protected: require explicit human accept before editing**
- `CLAUDE.md`
- `AGENTS.md` (read-only pointer; do not edit unless the human explicitly asks for that file)
- `.claude/skills/**`
- `meta/vaultos-manifest.md` and other schema/workflow design notes in `meta/`
- `.obsidian/**` settings and snippets, unless the user is explicitly asking for Obsidian UI/config work

For protected files, first state the intended change and wait for a clear accept such as "go", "yes", "do it", or an explicit instruction naming the file/change. A broad wiki/import instruction is not permission to edit protected workflow/config files.

When proposing edits to a protected file, show changes as a unified diff (only changed lines plus minimal context), not the full new section. Re-reading unchanged content to find the change wastes the user's attention.

**Agent-owned without extra accept**
- `wiki/**` during wiki ingest, lint, query, and synthesis work, within this schema.
- `raw/**` only as the destination of an explicit triage/import operation; do not mutate raw files after they land.
- `inbox/**` only for triage routing into `raw/`; do not edit inbox file contents in place.
- `handoff.md` and `todo.md` as session state.

If a task needs both protected-file edits and agent-owned wiki/raw work, split the work: do the wiki/raw work normally, but pause for accept before touching protected files.
