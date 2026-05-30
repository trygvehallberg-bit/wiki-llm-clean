---
kind: source
title: "Karpathy - LLM Wiki"
created: 2026-05-23
updated: 2026-05-30
ingest_model: claude-opus-4-8
source_path:
  - "raw/articles/2026-05-22_llm_wiki_karpathy.md"
tags:
  - teknologi
---

> [!infobox]
> **Type**: Idénotat / mønsterbeskrivelse
> **Forfatter**: [[Andrej Karpathy]]
> **Rolle i vaulten**: prinsippkilden for et persistent, LLM-vedlikeholdt wiki som mellomlag mellom råkilder og spørsmål — mønsteret denne vaulten implementerer
> **Kilde**: `raw/articles/2026-05-22_llm_wiki_karpathy.md`

Karpathy - LLM Wiki beskriver et mønster der en LLM ikke bare søker i dokumenter ved query-time, men bygger og vedlikeholder et persistent markdown-wiki som kompilert kunnskap.

## Nøkkelpåstander

- RAG gjenoppdager kunnskap ved hvert spørsmål, mens et vedlikeholdt wiki lar syntese, kryssreferanser og motsigelser akkumulere.
- Råkilder bør være immutable, mens wiki-laget kan være agent-eid og kontinuerlig oppdatert.
- Schema-filen er disiplinlaget som gjør agenten til wiki-vedlikeholder heller enn en generell chatbot.
- `index.md` og `log.md` har ulike roller: index er innholdskatalog, logg er kronologisk operasjonshistorikk.
- Nyttige svar bør kunne files tilbake i wikien som synteser, sammenligninger eller andre varige sider.

## Kontekst

Dette er den direkte arkitekturkilden for selve vault-mønsteret: `inbox`/`raw`/`wiki`, source-sider, entities, concepts, index og logg. Den beskriver prinsippet bak kompilert kunnskapsvedlikehold, ikke en bestemt app eller plugin.

*Seed-eksempel i VaultOS-malen — det første source-eksempelet en ny vault leveres med, og kilden hele mønsteret bygger på.*

## Åpne spørsmål

- Når blir index-basert navigasjon for liten, slik at lokalt søk eller hybrid BM25/vektor-søk trengs?
- Hvilke typer svar er verdifulle nok til å files tilbake som egne wiki-sider?
- Hvor strengt bør mennesket gå gjennom agentens wiki-endringer ved batch-ingest?

## Kryssreferanser

- [[Andrej Karpathy]] — forfatter
