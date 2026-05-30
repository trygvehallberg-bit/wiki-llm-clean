---
kind: source
title: "Karpathy - LLM Wiki"
created: 2026-05-23
updated: 2026-05-28
ingest_model: gpt-5
source_path:
  - "raw/articles/2026-05-22_llm_wiki_karpathy.md"
tags:
  - teknologi
---

> [!infobox]
> **Type**: Idénotat / mønsterbeskrivelse
> **Tema**: [[Second brain workflows]]
> **Rolle i vaulten**: Prinsippkilde for persistent, LLM-vedlikeholdt wiki som mellomlag mellom råkilder og spørsmål
> **Kilde**: `raw/articles/2026-05-22_llm_wiki_karpathy.md`

Karpathy - LLM Wiki beskriver et mønster der en LLM ikke bare søker i dokumenter ved query-time, men bygger og vedlikeholder en persistent markdown-wiki som kompilert kunnskap.

## Nøkkelpåstander

- RAG gjenoppdager kunnskap ved hvert spørsmål, mens en vedlikeholdt wiki lar syntese, kryssreferanser og motsigelser akkumulere.
- Råkilder bør være immutable, mens wiki-laget kan være agent-eid og kontinuerlig oppdatert.
- Schema-filen er disiplinlaget som gjør agenten til wiki-vedlikeholder heller enn generell chatbot.
- `index.md` og `log.md` har ulike roller: index er innholdskatalog, logg er kronologisk audit trail.
- Nyttige svar bør kunne files tilbake i wikien som synteser, sammenligninger eller andre varige sider.

## Kontekst

Dette er en av de mest direkte arkitekturkildene for selve vault-mønsteret her: `inbox`/`raw`/`wiki`, source-pages, entities, concepts, index og logg. Kilden skiller seg fra Obsidian-oppsettkildene ved at den beskriver prinsippet bak kompilert kunnskapsvedlikehold, ikke bare en konkret app eller plugin.

## Åpne spørsmål

- Når blir index-basert navigasjon for liten, slik at lokal search eller hybrid BM25/vector-søk trengs?
- Hvilke typer svar er verdifulle nok til å files tilbake som egne wiki-sider?
- Hvor strengt bør mennesket reviewe agentens wiki-endringer ved batch-ingest?

## Kryssreferanser

- [[Agenten trenger en kropp]] - bruker LLM Wiki som grunnformen for agentens vedvarende kunnskapskropp
- [[Second brain workflows]] — hovedkonsept
- [[Obsidian]] — praktisk IDE for markdown-wikien
- [[Knowledge feedback loops]] — returkanalen tilbake til brukeren
- [[Agentic OS]] — bredere system rundt agentarbeid
- [[Karpathy - LLM thought map]] — annen Karpathy-relatert AI-kilde i vaulten
- [[Wikien som metakognitivt stillas]] — syntese: wiki-mønsteret lest som eksternt stillas for Kolbenes metakognitive læringssløyfe
- [[Vaultens skjema og operasjoner]] — den filede operasjonaliseringen av Karpathy-mønsteret for *denne* vaulten (CLAUDE.md + fire wiki-skills som ett dokumentsett)
- [[Arkitekturbeslutninger for vaulten]] — ADR-record over stabile beslutninger som operasjonaliserer Karpathy-mønsteret konkret i denne vaulten
- [[Skill - wiki-ingest]], [[Skill - wiki-lint]], [[Skill - wiki-query]], [[Skill - wiki-synthesis]] — de fire skill-sourcene siterer denne som eksplisitt arkitekturkilde
