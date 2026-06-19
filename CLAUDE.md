# CLAUDE.md

This file is auto-loaded by Claude Code. It has two parts:

- **Part A: Behavioral baseline.** General guidelines for any work in this repo.
- **Part B: Vault schema.** How this specific knowledge vault is structured and operated.

For vault operations, Part B overrides Part A where they conflict (see [§B.5 Schema overrides](#b5-schema-overrides)).

```table-of-contents
```
---

# Part A: Behavioral baseline

Behavioral guidelines to reduce common LLM mistakes. Bias toward caution over speed. For trivial tasks, use judgment.

## A.1 Think before coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them. Don't pick silently.
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
- If you notice unrelated dead code, mention it. Don't delete it.
- Remove imports/variables/functions that *your* changes made unused. Don't remove pre-existing dead code.

The test: every changed line should trace directly to the user's request.

## A.4 Goal-driven execution

**Define success criteria. Loop until verified.**

Strong success criteria let you work independently. Weak criteria ("make it work") require constant clarification.

## A.5 Calibrate explanation to stakes

Triage first, then explain:

- **Chore.** Routine, reversible, one command. Just do it. A one-line "done" beats a recap.
- **Choice.** Real trade-off but low risk. 2-line either/or with a recommendation.
- **Decision.** Load-bearing, hard to reverse. Full analysis.

### Default to doing, not asking

The vault exists to be used. Asking permission on chores is itself a cost. Default to acting on reversible work; ask only when:

- The action is destructive or hard to undo (deletion, force-push, mass rename).
- The action edits a protected design doc (`CLAUDE.md`, `.claude/skills/**`, schema docs in `meta/`) without prior accept in this thread.
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
- No extended apologies or self-flagellation on routine mistakes. Name the fix and move on.
- No bullet-recap of a change that's already self-explanatory from context.
- No restating in different words what you just said.

"Done. [[link]]" beats a five-bullet summary when the work is small.

## A.6 Prose that doesn't read as AI

**Write like a person, not a model. Applies to every piece of natural prose you write (chat, wiki, meta, handovers), in any language.** Telegraphic agent-first artifacts (handoff/todo/log, dated reports) keep their functional formatting; this governs prose meant to be read as prose. Language-specific idiom rules (the wiki language's preposition and loanword patterns, and the like) live in the language pack and point back here.

- **No reflexive contrastive negation.** Patterns like "not X, but Y", "not just X but also Y", "the point isn't X". Use contrast only when it sorts real alternatives or corrects a likely misreading. Otherwise state the claim straight.
- **No signal phrases.** "It's worth noting", "importantly", "the key thing is", "crucially", "all in all". Cut them and make the point.
- **Break the em-dash habit.** Rewrite the sentence, or reach for period, comma, colon, or parenthesis if that fits better. The dash reads as an AI tell even when it is grammatically fine. The deeper habit to drop is appending an afterthought rather than starting a new sentence.
- **Limit modal hedging.** When advice is clear, write it as imperative or present tense ("Give each row one entry"), not a run of "should" that flattens every recommendation to the same weak register.
- **Full sentences, not fragments.** Bullets and sentences carry a verb. Concision comes from cutting filler (dead words, repetition, padding), not from amputating a sentence to a bare statement of fact. A short sentence is right when the content is short, wrong when it's clipped to seem efficient.
- **Prefer the verb to the nominalization.** "We assess whether it fits", not "an assessment of suitability is performed". Keep a nominalization only when it's an established term that adds precision.

---

# Part B: Vault schema

This is an LLM-maintained knowledge vault implementing Karpathy's LLM Wiki pattern (full source: [[Karpathy - LLM Wiki]]). Deferred items: [[backlog]].

> [!info] Parametric config (Claude Code `@import`)
> This schema reads parametrically. The per-vault parameters and the active language/form pack are imported below; Part B sections point into them rather than inlining the values. The pattern (rules) stays here in CLAUDE.md; the parameters (values) live in the imported files. The imports are parameter tables CLAUDE.md routes into, not a competing rulebook.

@meta/vault-config.md
@meta/vaultos-lang-en.md

## B.0 Where to start

**Before your first reply in any session, including a greeting, check whether `first-time.md` exists at the vault root.** If it does, a human is setting up for the first time: **do not** open with a generic greeting or a skill list. Read `first-time.md` immediately and start walking them through its checklist (it points into `README.md`), then offer to delete it. (It is onboarding only. Nothing depends on it, so its absence is the normal steady state; then greet and proceed normally.)

Pointers an incoming session should hit before non-trivial work:

- **Before any non-trivial edit, read `handoff.md` and `todo.md` at the vault root.** If they say "No ongoing task" and your work isn't trivial, update them before stopping. For substantial follow-up, also read the linked handover under `meta/handovers/`. The full incoming/outgoing protocol lives in [[meta/handoff-protocol]].
- **Once you have run `lint`, the most recent report under `wiki/syntheses/rapporter/lint-rapporter/` is the active work queue** — unchecked items are the follow-ups, and the report's final section suggests an order. A fresh vault has none yet.
- **Read [[Karpathy - LLM Wiki]] before discussing system structure, intent, or schema changes.** It is Karpathy's original pattern document: the *why* behind the three-layer architecture and the schema-as-configuration premise. Don't propose schema edits without reading it.

## B.1 Purpose and premises

- **Collaboration mode (solo / shared) is a setup parameter; see `meta/vault-config.md`.** **Shared:** multiple colleagues drop sources and one wiki emerges (dedup + multi-author handling, §B.6, apply). **Solo:** a single person's vault. In both modes the **wiki layer is single-author** — humans (one or several) only write to `raw/`, and you are the sole author of everything in `wiki/`.
- **Canonical instruction file (CLAUDE.md / AGENTS.md) is a setup parameter; see `meta/vault-config.md` and §B.12.** One file holds the full schema; the other is a thin pointer to it. The choice follows the primary AI tool (Claude Code → `CLAUDE.md`; Codex or other → `AGENTS.md`).
- **Hands-off ingest.** Whoever triggers ingest does so without per-source steering. This schema must be precise enough that you don't need to guess.
- **Dynamic.** Old sources get re-ingested as models improve. Wiki pages record which model last touched them.
- **Wiki language is a setup parameter; English is the shipped default.** Wiki content (`wiki/` page bodies, summaries, index entries, log entries, source pages) is written in the chosen wiki language; sources may arrive in any language and are normalized to it. Operational/meta documentation (`CLAUDE.md`, `AGENTS.md`, `meta/**`, this first-run plan, skills) stays in English unless explicitly requested otherwise. (See `meta/vault-config.md`. The active form details live in the swappable pack `meta/vaultos-lang-en.md`; a Norwegian pack ships alongside as `meta/vaultos-lang-no.md` for vaults that choose Norwegian.)

## B.2 Layout

```
<vault-root>/
├── CLAUDE.md        ← this file
├── AGENTS.md        ← default pointer to CLAUDE.md; canonical/pointer roles swap at setup (§B.12)
├── handoff.md       ← State layer: current ongoing work and next step, updated every session
├── todo.md          ← State layer: short mutable task list for current/remote follow-up
├── .claude/         ← Claude Code config (see B.4, B.13)
│   ├── skills/      ← operation + specialized skills (wiki-*, media-log-ingest, dikt-analyse, …)
│   ├── hooks/       ← Write/Edit hooks: frontmatter bump, skill mirror, protected-file guard (B.13)
│   ├── agents/      ← subagents, e.g. norsk-prosa prose reviewer (B.13)
│   └── settings.json ← hook wiring + permissions
├── .agents/skills/  ← auto-synced mirror of .claude/skills for non-Claude agents (B.13)
├── meta/            ← human-curated documentation; do not edit unless asked
│   ├── LLM Wiki - Karpathy.md        ← Karpathy's original idea doc (the pattern source)
│   ├── plan.md
│   ├── backlog.md
│   ├── vault-config.md               ← @imported instance parameters (see top of this file)
│   ├── vaultos-lang-en.md            ← @imported language/form pack (English, default)
│   ├── vaultos-lang-no.md            ← optional Norwegian language/form pack (swap in at setup)
│   ├── vaultos-manifest.md           ← portable VaultOS manifest (template staging)
│   ├── synthesis-generation-recipe.md
│   ├── handoff-protocol.md           ← rules for handoff.md, todo.md, and handovers/
│   ├── feedback/                     ← design proposals (proposal-NNN-*)
│   ├── style/                        ← source notes behind the writing standard
│   ├── handovers/                    ← dated detailed handovers after substantial work
│   └── …                             ← working dirs (history, ideas, model-test, export)
├── inbox/           ← STAGING. Humans drop files here; triage moves them to raw/.
├── raw/             ← Source documents. READ-ONLY after triage. Frozen archive.
│   ├── articles/
│   │   └── <corpus>/  ← exception for multi-file archives from a single publication; preserves original filenames
│   ├── papers/
│   ├── transcripts/
│   ├── media_logs/  ← Structured imports such as Goodreads/Letterboxd item logs
│   ├── Snipd/       ← Plugin-synced podcast highlights; see plugin-sync roots note below
│   └── assets/      ← images, PDFs referenced from raw files
├── wiki/            ← LLM-OWNED. Create and maintain everything here.
│   ├── home.md      ← human-facing category-chooser launcher (Homepage-plugin entry point); callout-card UX, see B.3 exception
│   ├── index.md     ← catalog of all wiki pages (LLM/query entry point)
│   ├── log.md       ← append-only operations log
│   ├── overview.md  ← top-level narrative; the filed answer to "what is this vault currently about?", refreshed via /wiki-query when material has shifted (lint flags staleness, never regenerates)
│   ├── tags.md      ← canonical tag registry (see B.3)
│   ├── entities/    ← people, orgs, products, named things
│   ├── concepts/    ← ideas, techniques, themes
│   ├── sources/     ← one summary page per ingested source
│   └── syntheses/   ← analyses, comparisons, lint reports
├── tools/           ← versioned helper scripts (e.g. media-log digest); not wiki content
└── personal/        ← Personal operational layer. OUTSIDE wiki schema and wiki ops. See B.10.
    └── <domain>/    ← personal domains (health, finance, home & garden, …), each with personal data and notes
```

**Read/write boundaries:**

- `inbox/` is **staging**. Humans drop files here in any format, any name. The agent has write access, but only via the triage phase of `/wiki-ingest`. Don't modify inbox files in place; just route them.
- `raw/` is read-only **after triage**. The agent writes to `raw/` only as the destination of a triage move. Once a file lands here with its canonical name, it is frozen for the life of the vault.
- `meta/` is human-curated. Don't edit unless explicitly asked.
- `handoff.md` and `todo.md` are the mutable session state layer. Update them at handoff points, before long pauses/remote continuation, and when a task becomes complete or blocked.
- `wiki/` is your domain. Create, edit, and reorganize freely within the conventions below.
- `personal/` is owned by the human. The agent edits there only when explicitly directed: domain work, log entries, plan updates. Wiki operations (ingest/lint/query/synthesis) never touch it. See B.10.
- Protected workflow/config files are changed only after explicit human accept. See B.12. Exception: `/wiki-lint` Phase 6 updates the §B.0 latest-lint pointer as a single-line edit; see the wiki-lint skill.

**Audience: human-first vs. agent-first.**

Some pages are written for human reading: `wiki/{entities,concepts,sources}/**`, substantial syntheses, `wiki/{home,overview,index}.md`. The §B.3 mother-tongue idiom patterns, infobox discipline, and first-line stranger test all apply here.

Other pages are agent-first working artifacts: `handoff.md`, `todo.md`, `meta/handovers/**`, `wiki/log.md`, and dated outputs such as `wiki/syntheses/rapporter/Triage - YYYY-MM-DD.md`, `wiki/syntheses/rapporter/lint-rapporter/Lint - YYYY-MM-DD.md`, and `wiki/syntheses/rapporter/Reingest - <topic> - YYYY-MM-DD.md`. Telegraphic format, checkbox tables, and file-path enumeration are functionally correct here. The mother-tongue prose lint, the infobox rule, and the stranger test do not apply. Lint and ingest read this axis rather than enumerating exceptions.

**Plugin-sync roots (e.g. `raw/Snipd/`):**

Some `raw/` subfolders are synced live by Obsidian plugins and differ from triage-canonical paths: folder casing and internal layout follow the plugin (not the lowercase-slug convention in B.3), triage is skipped (`/wiki-ingest` Phase 1 already short-circuits anything under `raw/`), and plugin-owned support files are overhead, not sources (lint must not flag them; ingest must not process them). Some plugins also expose cover/logo URLs in episode frontmatter that are valid inline image sources for wiki pages (reference `![Cover](url)`; do not mirror into `raw/assets/`).

A plugin-sync root that accretes content across sessions (a plugin keeps adding highlights while the user works through a source) also needs an **ingest-readiness gate**, so a still-growing item is not ingested half-finished. Ingest gates on a settling window over the plugin's last-updated field, plus a worthiness pass that drops low-engagement or off-domain items rather than auto-ingesting the whole root (procedure: `/wiki-ingest` Phase 0). An in-file marker would not survive the next plugin export (the plugin regenerates the file), so the durable readiness signal is a field the plugin itself writes.

The specific plugin-sync roots, their overhead-file names, their cover-URL conventions, and the ingest-gating field and thresholds for this vault are parameters; see `meta/vault-config.md`.

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
entity_type: person               # for kind: entity only; value from the enum in meta/vault-config.md
trigger_skill: wiki-synthesis     # for kind: synthesis only; which skill filed the page
trigger_mode: user-requested      # for kind: synthesis only; how the filing was triggered
tags: []                          # optional; draw from wiki/tags.md, see B.3
---
```

**List fields are always lists.** `sources:` and `source_path:` are always block-style lists, even when there's a single entry. Keeps the shape consistent for anything reading frontmatter and makes dedup (multiple raw files → one wiki source page) a no-op rather than a type change.

- `created` is the date you created the page.
- `updated` is bumped on every edit. A PostToolUse hook (`.claude/hooks/bump-frontmatter.py`, see B.13) does this automatically on wiki content pages and flags missing required fields; lint stays the deeper backstop.
- `ingest_model` is your model id at the time of the most recent edit. Use the exact platform-versioned ID (e.g. `claude-opus-4-7`, `claude-sonnet-4-6`, `gpt-5-codex`), not a generic family alias (e.g. `gpt-5`, `claude`). Used by lint to find re-ingest candidates.
- For `kind: source`, omit `sources:` (the source is itself) and set `source_path:`. For other kinds, set `sources:` and omit `source_path:`.
- For `kind: entity`, set `entity_type:` from the canonical enum in `meta/vault-config.md` (`person` | `org` | `product` | `work` | `place` | `event` | `dataset` | `publication`). The infobox `Type` line mirrors it. Lint sub-check 9h flags missing or out-of-enum values.
- For `kind: synthesis`, set `trigger_skill:` (`wiki-ingest` | `wiki-query` | `wiki-synthesis` | `wiki-lint`: which skill filed the page) and `trigger_mode:` (`user-requested` | `user-selected` | `agent-followon`: how the filing was triggered). Other kinds omit both. See §B.4.1 for semantics. Lint sub-check 9f flags missing or out-of-vocabulary values.

### Filenames and slugs

Two naming conventions, by kind:

- **All wiki pages use natural form.** Capitalized appropriately for the page language (sentence case for concepts, proper case for entities), spaces preserved, ASCII. Why: every folder the user navigates should read like natural language, not like a URL bar.
  - Entities: `Vivian Balakrishnan.md`, `Nano Claw.md`, `AIE Singapore 2026.md`.
  - Concepts: `Second brain workflows.md`, `Neuro-symbolic AI.md`, `AI democratization.md`.
  - Sources: `<Speaker/Author> - <Topic>.md` for talks (e.g., `Balakrishnan - Second brain workflows.md`); `<Title>.md` for papers/articles (add `(Author Year)` for disambiguation when titles collide).
  - Syntheses: descriptive title in sentence case (e.g., `Attention vs Mamba comparison.md`). Date-stamped exception: `Lint - YYYY-MM-DD.md`, `Reingest - <topic> - YYYY-MM-DD.md`.
- **Sources need a distinguishing element:** speaker/author prefix for talks, title for papers. A source about "Second brain workflows" would otherwise collide with the concept page of the same name. Sources are documents about a topic, not the topic itself.
- **Per-corpus / per-author source subfolders.** When one author or corpus accumulates many source pages, group them under `wiki/sources/<Author or Corpus>/` (e.g. `wiki/sources/Scott Alexander/` for the Slate Star Codex + Astral Codex Ten essays, `wiki/sources/GOAT/` for the book-ingest pilot). Filenames are unchanged inside the folder (keep the existing prefix, e.g. `SSC - <Title>.md`); `[[wikilinks]]` resolve by basename, so grouping never breaks links. Use a subfolder only once a single source/author passes ~10 pages; keep smaller sets flat. These subfolders are schema, not a lint flag.
- **Slugs survive in two places only**: `raw/<type>/<YYYY-MM-DD>_<slug>.md` (machine-organized archive, agent rarely navigates) and tags (labels, not folders).
- `wiki/syntheses/rapporter/lint-rapporter/Lint - YYYY-MM-DD.md` and `wiki/syntheses/rapporter/Reingest - <topic> - YYYY-MM-DD.md`: date-stamped exception for periodic outputs (natural form, consistent with other syntheses). Lint reports nest under `rapporter/lint-rapporter/`; Triage/Reingest reports have no filed examples yet, so their subfolder convention is still open.
- `raw/<type>/<YYYY-MM-DD>_<slug>.md`: date-prefixed canonical form. ISO 8601 hyphens in the date, underscore between date and slug, underscores within the slug. This is the **output** of triage, not the input. Humans drop files into `inbox/` with any name; the agent generates this canonical path during the triage phase of `/wiki-ingest`. Raw filenames always use slug form regardless of source kind.
- `raw/media_logs/<export-name>/`: exception for structured media-log item cards exported from services such as Goodreads or Letterboxd. Preserve the import filenames inside the export folder unless there is a specific dedup/encoding problem; the folder, not each item file, is the canonical raw source unit. Prefer aggregate source/synthesis pages over one wiki page per item.
- **Reserved Vault DNA names.** Wiki entity, source and concept filenames must not match (case-insensitively) the agent-instruction filenames that AI tooling auto-loads as project context, the vault's "DNA". When a natural page name would collide (e.g., the AI product family Claude), use parenthetical disambiguation (`Claude (Anthropic).md`) and add the natural form to the page's `aliases:` frontmatter so `[[Claude]]`-wikilinks still resolve. The current reserved-name list is a parameter; see `meta/vault-config.md` (maintain it there; extend when new auto-load conventions emerge).

**Derivation rules:**
- For entities: drop honorifics (`Dr`, `Prof`, `Mr`), preserve given-name + surname order and capitalization, keep accents in ASCII-safe form where reasonable. Org/product/event names stay as commonly written.
- For concepts: sentence case in the page language (first word capitalized + proper nouns/acronyms). `Second brain workflows`, `AI democratization`, `Neuro-symbolic AI`. Avoid title case (`Second Brain Workflows`); concepts aren't titles.
- For source pages (transcripts): `<Speaker surname> - <Topic in sentence case>.md`. Drop honorifics. Topic is short, not the full talk title. When the literal title is over-long or multi-clause, summarize the topic from the talk's content (e.g., `Alyx planning states, large JSON abstractions, and reliable agent checkpoints` → `Production lessons from building Alyx`). When `<Surname> - <Topic>` would collide with an existing source, use `<Full given name> <Surname> - <Topic>` instead (e.g., `Heng Hong Lee - …`, `Jun Yu Tan - …`).
- For source pages (papers/articles): `<Title in sentence case>.md`. Append `(Author Year)` only if needed to disambiguate.
- For syntheses: descriptive name in sentence case; dated outputs use `Lint - YYYY-MM-DD.md` and `Reingest - <topic> - YYYY-MM-DD.md`.
- For raw filenames and tags (the only remaining slug contexts): lowercase, underscore-separated, ASCII. Strip articles ("the", "a") if the slug gets long. No trailing punctuation. (Hyphens are reserved for ISO 8601 dates and grammatical compounds in titles like `AI-native`, `sim-to-real`.)
- **Frontmatter is authoritative.** If the raw file has a `title:` field, derive the name (or slug) from it. Fall back to the filename only if no title is present.

Same-source dedup still works under this rule: ingesting the Balakrishnan transcript twice produces the same source filename (`Balakrishnan - Second brain workflows.md`) and the same entity name (`Vivian Balakrishnan.md`). Collision check happens at the filename layer in both cases.

### Tags

Tags exist to connect pages that would otherwise stay far apart: across time, across source, across kind. The canonical registry lives at `wiki/tags.md`. **Read it before tagging.**

**Tag budget per page:**
- **1 hovedtag** (top-level domain), required when a fit is clear. Drawn from the 5–10 hovedtags in `wiki/tags.md`.
- **0–3 sub-tags:** specific themes that bridge this page to ≥2 others. Optional. Not every page needs sub-tags.
- **Maks 4 tags total.** Pages without a clear thematic bridge stay at 1 tag.

**Current hovedtags** are a per-vault parameter; see `meta/vault-config.md` for the list, with the canonical live registry at `wiki/tags.md` (read it before tagging). Hovedtags are tags and homepage entry points, **not folders**. Do not create a matching `wiki/01 Kultur/`-style taxonomy. Page placement stays governed by page kind (`wiki/sources/`, `wiki/concepts/`, `wiki/entities/`, `wiki/syntheses/`); domain grouping happens through frontmatter tags and the `wiki/home.md` cards.

**Apply an existing tag freely** when it fits the page.

**Propose a new sub-tag when:**
- The tag would apply to **at least 2 existing pages + the page in front of you** (3 total minimum).
- It does **bridge-work**: surfaces a connection between pages distant in source, time, or kind. Descriptive tags that duplicate what wikilinks already convey add nothing.
- Add it to `wiki/tags.md` with a one-line definition under its nearest hovedtag, then apply retroactively to the matching pages.

**Don't create a tag when:**
- One-page topic. The title and wikilinks already locate it.
- The page already has 4 tags.
- The tag would duplicate an existing tag's role.

**Tag form:** lowercase, underscore-separated, ASCII. Short. Hyphens reserved for ISO dates and grammatical compounds elsewhere, not in tag slugs. Flat namespace (no `ai/agents`-style nesting in the tag itself; `tags.md` may visually group sub-tags under their hovedtag).

**Lint actively curates tags** (consolidation checks): dead tags (1 use) flagged for removal, recurring untagged themes flagged for new-tag proposal, existing tags that fit untagged pages flagged for retroactive application. Application of curation findings happens after the human reviews; lint itself never silently changes tags.

### Body conventions

- **Writing & structure standard (four buckets).** All wiki prose is written to one standard; `/wiki-ingest` drafts to it and `/wiki-editor` scores against it. The four buckets are the portable pattern. The full rules and examples live in the always-imported language pack (`meta/vaultos-lang-en.md`, "Writing & structure standard"), with a one-line-per-bucket checklist at each writing step:
  - **Structure & organization:** define in the first sentence (lead = the page in miniature); most-important-first, rising difficulty; one page, one topic (hub when too big); right length, not maximal; descriptive subheadings; link inline + `## Cross-references` at the bottom.
  - **Clarity for the reader:** the **stranger test** (first line + `[!infobox]` readable by a newcomer who hasn't read the source or known the speaker; lead with substance, attribution after); define each term once (never explain jargon with jargon); jargon must do work or it's cut; don't smuggle the thing you're explaining into the analogy.
  - **Prose & sentence level:** active voice, full sentences; the language-independent anti-AI-prose patterns in §A.6; plus the wiki language's idiom anti-patterns (the "Natural English" section of the pack; definitions + tests there).
  - **Content, source & durability:** attribute contested claims, no implicit value judgments; write to last (no datestamping, concrete years); media-log epistemic layers.
- **Cross-references use `[[wikilinks]]`**, never raw paths. Obsidian's graph view depends on it.
- **Citations** point to `wiki/sources/<slug>` pages, never directly into `raw/`. Source pages are the single point of truth for what a source says.
- **Callouts** add value when they convey *semantic type*, not just visual variety. Use the following types where the content has that shape, and stop. 2–5 callouts per source page is a healthy ceiling; more turns the page into noise.
  - `> [!quote]`: verbatim quotes where wording is part of the value (not paraphrases).
  - `> [!important]`: load-bearing claims, key conclusions, hard constraints.
  - `> [!warning] Conflict`: contradictions between sources or pages. Example:
    ```
    > [!warning] Conflict
    > [[Source A]] claims X, but [[Source B]] claims Y.
    ```
  - `> [!warning]`: risks, open commitments, things to watch.
  - `> [!tip]`: practical advice, rules of thumb, actionable insights.
  - `> [!example]`: concrete stacks or scenarios illustrating an abstract point.
  - `> [!info]`: neutral context or background that helps but isn't core.
  - `> [!question]`: open questions worth tracking (alternative to bullets in `## Open questions`).
  - `> [!infobox]`: Wikipedia-style right-rail sidebar with type/role/key claims/key terms. Default-on for source/entity/concept pages; see "Infobox sidebar" sub-section below.
  - `> [!banner]`: full-width header/footer band on `home.md` (sheds the standard callout chrome via CSS). Reserved for that one page; do not use elsewhere.
  - Navigational pages (`index.md`, `log.md`, `overview.md`, `tags.md`) get no callouts; they're not content. **Exception: `home.md`** is the human-facing category-chooser launcher (Homepage-plugin entry point) and intentionally uses `[!banner]` for its header/footer plus one category callout (`[!tip]`, `[!info]`, `[!example]`, `[!success]`, `[!important]`, `[!question]`, `[!abstract]`) per top-level door; same semantic-type-not-just-decoration discipline still applies (each card's callout type carries meaning).
- **Section headings** on source pages: the canonical names live in the always-imported language pack (`meta/vaultos-lang-en.md`). Skip sections that don't apply.

### Infobox sidebar (default-on)

Source, entity, and concept pages carry an `> [!infobox]` callout at the top, rendered as a right-rail floated sidebar via `.obsidian/snippets/infobox.css`. Goal: a newcomer reading the page should be able to orient themselves from the infobox alone before the body text: type, who/when, top claims, and any specialized vocabulary defined inline. Infobox field labels are in the wiki language on wiki pages; the field *roles* below are the portable pattern, and the labels are catalogued in the language pack (`meta/vaultos-lang-en.md`).

Content varies by `kind`:

**Source pages:**
- **Type:** talk / paper / article (drawn from `source_path` directory)
- **Foredragsholder/forfatter:** one line; wikilink the name (`[[Surname]]` or `[[Full Name]]`) so the source becomes a visible graph edge to the author's entity page. For talks, format as `[[Surname]] (org), role`.
- **Dato / arena:** one line
- **Key terms:** 3-5 short one-line definitions of vocabulary the body uses that a newcomer wouldn't know

The infobox does **not** carry key claims; those live in the body's `## Key claims` section. The infobox is at-a-glance orientation (who/when/jargon), not a tl;dr.

**Entity pages:**
- **Type:** the page's `entity_type` (person / org / product / work / place / event / dataset / publication)
- **Rolle:** one line, what they're known for
- **Tilknytninger:** orgs / events / collaborators ([[wikilinks]])
- **Kilder:** top 2-3 wiki source pages for this entity
- **Key terms:** 3-5 short defs; optional if the entity isn't conceptually heavy

**Concept pages:**
- **Kort definisjon** (tighter than the page's first line, can be formula-like)
- **Argumentert av:** "N kilder" with top 2-3 wikilinked
- **Relatert:** sister concepts ([[wikilinks]])
- **Key terms:** 3-5 short defs of vocabulary the body uses

**When to skip:**
- Page is trivially short (stub entity with one source, no specialized terms)
- All vocabulary in the body is common-English and the page is unambiguous from the title alone

**Lint enforces:** any source/entity/concept page with specialized vocabulary or jargon that lacks an `[!infobox]` gets flagged for retrofit.

### Transcripts (extension to source pages)

When `source_path` points into `raw/transcripts/`, extend the standard source page with these sections:

- **`## Speakers`:** one bullet per speaker, with name and role (host, guest, panelist, audience). Use the names that appear in cross-references throughout the wiki.
- **`## Talk metadata`:** venue, date of recording (if different from ingest date), event or series name, link to original recording if present in the raw file.
- **`## Timestamped highlights`:** citable moments. Format: `- [HH:MM:SS] <speaker>: <claim or quote>`. Aim for 5–15 entries per hour of transcript, not exhaustive.
- **`## Q&A`** (optional): if the transcript has a Q&A segment, capture it here with per-turn attribution. Audience questions get their own bullets even when the asker is unnamed.

The base sections (`## Key claims`, `## Context`, `## Open questions`, `## Cross-references`) still apply. Transcript-specific sections go between `## Context` and `## Open questions`.

### Media logs and intent lists

Imported media logs can contain both consumed works (`read`, `watched`) and unconsumed candidates (`to-read`, watchlist, `currently-reading`). Store structured item-card exports under `raw/media_logs/` during triage, and treat their statuses as different epistemic layers:

- **`read` / `watched` items are experience data.** They can support source pages, entity pages, concept pages, rating analysis, and recommendation syntheses.
- **`to-read` / watchlist items are possibility data.** They should not support claims about taste, knowledge, influence, or intellectual formation unless clearly framed as intent, curiosity, or candidate material.
- **`currently-reading` is provisional.** Use it only as active interest, not as completed evaluation.
- **Prefer aggregate source/synthesis pages for media logs** over one wiki source page per book, film, album, or episode.
- **When media logs reveal gaps, record them as knowledge holes or next investigations,** not as established conclusions.

The `/media-log-ingest` skill (B.4) operationalizes these conventions: parse and cover-fetch as scripts, attribution and aggregate-page writing by the model.

### User notes and source provenance

User-supplied material often carries the user's own steering, and every source has an origin type worth keeping visible. Two conventions follow.

- **User-comment fields are steering input.** When a source carries a user note (the web-clipper note/comment field, a margin note, a covering message), read it as the user's half of the Karpathy role-split: pointers, not dictation (same principle as §B.4.1). It carries **emphasis** (which points the user finds important: weight `## Key claims`, the ingress, and ordering accordingly) and the user's **own cross-links** (treat stated connections to other topics as concrete candidates for entity/concept wikilinks, `## Cross-references`, tags, and synthesis seeds, not loose background). **It is additive emphasis, not a filter or a blinder.** Read and curate the whole source on its own merits first, then let the note lift and order what it flags. Never narrow coverage to only the flagged points, and stay alert to substance the user did not mention, including material that complicates or contradicts the user's own take. Tunnel vision on the comment is the failure mode to avoid: it steers focus and order, never whether material is covered. An empty field means no steering. Procedure detail lives in `/wiki-ingest`.
- **Keep the source type visible so fact and assertion stay distinguishable.** Record what a source *is* as a neutral type (talk / paper / article / idea-note / dialogue / clipping) in the infobox `Type` line and frontmatter; attribute in-body per the four-bucket attribution rule ("X argues", "according to Y"). This keeps the *origin type* legible: a reader can tell established/factual material from a source's own assertion or synthesis, and see where each came from. This is origin transparency, not a reliability ranking. Facts can be wrong and assertions can be right; what matters is knowing the origin. Provenance is a label, never a disclaimer of validity.

## B.4 Operations

Four core operation skills, plus topic-triggered specialized skills (below). **CLAUDE.md is the schema authority on conventions; the skills are the procedure authority.** Skills reference back here; they never restate policy. If they ever drift, lint catches it (Check 9 in `/wiki-lint`).

- **`/wiki-ingest`:** Ingest a source into the wiki. Absorbs the whole source lifecycle: triage (when the source is in `inbox/`), fresh ingest, and diff-and-reconcile re-ingest (when a `wiki/sources/` page already exists for the source). See `.claude/skills/wiki-ingest/SKILL.md`.
- **`/wiki-lint`:** Periodic vault health check. Output is a date-stamped triage checklist at `wiki/syntheses/rapporter/lint-rapporter/Lint - YYYY-MM-DD.md`. Never silently fixes anything. See `.claude/skills/wiki-lint/SKILL.md`.
- **`/wiki-query`:** Answer a question against the wiki. Reads the index first, drills via wikilinks, answers with cited claims, and may surface synthesis directions without filing them unless explicitly asked. See `.claude/skills/wiki-query/SKILL.md`.
- **`/wiki-synthesis`:** Generate synthesis ideas or run an explicit vault-backed synthesis workflow. Default mode is idea generation, not a vault scan. See `.claude/skills/wiki-synthesis/SKILL.md`.

Specialized skills (same authority split, invoked by topic rather than as part of the core loop):

- **`/media-log-ingest`:** Bulk media-log exports (Goodreads/Letterboxd/Kindle) into aggregate pages; mechanical parse + cover-fetch scripts, attribution and page-writing by the model. See `.claude/skills/media-log-ingest/SKILL.md` and §B.3 "Media logs and intent lists".
- **`/dikt-analyse-norsk`, `/wiki-parable`:** poem analysis and analytical parables; triggered by topic, not by the ingest/lint/query/synthesis loop.

### B.4.0 Plan-before-run threshold

Any operation expected to touch more than ~15 wiki pages, or to run on more than one source in a single invocation, presents a one-paragraph plan first (scope, expected touches, risks) and waits for go. Single-source ingest stays fully hands-off (per B.5). Anchored on the LLM Wiki principle: **"Ingest one at a time, stay involved."**

**Model-awareness (not friction).** Ingest quality is model-dependent, but the bar is easy to clear (see "Ingest-recommended tier" in `meta/vault-config.md`): both ecosystems' top tiers (Opus/high, GPT-5.5/high) tied at the top, and one notch down (Sonnet, GPT-5.3-Codex) is fully usable. Single-source ingest stays hands-off, with no blocking model question. `wiki-ingest` stays silent on every workhorse-or-better tier (Sonnet, Opus, GPT-5.5, GPT-5.3-Codex) and flags only the case that actually hurts: the weakest tier that collapses prose (Haiku-class), where it emits a one-line note at its opening (no gate; the colleague stays in control). Batch / multi-source ingest folds model + effort confirmation into the plan-before-run pause above, rather than adding a new interruption point.

### B.4.1 Synthesis generation modes

The expanded rationale and portable recipe live in `meta/synthesis-generation-recipe.md`; this section is the operational rule for this vault.

**Default interpretation:** when the user says "create synthesis", "make synthesis", or asks for synthesis ideas without naming vault sources, treat it as **idea synthesis**. Generate candidate theses, frames, or questions. Do not assume the vault has enough content, do not scan the vault by default, and do not create files.

**Explicit vault-backed mode:** only run the vault-backed synthesis workflow when the user asks for it with language such as "from the vault", "using existing sources", "scan the vault", "file a synthesis", or when the user has picked a previously proposed candidate to write. In survey mode, propose 3-5 candidates with source basis + one-line thesis and wait for the human to pick before filing.

**During ingest:** notice synthesis seeds, strengthen role-labeled `## Cross-references` entries, and log possible synthesis directions when a real 3+ source cluster appears. Do not auto-file synthesis pages during ingest.

**Synthesis provenance (frontmatter `trigger_skill:` + `trigger_mode:`).** Every filed synthesis carries both fields so audit doesn't have to depend on grepping `log.md`. `trigger_skill:` is the skill that filed the page (`wiki-synthesis`, `wiki-query` filing a followon, `wiki-lint` recording a lint-driven synthesis, or `wiki-ingest` in the rare case where a kryssref gesture during ingest leads to filing). `trigger_mode:` is the authority behind the filing:

- `user-requested`: the user explicitly invoked the skill with a synthesis ask ("file a synthesis on X").
- `user-selected`: the user picked from a slate of candidates the agent proposed.
- `agent-followon`: the agent inferred filing from context: a kryssref gesture to a not-yet-existing synthesis, a prior ingest log seed, or a query that naturally crossed the 3-source threshold and a user gesture interpretable as accept.

The fields record *the filing event*, not edit history. Subsequent edits leave them alone; only re-filing from scratch resets them.

### B.4.2 Git operations and skill commits

**No automatic git.** The vault never touches a remote on its own. Normal operations (ingest, lint, query, synthesis) do **zero** git: wiki content syncs through Obsidian Sync, and git is reserved for explicit commits you ask for and the curated `update` operation. You are never pinging GitHub involuntarily just by using the vault. Update-awareness is decoupled: run `update` when you want it, or set up a routine that checks on a cadence, never bound to a per-action preflight.

**Commits:** Do not auto-commit or auto-push during normal vault work. When files Obsidian Sync does not handle (`.claude/skills/`, dotfiles like `.gitattributes`/`.gitignore`, anything in `.gitignore` you've deliberately edited) have been changed in this session, propose a commit at session end. Do not commit silently. Everything else flows through Obsidian Sync.

## B.5 Schema overrides

Part A says "minimum work, nothing speculative" and "touch only what you must." For vault operations these still apply *within reason*, but with explicit exceptions:

- **Creating new wiki pages on ingest is the job, not a violation.** Don't ask permission to create entity/concept pages during ingest.
- **Formal syntheses are the exception to that ingest rule.** Idea synthesis is the default; vault-backed synthesis pages are filed only after an explicit user request or after the user selects a candidate.
- **Touching 10–15 files per ingest is normal.** That's the design.
- **Don't refactor unrelated wiki content.** When ingesting source A, only touch pages where source A is genuinely relevant. No drive-by improvements.
- **Lean toward creating a new page** when in doubt about whether an entity/concept deserves one. Cheap to merge later, expensive to discover the omission six months in.

## B.6 Dedup and multi-colleague

- If two `raw/` files describe the same underlying thing, both files stay (raw is immutable). The `wiki/sources/` page is shared: same slug, both paths appear in the `source_path:` list (which is always a list, see B.3), body merges both reads with a note about the duplication.
- In **shared** mode, colleagues share the live vault through Obsidian Sync; in **solo** mode it is simply your own sync. Git history is a secondary audit trail of the snapshots you commit, taken when you ask, not one commit per operation (see B.7).

## B.7 Commits

This is a personal notes vault, not a team codebase. Commits are snapshots and sync events, not reviewable change-units. The default model is "snapshot when the user asks," not "one commit per operation."

### When the user says "commit" or "commit push"

Treat as "snapshot the whole working tree now, finish the job":
- Stage everything dirty (including `personal/` if the user changed it; it's still their vault).
- One commit, one message, push if "push" was in the request.
- Don't ask for permission. Don't split into per-operation commits unless the user explicitly asks for groupings.

The agent's job is to capture current state, not to curate a clean narrative across many commits.

### Cadence (when not explicitly prompted)

- **No auto-commit.** Nothing commits unless the user asks.
- **Single-source ingest doesn't trigger a commit on its own** (per B.5).
- **No automatic git operations.** The vault never touches a remote on its own; update-checking is explicit/curated (see B.4.2).

### Message format

One concise line describing what's in the snapshot. A loose taxonomy helps `git log` scanning but is not required:

`ingest|lint|query|synthesis|schema|config|housekeeping|vault: <one-line summary>`

When the snapshot spans multiple types (typical at end of a long session), pick the dominant one or use `vault:` as a catch-all. Touched-file lists in the commit body are optional. `git show` already exposes the file set, so don't restate it unless it adds judgment a reader couldn't reconstruct.

**No `Co-Authored-By` trailer.** The agent identity is already recorded via `ingest_model:` frontmatter on touched pages.

### When to be more careful

- **Destructive git operations** (force-push, `reset --hard`, branch deletion, history rewrite): ask first regardless of cadence.
- **Working tree contains files the user clearly didn't intend to commit** (`.env`, credentials, accidental notes): flag before committing.
- **Amending an existing commit:** prefer a new commit unless the user explicitly says amend.

## B.8 When in doubt

- Source unclear → file the ambiguity in the source page's `## Open questions`, move on.
- Page would conflict with itself → flag via `> [!warning] Conflict`, don't pick a side.
- Don't know if something deserves its own page → create one, lean permissive.
- Asked something this schema doesn't cover → answer the human and propose a schema update at the end of your reply.

## B.9 Not yet in scope

Tracked in [[backlog]]:
- Scheduled/remote automation: all operations are currently triggered live in a session.
- Public-facing slice of the wiki, multi-vault federation.
- Search engine (qmd or similar): defer until index-file lookup outgrows itself.

## B.10 Personal layer (`personal/`)

`personal/` is a top-level folder for personal operational content: personal domain projects, data, plans, private notes. It is **outside the wiki schema** (no required frontmatter, no slug discipline, no `kind:` field, no infobox), and **outside wiki operations** (`/wiki-ingest`, `/wiki-lint`, `/wiki-query`, `/wiki-synthesis` do not touch it).

**Bridge rule (one-way):**
- `personal/ → wiki/` linking is fine. Personal notes can freely cite wiki concepts/sources for backing (`[[HRV og restitusjon]]`).
- `wiki/ → personal/` linking is not allowed. Wiki claims rest on external sources, never on private-life data or experience. Here "private-life data or experience" means health, finances, lived personal life, the kind of thing that lives in `personal/`. It does **not** mean everything the user authored.

**The boundary is curation-intent, not authorship.** `personal/` is the layer the user keeps outside curation by design (currently). The user's own intellectual notes, clippings, and idea-dialogues are normal curatable wiki source material: ingest and curate them like any other source. Record provenance as a neutral source type (`idénotat`, `dialog`, `clipping`), never as a reliability disclaimer or a quarantine caveat. The wiki exists for the agent to curate content, including material the user made and noted; lean toward bringing more of it in, not walling it off. Keeping the source type visible is also what lets a reader tell established fact from the source's own assertion (see §B.3 "User notes and source provenance").

Subfolders under `personal/<domain>/` may include a `delt/` subfolder for content that's a candidate for sharing. **Default policy: `delt/` content stays in `personal/` permanently.** Promotion to `wiki/syntheses/` is not automatic and is not currently supported. Revisit if a real need emerges.

See the personal-layer README (created at setup if you opt into a personal layer) for scope details and what belongs where.

## B.11 State layer (`handoff.md`, `todo.md`, `meta/handovers/`)

The state layer is three files, intentionally outside the wiki schema (no frontmatter, no infobox, no index entry, no source authority):

- `handoff.md`: short re-entry prompt for the next agent (current state, next safe action, do-not-do warnings, pointers to deeper context).
- `todo.md`: short ordered active work queue.
- `meta/handovers/<YYYY-MM-DD>-<topic>.md`: detailed narrative handover, created only after substantial work. Linked from `handoff.md`.

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
- `AGENTS.md` — by default the read-only pointer to the canonical `CLAUDE.md`. Which of the two is canonical (full schema) vs. pointer is a setup parameter (`meta/vault-config.md` → "Canonical instruction file"); the setup wizard performs any swap. During normal work, treat the **pointer** file as read-only and edit the **canonical** file for schema changes — and even that only on explicit human accept.
- `.claude/skills/**`
- `meta/backlog.md` and other schema/workflow design notes in `meta/`
- `.obsidian/**` settings and snippets, unless the user is explicitly asking for Obsidian UI/config work

A PreToolUse guard (`.claude/hooks/guard-protected.py`, see B.13) backs this list and the frozen `raw/**` zone with a soft `ask` confirmation on Write/Edit, even under `acceptEdits`. It confirms rather than blocks, and is a convenience; this section remains the authority.

For protected files, first state the intended change and wait for a clear accept such as "go", "yes", "do it", or an explicit instruction naming the file/change. A broad wiki/import instruction is not permission to edit protected workflow/config files.

When proposing edits to a protected file, show changes as a unified diff (only changed lines plus minimal context), not the full new section. Re-reading unchanged content to find the change wastes the user's attention.

**Agent-owned without extra accept**
- `wiki/**` during wiki ingest, lint, query, and synthesis work, within this schema.
- `raw/**` only as the destination of an explicit triage/import operation; do not mutate raw files after they land.
- `inbox/**` only for triage routing into `raw/`; do not edit inbox file contents in place.
- `handoff.md` and `todo.md` as session state.

If a task needs both protected-file edits and agent-owned wiki/raw work, split the work: do the wiki/raw work normally, but pause for accept before touching protected files.

## B.13 Automation layer (hooks and subagents)

Mechanical helpers that enforce or automate Part B rules. They are conveniences and backstops; CLAUDE.md remains the authority. All load at **session start** (edit them and restart to pick up changes). They are wired in `.claude/settings.json`; the scripts are Python, which is on PATH in the hook shell (node is not).

**Hooks** (`.claude/hooks/`, matcher `Write|Edit`):
- **`bump-frontmatter.py`** (PostToolUse): on `wiki/{entities,concepts,sources,syntheses}/**`, bumps `updated:` to today (idempotent per day, so repeated edits don't churn) and flags missing required frontmatter fields per `kind` (B.3). Reports to the agent; never blocks.
- **`mirror-skills.py`** (PostToolUse): copies any edited `.claude/skills/**` file to the parallel `.agents/skills/**`, keeping the non-Claude-agent mirror in sync. Removes the manual copy step and the config↔skill drift that lint Check 9a watches for.
- **`guard-protected.py`** (PreToolUse): on Write/Edit to frozen `raw/**` (B.2) or a protected file (B.12), returns a soft `ask` confirmation with a reason, even under `acceptEdits`. It confirms, never hard-denies. Triage routes with `mv`, so it fires only on the abnormal in-editor case.

**Subagents** (`.claude/agents/`):
- **`prose-reviewer`** (read-only; `Read, Grep, Glob`): reviews human-facing prose against the §A.6 anti-AI patterns and the wiki language's idiom anti-patterns (bucket 3 of the writing standard; "Natural English" in the default pack). Reports violations with rewrites; does not edit. Invoke via `@agent-prose-reviewer` or a review request. This is the **wiki-language** prose reviewer (English by default); setup regenerates it for any other wiki language — a Norwegian `norsk-prosa` variant ships alongside for vaults that choose Norwegian (the §A.6 layer is language-independent and carries over). See `first-time.md` Phase 2. It overlaps with the planned `/wiki-editor`: when that is built it should incorporate or supersede the prose reviewer for the prose layer, not duplicate it.

Helper scripts that are neither hooks nor agents (e.g. `pdf2md.py`, `optimize-images.py`) live in `tools/`: version-controlled, but outside wiki operations. **`tools/lint-scan.py`** is the read-only mechanical pre-pass for `/wiki-lint` (stdout-JSON, dependency-free, exit-code ABI; see the skill's Phase 0a). It reads schema-derived enums from `meta/vault-config.md` + `wiki/tags.md` and keeps a few constants inline; lint Check 9j watches that inline set for drift against §B.3, symmetric with 9i.

**`tools/pdf2md.py`** converts a PDF to Markdown while preserving embedded images (PyMuPDF; run `--report` first). Standing convention for book/document PDFs: convert with it, confirm the report shows text + all images captured (it refuses to greenlight scanned/OCR-needed PDFs), then delete the source PDF. Books live in `inbox/books/`, one `.md` per book (one file per chapter/story for collections, split by parsing the table of contents). Bulky source PDFs stay local-cold per `.gitignore`; the resulting markdown is tracked. Full usage in `tools/README.md`.
