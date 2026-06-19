---
name: wiki-lint
description: Periodic health check of this vault. Triggers on "run lint", "lint the vault", "lint pass", or any general request to audit the vault for orphans, contradictions, stale claims, missing cross-references, synthesis readiness, hub-concept gaps, tag gaps, re-ingest candidates, source gaps, or schema-vs-skills drift. Output is a date-stamped triage checklist at `wiki/syntheses/rapporter/lint-rapporter/Lint - YYYY-MM-DD.md`. Lint never silently fixes anything; it proposes work for the human or for a follow-up ingest/query session. Do NOT invoke for single-source ingest or for question-answering.
---

# /wiki-lint

Periodic vault hygiene pass. Produces a triage checklist as a synthesis page; never auto-applies fixes.

This skill is procedure. **All conventions live in [CLAUDE.md](../../../CLAUDE.md) §B.3.** When a check needs to know what counts as "correct," follow B.3; don't reinvent.

## When this skill runs

- User says "run lint", "lint the vault", "lint pass", or asks for a vault audit.
- On schedule (if cron is wired up; currently not).
- Sometimes triggered tacitly: user asks "what should I work on next?" in a way that calls for a survey, not a query.

If you're not sure whether the user wants lint vs query vs ingest, ask. Lint is the heaviest of the three.

## Phase 0: Plan check

A full lint reads index, log, tags, every source page, and samples many entity/concept pages. That's expected.

**Full write set** (declared up front so the operator knows what gets touched):

1. **New file:** `wiki/syntheses/rapporter/lint-rapporter/Lint - YYYY-MM-DD.md`, the report itself (Phase 3).
2. **Append:** `wiki/log.md`, one log entry (Phase 4).
3. **Single-line edit:** `wiki/index.md`: add the new report under `## Syntheses` (Phase 5).
4. **Single-line edit:** `CLAUDE.md` §B.0: update the "Latest lint" wikilink pointer (Phase 6).

No other writes. No content fixes (per "What lint does NOT do"). If the user wants something narrower ("just check orphans" / "just check stale claims"), honor that scope rather than running the full sweep, and shrink the write set accordingly (skip the CLAUDE.md pointer update if the report is not the new canonical latest-lint).

## Phase 0a: Mechanical pre-pass (`tools/lint-scan.py`)

A read-only scanner front-loads the deterministic tier so the model doesn't read the whole vault to compute structural facts. It adds **no writes** (stdout JSON only), so the Phase 0 write set is unchanged.

1. Run `python tools/lint-scan.py --mechanical --json`. **Branch on the exit code** (this is what makes the script a soft accelerator, not a hard dependency):
   - **0** — parse the JSON. `findings` covers the mechanical/hybrid-mechanical side of Checks 3, 6, 7 (raw coverage), 8, 9b/9e/9f/9g/9h, 10b (infobox candidates), 12, 13, plus the latest-lint pointer (Phase 6 input) and an N4 encoding/partial-write watch. Use these instead of recomputing them by hand.
   - **3** (config unreadable) or **command failure / `python` or the script absent** — fall back to doing those mechanical checks manually, exactly as before. The script is an accelerator; lint must still run without it.
2. Run `python tools/lint-scan.py --semantic-pack` to get a compact bundle of files/findings to read next (broken-link pages, stranger-test first-line candidates, infobox-missing candidates, raw clusters, overview staleness). **This is the token win:** it narrows the semantic tier's reading to a focused set instead of the whole vault.
3. Check `meta.config_warnings` and `meta.schema_derived_inline` in the output — feed them into Check 9j.

The script owns no judgment. The agent still runs every semantic check (1, 2, 4, 5, 9a, 10a/c/e, 11, 14, 15, 16, 17, 18), decides every proposal, and writes the narrative report. Coverage is unchanged from the no-fix contract; the pre-pass only supplies evidence faster. `--fix-safe` emits safe-fix *candidates* as JSON (read-only; the agent/operator applies them) and is used only in an explicit resolve-mode follow-up, never during a pure lint.

## Phase 1: Survey

Phase 0a already precomputed most structural facts. Read the high-signal context the script can't judge: skim `wiki/log.md` tail for recent operations and flagged synthesis seeds, and read [CLAUDE.md](../../../CLAUDE.md) for schema lint (Check 9). Steps below are the manual fallback when Phase 0a's script was unavailable.

1. **Read `wiki/index.md`** for the catalog of pages.
2. **Read `wiki/log.md`** (or its tail if very long) to see recent operations, deferred work, and flagged synthesis candidates.
3. **Read `wiki/tags.md`** before any tag analysis.
4. **Read [CLAUDE.md](../../../CLAUDE.md)** at least once during a lint; schema lint requires it (see Check 9).
5. **List source-page frontmatter** (`ingest_model`, `updated`) to identify re-ingest candidates.

## Phase 2: Run the checks

Each check is independent. Skip any that aren't applicable. For each finding, format as a `- [ ]` checklist line so the human can triage in one pass.

### Check 1: Contradictions

Cross-source disagreements that aren't already flagged with `> [!warning] Conflict`. Cite both sides via wikilinks.

### Check 2: Stale claims

Earlier claims that a later source has refuted or updated. The vault's `## Re-ingest history` sections + the log usually surface these; this check is "what slipped through?"

### Check 3: Orphan pages

Pages with zero inbound wikilinks (excluding `index.md`, `log.md`, `overview.md`, `tags.md`; those are navigational, every page links back through them). An orphan is an integration failure, not a deletion candidate. For each orphan, scan other wiki pages for unlinked mentions of the orphan's topic and **propose specific link additions** in the lint report (e.g., "add `[[orphan-name]]` to `wiki/concepts/foo.md` at line 14"). Never delete pages.

### Check 4: Hub concepts without pages

Topics mentioned in 3+ pages but lacking their own `wiki/concepts/<name>.md`. Propose the page; don't create it.

### Check 5: Missing cross-references

Pages that obviously belong together but don't link to each other. Common cases: two sources arguing the same thing without a wikilink between them, a concept page that doesn't mention a clearly relevant source, an entity page that should link to a related entity.

### Check 6: Re-ingest candidates

- **Date-based:** `ingest_model` older than 3 months from today.
- **Model-parity:** sources still on an older model id while the rest of the vault has moved on (e.g., Sonnet-4-6 sources when Opus-4-7 became the default).

### Check 7: Source gaps

Open questions on source pages that no later source has addressed. Cross-check by grepping the open-question terms across the whole vault; if a later source now mentions the term, propose resolving the question.

Also: raw files in `raw/` with no corresponding `wiki/sources/` page (deferred or forgotten ingests).

### Check 8: Tag gaps

Topics recurring across 3+ pages with no entry in `wiki/tags.md`. Propose the tag and its definition; do not apply silently. See CLAUDE.md B.3 tag policy.

### Check 9: Schema layer integrity

Sub-checks across documents that are supposed to agree (CLAUDE.md, AGENTS.md, every SKILL.md under `.claude/skills/`, `meta/` files, navigational pages).

**9a. Schema ↔ skills drift.** Cross-check CLAUDE.md against all skills under `.claude/skills/` (the four core operations plus the specialized skills `media-log-ingest`, `dikt-analyse-norsk`, `wiki-parable`; skip the third-party `tufte-claude-skill`). The specialized skills also hardcode Norwegian headings/labels, so they are in scope for drift. The schema is the single source of truth on conventions; skills must reference it, not restate it. Catch:
- A skill that hard-codes a value the schema also states (drift risk).
- A Norwegian section heading or infobox label that diverges between CLAUDE.md, a skill's hardcoded copy, and the canonical value in `meta/vaultos-lang-no.md`. The pack is the intended single source; flag any mismatch across the three.
- A skill that references a CLAUDE.md section that no longer exists.
- A schema rule that no skill implements (orphan rule).
- A vocabulary mismatch (e.g., schema says "source page", skill says "ingest page").

**9b. Cross-doc wikilink resolution.** For every `[[wikilink]]` appearing in CLAUDE.md, `meta/plan.md`, `meta/backlog.md`, `wiki/overview.md`, and `wiki/home.md`, verify the target file exists (basename match, or an `aliases:` entry on a file in the vault). Unresolved wikilinks in the schema layer break Obsidian's graph view and confuse fresh agents that follow the links. Propose the fix: rename the target file, add an alias, or rewrite the link.

**9e. `kind:` enum coverage.** Compare actual `kind:` values used across `wiki/` to the enum listed in CLAUDE.md §B.3 frontmatter shape. Any in-use kind not in the enum (or any enum entry with no convention-block in B.3) is a finding.

**9f. Synthesis trigger fields.** For every `kind: synthesis` page, verify both `trigger_skill:` and `trigger_mode:` are present and values fall in the CLAUDE.md §B.4.1 vocabulary (`trigger_skill` ∈ {`wiki-ingest`, `wiki-query`, `wiki-synthesis`, `wiki-lint`}; `trigger_mode` ∈ {`user-requested`, `user-selected`, `agent-followon`}). Missing-on-old-syntheses is a backfill finding (best-effort from log.md); missing on freshly filed pages is a skill bug. Don't auto-fix; propose values per page so the user can confirm before they land.

**9g. Reserved Vault DNA name collisions.** Case-insensitively compare every filename under `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/syntheses/` against the canonical reserved agent-instruction filenames in `meta/vault-config.md` ("Reserved Vault DNA names"). Any case-insensitive match is a finding: the file must be renamed with parenthetical disambiguation (`<Name> (<context>).md`) and the natural form added to `aliases:` so inbound `[[<Name>]]`-wikilinks still resolve. This is correctness-grade, not stylistic: on case-insensitive filesystems (Windows, default macOS) such pages are auto-loaded by AI tooling as project context and pollute agent context with wiki content.

**9h. Entity type coverage.** Every `kind: entity` page must carry `entity_type:` with a value in the `meta/vault-config.md` "Entity types" enum (`person` | `org` | `product` | `work` | `place` | `event` | `dataset` | `publication`). Flag pages missing the field or carrying an out-of-enum value. Don't auto-fix; propose the value per page (read the infobox `Type` line and body to classify) so the user confirms before backfill lands. The infobox `Type` line should mirror the frontmatter value.

**9i. Automation layer drift (§B.13).** Cross-check the hooks and subagents documented in CLAUDE.md §B.13 against what actually exists. Catch: a hook listed in §B.13 but missing from `.claude/hooks/` or not wired in `.claude/settings.json` (or vice versa); a subagent in `.claude/agents/` not described in §B.13; the `.claude/skills/` → `.agents/skills/` mirror out of sync (the `mirror-skills.py` hook should keep them identical, so any divergence is a finding); the `norsk-prosa` subagent is the read-only prose-review tool for the Check 10 patterns, so prefer pointing the user to it over restating prose rules. Don't auto-fix; propose.

**9j. `tools/lint-scan.py` schema drift.** The mechanical pre-pass (Phase 0a) reads most schema-derived values from `meta/vault-config.md` + `wiki/tags.md` (entity_type enum, hovedtags, reserved DNA names, model baseline, registered tags), but a few stay hardcoded because they aren't in a machine-readable config block: kind enum, tag budget, nav basenames, trigger_skill/trigger_mode vocab. Compare the script's `meta.schema_derived_inline` block against CLAUDE.md §B.3, and surface any `meta.config_warnings` (a section the script could not parse). Either is drift between the script and the schema it encodes — symmetric with 9i. Don't auto-fix; propose (usually a one-line constant edit or a vault-config section the script expects).

For each finding, propose the fix in the lint report. Schema-layer fixes are usually one-line edits; flag them clearly so the user can land them in a single pass.

### Check 10: Newcomer readability

Diagnoses pages against the full four-bucket writing & structure standard (`meta/vaultos-lang-no.md`, "Skrive- og strukturstandard"), not just the prose anti-patterns. All sub-checks are flag-only, never auto-fix.

**(a) First-line stranger test.** For each source/entity/concept page, read the first line. Would a curious newcomer who hasn't read the source and doesn't know the speaker understand what the page is about? If the first line leans on inside-jargon, name-drops, or assumes prior reading ("Karpathy/Sequoia: deep argument..."), flag for rewrite. See CLAUDE.md B.3 stranger-test rule. Propose a rewrite in the report: short, substance-first, attribution-after.

**(b) Missing `[!infobox]` on jargon-heavy pages.** Source / entity / concept pages without an `[!infobox]` callout get flagged if the body uses specialized vocabulary a newcomer wouldn't know. Trivially short pages (one-paragraph entities, no jargon) are not flagged. The infobox should carry kind-specific content (see CLAUDE.md B.3 "Infobox sidebar") with 3-5 key-term definitions inline. Propose the page in the report with a brief sketch of what the infobox should contain.

**(c) Prose quality.** Spot-check 5–10 random source/entity/concept pages for the anti-AI-prose patterns. The language-independent ones live in CLAUDE.md §A.6 (reflexive contrastive negation, signal phrases, em-dash habit, modal hedging, amputated fragments, nominalization); the wiki-language-specific ones live in the active pack's "Natural <language>" section (`meta/vaultos-lang-en.md` by default — plain-verb preference, consistent spelling convention, no false register-lift; the Norwegian pack instead flags wrong language prepositions, stranded English-pattern prepositions, Latinate nominalizations, and unmarked anglicisms). Flag specific lines in the report with proposed rewrites; flag-only, never auto-fix. Skip agent-first pages per CLAUDE.md §B.2 audience-axis (their telegraphic format is intentional).

**(d) Systematic idiom sweep (wiki-language-specific).** Where (c) spot-checks 5–10 pages, (d) is a full-vault regex sweep for the most detectable idiom markers the active pack defines. This check is only as meaningful as the language's loanword-bleed problem: for an **English** wiki (the default) there is little to scan, so it is largely inactive; for a **Norwegian** wiki it is the unmarked-anglicism sweep from `meta/vaultos-lang-no.md` "Naturlig norsk". Example patterns (Norwegian pack):
- English `-s`/`-es` verb forms in Norwegian context: `\b(refreshes|outgrows|fails|triggers|files|runs|works)\b` followed by a Norwegian preposition/adverb
- Recurring anglicism phrases: `Status: live`, `fails silently`, `audit trail`, `vanity-dashboard`, `judgment-heavy`, `spot-check`, `outgrows itself`

Run as one pass on `wiki/sources/`, `wiki/entities/`, `wiki/concepts/`, `wiki/syntheses/` bodies (skip infoboxes since their telegram form is intentional; skip agent-first pages per CLAUDE.md §B.2 audience-axis). Flag-only; never auto-fix.

**(e) Structure & content (the rest of the four-bucket standard).** Spot-check the same pages against buckets 1 (structure), 2 (clarity beyond the first line), and 4 (content) of the writing standard (`meta/vaultos-lang-en.md`): does the first sentence define the headword and the opening paragraph work as a lead? rising difficulty (simple/important first, complex last)? one page, one topic (flag topic-fusion as a split candidate)? right length, not maximal? jargon defined once and never explained with other jargon? contested claims attributed, no implicit value judgments? durable phrasing (no "recently"/datestamping, concrete years)? Flag specific pages with the bucket and the gap; flag-only, never auto-fix. Skip agent-first pages per CLAUDE.md §B.2 audience-axis.

When the volume of flags is large (e.g., during the 2026-05 retroactive cleanup pass), group findings by page kind (sources first, then concepts, then entities) and by severity. Concept pages probably go first overall since their definitions propagate into many source pages.

### Check 11: Synthesis readiness

This is an idea-candidate check, not a missing-page error. Do not say the vault "should have" a synthesis page unless the user has asked for vault-backed synthesis work.

Flag:

- Source pages whose `## Cross-references` contain bare wikilinks with no role labels.
- Concept pages that gather multiple sources but lack an explicit source-bullet tally such as `## Argued by` or the wiki language's equivalent.
- Log entries that are too mechanical to carry synthesis signal, especially entries that omit clusters joined or candidate ideas surfaced.
- 3+ source clusters that look like possible synthesis ideas. Phrase them as candidates, not required fixes.

### Check 12: Overview staleness

Compare the modification time of `wiki/overview.md` against the most recent mtime under `wiki/syntheses/` (excluding `Lint - YYYY-MM-DD*.md` files, which are lint artifacts not vault syntheses). If overview is older than the newest synthesis, flag for refresh in the lint report. Overview is the filed answer to "what is this vault currently about?" and should reflect the current synthesis layer (see wiki-query SKILL.md "Special case: overview.md"). Flag-only; lint **does not** regenerate overview. Refresh is owner-prompted via `/wiki-query` on the standing question.

### Consolidation checks (13–17)

Checks 13–17 ask a different question from 1–12: not "what's wrong?" but "what couplings could be tighter, and what's dead weight?" Same flag-only output: proposals only, no silent application. The user reviews and may ask Claude to apply specific findings as a separate operation outside lint.

### Check 13: Dead tags

Tags currently applied to only 1 page (or 0 pages). Per CLAUDE.md B.3, one-page tags add nothing; the page's title and wikilinks already locate it. Propose removal from `wiki/tags.md` and the single using page. Exception: hovedtags stay even at low use; only sub-tags qualify.

### Check 14: Tag merge candidates

Pairs of tags that always co-occur on the same set of pages (or near-always, 1 outlier max). Likely describe the same theme from two angles. Propose a merge: keep the more general or more established name, retire the other, update all pages.

### Check 15: Retroactive tag application

For each existing sub-tag, scan all wiki pages without that tag for clear topical matches. If a sub-tag would fit 2+ untagged pages, propose adding it to them. This is how tags actually grow into bridge-builders rather than one-off labels.

### Check 16: Linkification candidates

Entity or concept names that appear in page bodies as plain text but are not wikilinked, when a corresponding `wiki/entities/<Name>.md` or `wiki/concepts/<Name>.md` exists. Propose specific `[[wikilink]]` insertions with file path + line number for each. Bridges that the graph view is currently missing.

### Check 17: Hub-concept page seeds

Where Check 4 flags "3+ pages mention this concept but no concept page exists," this check goes further: for the highest-value cluster(s), draft a seed for the proposed page: a one-line definition, the list of sources that would link in, and a sketch of cross-references. Don't create the page; propose the seed in the lint report so the user can land it in one ingest-like operation.

### Check 18: Meta-synthesis open questions

Some syntheses are *about the vault itself* and aggregate open architectural questions that affect future schema, operation, or scope decisions. Their `## Open questions` sections are easy to forget because they live on synthesis pages that nobody routinely re-reads.

This check is **flag-only surfacing** (distinct from Check 7's term-matching): read `## Open questions` from each meta-synthesis below and list every bullet verbatim in the lint report under a section header `## §18 Open architecture questions`, with the source synthesis named for each bullet. No term-matching, no resolution attempts, no proposed answers; just visibility.

**Meta-syntheses currently in scope** (hardcoded list; if it grows beyond ~5 pages, consider migrating to a `meta_synthesis: true` frontmatter flag and rewriting to scan by flag):

- _(none yet — a fresh template ships with no meta-syntheses. Add pages here as you file syntheses that aggregate the vault's own open architectural questions.)_

If a listed page does not exist, skip silently. If a listed page exists but has no `## Open questions` section, note "(no open questions)" in §18.

## Phase 3: Write the report

Path: `wiki/syntheses/rapporter/lint-rapporter/Lint - YYYY-MM-DD.md` (natural form per CLAUDE.md B.3).

Frontmatter (lint reports typically have no external `sources:`, since they synthesize the vault itself, so the empty inline `[]` form is correct here; any non-empty `sources:` or `source_path:` list must be block-style per CLAUDE.md B.3):

```yaml
---
kind: synthesis
title: "Lint - YYYY-MM-DD"
created: YYYY-MM-DD
updated: YYYY-MM-DD
ingest_model: <model id>
sources: []
tags: []
---
```

Body: brief lead (scope + counts), then numbered sections per check, then a final "Suggested order of operations" if several items are interrelated. Findings are checklist lines; let the human triage.

## Phase 4: Log entry

Append to `wiki/log.md`:

```
## [YYYY-MM-DD] lint | <one-line scope>
<one-paragraph summary of top findings>
```

## Phase 5: Index update

Add the lint report as a single line under `## Syntheses` in `wiki/index.md`, following the existing format.

## Phase 6: Update the "Where to start" pointer

Open `CLAUDE.md` and update the §B.0 "Latest" wikilink so it points at the new lint report. Single-line edit; do not touch anything else in CLAUDE.md. This is what lets a fresh session land on the open-work queue without being hand-held.

## What lint does NOT do

- Lint **does not** apply fixes. Even obvious-looking ones. Every finding is a proposal.
- Lint **does not** rewrite syntheses. If a synthesis needs restructuring, propose it as a finding; the user kicks off the rewrite separately.
- Lint **does not** treat missing synthesis pages as errors. It may surface synthesis-ready idea candidates, but filing them belongs to `/wiki-synthesis` after the user asks.
- Lint **does not** ingest new sources, even if it spots them in `raw/`. Propose the ingest as a finding (Check 7).
- Lint **does not** trigger `/wiki-ingest`, `/wiki-query`, or `/wiki-synthesis` automatically. It's a survey, not an orchestrator.

## Neighbor awareness

- **/wiki-ingest:** most lint findings translate into an ingest or re-ingest the human asks for after reading the report.
- **/wiki-query:** if a lint finding raises a substantive question ("what's the actual relationship between these 6 sources?"), that's a query, not a lint deliverable.
- **/wiki-synthesis:** if lint surfaces synthesis-ready candidates, the human chooses whether to develop them as idea synthesis or vault-backed synthesis work.
