---
kind: source
title: "Karpathy - LLM Wiki"
created: 2026-05-23
updated: 2026-05-30
ingest_model: claude-opus-4-8
source_path:
  - "raw/articles/2026-05-22_llm_wiki_karpathy.md"
tags:
  - technology
---

> [!infobox]
> **Type**: Idea note / pattern description
> **Author**: [[Andrej Karpathy]]
> **Role in the vault**: the principle source for a persistent, LLM-maintained wiki as a layer between raw sources and questions — the pattern this vault implements
> **Source**: `raw/articles/2026-05-22_llm_wiki_karpathy.md`
> **Original**: [Karpathy's public gist (April 2026)](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

Karpathy - LLM Wiki describes a pattern where an LLM does not merely retrieve from documents at query time, but builds and maintains a persistent markdown wiki as compiled knowledge.

## Key claims

- RAG rediscovers knowledge on every question, whereas a maintained wiki lets synthesis, cross-references, and contradictions accumulate.
- Raw sources should be immutable, while the wiki layer can be agent-owned and continuously updated.
- The schema file is the discipline layer that turns the agent into a wiki maintainer rather than a generic chatbot.
- `index.md` and `log.md` play different roles: index is a content catalog, the log is chronological operation history.
- Useful answers should be filable back into the wiki as syntheses, comparisons, or other durable pages.

## Context

This is the direct architectural source for the vault pattern itself: `inbox`/`raw`/`wiki`, source pages, entities, concepts, index, and log. It describes the principle behind compiled knowledge maintenance, not a particular app or plugin.

*Seed example in the VaultOS template — the first source example a new vault ships with, and the source the whole pattern builds on.*

## Open questions

- When does index-based navigation become too small, so that local search or hybrid BM25/vector search is needed?
- Which kinds of answers are valuable enough to file back as their own wiki pages?
- How strictly should the human review the agent's wiki edits during batch ingest?

## Cross-references

- [[Andrej Karpathy]] — author
- [Karpathy's LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — the public original the text is reproduced from
