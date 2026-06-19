---
name: wiki-synthesis
description: Generate synthesis ideas or file explicit vault-backed synthesis pages. Triggers on "create synthesis", "make synthesis", "synthesis ideas", "what syntheses are possible", or explicit requests to scan the vault, use existing sources, or file a synthesis. Default mode is idea generation; do NOT scan the vault or write files unless the user explicitly asks for vault-backed synthesis or selects a candidate to file.
---

# /wiki-synthesis

Generate synthesis ideas first; file vault-backed syntheses only when explicitly requested.

This skill is procedure. **All conventions live in [CLAUDE.md](../../../CLAUDE.md) §B.3 and §B.4.1.** The expanded rationale is [meta/synthesis-generation-recipe.md](../../../meta/synthesis-generation-recipe.md); use it as background, not as text to duplicate.

## Mode selection

Default to **Mode A: idea synthesis** unless the user's wording clearly asks for vault content or file creation.

Use **Mode B: vault-backed survey** only when the user says things like "from the vault", "using existing sources", "scan the vault", "what syntheses are writable now", or asks for candidates from existing wiki content.

Use **Mode C: file selected synthesis** only when the user explicitly asks to file/write/create a wiki synthesis page, or picks a candidate from Mode B and asks you to write it.

If the user says only "create synthesis" or "make synthesis", do **not** scan the vault. Generate ideas.

## Mode A: Idea synthesis

No file writes. No vault scan unless the user asks for it or gives a specific note/source to read.

1. Identify the prompt's domain, tension, or desired output shape.
2. Generate 3-5 candidate synthesis ideas. Each candidate needs:
   - a working title;
   - a one-sentence thesis;
   - why it is interesting now;
   - what evidence, examples, or sources would make it stronger.
3. Prefer sharp positions over topic labels. Reject "these things are all about X" as too weak.
4. End by asking which candidate to develop if a choice is needed. Do not offer to file a wiki page unless the user asks.

## Mode B: Vault-backed survey

Read only enough of the vault to propose candidates. Do not write files.

1. Read `wiki/log.md` tail for recent cluster notes and possible synthesis directions.
2. List `wiki/syntheses/` and skim titles/frontmatter so existing syntheses are not duplicated.
3. Scan recent or relevant source pages' `## Kryssreferanser` sections for repeated co-occurrences and role labels.
4. When relevant, inspect concept pages for source-bullet tallies such as `## Argued by` / Norwegian equivalents.
5. Propose 3-5 candidates. Each candidate must include:
   - source basis: 3+ source wikilinks when available;
   - thesis: the position the sources jointly support;
   - why now: what changed or what cluster became visible;
   - distinction: why this is not already covered by an existing synthesis.
6. Wait for the human to pick before filing.

## Mode C: File selected synthesis

This mode mutates wiki files, so follow CLAUDE.md write safety and plan-before-run thresholds.

1. Confirm the selected candidate has a thesis and source basis. If fewer than 3 source pages support it, either keep it as an idea or ask whether the user wants a provisional synthesis.
2. Create `wiki/syntheses/<Descriptive title in sentence case>.md` with `kind: synthesis`, block-style `sources:`, tags from `wiki/tags.md` when clear, and a first line that states the thesis. Set `trigger_skill: wiki-synthesis` and `trigger_mode:` based on how this filing arrived: `user-requested` if the user explicitly asked, `user-selected` if they picked from a slate, `agent-followon` only if you inferred filing from context (rare for this skill; most paths through `wiki-synthesis` are user-requested or user-selected). See CLAUDE.md §B.4.1 for the field semantics.
3. Structure the body around the argument:
   - shared diagnosis first;
   - labeled vantages, positions, or layers next;
   - `## Hvor klyngen er stille` or `## Åpne spørsmål` for what the sources do not address;
   - `## Kryssreferanser` for adjacent concepts, sources, and syntheses.
4. Update every cited source page's `## Kryssreferanser` with a one-line backlink to the synthesis naming that source's role in the synthesis.
5. Add the synthesis to `wiki/index.md` under `## Syntheses`.
6. Append a narrative `wiki/log.md` entry: `## [YYYY-MM-DD] synthesis | <title>`, naming the thesis, sources used, and any nearby synthesis ideas left open.
7. Read back every edited file before reporting completion.

## Candidate quality rules

Good candidates have a shared diagnosis with different prescriptions, the same prescription from different vantages, a real conflict, or a causal explanation for an observed pattern.

Reject candidates that are only topic lists, rely on one real source plus two mentions, restate a single source with footnotes, or duplicate an existing synthesis without a new axis.
