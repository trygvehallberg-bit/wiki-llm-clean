---
name: wiki-parable
description: "Create original analytical wiki parables for this vault: philosophical apologues, toy worlds, mechanism stories, or rationalist-style concept parables. Use when the user asks for a wiki-parable about a topic, a philosophical parable, an essayistic apologue, a small fictional model that explains a concept, or references Scott Alexander / Slate Star Codex as a genre cue. Convert author-style requests into genre-level method; do not imitate a living author's distinctive prose voice."
---

# Wiki Parable

Create original, source-aware parables that make an abstract mechanism visible. The output is usually a filed wiki synthesis under `wiki/syntheses/parables/`.

Use broad genre tools from analytical essaying: a toy world, clear incentives, mechanism-first storytelling, steelmanning through the scene, sparse humor that clarifies the model, and source footnotes that keep the body readable.

## Mode Selection

Default to file mode when the user says "create a wiki-parable about X" or otherwise asks to make one for the wiki.

Use chat-draft mode when the user asks for ideas, variants, a sketch, or a sample without filing.

Use vault-backed mode when the topic maps to existing wiki pages or when the user asks to use vault sources.

Use hypothetical mode only when the user explicitly asks for a thought experiment with no source basis. Prefer vault-backed mode for filed pages. Keep `sources: []`, make the hypothetical status explicit, and avoid empirical claims that need sources.

## Style Boundary

Write in the genre of analytical apologue, not as a pastiche of any living author.

If the user asks for a Scott Alexander style, SSC style, or similar, translate that to these moves:

- start with a concrete confusion or friction;
- use a small fictional world to reveal a mechanism;
- move from individual experience to incentives, system outcome, and meta-error;
- make the strongest opposing model visible inside the scene when that improves the parable;
- show uncertainty rather than smoothing it away;
- use one sharp or lightly absurd image only when it carries the mechanism.

Do not copy catchphrases, recurring named devices, paragraph rhythms, or distinctive voice markers from a specific living author. Do not mention this boundary in the filed wiki page unless the user asks.

## Context Gathering

1. Read enough local context to avoid duplicating existing syntheses:
   - scan `wiki/index.md` for the topic and nearby concepts;
   - list `wiki/syntheses/` and `wiki/syntheses/parables/` if it exists;
   - read relevant concept, entity, source, and synthesis pages.
2. If the topic depends on current facts, verify them or keep the parable explicitly abstract.
3. Use source pages for factual claims. Do not invent citations.
4. Treat the parable as an interpretation of sources, not a substitute for source-backed synthesis. If fewer than three sources support the page, label the argument as provisional in the infobox.
5. Keep source names out of the body prose unless attribution is substantively part of the argument. Put source detail in footnotes and frontmatter.

## Build The Toy World

Design the parable before writing the page.

A useful toy world has:

- 2-4 actors;
- one scarce resource, rule, deadline, status ladder, or hidden constraint;
- a local incentive that looks reasonable from inside the scene;
- one decision each actor can defend;
- an aggregate outcome no actor wanted;
- one detail that feels odd but maps cleanly to the mechanism.

Reject decorative stories. Every strange object, rule, institution, or joke needs to help explain the model.

## Required Page Shape

Create the file at:

`wiki/syntheses/parables/<Descriptive title in sentence case>.md`

Use the normal synthesis frontmatter. For lint compatibility with the current vault schema, set `trigger_skill: wiki-synthesis` and `trigger_mode: user-requested` unless the user selected the parable from a candidate list, in which case use `user-selected`.

After the infobox, the body should have only three sections: `## Parabelen`, `## Fotnoter`, and `## Tema`. Do not add direct analysis sections such as `## Hva parabelen viser`, `## Mekanismen`, `## Hva modellen forklarer godt`, `## Hvor modellen overdriver`, `## Beste innvending`, or `## Epistemisk status`. Put source support in frontmatter and footnotes. Put caveats in the infobox if needed. Let the story carry the mechanism.

Template:

```markdown
---
kind: synthesis
title: "<Title>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
ingest_model: <model id>
sources:
  - "[[Source page]]"
trigger_skill: wiki-synthesis
trigger_mode: user-requested
tags:
  - <tag from wiki/tags.md when clear>
---

<One story-opening sentence in Norwegian. It can hint at the mechanism, but should read as part of the tale.>

> [!infobox]
> **Type:** parabel / syntese
> **Kort tese:** <one-line mechanism claim>
> **Sentrale tema:** [[Concept]] · [[Concept]] · [[Concept]]
> **Kildegrunnlag:** <kort: bredt / moderat / smalt / hypotetisk>
> **Epistemisk status:** <one-line confidence label>

## Parabelen

<The fictional scene. Use footnote markers for factual anchors only when needed.[^1]>

## Fotnoter

[^1]: Source detail as a concise note, normally with wikilinked source pages. Keep factual support here rather than in the body prose.

## Tema

<Short comma-separated theme line. Name the field of the parable, not the lesson.>
```

Write wiki page bodies in Norwegian unless the user asks for another language. Follow `CLAUDE.md` prose rules and the Norwegian language pack.

Use `sources: []` only for a purely hypothetical parable with no source basis. For ordinary filed parables, include source pages in frontmatter and footnote definitions.

## Filing Steps

1. Create `wiki/syntheses/parables/` if missing.
2. Create the parable page.
3. Add one line to `wiki/index.md` under `## Syntheses`. Use `[[Title]]` when unique; use `[[parables/Title|Title]]` if the title could collide.
4. Append `wiki/log.md` with `## [YYYY-MM-DD] synthesis | <Title>`, naming the topic, whether the parable was vault-backed or hypothetical, and the main linked pages.
5. If the parable uses source pages, add concise backlinks in their `## Kryssreferanser` sections only when the link adds real navigation value.
6. Read back every edited file before reporting completion.

## Quality Check

Before finishing, verify:

- the parable can be summarized as a mechanism, not only as a moral;
- the story has actors, incentives, constraints, choices, and consequences;
- the body has no direct analysis blocks, and the mechanism is visible through actors, incentives, constraints, choices, and consequences;
- the infobox names central themes and the strength of the source basis;
- source-backed claims have footnotes, and the body avoids inline source exposition;
- the infobox and footnotes separate source-backed claims from speculation;
- the page links to existing concepts instead of creating isolated prose;
- the tone stays clear, concrete, and original.
