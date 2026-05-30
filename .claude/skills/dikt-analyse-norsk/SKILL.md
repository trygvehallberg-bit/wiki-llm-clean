---
name: dikt-analyse-norsk
description: Enrich a wiki source page for a poem with structured analysis — full diktekst, rhyme/meter form analysis, color-coded rhymes, meter underlining, and optional margin sidenotes. Triggers on "dikt-analyse", "analyser diktet", "rim-analyse", "metrisk analyse", "poetry analysis" when the input is an existing source page or a freshly ingested poem. Primary language: norsk (bokmål, nynorsk, dansk, riksmål, oldnorsk). Secondary: engelsk og andre europeiske språk LLM-en kan analysere fonetisk uten ekstern uttaleordbok. Do NOT trigger for non-poem sources, for query/lint operations, or when the source page already has a complete diktanalyse-section set.
---

# /dikt-analyse-norsk

Strukturert lyrikk-analyse skreddersydd for nordiske og europeiske språk LLM-en kan analysere uten ekstern uttaleordbok (CMUDict og engelsk-orienterte verktøy er ikke brukt — alt drives av modellens egen fonetiske intuisjon).

Skillen er **procedure** — konvensjoner og maler. **All vault-schema lever i [CLAUDE.md](../../../CLAUDE.md) §B.3** og overstyrer hvor de overlapper.

## Når skillen kjører

- Brukeren sier "dikt-analyse", "analyser diktet", "rim-analyse", "metrisk analyse", eller refererer til en eksisterende source-side som et dikt som trenger utdypende analyse.
- Brukeren ingester et nytt dikt via `/wiki-ingest` og vil ha analyse i samme operasjon.
- Brukeren peker på `wiki/sources/<dikt>.md` og ber om utvidelse.

**Ikke trigger** for:
- Prosa-source-sider (artikler, transkripter, dokumentasjon).
- Query/lint-operasjoner.
- Sider som allerede har komplett `## Diktekst` + `## Form` + `## Bilder og motiv` + `## Allusjoner og referanser`.

## Phase 0 — Plan check og forutsetninger

**Forutsetninger:**
- Diktet finnes i `raw/articles/<dato>_<slug>.md` (eller liknende rå-path).
- En `wiki/sources/<dikt>.md`-side eksisterer (opprettet av `/wiki-ingest` eller manuelt).
- Diktets fulle tekst er tilgjengelig (ikke kun bildelenker — hvis bare image, skip og flagg i `## Åpne spørsmål`).

**Plan-before-run:** Single-dikt-analyse trenger ikke plan. Multi-dikt-batch (mer enn 3 dikt i én invokasjon) krever plan-paragraf først per CLAUDE.md §B.4.0.

## Phase 1 — Les diktet og identifiser form

Les diktets fulle rå-tekst. Identifiser:

1. **Strofeform** — antall linjer per strofe, antall strofer, fri/lukket form.
2. **Versemål** (best effort — LLM-judgment, ikke autoritativt):
   - **Aksentuelt** (norsk/germansk tradisjon, gammelnorrøn) — tell trykk per linje, ignorér uvektige stavelser.
   - **Syllabisk-aksentuelt** (klassisk europeisk: jambisk, trokeisk, daktylisk pentameter/heksameter) — tell både stavelser og trykk-mønster.
   - **Syllabisk** (romansk tradisjon, sonett-tradisjonen i fransk) — tell stavelser, fri trykksbruk.
   - **Fri vers** — ingen fast metrum.
3. **Rim-mønster** — tegn rim-grupper med bokstaver (A, B, C, ...). Vanlige:
   - Kuplett: AABB
   - Kryssrim: ABAB
   - Omsluttende: ABBA
   - Ottava rima: ABABABCC
   - Terza rima: ABA BCB CDC ...
   - Sonett-skjemaer (italiensk: ABBA ABBA CDE CDE; engelsk: ABAB CDCD EFEF GG)
   - Heroisk kuplett: AA BB CC ...
   - Fri rim / blank verse: ingen rim.
4. **Rim-type per gruppe** — kvinnelig (toleddet med trykk-lett slutt, "-ar/-er/-de") vs mannlig (eneledd med trykk-tung slutt, "-aag/-art").
5. **Lyd-virkemidler** utenom rim — alliterasjon, assonans, konsonans, anafora, epifora.

## Phase 1.5 — SNL-verifisering (norske dikt)

**Påkrevd for norske, danske og skandinaviske dikt før forfatter-entity opprettes eller eksisterende entity utvides.** Hopp over for engelske/internasjonale dikt (SNL dekker hovedsakelig nordisk og norsk kanon).

Bruk Store norske leksikon API til å verifisere:

1. **Søk på forfatteren** — `https://snl.no/api/v1/search?query=<forfatter-navn>&limit=3`
2. **Hent full artikkel** — `https://snl.no/<permalink>.json` for autoritative biografi, dateringer, verks-katalog
3. **Kryss-sjekk:** finnes diktet eller diktsamlingen i SNLs verks-liste? Stemmer publiseringsår med rå-fila? Er det andre forfattere SNL knytter til samme verk eller tema?
4. **Bonus-funn:** musikalsk arv (Grieg/Sibelius/Tveitt-vertonering), oversettelses-historie, kanoniserings-status. Disse beriker source-side `## Kontekst`.

**Resultat-håndtering:**
- **Bekreftet:** legg inn `Ekstern referanse — [SNL: <Tittel>](<URL>)` i entity infobox og noter "Verifisert mot SNL" i source `## Kontekst`.
- **Ikke bekreftet i SNL:** forfatteren kan likevel være korrekt (SNL dekker ikke alle), men marker da som "Forfatter ikke verifisert i SNL" i `## Åpne spørsmål`.
- **Konflikt:** rå-fila sier én forfatter, SNL en annen → følg SNL og noter divergensen i `## Åpne spørsmål`.

**Også relevant for andre entiteter** i dikt-konteksten:
- Steder (Rondane, Hardanger, Tinn)
- Verk og samlinger (Ferdaminni, Heroica)
- Litteraturhistoriske bevegelser (landsmålet, det moderne gjennombrudd, symbolismen)

**Lisens-merknad — tekst:** SNL-artikler har «begrenset» lisens (CC-BY-NC-ND eller liknende). Vi kan **sitere kort, parafrasere fritt og lenke til artikkelen** — men ikke gjengi artiklene verbatim i lengre passasjer.

**Lisens-merknad — bilder:** sjekk `first_image_license`-feltet i søkeresultatet eller artikkel-JSON. Vanlige utfall:
- **«Falt i det fri» / «Public domain»** — fri bruk uten begrensning.
- **«CC-BY ...»** — fri bruk med attribusjon til SNL og fotograf.
- **«Gjengitt med tillatelse»** — SNL har spesifikk avtale med opphavsrettshaver. For privat, ikke-kommersiell vault-bruk laster vi ned med eksplisitt attribusjon; ikke gjenbruk i offentlig publisering uten egen klarering.
- **«Begrenset»** eller annen restriksjon — vurder per tilfelle; default er lenke til artikkelen heller enn embed.

**Last ned-konvensjon:** Bilder skal lastes ned lokalt under `raw/assets/snl/<slug>.jpg` med beskrivende filnavn. Bruk Obsidians `![[filnavn.jpg|<bredde>]]`-wikilink-syntaks for embed. Hot-linking unngås — SNL kan endre URL-er, og lokal lagring sikrer vault-portabilitet.

```bash
curl -sL -o "raw/assets/snl/<slug>.jpg" "https://media.snl.no/media/<id>/<original-filnavn>.jpg"
```

**Embed-konvensjon i infobox:**

```markdown
> [!infobox]
> ![[<slug>.jpg|180]]
> *Bilde: [SNL](<artikkel-URL>), <lisens-status>.*
>
> **Type** — person
> **Rolle** — ...
```

**Embed-konvensjon i body (større visning, eks. landskap):**

```markdown
![[<slug>.jpg|400]]
*<Bildetekst>. Bilde: [SNL](<artikkel-URL>), <lisens-status>.*
```

SNL-API kan også brukes bredere i andre vault-områder.

## Phase 2 — Bygg seksjonene

Sett inn følgende seksjoner mellom `## Kontekst` og `## Åpne spørsmål` i kildens source-side (parallell til transcripts-extension i CLAUDE.md §B.3):

### `## Diktekst`

Diktets verbatim tekst som en blockquote (`>` per linje). Bevar original ortografi, tegnsetting og linjebrudd. Avslutt med en italic-attribusjon hvis kjent (`*Fra <samling/diktbok>, <år>*`).

**Float-clear på H2:** håndteres automatisk av `.obsidian/snippets/infobox.css` med regelen `.callout[data-callout="infobox"] ~ h2 { clear: right; }`. Alle H2-headers etter en infobox vil clearer right-floaten, så hver seksjon starter rent full-bredde under infoboxen. Krever ingen manuell `<div>`-markup per side. Hvis infobox-snippet er deaktivert eller fjernet, faller layouten tilbake til normal markdown-flyt (uten right-rail).

**Rim-fargekode** (HTML-inline, fungerer i Obsidian både i edit og read mode):

| Rim-gruppe | Bakgrunnsfarge | Hex |
|---|---|---|
| A | gul | `#fef08a` |
| B | lyseblå | `#bae6fd` |
| C | rosa | `#fbcfe8` |
| D | lysegrønn | `#bbf7d0` |
| E | lysenlilla | `#e9d5ff` |
| F | oransje | `#fed7aa` |

**Dark-mode-kritisk:** Hver `<span style="...">` MÅ inkludere `color:#000` for at teksten skal være lesbar i mørkt tema. Pattern:

```html
<span style="background:#fef08a; color:#000">rim-ord</span>
```

For konsekvent palett over alle dikt, bruk samme farge per posisjon i rim-skjemaet (A=gul, B=blå, C=rosa) selv om rim-ordene endrer seg per strofe. I ottava rima er A/B/C ulike i hver strofe, men fargene reflekterer rollen, ikke det spesifikke rim-ordet.

**Plassering av span:** wrap selve rim-ordet, ikke følgende tegnsetting:
- Riktig: `<span style="background:#fef08a; color:#000">Dalar</span>,`
- Feil: `<span style="background:#fef08a; color:#000">Dalar,</span>`

**Header over diktet** (innledende linje før blockquoten):

```markdown
Rim-fargekode: <span style="background:#fef08a; color:#000">A</span> · <span style="background:#bae6fd; color:#000">B</span> · <span style="background:#fbcfe8; color:#000">C</span> — <rim-mønster-navn>.
```

### `## Form`

3-6 setninger som forklarer:
- Versemål (med ærlig nivå av tentativitet — "løs jambisk pentameter" er bedre enn "strikt jambisk pentameter" når analysen er judgment).
- Strofeform.
- Rim-mønster med skjemaforklaring.
- Språklig register (dialekt, arkaisk, formelt, daglig).
- Eventuelle historiske/tradisjonelle referanser (italiensk renessanse, romantikk, modernisme, etc).

### `## Bilder og motiv`

4-8 bullet-punkter med diktets sentrale bilder eller motiver, hver med ett-to-setnings-utdyping og gjerne sitater fra teksten i anførselstegn.

### `## Allusjoner og referanser` (optional)

Bullet-punkter for hver eksplisitt eller subtil intertekstuell referanse:
- Sitater fra andre verk.
- Historiske/mytologiske referanser.
- Sjanger-/tradisjons-referanser (sonett-tradisjonen, klagedikt, ode-tradisjon, etc).
- Språkpolitiske eller kulturelle peker (særlig relevant for landsmål-/nynorsk-dikt).

Hopp over seksjonen hvis ingen klare allusjoner finnes; ikke fabrikker.

## Phase 3 — Metrisk understreking (optional)

For nordeuropeiske aksentuell-syllabiske dikt der trykk-mønsteret er sentralt (Aasen, Bjørnson, Wergeland, Welhaven; Shakespeare-sonett; Goethe), kan stressede stavelser understrekes med `<u>...</u>`-tag.

**Konvensjon — markér én strofe som metrisk demo:**
- Velg den første strofen som demonstrasjon.
- Resten av strofene har kun rim-fargekode (ikke meter-underline).
- Note i `## Diktekst`-headeren: "Strofe N har metrisk understreking som demonstrasjon; resten har kun rim-fargekode."

**Hvorfor bare én strofe:** full metrisk understreking gjør lesningen tung. Demonstrasjonen viser mønsteret; leseren ekstrapolerer.

**Syllabe-nivå** vs ord-nivå:
- For flersttavelses-ord, understrek bare den stressede stavelsen: `<u>at</u>ter`, `<u>Da</u>lar`.
- For enstavelses-stressede ord, understrek hele ordet: `<u>Fjøll</u>`, `<u>saag</u>`.

**Når rim-span og meter-underline overlapper:**

```html
<span style="background:#fef08a; color:#000"><u>Da</u>lar</span>
```

Underline ligger innenfor span. Begge regler virker.

**Hopp over metrisk understreking hvis:**
- Diktet er fri vers / uten konsistent meter.
- Diktet er på et språk LLM-en har lav konfidens om uttale (oldnorsk uten kjente korpora, obskure dialekter).
- Diktet er svært kort (under 8 linjer) — analysen blir overdimensjonert.

## Phase 4 — Margenotater via sidenote-callout (optional, krever CSS)

Hvis vaulten har `obsidian-sidenote-callout`-CSS-snippet installert (`.obsidian/snippets/sidenote.css`), kan komplekse rim-mønstre, allusjoner eller ord-glosser plasseres som margenotater rett ved versene de gjelder.

**Default: høyre marg.** Norske lesere forventer margenotater til høyre for hovedteksten (jf. Tufte-tradisjonen og akademisk standard). Bruk `aside-r`-modifier som default. Bruk `aside-l` (venstre marg) bare når dikt-layouten allerede har noe annet til høyre (eks. en stor illustrasjon flytende der).

**Syntaks (per [xhuajin/obsidian-sidenote-callout](https://github.com/xhuajin/obsidian-sidenote-callout)):**

```markdown
> [!NOTE|aside-r] Allusjon
> "Barnemaal" — referanse til landsmålet som folkets *eigentlege* mål, sentralt for landsmålsprosjektet.
```

Plasser callouten umiddelbart etter den linjen den kommenterer (innenfor samme blockquote-blokk eller mellom strofer).

**Hvis snippet ikke er installert:** fall tilbake til markdown-fotnoter (`[^1]`) eller `## Allusjoner og referanser`-seksjonen.

## LLM-judgment caveats

Vær **eksplisitt om usikkerhet**. Marker svake påstander med "tentativ", "best effort", "leser-judgment":

- **Forfatterattribusjon må verifiseres** før entity opprettes. Diktet i raw-filen kan ha lavkvalitets-metadata eller manglende forfatter; LLM kan også feilattribuere kulturelt nære navn (eks. norsk landsmålsdiktning der både Aasen og Vinje skrev i samme periode, samme språk, samme tradisjon). Hvis attribuering ikke kan bekreftes fra rå-fila eller pålitelig allmenn kunnskap: marker forfatter som "ukjent" eller "uverifisert" i infobox, og flagg under `## Åpne spørsmål` — ikke opprett forfatter-entity før verifisering.
- **Metrisk analyse er judgment, ikke autoritet.** Norsk verselære er notorisk fleksibel — samme linje kan leses som 4-stress eller 5-stress avhengig av leser. Klassiske former (sonett, ottava rima) er mer stabile enn fri vers.
- **Dialekt-rim** (vestlandsk nynorsk, dansk fra 1800-tallet, oldnorsk) kan involvere lydhistoriske rim som ikke matcher moderne uttale. Hvis usikkert: noter det.
- **Internrim/multi-syllabic** rap-stil rim er vanskeligere enn klassiske end-rim. Hvis applisert: marker som "potensielt internrim", ikke bekreftet.
- **Allusjons-deteksjon** er bedre på berømte intertekstuelle peker (Bibel, klassisk gresk/latin, kanonisk skandinavisk litteratur). For obskure peker: skip eller flagg som hypotetisk.

**Språkpurisme:** Skriv på norsk i wiki-laget per CLAUDE.md B.1. Unngå engelske termer der norske finnes — bruk "ordspill" (ikke "pun"), "tvisyn" eller "dobbeltsyn" (ikke "ambiguity"), "lesehistorie" eller "mottakelse" (ikke "resepsjonshistorie"-jargong med mindre brukeren spesifikt ber om litteraturvitenskapelig terminologi).

**Når i tvil:** Mindre er mer. Klar form-analyse av rim-skjemaet + fargekoding er det viktigste bidraget. Meter, allusjoner og bilder er supplementer som kan utdypes når brukeren ber om det.

## Filendringer per analyse

For en typisk dikt-analyse-kjøring:

1. **Edit:** `wiki/sources/<dikt>.md` — legg til `## Diktekst`, `## Form`, `## Bilder og motiv`, `## Allusjoner og referanser` (sistnevnte optional).
2. **Frontmatter:** bump `updated:` til dagens dato, sett `ingest_model:` til kjøremodell.
3. **Eventuelt:** opprett forfatter-entity hvis diktet er fra en kjent forfatter uten eksisterende entity-side.
4. **Log:** legg én linje i `wiki/log.md` på logg-linjeformatet: `## [YYYY-MM-DD] dikt-analyse | <dikt-tittel>`.

Skillen oppretter ikke index-entries (diktet har allerede source-entry fra `/wiki-ingest`); justerer index bare hvis forfatter-entity er ny.

## Nabo-skills

- **`/wiki-ingest`** — kjøres før dikt-analyse hvis diktet ikke har source-side ennå. Skillen kan kjedes inn etter wiki-ingest.
- **`/wiki-lint`** — kan flagge dikt-source-sider uten `## Diktekst`-seksjon som kandidater for dikt-analyse.

## Mal — ny dikt-source-side (skeleton)

```markdown
---
kind: source
title: "<Diktets tittel>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
ingest_model: <model id>
source_path:
  - raw/articles/<dato>_<slug>.md
tags:
  - kultur
  - litteratur
---

> [!infobox]
> **Type** — dikt (lyrikk)
> **Forfatter** — [[<Forfatter>]]
> **Publisert** — <år>, fra *<Samlingstittel>*
> **Språk** — <språk/dialekt>
>
> ## Nøkkelbegreper
> - **<Term>** — kort definisjon.

<Stranger-test-førstelinje per CLAUDE.md §B.3 — én setning som forklarer hva diktet er og hva det handler om.>

## Nøkkelpåstander

- ...

## Kontekst

<Plassering i forfatterskapet, samtid, sjanger.>

## Diktekst

Rim-fargekode: <span style="background:#fef08a; color:#000">A</span> · <span style="background:#bae6fd; color:#000">B</span> · <span style="background:#fbcfe8; color:#000">C</span> — <rim-mønster>. <Optional: Strofe N har metrisk understreking.>

> <linje 1 med <span>-rim-ord</span> og evt <u>stress</u>-merker>
> ...
>
> *<Attribusjon>*

## Form

<3-6 setninger om versemål, strofe, rim, register.>

## Bilder og motiv

- **<Bilde>** — utdypning.

## Allusjoner og referanser

- ...

## Åpne spørsmål

- ...

## Kryssreferanser

- [[<Forfatter>]] — forfatter
- ...
```
