# VaultOS language/form pack: English (`en`)

> **Imported by `CLAUDE.md` via `@import`. Not a wiki page.** No `kind:` frontmatter; outside wiki operations (§B.2).
>
> This is the **English language/form pack** for VaultOS: the section names, infobox field labels, and the writing standard that fill the portable pattern for an English wiki (the language-independent anti-AI-prose rules live in `CLAUDE.md` §A.6). It is **the shipped default**, but still optional and swappable — a non-English vault replaces it with its own `vaultos-lang-<xx>.md` (a Norwegian pack ships alongside as `vaultos-lang-no.md`). The *pattern* (which sections exist, that an infobox defines jargon) stays in `CLAUDE.md` Part B; this pack supplies the English *fill*.
>
> **Provisional note (single source of truth):** these section names and field labels are currently **also hardcoded in the `wiki-*` skills**, which are not yet wired to read this file. Until that step, the skills + Part B remain the single source of truth; this pack mirrors them for portability staging. When the skills are parameterized, lint Check 9a should be extended to police config↔skill drift.

## Standard source-page section headings
- `## Key claims`
- `## Context`
- `## Open questions`
- `## Cross-references`

**Transcript extension** (source pages whose `source_path` is under `raw/transcripts/`), inserted between `## Context` and `## Open questions`:
- `## Speakers`
- `## Talk metadata`
- `## Timestamped highlights`
- `## Q&A` (optional)

**Synthesis pages** may use `## Where the cluster is silent` for what the cited sources collectively do not address.

## Infobox field labels (by kind)
Infobox field labels are in the wiki language (English here). The field *roles* (what each slot carries) are the portable pattern in §B.3 "Infobox sidebar"; the labels below are the English fill.

- **Source pages:** `Type` · `Speaker/author` · `Date / venue` · `## Key terms`
- **Entity pages:** `Type` · `Role` · `Affiliations` · `Sources` · `## Key terms`
- **Concept pages:** `Short definition` · `Argued by` · `Related` · `## Key terms`

## Writing & structure standard (four buckets)

The positive construction rule for wiki prose (how a page is built and read), adapted from encyclopedic author guidance and plain-language principles. It governs *all* writing in the vault: `/wiki-ingest` drafts to the standard, `/wiki-editor` scores against it, and `/wiki-query`/`/wiki-synthesis` follow it when they write prose. The language-independent anti-AI patterns live in `CLAUDE.md` §A.6 and apply in any language; the "Natural English" idiom notes below are the English side of bucket 3. The portable skeleton (the bucket names) lives in `CLAUDE.md` §B.3; this is the English content.

### Bucket 1: Structure & organization
- **Definition and lead.** The first sentence defines the subject ("X is …"); the opening paragraph is the whole page in miniature. Get to the point; skip "a term for".
- **Rising difficulty (inverted pyramid).** Descending importance, rising difficulty: the simplest and most important first, the narrow and complex last. The welcome-mat discipline applies to section openings too, not just the page's first line.
- **One page, one topic.** Split ambiguous subjects into their own pages; use a hub when a topic is too big for one page (the companion-hub / hub-concept pattern).
- **Right length, not maximal.** Tell the most important things, not everything. The tension with book ingest's "sated, not short" resolves like this: sate the depth within one unit of meaning, but split the page when it fuses several topics.
- **Descriptive subheadings.** Plain signposts ("Cause", "Treatment", "Background") over creative headings, alongside the canonical section names above.
- **Link density and wikilinks.** Link generously inline with `[[wikilinks]]` (never raw paths), and gather further reading in `## Cross-references` at the bottom. Inline links carry the running text; the bottom section carries what the reader should read next.
- **Callouts and infobox.** Callouts convey semantic type (not variety), and the infobox discipline applies. Both are defined in `CLAUDE.md` §B.3.

### Bucket 2: Clarity for the reader
- **Stranger test** (first line + infobox). Both must be readable by a curious newcomer who has neither read the source nor knows the speaker. The test covers the welcome mat (first line + infobox), not the wallpaper: the body below may use the jargon the infobox defines and the page is *about*. Lead with what the source claims or what the page covers; attribution comes after the substance.
- **Define each term once.** Use a gloss ("tonsillitis (a throat infection)") or an inline definition the first time a term appears. Never explain one piece of jargon with another. The page's vocabulary is defined in the infobox's `## Key terms`, so the body can use it freely.
- **Jargon must do work, or it is cut.** A term is load-bearing if the sentence collapses without it. Test: swap the word for its own definition. If the sentence loses nothing, the word was decorative.
- **Don't smuggle the thing you're explaining into the analogy.** If X needs an analogy Y that only makes sense via X, it leaves the reader more confused. When you hit something that is bedrock for its own field (a primitive), say so ("treat as bedrock for this page") and drop a `[[wikilink]]` downward rather than building a circular analogy.

### Bucket 3: Prose & sentence level
- **Readable language.** Active voice; use full stops rather than chaining clauses; subject early and connectives between sentences; break up tangled subordinate clauses; paragraphs rarely over ten lines.
- **The anti-patterns.** The negative side of this bucket. The language-independent ones live in `CLAUDE.md` §A.6; the English-specific ones are in "Natural English" just below.

### Bucket 4: Content, source & durability
- **Attribution and balance.** No implicit value judgments. Attribute contested claims ("X argues", "according to Y"), and keep established fact separable from the source's own assertions or synthesis. The origin type should be visible: the source type in the infobox plus attribution in the text. This is origin transparency, not a reliability ranking — facts can be wrong and assertions can be right; the point is that it's worth knowing where a claim comes from. Make it explicit when documentation is missing.
- **Citations point to sources, not to `raw/`.** Source pages are the single point of truth for what a source says.
- **Write to last.** No datestamping ("recently", "over the past year"); use concrete years, and always a year for figures that change.
- **Media-log layers.** Read/watched is experience data (can carry claims); to-read/watchlist is possibility data (only as intent or candidate); currently-reading is provisional.

### Short checklist (at the writing point)
Condensed form (one line per bucket) that ingest and editor point to:
> **Structure:** define in the first sentence · most important first, rising difficulty · one page, one topic · link inline. **Clarity:** stranger test · define each term once. **Prose:** active, full sentences · no anti-patterns. **Content:** attribute · no datestamping · citations point to sources, not raw.

## Natural English: language-specific anti-patterns
The wiki body and English chat replies should read as English written by a fluent writer. The language-independent anti-AI patterns (reflexive contrastive negation, signal phrases, the em-dash habit, modal hedging, telegraphic bullets, nominalization, amputated sentences) live in `CLAUDE.md` §A.6 and apply in any language. English is close to the baseline those rules were written against, so this section is light; the genuinely English-specific notes:
- *Prefer the plain verb.* "use", not "utilize"; "about", not "in regard to"; "help", not "facilitate". Latinate bureaucratic nominalizations are the English form of the §A.6 nominalization rule.
- *Pick a spelling convention and hold it.* American or British, consistently within the vault; don't mix "-ize"/"-ise" or "color"/"colour" within a page.
- *No false register-lift.* Don't reach for a longer or more formal word to sound authoritative ("commence" for "start", "individuals" for "people") unless the precise term adds something.
- *Exception: named vault primitives* stay as they are — `source`, `entity`, `concept`, `synthesis`, `wikilink`, `infobox`, `ingest`, `lint`, `schema`, `trigger`.
