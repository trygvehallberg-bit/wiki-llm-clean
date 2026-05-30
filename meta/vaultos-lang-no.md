# VaultOS language/form pack — Norwegian (`no`)

> **Imported by `CLAUDE.md` via `@import` — not a wiki page.** No `kind:` frontmatter; outside wiki operations (§B.2).
>
> This is the **Norwegian language/form pack** for VaultOS: the section names, infobox field labels, and prose anti-patterns that fill the portable Part B pattern for a Norwegian wiki. It is **part of VaultOS but optional and swappable** — a non-Norwegian vault replaces it with its own `vaultos-lang-<xx>.md`. The *pattern* (which sections exist, that an infobox defines jargon, that prose must read as mother-tongue) stays in `CLAUDE.md` Part B; this pack supplies the Norwegian *fill*.
>
> **Provisional note (single source of truth):** these section names and field labels are currently **also hardcoded in the `wiki-*` skills**, which are not yet wired to read this file (deferred — see proposal-003 roadmap). Until that step, the skills + Part B remain the single source of truth; this pack mirrors them for portability staging. When the skills are parameterized, lint Check 9a should be extended to police config↔skill drift.

## Standard source-page section headings
- `## Nøkkelpåstander`
- `## Kontekst`
- `## Åpne spørsmål`
- `## Kryssreferanser`

**Transcript extension** (source pages whose `source_path` is under `raw/transcripts/`), inserted between `## Kontekst` and `## Åpne spørsmål`:
- `## Talere`
- `## Metadata for foredraget`
- `## Tidsstemplede høydepunkter`
- `## Spørsmål og svar` (optional)

**Synthesis pages** may use `## Hvor klyngen er stille` for what the cited sources collectively do not address.

## Infobox field labels (by kind)
Infobox field labels are Norwegian on wiki pages. The field *roles* (what each slot carries) are the portable pattern in §B.3 "Infobox sidebar"; the labels below are the Norwegian fill.

- **Source pages:** `Type` · `Foredragsholder/forfatter` · `Dato / arena` · `## Nøkkelbegreper`
- **Entity pages:** `Type` · `Rolle` · `Tilknytninger` · `Kilder` · `## Nøkkelbegreper`
- **Concept pages:** `Kort definisjon` · `Argumentert av` · `Relatert` · `## Nøkkelbegreper`

## Naturlig norsk — six anti-patterns
Wiki-bodyen skal kjennes som norsk skrevet av en norsk skribent. Seks mønstre å unngå:
- *Feil preposisjon om språk.* Man skriver *på* et språk, ikke *i*. Tilsvarende *snakke på*, *oversette til/fra*, *publisere i (avis) / på (nettsted)*.
- *Hengende preposisjoner i engelsk mønster.* "Landsmålet Vinje skrev i" → "landsmålet som Vinje skrev på". Bruk "som" + preposisjon eller omformuler.
- *Agent-/prosess-nominaliseringer av latinske verb.* Verbet ("kodifisere") er fint norsk; substantivet ("kodifikator", "kodifisering") klinger jus-/byråkrat-akademisk. Bytt til verbform der det går. Test: "Jeg driver sjeldent med biologisering selv om jeg er biolog."
- *Telegram-bullets.* Komma-separerte fragment-tags og nominaliserings-sandwicher uten verb leser som hastverk. Bullets skal være hele setninger med verb; lengden styres av innholdet, ikke av at det skal "være kort".
- *AI-rhetoriske vendinger.* Kontrastiv negasjon ("det er X, ikke Y, som ...", "ikke bare X, men også Y") og signalfraser ("det er verdt å merke seg", "viktig her er at", "sentralt er") er retorisk staffasje. Bruk motsetning bare når den faktisk gjør semantisk arbeid.
- *Umerket anglisme.* Engelske leksemer (substantiv, verb, faste uttrykk) sklir uomformulert inn i norsk syntaks: "Status: live", "outgrows itself", "fails silently", "vanity-dashboard". Test: ville ordet trengt kursivering for å føles korrekt i en redigert norsk tekst? Hvis ja, omformuler (ofte med norsk verb, ikke 1:1-substantivbytte). Unntak: navngitte vault-primitiver og deres norske bøyninger (`source`, `entity`, `concept`, `synthesis`, `wikilink`, `infobox`, `ingest`/`ingestes`/`ingestet`/`re-ingestes`/`re-ingestet`, `lint`, `schema`, `trigge`/`trigges`/`trigget`).
